# 1852 Richards Liverpool Book of Mormon
[Markdown](#what-is-markdown) & Plain Text extractions of the content of the 1852 edition of the Book of Mormon published by Franklin D. Richards in Liverpool, England ("Third European Edition", stereotyped; "Published by F. D. Richards, 15, Wilton Street", sold at the L. D. Saints' Book Depot, London; printed by William Bowden, London). Extracted using AI.

## Files
* [book-of-mormon-1852.md](book-of-mormon-1852.md): the whole text in a single [Markdown](#what-is-markdown) file (about 276,000 words): the title page, the testimonies of the Three and Eight Witnesses, the table of contents and the Book of Mormon. Each printed page appears once, in printed order (see [Sources](#sources) for the duplicate and missing leaves). A `<!-- page NNN -->` comment marks where each page file begins.
* [book-of-mormon-1852.txt](book-of-mormon-1852.txt): the same text as plain text, with no [Markdown](#what-is-markdown).
* [book-of-mormon-1852-sparse.txt](book-of-mormon-1852-sparse.txt): plain text of the Book of Mormon proper only: the title page (PDF page 12) that was translated from the plates ("An account written by the hand of Mormon…"), followed by the text from 1 Nephi through Moroni (PDF pages 22–598). It leaves out the 1852 imprint on the title page (translator, edition, publisher, year), the title-page verso, the testimonies of the witnesses and the table of contents. Verse numbers are left out; the verses are separate paragraphs, so the text reads as continuous prose.
* [book-of-mormon-1852-sparse-verses.txt](book-of-mormon-1852-sparse-verses.txt): the same sparse text with the verse numbers kept ("6. And now…"). The 1852 edition is the first to print verse numbers.
* [book-of-mormon-1852-pages/](book-of-mormon-1852-pages/): one [Markdown](#what-is-markdown) file per page of the scan PDF (`page-001.md` to `page-605.md`, 605 files) plus `page-154a.md` and `page-154b.md` for the two printed pages missing from the scan, with running heads, headings and signature marks. File numbers are PDF page numbers (the printed page number is PDF page minus 21 at the start of the text, drifting later because of the duplicate and missing leaves). These are the source of truth; the files above are generated from them. Pages with no text (covers, blank leaves) have a one-line description. The duplicate leaves each have their own file, but appear only once in the combined files.
* [printer-typos.md](printer-typos.md): a catalog of the printer's slips and misspellings in the 1852 print (about 80 occurrences, each with its page and context), leaving out spellings that were normal or intentional for the period, such as "shew" (likely, not exhaustive).

## What is in the 1852 edition
* This is the **Third European Edition**, stereotyped, published by Franklin D. Richards in Liverpool in 1852. The print has printer's errors of its own, all kept as printed.
* **Verse numbers are printed in the text** ("6. And now…"), at the start of each verse paragraph, with each chapter's first verse starting again at 1. They are kept in every file in this repository (the page files, the Markdown, the plain text and the sparse-verses text; only the sparse text leaves them out). There are no double columns, no footnotes and no cross-references: the text is in paragraphs on a single wide column. Chapters are numbered within each book in Roman numerals ("CHAPTER II.", sometimes printed "CHAP. XX."), often with a short rule printed above the heading, and some chapters open with an italic summary.
* The **running head has three parts**. On even pages: the page number, the book name and the chapter mark (`336 | BOOK OF ALMA. | [CHAP. XVII.`); on odd pages: the chapter mark, the book name and the page number (`CHAP. XXI.] | BOOK OF ALMA. | 331`). Heads, folios and the odd ones (for example "BOOK OP MORONI.", "BOOK OE NEPHI.", a few misprinted folios such as `56` for 156, `202` for 292 and `811` for 311) are kept as printed.
* Spelling, capitalization, punctuation and grammar are kept exactly as printed, **printer's errors included**; nothing has been corrected from other editions, with three exceptions chosen by the owner when reviewing worn spots (see [Artificial Intelligence](#artificial-intelligence)). Punctuation is ordinary (commas, semicolons, colons and periods).
* The books, with the PDF page where each opens: First Book of Nephi (22, printed page 1), Second Book of Nephi (74), Jacob (135), Enos (printed page 134, in the second scan: `page-154a.md`), Jarom (157), Omni (159), Words of Mormon (162), Mosiah (164), Alma (230), Helaman (422), two successive books each headed "The Book of Nephi" (467 and 527), "The Book of Mormon" (531), Ether (551) and Moroni (585). As in the earlier editions, there is **no 3 Nephi or 4 Nephi by name**. Many books open in the middle of a page.
* The front of the book has the title page (PDF page 12), its verso ("ENTERED AT STATIONERS' HALL."), the **Testimony of the Three Witnesses and the Testimony of the Eight Witnesses** (page 14, both on one leaf) and a two-column **table of contents** by topic (PDF pages 16–21, with roman folios and "PAGE" column heads and dotted leaders; each entry is its own line in the page files, with the leader written as "…"). There is no index at the back. The text ends on PDF page 598 (printed page 563) with the end of Moroni, and the next page (PDF page 599) is the printer's imprint ("LONDON: PRINTED BY WILLIAM BOWDEN, 16, PRINCES STREET, RED LION SQUARE.").
* Signature marks at the foot of pages ("B", "B 2", "2 A", …) are recorded as footers.

## Sources
Transcribed from the 605-page PDF of a Google Books scan of the 1852 edition, available from the Internet Archive as [book-of-mormon-1852-liverpool-edition](https://archive.org/details/book-of-mormon-1852-liverpool-edition) (the item [bookmormon00smitgoog](https://archive.org/details/bookmormon00smitgoog) holds the same file; the two are byte-identical, not independent scans). The PDF is not included in this repository. Each PDF page holds one grey bitmap of one leaf (about 2200 x 3560 px); the PDF has no text layer except on page 1, which is Google's boilerplate. Page 1 is that boilerplate, pages 2–3 the front cover and a library label, 4–11 blank leaves and two half-titles ("THE BOOK OF MORMON."), page 12 the title page, 13 its verso (with a library stamp), 14 the testimonies, 15 a blank leaf, 16–21 the table of contents, 22 the opening of 1 Nephi, 23–598 the text, 599 the printer's imprint, 600–603 blank leaves, 604 a blank leaf with a label and 605 the back cover. Library stamps, labels and pencil notes are described only, not transcribed.

**Duplicate pages.** The scan photographed some leaves twice, so **16 PDF pages are duplicates**: the same printed page appears twice, each with its own image. They fall in four places: two pages of Jacob (printed pages 126–127), a long stretch at the opening of Alma (printed pages 200–217, which is in the scan twice), and one pair each in Alma (pages 310–311) and Helaman (pages 402–403). Every PDF page has its own page file, transcribed from its own image only (never copied from its twin), but in the combined files (`.md`, `.txt` and the sparse texts) each printed page appears **once**, using the first copy. The second copies, which are left out of those files, are:

| Printed page | First copy (used) | Duplicate (left out) |
|---|---|---|
| 126 (Jacob) | PDF 147 | PDF 155 |
| 127 (Jacob) | PDF 148 | PDF 156 |
| 200 (Alma) | PDF 221 | PDF 231 |
| 208 (Alma) | PDF 229 | PDF 239 |
| 209 (Alma, the opening of the Book of Alma) | PDF 230 | PDF 232 (damaged: the left part of its lines is cut off) and PDF 240 |
| 210 | PDF 233 | PDF 241 |
| 211 | PDF 234 | PDF 242 |
| 214 | PDF 235 | PDF 245 |
| 215 | PDF 236 | PDF 246 |
| 216 | PDF 237 | PDF 247 |
| 217 | PDF 238 | PDF 248 |
| 310 (Alma) | PDF 341 | PDF 343 |
| 311 (Alma) | PDF 342 | PDF 344 (printed folio `811`) |
| 402 (Helaman) | PDF 435 | PDF 437 |
| 403 (Helaman) | PDF 436 | PDF 438 |

The twins agree closely; their few differences (worn type, a mark that is a comma on one and a semicolon on the other) are listed in [duplicates-log.md](duplicates-log.md).

**Missing pages and the second scan.** Printed pages **134 and 135** are **missing from the scan**: one leaf, the opening of the Book of Enos (verses 1–6 in this edition's numbering). The scan goes from printed page 133, the end of Jacob (PDF 154, signature mark `N`, "Brethren, adieu."), straight to printed page 136 (PDF 157), which has the head of Jarom and the end of Enos; PDF pages 155–156, which sit where the missing leaf should be, are duplicate Jacob pages 126–127. Those two pages were transcribed from a **second, independent scan**: the Internet Archive item [BookOfMormon1852LiverpoolEdition](https://archive.org/details/BookOfMormon1852LiverpoolEdition) (569 page images `NNN.jpg` of 460 x 782 px, uploaded in 2014; the image number is the printed page plus 8, so printed pages 134–135 are images 142–143). It is the same typesetting, with a Google watermark at the foot. They are written to [`page-154a.md`](book-of-mormon-1852-pages/page-154a.md) (printed page 134) and [`page-154b.md`](book-of-mormon-1852-pages/page-154b.md) (printed page 135), inserted after PDF page 154, each with a `source:` comment; PDF 157 continues Enos's last sentence, so it starts with a `<!-- cont -->` marker. These two pages come from small images read at high zoom, so they are the least certain pages in the set; no other page was taken from the second scan.

Printed pages 212–213 are also not in the first run of the Alma opening (PDF 235, printed page 214, follows PDF 234, printed page 211) but are present in the second run (PDF 243–244, the pages that follow PDF 234), so nothing is missing from the text; in the combined files they are placed after page 211. Every other printed page, 1 to 563, is present in the scan.

## What is Markdown?
Markdown is a simple way of writing formatted text using plain characters, such as `#` for headings and `*asterisks*` for *italics*. A Markdown file is still readable as ordinary text, and can also be displayed with formatting.
* Learn more at [markdown.org](https://markdown.org/).
* Tools for displaying, editing, or converting Markdown files: [https://markdown.org/tools/](https://markdown.org/tools/)

## Artificial Intelligence
Extracted with Claude Code from Anthropic using the Sonnet 5.5 model. Each page is transcribed from one full-page image of the scan (there is no text layer or OCR), four pages at a time, by separate AI agents (a pilot set of pages was written first in the main session to fix the conventions); a script then checks the structure of every page file (chapter and verse sequence, markers, heads). A local OCR (tesseract) was compared with the transcription of every page (585 pages compared); it agreed on 554 of them and flagged the others, which went into the first proofreading sample. Separate AI agents working blind (without seeing the transcriber's notes) then proofread every text page against the scan, four pages at a time: first a sample of 104 pages (44 chosen because the OCR comparison or the running heads flagged them, 60 drawn at random), then all the remaining text pages (PDF 44–598), and the two Enos pages (printed pages 134–135) against the second scan. The proofread changed only about a dozen pages: a comma, a few chapter marks and folios, missing continuation markers, and two misread words (`conceruing` and `spare net`, both printer's errors that the first pass had normalized). No errors were deliberately planted to measure how many a proofreader misses, so the proofread is a single blind check, not a double-keyed one. A second AI pass then re-examined about 40 doubtful readings at high zoom, and the owner reviewed 195 flagged items (31 proofreader disagreements and every remaining doubtful mark) against the scan in a checklist; the decisions, about 30 changes, were applied. Where a mark was too worn to tell a comma from a period, the gap after it and whether the next word starts with a capital letter were used to decide. The text is meant to show what the page shows, so printer's spellings and errors, punctuation, hyphenation and paragraphing are kept. Where the owner judged a worn spot, the evident intended word was written in three places (`substances`, `of` and `therefore` on PDF pages 547, 548 and 170, printed `subatances`, `ot` and `theretore`). A few things are deliberately **not** reproduced: the thin space the type may put before `;`, `:`, `?` and `!`, handwriting, stamps, labels, and ink specks, stains and bleed-through that are not letters or punctuation.

**This is an AI transcription. Only the flagged doubtful spots have been checked by a person; it has not been proofread in full by a person.**

**Status: all 605 pages of the scan (and the two pages from the second scan) are transcribed and structure-checked, and every text page has been proofread blind once by a separate AI agent. The doubtful spots were re-examined and the owner reviewed the flagged ones, but a full human proofread has not been done.** The proofread suggests that few errors remain, but expect some, especially colon versus semicolon and comma versus period on worn type, worn letters, and inserted or dropped words. About 140 doubtful readings that could not be settled are still marked in the page files and listed in [uncertain-log.md](uncertain-log.md). For anything that matters, check the scan.

These files record how it was checked:

* [uncertain-log.md](uncertain-log.md): every doubtful reading and layout note recorded in the transcription, by page.
* [transcription-notes.md](transcription-notes.md): the layout of the scan, the conventions used, the review status and the log of each pass.
* [proofread-disagreements.md](proofread-disagreements.md): the proofreaders' disagreements and the second pass's changes that were put to the owner for review.
* [duplicates-log.md](duplicates-log.md): the differences between the copies of the duplicate leaves.

## Rebuilding the combined files
```
python3 tools/compile_markdown.py   # book-of-mormon-1852.md
python3 tools/make_plaintext.py     # book-of-mormon-1852.txt
python3 tools/make_sparse.py        # book-of-mormon-1852-sparse.txt and -sparse-verses.txt
python3 tools/make_typo_catalog.py  # printer-typos.md
python3 tools/make_uncertain_log.py # uncertain-log.md
python3 tools/make_duplicates_log.py # duplicates-log.md
python3 tools/check_structure.py --allow-gaps   # mechanical checks of the page files
python3 tools/ocr_diff.py           # OCR-vs-transcription comparison (work/ocr/, needs tesseract)
# review checklist for the doubtful spots (needs the scan PDF; reads proofread-disagreements.md):
~/.venvs/lds-transcribe/bin/python tools/make_review_checklist.py   # work/review/checklist.html
```
`tools/pagelist.py` holds the list of skipped duplicate leaves and the printed order that the combined files follow. See [tools/README.md](tools/README.md) for the full pipeline.
