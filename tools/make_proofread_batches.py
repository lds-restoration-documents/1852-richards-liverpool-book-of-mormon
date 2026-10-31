#!/usr/bin/env python3
"""Build the blind-proofread batch list (4 PDF pages per batch) and the agent prompts.

Order: pages flagged by the OCR diff, running-head/folio candidates, pages whose folio/chapter mark was written
"from the sequence", the front matter (CONTENTS etc.), then a seeded random sample of the other text pages.
Writes work/proofread-batches.tsv (batch id, pages, reason) and work/proofread-prompts.md (one prompt per batch).
Usage: python3 tools/make_proofread_batches.py [--random 60] [--seed 1852]
"""
import argparse, random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FIRST = [
    ('ocr', [545, 581]),
    ('head', [34, 125, 178, 244, 312, 351, 514, 560, 586]),
    ('ocr', [41, 45, 107, 108, 131, 156, 199, 256, 271, 321, 415, 448, 452, 483, 503, 536, 537, 540, 553, 563, 569, 578]),
    ('sequence', [323, 393, 460, 481]),
    ('front', [14, 16, 17, 18, 19, 20, 21]),
]
TEXT = range(23, 599)  # PDF 22 (book opening) and blanks are covered separately; 154a/154b need the alt scan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--random', type=int, default=60)
    ap.add_argument('--seed', type=int, default=1852)
    args = ap.parse_args()
    seen, items = set(), []
    for why, pages in FIRST:
        for p in pages:
            if p not in seen:
                seen.add(p)
                items.append((p, why))
    pool = [p for p in TEXT if p not in seen and (ROOT / 'book-of-mormon-1852-pages' / f'page-{p:03d}.md').exists()]
    for p in sorted(random.Random(args.seed).sample(pool, args.random)):
        items.append((p, 'random'))
    batches = [items[i:i + 4] for i in range(0, len(items), 4)]
    out = ROOT / 'work'
    out.mkdir(exist_ok=True)
    with open(out / 'proofread-batches.tsv', 'w') as t, open(out / 'proofread-prompts.md', 'w') as m:
        for i, b in enumerate(batches, 1):
            bid = f'p{i:03d}'
            pages = ','.join(str(p) for p, _ in b)
            t.write(f"{bid}\t{pages}\t{','.join(sorted({w for _, w in b}))}\n")
            m.write(f"## {bid} (PDF {pages})\n\n")
            m.write(
                f"You are a blind proofreader of the 1852 Liverpool Book of Mormon transcription. Read "
                f"tools/proofread-run.md, then tools/proofread-spec.md and tools/transcription-spec.md, and follow them exactly. "
                f"Batch id: {bid}. PDF pages: {pages}. Log: work/proof-log-{bid}.md. "
                f"Use your own images in work/proof_{bid} (--full), delete only those when done. No git. "
                f"Reply in at most 8 lines.\n\n")
    print(len(items), 'pages,', len(batches), 'batches')


if __name__ == '__main__':
    main()
