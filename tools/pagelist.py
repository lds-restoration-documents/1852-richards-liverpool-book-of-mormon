"""Page-file naming and printed order for the 1852 transcription (shared by the build tools).

Files are `page-NNN.md` (NNN = PDF page) plus `page-154a.md` and `page-154b.md` (printed pp. 134-135, from the
second scan, which belong after PDF 154). `main_order()` gives the files in printed order with each printed page once.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES_DIR = ROOT / 'book-of-mormon-1852-pages'

# Duplicate leaves (same printed page twice): the first copy is used in the combined outputs, these twins are skipped.
# 155~147, 156~148 (Jacob pp. 126-127); 231~221 (p. 200); 239~229 (p. 208); 232 and 240 ~ 230 (p. 209; 232 is damaged);
# 241~233, 242~234, 245~235, 246~236, 247~237, 248~238 (pp. 210-211, 214-217); 343~341, 344~342; 437~435, 438~436.
SKIP = {155, 156, 231, 232, 239, 240, 241, 242, 245, 246, 247, 248, 343, 344, 437, 438}

# Printed pp. 212-213 sit at PDF 243-244, which follow PDF 234 (p. 211) in printed order; PDF 235 (p. 214) comes next.
MOVE_AFTER = {234: [243, 244]}
MOVED = {243, 244}

LABEL_RE = re.compile(r'page-(\d{3}[ab]?)\.md$')


def label(path):
    """'154a' for page-154a.md, '021' for page-021.md."""
    m = LABEL_RE.search(str(path))
    if not m:
        raise ValueError(f'not a page file: {path}')
    return m.group(1)


def pdf_number(lab):
    """PDF page number (int) of a label ('154a' -> 154)."""
    return int(lab[:3])


def all_files(pages_dir=PAGES_DIR):
    """Every page file in PDF order (154, 154a, 154b, 155, ...)."""
    return sorted(Path(pages_dir).glob('page-*.md'), key=lambda p: (pdf_number(label(p)), label(p)))


def main_order(pages_dir=PAGES_DIR):
    """Page files in printed order, each printed page once (twin copies skipped, 243-244 moved after 234)."""
    files = {label(p): p for p in all_files(pages_dir)}
    out = []
    for lab, p in files.items():
        n = pdf_number(lab)
        if n in SKIP or n in MOVED:
            continue
        out.append(p)
        for m in MOVE_AFTER.get(n, []):
            q = files.get(f'{m:03d}')
            if q is not None:
                out.append(q)
    return out


def header_folio(path):
    """The printed folio from the running head of a page file, or None (roman or missing)."""
    t = Path(path).read_text(encoding='utf-8')
    m = re.search(r'(?m)^\*\*Header:\*\*\s*(.*)$', t)
    if not m:
        return None
    parts = [re.sub(r'<!--.*', '', x).strip() for x in m.group(1).split('|')]
    for x in (parts[0], parts[-1]):
        if re.fullmatch(r'\d+|[ivxl]+\.?', x, re.I):
            return x.rstrip('.')
    return None


def strip_frontmatter(t):
    """Remove the YAML frontmatter block that compile_markdown.py puts at the top of book-of-mormon-1852.md."""
    if t.startswith('---\n'):
        end = t.find('\n---\n', 4)
        if end != -1:
            return t[end + 5:].lstrip('\n')
    return t
