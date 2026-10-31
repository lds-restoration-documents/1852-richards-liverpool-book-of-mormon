# Proofread run instructions (read after tools/proofread-spec.md)

You are an independent BLIND PROOFREADER of the 1852 Liverpool Book of Mormon. Read `tools/proofread-spec.md` completely and follow it exactly, and read `tools/transcription-spec.md`. Your batch id (`pNNN`) and your PDF pages are in your prompt.

Differences from the spec text for this run:
- Make your images with `~/.venvs/lds-transcribe/bin/python tools/prepare_images.py --pages A,B,C,D --full --out work/proof_pNNN`, view each `work/proof_pNNN/img/pNNNN.jpg` with the Read tool, and delete them at the end with the same command plus `--clean` (zoom spots: `--pages N --zoom 3 --box L,T,R,B --out work/proof_pNNNz`, delete afterwards). Never run `--clean` without your own `--out`.
- Write your log to `work/proof-log-pNNN.md`.
- Blindness: do NOT read `transcription-notes.md`, any other `work/proof-log-*.md`, `uncertain-log.md`, `printer-typos.md`, `duplicates-log.md`, `work/canaries*.json`, or anything in `work/ocr/`. The conventions you need are in the spec files and below. Do not read page files other than your own four (do not use other pages, including a duplicate twin, as examples).

Conventions in the page files (written by the transcription pass): first line `<!-- image NNN -->`; `**Header:** a | b | c` is the three-part running head with the printed folio (even pages `folio | BOOK OF X. | [CHAP. N.`, odd pages `CHAP. N.] | BOOK OF X. | folio`; kept as printed, errors included); `# THE … BOOK OF …` / `## CHAPTER N.` (or `CHAP. XX.` as printed); verses are paragraphs `N. text` with the printed verse number; italic `*…*`; small caps as capitals; `<!-- cont -->` on a flush-left first line; `---` then `Footer: X` for a signature mark; rules and ornaments are described in `<!-- … -->` comments only where printed; `<!-- uncertain: … -->` marks a doubtful reading; `[illegible]` marks unreadable text. Line-end hyphens are joined; page-end hyphens stay on the page. Printed errors, old spellings (shew, sware…) and odd punctuation are KEPT: never normalize.
CONTENTS pages (PDF 16–21): two columns each headed `PAGE`, left column first; each entry is its own paragraph with the dotted leader written as a single `…`; entries printed without a leader are written bare; compare every entry word by word and every page number digit by digit; numbers may be printed wrongly: keep them as printed. Roman folios in the head.
Front matter (PDF 12–14): title page, verso, testimonies: stacked lines in printed order and case.
Blank leaves, covers, labels (PDF 1–11, 599–605): only the page comment and a one-line description; confirm that no printed text was missed.
Printed pp. 134–135 (`page-154a.md`, `page-154b.md`) come from a different scan (archive.org `BookOfMormon1852LiverpoolEdition`, small 460x782 images); if asked to proofread them, use `work/alt/alt-p134.jpg` and `alt-p135.jpg` instead of the PDF.

The print does not follow the head pattern strictly: the chapter bracket may sit after the numeral on an even page (`CHAP. XII.]`), the period may be missing (`CHAP II.]`), and plural forms occur (`CHAPS. IV. V.]`). Write exactly what is printed; these are not errors to fix.

Check especially: words dropped or ADDED anywhere (compare line by line, word by word, not just line ends and page ends; an extra word such as `also` or `the` is easy to miss), clipped first or last words of lines, single-letter misreads, verse numbers (digits, sequence, missing), punctuation (colon vs semicolon, comma vs period), paragraph breaks, the cont marker, and the three-part head/folio/footer. For each page read the scan line by line and the page file in parallel; do not skim.

Edit only when certain, smallest possible edit, naming the scan evidence in the log. Final reply (max 8 lines): pages proofread, pages failed, edits grouped by kind with page numbers, number of disagreements.
