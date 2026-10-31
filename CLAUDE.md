# CLAUDE.md

Guidance for Claude Code in this repository.

## What this repo is

A text corpus, not software: AI-assisted transcription of the 1852 edition of the Book of Mormon (Liverpool: Franklin D. Richards), from `Book-of-Mormon-1852.pdf` (gitignored; Google Books scan via archive.org item `book-of-mormon-1852-liverpool-edition`). The PDF has **605 pages**: PDF 1 is Google's boilerplate (US Letter, has a text layer); the rest are one grey bitmap (~2200x3560 px) per leaf, **no text layer**. Method and tools are adapted from `../1841-young-kimball-pratt-liverpool-book-of-mormon` (newest; read its `transcription-notes.md`), `../1840-…`, `../1837-…`, `../1830-…`.

**Status (2026-10-31):** **The project is essentially complete.** Every PDF page 1–605 plus `page-154a/154b` is transcribed; every text page (PDF 44–598) had one blind AI proofread against the full-page image (first a 104-page sample, then batches p027–p141 in `work/proofread-batches2.tsv`; `page-154a/154b` against the alt scan); a second zoomed AI pass settled the doubtful spots; the owner reviewed a 195-item checklist (`work/review/checklist.html`, input `proofread-disagreements.md`) and the decisions (about 30 changes) were applied. Generated and current: `book-of-mormon-1852.md/.txt`, `-sparse.txt`, `duplicates-log.md`, `printer-typos.md` (78 occurrences), `uncertain-log.md` (141 uncertain comments); `check_structure.py --allow-gaps`: 0 errors, 9 expected warnings (verse jumps at duplicate/missing leaves). `README.md` was written 2026-10-31 (same format as the 1841 README, with Sources covering the 16 duplicate leaves, the missing printed pp. 134–135 and the second scan). Full log of every pass: `transcription-notes.md` §3. **Not done:** a full human proofread; a double-keyed or planted-error check (none was run, so the miss rate is unknown); about 14 doubtful spots stay ambiguous (owner chose "keep"); the owner has not committed anything (**never `git commit`/`git push` here**). If you change a page file, rerun the generators listed in the README ("Rebuilding"). Known caveats: PDF 44–528 were first transcribed from side-trimmed halves, but the proofread used full images.

## Differences from 1841
- **Verse numbers are printed inline** ("6. And now…"); keep them in the page files and in ALL outputs (.md, .txt, sparse) — owner decision.
- Running head has three parts. Even pages: `folio | BOOK OF X. | [CHAP. N.`; odd pages: `CHAP. N.] | BOOK OF X. | folio` (the chapter mark prints as `[CHAP. N.` on the right of even pages and `CHAP. N.]` on the left of odd pages; write the bracket as printed).
- Front matter has roman folios; CONTENTS (topic list, two columns, PAGE heads) is at the front, PDF ~16–21; no index at the back.
- **16 PDF pages are duplicate leaves** (same printed page twice): 147~155, 148~156, 221~231, 229~239, 230~240, 233~241, 234~242, 235~245, 236~246, 237~247, 238~248, 341~343, 342~344, 435~437, 436~438, 232~240 (232 = p. 209, Alma's opening; twin of 240, text partly cut off at the foot). Owner decision: transcribe every PDF page into its own file; combined outputs follow printed order with each printed page once (use the first copy unless the second is clearer; record differences between twins in a duplicates log).

- **Missing from the scan: printed pp. 134–135** (one leaf: the opening of the Book of Enos, verses 1–6 in the 1852 numbering; Enos ends on p. 136 and Jarom begins there). PDF 154 (p. 133) ends Jacob ("Brethren, adieu.", signature `N`) and PDF 157 is p. 136 (Jarom head); PDF 155–156 are duplicate Jacob pp. 126–127 sitting where the leaf should be. Printed pp. 212–213 are missing in the first Alma run (PDF 235 follows p. 211) but present in the second (PDF 243–244). Every other printed page 1–563 is present. Enos comes from a second, independent scan: archive.org item `BookOfMormon1852LiverpoolEdition` (569 page JPEGs `NNN.jpg`, 460x782 px, uploaded 2014; image = printed page + 8; images 142–143 = pp. 134–135, same typesetting, Google watermark at the foot; local copies `work/alt/alt-p134.jpg`, `alt-p135.jpg`). Pages 134–135 are transcribed from it into `book-of-mormon-1852-pages/page-154a.md` and `page-154b.md` (inserted after PDF 154; each has a `source:` comment; PDF 157 (p. 136) continues Enos's last sentence, so it starts with `<!-- cont -->`) and recorded in `transcription-notes.md`. archive.org items `bookmormon00smitgoog` and `book-of-mormon-1852-liverpool-edition` are byte-identical to our PDF (same MD5), not independent.
- A few PDF pages (4, 232, 427, 433, 461, 489) carry extra tiny image objects; `prepare_images.py` takes the largest.

## Files
`book-of-mormon-1852-pages/page-NNN.md` (NNN = PDF page, 3 digits) are the source of truth; everything else is derived. Page images: `~/.venvs/lds-transcribe/bin/python tools/prepare_images.py --pages A-B` writes two overlapping halves `work/img/pNNNN_a.jpg` (top) and `_b.jpg` (bottom) per page; `--full` the whole page; `--clean` deletes.

## Rules
- Write what the scan shows, never what you think it should say (no corrections from other editions/KJV/memory). Doubtful: `<!-- uncertain: … -->`; unreadable: `[illegible]`.
- Never transcribe without viewing the images. If the image tool fails, stop and report the page.
- Batches of 4 pages per subagent; skip pages whose file exists; `--clean` after each batch; check `df -h .` before each group (disk is tight).
- Review is lean: local tesseract diff, mechanical checks (verse-number continuity), blind proofread of flagged pages plus a random sample; record model and review per range in `transcription-notes.md`; never claim a page was proofread when it was not.
- No images in tracked files. **Never `git commit` or `git push`**; the owner does. `README.md` is owner-edited: change it with small edits only.
- Main session coordinates; subagents view images and reply in 1–2 lines.

## Next steps
All steps 1–5 are done (trial, bulk transcription, tools, review, README); see Status and `transcription-notes.md`. Optional: a second independent proofread of a random sample with planted errors to estimate the miss rate; a human proofread; a second look at the ~14 ambiguous spots (list in `proofread-disagreements.md`); the owner commits.

## Reference data (gitignored, in `work/survey/`)
`ocr-full/NNN.txt` = tesseract of every PDF page 2–605 (pages 232, 427, 433, 461, 489 re-OCR'd from the largest image); `heads-ocr.tsv`, `folios-ocr.tsv` = OCR of page heads/folios (noisy: leading digits often dropped); `pairs.txt` = duplicate pairs found; scripts `survey*.py`, `fullocr.py`. Do not request pages from sites that block automated access, and do not spoof a browser User-Agent (the harness denied that once).
