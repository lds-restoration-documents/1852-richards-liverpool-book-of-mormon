#!/usr/bin/env python3
"""Build the sparse plain-text file (Book of Mormon text only) from book-of-mormon-1852.md.

Keeps book titles, chapter headings and paragraphs (with their verse numbers) from the page ranges that hold the
Book of Mormon proper, plus the title page (PDF page 12: "An account written by the hand of Mormon upon
plates taken from the plates of Nephi ... Moroni"), which was translated from the plates; the imprint paragraphs
on it (translator, edition, printer, publishers, year) are dropped. Also dropped: the title-page verso, the
testimonies, the CONTENTS, the printer's imprint after the text (PDF 599), and any paragraph that is only an end marker such as FINIS.

The compiled Markdown carries <!-- page NNN --> markers, which this script uses
to decide what is in range. PAGE_RANGES is specific to the scan (PDF page
numbers, not printed folios): see transcription-notes.md §1.

Writes two files: book-of-mormon-1852-sparse.txt (verse numbers removed) and
book-of-mormon-1852-sparse-verses.txt (verse numbers kept).

Usage:  python3 tools/make_sparse.py [--md FILE] [--out FILE] [--out-verses FILE] [--verbose]
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pagelist  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

# Inclusive PDF-page ranges kept: the title page (12, which also carries the abridgment translated from the plates) and the
# text from page 22 (1 Nephi) through page 598 (end of Moroni). Outside it: covers and leaves (1-11), the title-page verso
# (13), the testimonies (14), the CONTENTS (16-21) and the imprint and blank leaves (599-605). Page-154a/154b (printed
# pp. 134-135, Enos) count as PDF 154 and are in range. Twin copies of duplicate leaves are not in the compiled Markdown.
# PROVISIONAL: confirm 598 as the last text page and the title-page paragraphs below against the page files.
PAGE_RANGES = [(12, 12), (22, 598)]

# On the title page, the paragraphs of the 1852 imprint are dropped (they start with these words).
TITLE_PAGE = 12
IMPRINT_PREFIXES = ('TRANSLATED BY', 'Third European', 'STEREOTYPED', 'Liverpool', 'PUBLISHED BY', 'London', 'SOLD AT', '85, JEWIN', 'AND BY ALL', '1852')

END_MARKERS = re.compile(r'\*?(THE END[.,]?|FINIS[.,]?)\*?', re.I)


def in_range(pg):
    return pg is not None and any(a <= pg <= b for a, b in PAGE_RANGES)


def annotate(md_text):
    """Split into paragraphs, each tagged with the image it starts on."""
    page = None
    items = []
    for p in md_text.split('\n\n'):
        ms = re.findall(r'<!-- page (\d+)[ab]? -->', p)
        clean = re.sub(r'\s*<!-- page \d+ -->\s*', ' ', p).strip()
        if ms and p.startswith('<!-- page'):
            page = int(ms[0])
        if clean:
            items.append((page, clean))
        if ms and not p.startswith('<!-- page'):
            page = int(ms[-1])
    return items


def plain(l):
    l = l.replace('**', '').replace('*', '')
    l = re.sub(r'^#{1,6}[ \t]+', '', l)
    l = re.sub(r'</?[a-zA-Z][^>]*>', '', l)
    return re.sub(r'(?<=\S) {2,}(?=\S)', ' ', l).strip()


VERSE_NUM = re.compile(r'^\d+\.\s+')


def strip_verse(p):
    return VERSE_NUM.sub('', p, count=1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--md', default=str(ROOT / 'book-of-mormon-1852.md'))
    ap.add_argument('--out', default=str(ROOT / 'book-of-mormon-1852-sparse.txt'))
    ap.add_argument('--out-verses', default=str(ROOT / 'book-of-mormon-1852-sparse-verses.txt'))
    ap.add_argument('--verbose', action='store_true', help='list the paragraphs that were dropped')
    args = ap.parse_args()

    if not PAGE_RANGES:
        raise SystemExit('PAGE_RANGES is empty: set the Book of Mormon page ranges at the top of this script first.')

    items = annotate(pagelist.strip_frontmatter(Path(args.md).read_text(encoding='utf-8')))
    kept, dropped = [], []
    for pg, p in items:
        if (in_range(pg) and not END_MARKERS.fullmatch(p.strip())
                and not (pg == TITLE_PAGE and p.lstrip('*').startswith(IMPRINT_PREFIXES))):
            kept.append(p)
        else:
            dropped.append((pg, p))
    for out, fn in ((args.out, strip_verse), (args.out_verses, lambda p: p)):
        text = '\n\n'.join(q for q in (fn(plain(p)) for p in kept) if q) + '\n'
        text = re.sub(r'\n{3,}', '\n\n', text)
        Path(out).write_text(text, encoding='utf-8')
        print(f'kept {len(kept)} paragraphs, dropped {len(dropped)}, {len(text.split())} words -> {out}')
    if args.verbose:
        for pg, p in dropped:
            print(pg, p[:70])


if __name__ == '__main__':
    main()
