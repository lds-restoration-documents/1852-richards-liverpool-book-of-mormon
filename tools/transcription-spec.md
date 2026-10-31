# Transcription spec — 1852 Richards (Liverpool) Book of Mormon

Instructions for transcribing agents. Source: `Book-of-Mormon-1852.pdf` (605 pages; a Google Books scan, grey bitmaps, no text layer). Files are keyed to the **PDF page number** (3 digits). Layout: PDF 1–21 front matter (1 Google boilerplate, 2–3 cover/library label, 4–11 blank/half-title leaves, 12 title page, 13 verso, 14 both testimonies, 16–21 CONTENTS with roman folios), 22 opens 1 Nephi (printed p. 1), 23–598 text (printed folio = PDF − 21 at the start, but **16 PDF pages are duplicate leaves and the folio offset drifts**: write the folio as printed), 599–605 blank leaves and back cover. Printed pp. 134–135 are not in the PDF (pilot files `page-154a.md`, `page-154b.md`).

Input for PDF page N in `work/`: `img/pNNNN_a.jpg` (top ~55% of the page) and `img/pNNNN_b.jpg` (bottom ~55%), each about 1550 px wide; **the two overlap by about 10%: a line seen in both halves is written once.** View both with Read before writing; also look at the edges (running head, signature mark). If an image fails, stop and report the page; never transcribe unseen. For a doubtful spot: `~/.venvs/lds-transcribe/bin/python tools/prepare_images.py --pages N --zoom 2 --box 0,0.4,1,0.6 --out work/zoom` (box = L,T,R,B fractions; delete it afterwards). Output: `book-of-mormon-1852-pages/page-NNN.md`. Skip pages whose file exists. Write each file right after viewing its page.

## Rules
- **Write what is printed, never what you think it should say.** Printer's errors, odd spellings (British `favoured`, `honour`, `labours` and American `labored` both occur), names, grammar, doubled or missing words, wrong running heads and wrong folios are kept. Never correct from other editions, the KJV, the modern text or memory: you know this book, so read letter by letter.
- **Verse numbers are printed** (`1.`, `2.` …) at the start of each verse; each verse is its own paragraph, written `N. text`. Write the number exactly as printed (the numeral glyphs 3/8, 5/6 are easily confused: use the next/previous verse as a check but report a mismatch with `uncertain`). A page-top fragment continuing a verse has no number.
- Doubtful reading: best guess plus `<!-- uncertain: … -->` right after it. Unreadable: `[illegible]`. Worn comma/period: more space and a capital next = period; less space and lowercase next = comma (add `uncertain`).
- Line-end hyphenation is joined into the whole word; words hyphenated in the original stay hyphenated (grep other page files if unsure). A word split across lines with no hyphen is written joined, with a comment.
- No space before `; : ? !` (the type has a thin space; not transcribed). Record punctuation, `&c.`, dashes `—` exactly.
- Italic = `*italic*` (no space inside the asterisks). Small caps = capitals (`I, NEPHI,`; `my FATHER.`). Black-letter (Old English) headings in the front matter are written in the case printed (`The Testimony of Three Witnesses.`).
- Ink specks, foxing, bleed-through, dirt, blots and page-edge shading are not text: ignore them without comment unless a blot hides a mark (then `uncertain`). Handwriting, library stamps/labels, barcodes: describe in an HTML comment only.

## Format
```
<!-- image NNN -->
**Header:** 180 | BOOK OF MOSIAH. | [CHAP. IX.        <- running head, parts separated by " | ", in printed left-to-right order (even pages: folio first, `[CHAP. N.` last; odd pages: `CHAP. N.]` first, folio last, e.g. `CHAP. I.] | FIRST BOOK OF NEPHI. | 3`); omit if none

<!-- cont --> iniquities. Yea, and ye ...             <- first line flush left = continues the previous page's paragraph

6. And now it came to pass that Alma, ...            <- verse paragraph

---

Footer: B                                            <- signature mark at the foot, not in the Header (omit if none)
```
- Book opening: `# THE FIRST BOOK OF NEPHI.` (and any subtitle as a plain line), a comment for each rule/ornament printed (`<!-- short centred rule printed above the chapter heading -->`), then `## CHAPTER I.`, then the italic summary as one paragraph. A book opening mid-page keeps the running head of the book the page began in (comment it). Chapter headings use the numerals as printed.
- If the page ends mid-sentence write the fragment (a page-end hyphen stays: `vis-`) and the next page starts `<!-- cont -->`; if the page's first line is flush left it is a continuation even after a full stop.
- Text cut off or missing in the scan: write only what is visible (each fragment line prefixed `[illegible]`), put a comment at the top saying what is lost and where the twin page is; never complete it.
- **Duplicate leaves** (see CLAUDE.md for the list): transcribe each PDF page from its own images; never copy from its twin.
- CONTENTS pages (PDF 16–21, two columns each headed `PAGE`): left column then right; each entry is its own paragraph `Entry text … 123` with the dotted leader written as one `…`; wrapped entries are joined into one line; book entries in small caps are written in capitals; short rules between books need no mark; an entry printed without a leader has none; roman folio and `CONTENTS.` in the Header.
- Title page, verso, testimonies: transcribe in full as stacked paragraphs in printed order, with a layout comment (see `page-012.md`, `page-014.md`).
- Blank leaves, covers, labels: the page comment plus a one-line description comment only.
- No commentary, summaries or modern corrections.

## Agent run notes
- A batch is 4 pages. Run `~/.venvs/lds-transcribe/bin/python tools/prepare_images.py --pages A-B` first, `--clean` when done. Final reply: pages written, pages failed, anything unusual (1–2 lines). Do not run `git`.
- Examples to match: `page-022.md` (book opening), `page-023.md` (verse page), `page-157.md` (cont + book opening), `page-017.md` (CONTENTS), `page-232.md` (damaged scan).
