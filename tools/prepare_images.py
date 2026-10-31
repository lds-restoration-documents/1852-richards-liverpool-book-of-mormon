#!/usr/bin/env python3
"""Extract the page images used for transcription from the scan PDF.

The PDF (Book-of-Mormon-1852.pdf, a Google Books scan, 605 pages) has one embedded 1-bit/grey bitmap per PDF page
(about 2200x3560 px; PDF page 1 is Google's boilerplate with a text layer), no text layer on the others. Dense verse
text would be downscaled to about 970x1570 by the image tool, so by default each page is written as two overlapping
halves (top 0-55%, bottom 45-100% of the height; sides trimmed to 2-98% of the width), pNNNN_a.jpg and pNNNN_b.jpg,
each about 1550 px wide. Use --full for the whole untrimmed page as pNNNN.jpg (front matter, odd layouts).
With --zoom Z (and optionally --box L,T,R,B as fractions of the page, e.g. 0,0.4,1,0.6) the page or box
is upscaled by Z and written as pNNNN_zZ[_box].jpg; upscaling adds no information, it only helps the eye
on a doubtful spot. Delete zooms afterwards with --clean.

Usage:
  python3 tools/prepare_images.py --pages 21-24
  python3 tools/prepare_images.py --pages 21 --full
  python3 tools/prepare_images.py --pages 21 --zoom 2 --box 0,0.4,1,0.6 --out work/zoom
  python3 tools/prepare_images.py --pages 21-24 --clean
Requires pypdfium2 and Pillow (~/.venvs/lds-transcribe/bin/python).
"""
import argparse
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / 'Book-of-Mormon-1852.pdf'


def parse_pages(spec, total):
    if not spec:
        return list(range(1, total + 1))
    out = []
    for part in spec.split(','):
        if '-' in part:
            a, b = part.split('-')
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def page_image(page):
    # some pages carry extra tiny image objects (specks, strips): take the largest
    best = None
    for o in page.get_objects():
        if o.type == 3:
            w, h = o.get_size() if hasattr(o, 'get_size') else (0, 0)
            im = o.get_bitmap().to_pil()
            if best is None or im.width * im.height > best.width * best.height:
                best = im
    if best is None:
        raise RuntimeError('no image on page')
    return best.convert('L')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pdf', default=str(PDF))
    ap.add_argument('--out', default=str(ROOT / 'work'))
    ap.add_argument('--pages', help='PDF page numbers, e.g. 1-16,302 (default: all)')
    ap.add_argument('--full', action='store_true', help='whole untrimmed page as pNNNN.jpg instead of two halves')
    ap.add_argument('--zoom', type=float, default=1)
    ap.add_argument('--box', help='L,T,R,B as fractions of the page (default: whole page)')
    ap.add_argument('--clean', action='store_true', help='delete generated images for --pages and exit')
    args = ap.parse_args()
    out = Path(args.out) / 'img'
    doc = pdfium.PdfDocument(args.pdf)
    pages = parse_pages(args.pages, len(doc))
    if args.clean:
        n = 0
        for p in pages:
            for f in out.glob(f'p{p:04d}*.jpg'):
                f.unlink()
                n += 1
        print(f'removed {n} files from {out}')
        return
    out.mkdir(parents=True, exist_ok=True)
    box = [float(v) for v in args.box.split(',')] if args.box else None
    suffix = ''
    if args.zoom != 1 or box:
        suffix = f'_z{args.zoom:g}' + ('_box' + args.box.replace(',', '-') if box else '')
    for n in pages:
        im = page_image(doc[n - 1])
        if not (args.full or box or args.zoom != 1):
            w, h = im.size
            l, r = int(0.02 * w), int(0.98 * w)  # was 6-94%, which clipped line ends on pages whose text runs to ~96% (e.g. 529, 541)
            for tag, (t, b) in (('a', (0, 0.55)), ('b', (0.45, 1))):
                part = im.crop((l, int(t * h), r, int(b * h)))
                k = 1550 / part.width
                part = part.resize((1550, int(part.height * k)), Image.LANCZOS)
                part.save(out / f'p{n:04d}_{tag}.jpg', quality=88)
            print(n, 'a+b', part.size)
            continue
        if box:
            w, h = im.size
            im = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
        if args.zoom != 1:
            im = im.resize((int(im.width * args.zoom), int(im.height * args.zoom)), Image.LANCZOS)
        im.save(out / f'p{n:04d}{suffix}.jpg', quality=88)
        print(n, im.size)


if __name__ == '__main__':
    main()
