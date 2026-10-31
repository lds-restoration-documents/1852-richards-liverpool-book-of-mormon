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
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pagelist  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

# Whole words the printer left a hyphen after at a page end (stray hyphens, not word breaks): never joined.
# Add them here when check_structure/compile output shows a glued word (1830 had 'sat', 'the').
KEEP_HYPHEN = set()


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
    Path(args.out).write_text(text, encoding='utf-8')
    print(f'{len(files)} pages, {joined} joins, {len(text.split())} words -> {args.out}')


if __name__ == '__main__':
    main()
