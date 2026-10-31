#!/usr/bin/env python3
"""Compile book-of-mormon-1852-pages/page-*.md into one Markdown file (main text only), in printed order.

Removes: HTML comments, any Marginal notes section, Footer: lines, **Header:**
running heads and printer's signature marks. Rejoins paragraphs that run across a
page break: a page whose first paragraph begins with the marker
`<!-- cont -->` continues the last paragraph of the previous page (the page
comment <!-- page NNN --> is left at the join). A <!-- page NNN --> comment is
put at the start of each page's text.

Printed order (see pagelist.py): each printed page once. The second copy of a duplicate leaf (16 PDF pages) is skipped,
page-154a/154b (printed pp. 134-135, from the second scan) follow PDF 154, and PDF 243-244 (pp. 212-213) follow PDF 234.
The page marker carries the file label (e.g. <!-- page 154a -->). Verse numbers stay in the text.

Usage:  python3 tools/compile_markdown.py [--pages-dir DIR] [--out FILE]
"""
import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pagelist  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

# Whole words the printer left a hyphen after at a page end (stray hyphens, not word breaks): never joined.
# Add them here when check_structure/compile output shows a glued word (1830 had 'sat', 'the').
KEEP_HYPHEN = set()

FRONTMATTER = """---
title: The Book of Mormon (Liverpool, 1852)
translator: Joseph Smith Jr.
publisher: Franklin D. Richards
place: Liverpool
publication_year: 1852
source_scan: https://archive.org/details/book-of-mormon-1852-liverpool-edition
source_scan_supplement: https://archive.org/details/BookOfMormon1852LiverpoolEdition (printed pp. 134-135, Enos, missing from the main scan)
transcription_method: AI-assisted transcription from page images; one blind AI proofread of every text page; owner review of 195 flagged items; no full human proofread
repository: https://github.com/lds-restoration-documents/1852-richards-liverpool-book-of-mormon
version: "{version}"
---

"""


def build_version(pages_dir):
    """Latest release tag, build date and the short hash of the last commit that touched the page files,
    e.g. 'v1.0.0 (2026-10-31, 88a940d)'. '+modified' follows the tag when the page files differ from the
    tagged release (later commits or uncommitted edits); '+dirty' is added to the hash for uncommitted page edits.
    Without any tag: '2026-10-31+88a940d'."""
    def git(*a):
        return subprocess.run(['git', '-C', str(ROOT), *a], capture_output=True, text=True, check=True).stdout.strip()
    today = datetime.date.today().isoformat()
    try:
        h = git('log', '-1', '--format=%h', '--', str(pages_dir)) or 'uncommitted'
        dirty = bool(git('status', '--porcelain', '--', str(pages_dir)))
        if dirty:
            h += '+dirty'
        try:
            tag = git('describe', '--tags', '--abbrev=0')
        except subprocess.CalledProcessError:
            return f'{today}+{h}'
        if dirty or git('diff', '--name-only', tag, '--', str(pages_dir)):
            tag += '+modified'
        return f'{tag} ({today}, {h})'
    except (OSError, subprocess.CalledProcessError):
        return f'{today}+unknown'


def clean_page(t):
    t = re.sub(r'<!--\s*image \d+\s*-->\n?', '', t)
    t = re.sub(r'<!--\s*cont\s*-->', '\x00', t)  # protect the marker through comment stripping
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    t = re.split(r'\n---\s*\n+### Marginal notes', t)[0]
    t = t.split('### Marginal notes')[0]
    t = re.sub(r'(?m)^\*\*Header:\*\*.*\n?', '', t)
    t = re.sub(r'(?m)^(- )?Footer:.*\n?', '', t)
    t = re.sub(r'(?m)^---+[ \t]*\n?', '', t)  # the rule above a Footer: line (it would otherwise be taken for the last paragraph)
    t = t.replace('\\*', '*')
    t = re.sub(r'(?<=\S)[ \t]{2,}(?=\S)', ' ', t)
    t = re.sub(r'[ \t]+$', '', t, flags=re.M)
    t = re.sub(r'\n{3,}', '\n\n', t).strip('\n')
    return t


def compile_pages(files):
    out = []
    joined = 0
    for f in files:
        n = pagelist.label(f)
        raw = open(f, encoding='utf-8').read()
        t = clean_page(raw)
        if not t.strip():
            continue
        paras = t.split('\n\n')
        first = paras[0]
        if first.startswith('\x00'):
            first = first.lstrip('\x00').lstrip()
            prev = out[-1].rstrip() if out else ''
            if not prev or prev.startswith(('#', '<!--')):
                raise SystemExit(f'page {n}: <!-- cont --> but no paragraph to continue')
            if (prev.endswith('-') and first[:1].islower() and not prev.endswith(' -')
                    and prev[:-1].split(' ')[-1].lower() not in KEEP_HYPHEN):
                word, _, rest = first.partition(' ')
                out[-1] = prev[:-1] + word + f' <!-- page {n} --> ' + rest
            else:
                out[-1] = prev + f' <!-- page {n} --> ' + first
            joined += 1
            out.extend(p.replace('\x00', '') for p in paras[1:])
            continue
        out.append(f'<!-- page {n} -->')
        out.extend(p.replace('\x00', '') for p in paras)

    text = '\n\n'.join(out) + '\n'
    return re.sub(r'\n{3,}', '\n\n', text), joined


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pages-dir', default=str(ROOT / 'book-of-mormon-1852-pages'))
    ap.add_argument('--out', default=str(ROOT / 'book-of-mormon-1852.md'))
    args = ap.parse_args()

    files = [str(f) for f in pagelist.main_order(args.pages_dir)]
    text, joined = compile_pages(files)
    text = FRONTMATTER.format(version=build_version(args.pages_dir)) + text
    Path(args.out).write_text(text, encoding='utf-8')
    print(f'{len(files)} pages, {joined} joins, {len(text.split())} words -> {args.out}')


if __name__ == '__main__':
    main()
