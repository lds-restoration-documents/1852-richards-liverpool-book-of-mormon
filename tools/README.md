# tools

The scripts and instructions used to produce the files in this repository. The page files in
`../book-of-mormon-1852-pages/` are the source of truth; the combined text files are generated from them.
(Adapted from the sibling `1841-young-kimball-pratt-liverpool-book-of-mormon`, `1840-robinson-smith-nauvoo-book-of-mormon`, `1837-pratt-goodson-kirtland-book-of-mormon` and `1830-grandin-palmyra-book-of-mormon` tooling.)

## Pipeline

1. **Prepare the images** (the scan is `../Book-of-Mormon-1852.pdf`, not in git; needs pypdfium2 and Pillow, e.g. `~/.venvs/lds-transcribe/bin/python`):
   `python3 tools/prepare_images.py --pages 12-15 [--zoom 2 --box L,T,R,B] [--out work]`
   extracts each page's embedded image to `work/img/`: by default two overlapping halves `pNNNN_a.jpg` / `_b.jpg` (sides trimmed to 2–98%), with `--full` the whole untrimmed page `pNNNN.jpg` (use it whenever a line end looks cut off: the earlier 6–94% trim clipped text on some pages). `--zoom`/`--box` upscale a region for a doubtful spot. Delete a batch's images afterwards with `--clean`. The PDF has no text layer or OCR.
2. **Transcribe**: AI agents (Claude) view the page image and write one `page-NNN.md` per PDF page following
   [transcription-spec.md](transcription-spec.md), four pages per agent. Blind proofreading followed [proofread-spec.md](proofread-spec.md) with
   the per-batch instructions in [proofread-run.md](proofread-run.md); a second pass on every doubtful place followed
   [uncertain-run.md](uncertain-run.md). These steps are done by agents, not by a script.
3. **Check**: `python3 tools/check_structure.py [--allow-gaps]` (page comment, `cont` markers, spacing before `; : ? !`, italics, verse-number continuity, chapter sequence per book, printed folio sequence; the duplicate/missing-leaf seams give expected warnings).
4. **Rebuild the combined files** (standard library only; run in this order; each writes to the repo root, `--out` redirects). `pagelist.py` holds the printed order: the combined outputs use each printed page once (first copy of each of the 16 duplicate leaves; `page-154a/154b` after PDF 154; PDF 243–244 after 234) and keep the inline verse numbers:
   ```
   python3 tools/compile_markdown.py     # -> book-of-mormon-1852.md
   python3 tools/make_plaintext.py       # -> book-of-mormon-1852.txt
   python3 tools/make_sparse.py          # -> book-of-mormon-1852-sparse.txt (no verse numbers) and -sparse-verses.txt
   python3 tools/make_typo_catalog.py    # -> printer-typos.md
   python3 tools/make_uncertain_log.py   # -> uncertain-log.md
   python3 tools/make_duplicates_log.py # -> duplicates-log.md
   ```

## Notes on the scripts

- `compile_markdown.py` strips comments, running heads and footers, and rejoins paragraphs that run across a page break using the `<!-- cont -->` marker; a line-end hyphen at a page end is closed up. Page markers carry the file label (`<!-- page 154a -->`). It aborts if a `<!-- cont -->` has no paragraph to continue.
- `make_sparse.py` keeps only the page ranges in `PAGE_RANGES` (page 12, the title page, whose abridgment text was translated from the plates, minus its imprint paragraphs, and pages 22–598, 1 Nephi through Moroni, with verse numbers); the testimonies (14), the CONTENTS (16–21) and the imprint and blank leaves (599–605) are left out. 
- `make_typo_catalog.py` builds `../printer-typos.md` from the curated lists in the script (empty until the proofread is done; `--candidates` prints the words not in the dictionary to triage); forms that do not occur simply produce no rows.
- `ocr_diff.py` (venv python, needs `tesseract`) OCRs the full untrimmed page images (cached in `work/ocr/`) and ranks pages by disagreement with the page files (`work/ocr/summary.tsv`, `work/ocr/diffs/NNN.txt`); it catches clipped or misread line ends. `page-154a/154b` have no PDF page and are not covered.
- `make_duplicates_log.py` builds `../duplicates-log.md`: for each of the 16 duplicate leaves, the heads, footers, word-level differences and `uncertain` marks of the used copy (A) and its skipped twin (B). The twins were transcribed independently, so identical text is a check, and a difference is a different reading of the same print.
- `make_uncertain_log.py` builds `../uncertain-log.md` from the comments in the page files.
- `make_review_checklist.py` (needs `~/.venvs/lds-transcribe/bin/python` and the PDF) builds `work/review/checklist.html` (gitignored, about 25 MB, images embedded; needs `tesseract`) from the disagreements in `../proofread-disagreements.md` and every `uncertain` comment in the page files. Each item shows the exact text from the raw page file around the item (verbatim, comments included, the item highlighted) and the scan. A red box and an enlarged view are drawn only when the file's last words before the spot are found in a local tesseract pass reliably (all words close, clearly better than any other place on the page); the caption shows what the OCR read inside the box. Otherwise the whole page is shown with nothing outlined. Keep/change/can't-tell buttons; decisions are kept in the browser and exported as text. Unlike 1837 there is no `review_items.json`: the items are read from the two sources, so it stays current.
