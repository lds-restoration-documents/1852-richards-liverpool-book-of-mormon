#!/usr/bin/env python3
"""Build printer-typos.md: a catalog of the likely printer's typos and misspellings in the 1852 text.

The list of forms is curated below (SECTIONS, RECURRING; filled in after the proofread from the output of
`--candidates`); this script finds every occurrence of each form in book-of-mormon-1852.md, with its image, printed
folio and a snippet of context, so the page numbers and contexts always come from the current text. Spellings that were
normal or intentional for the period or the edition (shew, sayeth, marvellous, ...) are deliberately NOT cataloged; see
NOT_INCLUDED at the end of the output.

Usage:
  python3 tools/make_typo_catalog.py [--md FILE] [--out FILE]
  python3 tools/make_typo_catalog.py --candidates [--md FILE]    # words not in /usr/share/dict, with counts and pages
"""
import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pagelist  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

# Sections: ('title', [(printed, should_be, note), ...]). `printed` is matched as a whole word, case-sensitive; a tuple
# (pattern, label) matches a literal string (e.g. a doubled word). Forms that do not occur simply produce no rows.
# Empty until the proofread is done: run --candidates and triage the list by eye against the scan.
SECTIONS = [
    ('Letters dropped, added or wrong (single-word slips)', [
        (w, sh, n) for w, sh, n in [
            ('acording', 'according', ''), ('adminster', 'administer', ''), ('apppointed', 'appointed', 'three p'), ('bablings', 'babblings', ''),
            ('beome', 'become', ''), ('brethen', 'brethren', ''), ('commandmennts', 'commandments', 'extra n'), ('commmandments', 'commandments', 'extra m'),
            ('conceruing', 'concerning', 'u for n'), ('decendant', 'descendant', ''), ('dilligence', 'diligence', ''),
            ('exceedidgly', 'exceedingly', 'd for n'), ('excerciseth', 'exerciseth', ''), ('exhalt', 'exalt', ''),
            ('garmeuts', 'garments', 'worn n'), ('heaken', 'hearken', ''), ('inquities', 'iniquities', ''), ('insomnch', 'insomuch', 'worn u'),
            ('iu', 'in', 'worn n'), ('messenge', 'messenger', 'no r'), ('murmer', 'murmur', ''), ('nothward', 'northward', ''),
            ('persuded', 'persuaded', ''), ('poeple', 'people', ''), ('provisons', 'provisions', ''), ('rccords', 'records', 'worn e'),
            ('reigu', 'reign', 'worn n'), ('repentence', 'repentance', ''), ('seach', 'search', ''), ('strategem', 'stratagem', ''),
            ('thay', 'they', ''), ('tinkliug', 'tinkling', 'worn n'),
            ('wilderdess', 'wilderness', 'd for n'), ('witheld', 'withheld', ''), ('withersoever', 'whithersoever', ''), ('witholding', 'withholding', ''),
            ('wlth', 'with', 'worn i'), ('wth', 'with', 'no i'), ('arriven', 'arrived', ''),
            ('govenor', 'governor', ''), ('kindom', 'kingdom', ''), ('trangress', 'transgress', ''), ('trangression', 'transgression', ''),
            ('ites', 'its', ''), ('ferest', 'forest', ''),
        ]]),
    ('Words run together or split', [
        ('havebecome', 'have become', 'no space printed'),
        ('Almtarried', 'Alma tarried', 'the page ends `Alm-` and the next page starts `tarried`: the `a` is missing; joined here without the hyphen'),
    ]),
    ('Wrong, missing or doubled words (grammar slips kept as printed)', [
        (('of of', 'of of'), 'of', 'doubled word'), (('and and', 'and and'), 'and', 'doubled word'),
        (('had began', 'had began'), 'had begun', 'wrong participle'), (('had took', 'had took'), 'had taken', 'wrong participle'),
        (('had wrote', 'had wrote'), 'had written', 'wrong participle'),
    ]),
    ('Variant spellings of names (next to a much more frequent spelling)', [
        ('Moronhihah', 'Moronihah', ''), ('Corantumr', 'Coriantumr', ''), ('Reedeemer', 'Redeemer', ''), ('Reedemer', 'Redeemer', ''),
        ('Lamanities', 'Lamanites', ''), ('Nepites', 'Nephites', ''), ('Jordon', 'Jordan', ''),
    ]),
]

# Misspellings that recur (the same slip printed several times): (label, [forms], should_be, why).
RECURRING = [
    ('arriven', ['arriven'], 'arrived', 'wrong ending'),
    ('govenor', ['govenor'], 'governor', 'dropped r'),
    ('kindom', ['kindom'], 'kingdom', 'dropped g'),
    ('trangress/trangression', ['trangress', 'trangression'], 'transgress(ion)', 'dropped s'),
    ('Reedeemer/Reedemer', ['Reedeemer', 'Reedemer'], 'Redeemer', 'extra e'),
]

NOT_INCLUDED = """## Not included: spellings that were normal or intentional

Spellings that were normal or intentional for the period or the edition are not printer's slips and are left out: `shew`/`shewed`/`shewn`/`sheweth`/`shewing`, `annointed`, `burthen(s)`/`burthensome`, `centre`, `sepulchre`, `marvellous`, `labour`/`favour`/`honour` and similar British spellings (which occur beside American `labored`), `-ize/-ise` variants, and the Old English verb forms. Book and proper names are listed only where a variant sits next to a much more frequent spelling.
"""


def load(md):
    raw = md.read_text(encoding='utf-8')
    parts = re.split(r'<!-- page (\d+)[ab]? -->', raw)
    segs, cur = [], 0
    for i, t in enumerate(parts):
        if i % 2 == 1:
            cur = int(t)
            continue
        t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
        segs.append((cur, re.sub(r'\s+', ' ', t)))
    return segs


def find(segs, spec):
    """Yield (page, snippet) for each occurrence."""
    if isinstance(spec, tuple):
        pat, hit = spec
        rx = re.compile(r'(?<![A-Za-z])' + re.escape(pat) + r'(?![A-Za-z])')
        hl = hit
    else:
        rx = re.compile(r'(?<![A-Za-z])' + re.escape(spec) + r'(?![A-Za-z])')
        hl = spec
    for pg, t in segs:
        if pg < 22 or pg > 598:
            continue
        for m in rx.finditer(t):
            a = max(0, m.start() - 38)
            b = min(len(t), m.end() + 30)
            s = t[a:b]
            i = s.find(hl) if hl in s else 0
            s = s[:i] + '**' + s[i:i + len(hl)] + '**' + s[i + len(hl):]
            yield pg, ('…' if a else '') + s.strip() + ('…' if b < len(t) else '')


def printed(pg):
    """The printed folio, from the page's running head (it drifts from the PDF number at the duplicate leaves)."""
    f = pagelist.PAGES_DIR / f'page-{pg:03d}.md'
    return (pagelist.header_folio(f) or '—') if f.exists() else '—'


def row(spec, should, note, segs):
    out = []
    for pg, snip in find(segs, spec):
        label = spec[1] if isinstance(spec, tuple) else spec
        out.append((pg, '| `%s` | %s | %d | %s | %s%s |' % (label, should, pg, printed(pg), snip.replace('|', '\\|'),
                                                           (' (' + note + ')') if note else '')))
    return out


INFLECT = ('s', 'es', 'ed', 'd', 'ing', 'eth', 'th', 'est', 'st', 'ly', 'er', 'ers', 'ness', 'ful', "'s")


def known(lw, words):
    """True if lw, or lw with a common inflection removed (web2 has base forms only), is a dictionary word."""
    if lw in words:
        return True
    for suf in INFLECT:
        if lw.endswith(suf) and len(lw) > len(suf) + 2:
            stem = lw[:-len(suf)]
            if stem in words or stem + 'e' in words or (len(stem) > 2 and stem[-1] == stem[-2] and stem[:-1] in words) \
                    or (stem.endswith('i') and stem[:-1] + 'y' in words):
                return True
    return False


def candidates(segs, top=None):
    """Words not in the system dictionary (lower-cased), with counts and the first pages, for triage by eye."""
    words = set()
    for f in ('/usr/share/dict/web2', '/usr/share/dict/words'):
        try:
            words |= {l.strip().lower() for l in open(f, errors='ignore')}
        except OSError:
            pass
    if not words:
        raise SystemExit('no /usr/share/dict word list found')
    seen = defaultdict(list)
    for pg, t in segs:
        if pg < 22 or pg > 598:
            continue
        for w in re.findall(r"[A-Za-z]+", re.sub(r'^\d+\.\s', '', t)):
            lw = w.lower()
            if not known(lw, words):
                seen[w].append(pg)
    rows = sorted(seen.items(), key=lambda kv: (len(kv[1]), kv[0]))
    for w, pgs in rows[:top]:
        print(f'{w}\t{len(pgs)}\t{",".join(str(p) for p in pgs[:6])}')
    print(f'# {len(rows)} distinct forms not in the dictionary (rare ones first; names and archaic words are expected)', file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--md', default=str(ROOT / 'book-of-mormon-1852.md'))
    ap.add_argument('--out', default=str(ROOT / 'printer-typos.md'))
    ap.add_argument('--candidates', action='store_true', help='list words not in the dictionary and exit')
    args = ap.parse_args()
    segs = load(Path(args.md))
    if args.candidates:
        candidates(segs)
        return
    total, missing = 0, []
    header = '| Printed | Should be | Image | Printed p. | In context |\n|---|---|---|---|---|'
    body = []
    for title, items in SECTIONS:
        rows = []
        for spec, should, note in items:
            r = row(spec, should, note, segs)
            if not r:
                missing.append(spec)
            rows += r
        rows.sort(key=lambda x: x[0])
        total += len(rows)
        body.append('\n## %s (%d)\n\n%s\n%s' % (title, len(rows), header, '\n'.join(r for _, r in rows)))
    rec = []
    for label, forms, should, why in RECURRING:
        hits = sorted(h for f in forms for h in find(segs, f))
        total += len(hits)
        rec.append('| `%s` | %s | %d | %s | %s |' % (label, should, len(hits), why, ', '.join(str(p) for p, _ in hits)))
    intro = f"""# Printer's typos and misspellings in the 1852 Book of Mormon

A catalog of the places where the 1852 print itself has a slip of the type, a misspelling, or a doubled word, as the transcription records
it. {total} occurrences, grouped by the kind of slip, each with its image (PDF page), printed folio and context.

**What is and is not here.** The transcription keeps every printed error exactly as printed (nothing was corrected from other editions), so
all of these are in the page files as printed. This list leaves out spellings that were normal or intentional for the period or the edition
(see the end of the file). It is built from a dictionary scan of the whole text, triaged by eye, so it is **likely, not exhaustive**: a slip that
happens to produce another real word is only caught where it was noticed. Some rows are worn-type readings: the scan shows a letter that looks like
the printed one, which the transcription kept as printed.

**Where to see the original.** Numbers are PDF page numbers of the scan Book-of-Mormon-1852.pdf (605 pages); the printed folio is read from each
page's running head. No images are included in this repository.

Generated by `tools/make_typo_catalog.py` from the live text, so page numbers and contexts stay current if the pages are edited.
"""
    recsec = ('\n## Misspellings that recur\n\nThe same slip printed more than once (compositor habits rather than one-off slips).\n\n'
              '| Printed | Should be | Times | Slip | images |\n|---|---|---|---|---|\n' + '\n'.join(rec))
    Path(args.out).write_text(intro + '\n'.join(body) + '\n' + recsec + '\n\n' + NOT_INCLUDED, encoding='utf-8')
    print(f'{total} occurrences -> {args.out}')
    if missing:
        print('NOT FOUND in the text:', missing)


if __name__ == '__main__':
    main()
