# CISSP Study Portal

An interactive study portal for the ISC2 CISSP exam: **2,615 practice questions**, each
filed under the sub-section of the official CISSP exam outline that it tests, with a
tailored study guide for every one of the 61 sub-sections.

Open **`CISSP_Study_Portal.html`** in a browser (it works straight from `file://` — keep it
next to `cissp-data.js`).

## What's inside

- **61 sub-sections** across the 8 domains. Click a sub-section and you get only the
  questions that belong to it.
- **A study guide per sub-section**, built from the questions it holds:
  - *Focus* — what the sub-section covers in exam terms
  - *Must know* — the facts the questions test (262 bullets)
  - *Deeper lesson notes* — deeper insights per topic
  - *Key terms & meanings* — a glossary of **1,201 terms** with definitions
  - *Also know these terms* — further vocabulary appearing in that sub-section
- **Global A–Z glossary** with a live filter and jump-to-section buttons.
- **Question reader**: one-at-a-time or continuous document layout, answer → explanation,
  mark for review, search across all questions, keyboard shortcuts, progress saved in the
  browser.

## Layout

| Path | Purpose |
|---|---|
| `CISSP_Study_Portal.html` | The single-page app |
| `cissp-data.js` | Question bank + guides (loaded by the app) |
| `subsection_keywords.py` | Curated within-domain vocabulary used for classification |
| `classify_subsections4.py` | Rule-based sub-section classification |
| `merge_adjudication.py` | Merges reviewed labels, applies consistency corrections |
| `subsection_guides.py` | Curated focus + must-know content for the 61 sub-sections |
| `subsection_deep_notes.py` | Deeper lesson notes per sub-section |
| `subsection_glossary_extra.py` | Curated definitions and overrides |
| `defs.py` | Definition extractor (indexes the reference books) |
| `enrich_guides.py` | Builds the per-sub-section term glossaries |
| `build_web_data2.py` | Assembles `cissp-data.js` |
| `extract_pdf.py`, `extract_books.py` | Text extraction from the source question PDF and the reference books |
| `smoke_test2.js` | Headless verification of data and UI |
| `make_batches.py` | Builds the review batches used for question-by-question adjudication |
| `validate_final.py`, `sample_sections_final.py`, `check_placement.py` | Quality inspection helpers |
| `_classify/final_assignments.json` | Question → sub-section mapping |
| `_classify/guide_terms.json` | Mined term meanings |
| `archive/` | Earlier iterations (first-pass organisers, PDF builders, superseded classifiers) kept for reference only |

## How the questions were organised

1. **Classification.** Every question was placed in a sub-section: curated within-domain
   keyword rules first, then the uncertain ones reviewed question-by-question against the
   official outline, then consistency corrections (for example unifying TCSEC / Common
   Criteria / reference-monitor questions into 3.4).
2. **Text repair.** The source PDF extraction split words ("th e", "technolo gy", "ofa",
   "classificati on") and lost spaces. A repair engine with ~2,000 learned rules rebuilt
   the text, guarded against false joins (it preserves "U.S.", "a T1", "ring zero memory").
3. **Answer integrity.** Options beyond letter D, offset option labels (E–H while the answer
   key refers to position) and "?" bullet lists were parsed correctly, leaving **0 questions
   without an answer and 0 with fewer than two options**.

## Regenerating the data

```bash
python classify_subsections4.py     # rule-based labels
python merge_adjudication.py        # merge reviewed labels + corrections
python enrich_guides.py             # mine key-term meanings (needs the reference books)
python build_web_data2.py           # rebuild cissp-data.js
node smoke_test2.js                 # verify
```

`extract_books.py` re-creates the plain-text extracts of the reference study guide and exam
companion; those extracts are intentionally not committed.

## Verification

`node smoke_test2.js` checks question integrity, sub-section coverage, glossary quality and
every portal view. All checks pass.

## Notes

- Sub-section boundaries are occasionally fuzzy in the CBK (physical security spans 3.9 and
  7.14; DR processes 7.11 versus DR testing 7.12), so a few questions sit in the closer of
  the two.
- A handful of sub-sections are naturally sparse in this question bank (2.3 has none,
  6.3/6.4 have one each); their study guides still describe what they cover.
