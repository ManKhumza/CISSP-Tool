# CISSP Study Portal

An interactive study portal for the ISC2 CISSP exam: **2,615 practice questions**, each
filed under the sub-section of the official CISSP exam outline that it tests, with a
tailored study guide for every one of the 61 sub-sections.

Open **`CISSP_Study_Portal.html`** in a browser (it works straight from `file://` — keep it
next to `cissp-data.js`).

For **accounts + progress sync across devices**, run the bundled Express backend instead
(requires Node 22.5+, which has the built-in `node:sqlite` driver — no native compiler needed):

```bash
npm install     # express, bcryptjs, jsonwebtoken, cors, dotenv
npm start       # serves the portal at http://localhost:3000
```

Create a `.env` next to `server.js` to change the port / JWT secret (a working default is
provided, but set a real secret in production):

```
PORT=3000
JWT_SECRET=your-super-secret-jwt-key-change-in-production
```

Sign up with an email, and your answer history, marks and per-sub-section progress are
synced to the local SQLite database (`cissp_progress.db`) every two minutes and on sign-in.
Progress is also still stored in the browser, so the portal works offline with or without a
server.

## Phone and PWA use

The portal is an installable Progressive Web App. On Android/Chrome, use **Install app** in
the toolbar or the browser's install action. On iPhone/iPad, open the site in Safari, tap
**Share**, then **Add to Home Screen**. The question bank and app shell are cached after the
first successful visit, so study mode and on-device progress continue to work offline.

The bundled Vercel configuration creates a static deployment:

```bash
npm run build:static
vercel --prod
```

Static hosting stores progress on each device. Cross-device account sync still requires the
Express server and its database (or a managed database replacing SQLite); the static build
labels this mode **On-device** instead of showing a non-functional sign-in button.

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
- **Professional UX**: dark mode, sidebar with progress ring and auto-scroll,
  keyboard shortcuts (←/→ navigate, s=show answer, m=mark, n=next unanswered, g=toggle guide, /search), print stylesheet, mobile drawer.

## Layout

| Path | Purpose |
|---|---|
| `CISSP_Study_Portal.html` | The single-page app |
| `cissp-data.js` | Question bank + guides (loaded by the app) |
| `server.js` | Express backend: user accounts (JWT) + progress sync (`node:sqlite`) |
| `public/auth.js` | Client auth + auto-sync module |
| `package.json`, `.env` | Backend deps and config |
| `subsection_keywords.py` | Curated within-domain vocabulary used for classification |
| `classify_subsections4.py` | Rule-based sub-section classification |
| `merge_adjudication.py` | Merges reviewed labels + consistency corrections |
| `subsection_guides.py` | Curated focus + must-know content for the 61 sub-sections |
| `subsection_deep_notes.py` | Deeper lesson notes per sub-section |
| `subsection_glossary_extra.py` | Curated definitions and overrides |
| `defs.py` | Definition extractor (indexes the reference books) |
| `enrich_guides.py` | Builds the per-sub-section term glossaries |
| `build_web_data2.py` | Assembles `cissp-data.js` |
| `extract_pdf.py`, `extract_books.py` | Text extraction from the source question PDF and local reference books |
| `smoke_test2.js` | Headless verification of data and UI |
| `make_batches.py` | Builds the review batches used for question-by-question adjudication |
| `validate_final.py`, `sample_sections_final.py`, `check_placement.py` | Quality inspection helpers |
| `textrepair.py` | Text repair engine (runs after any rebuild) |
| `detect_text_defects.py` | Scans for residual artefacts |
| `_classify/final_assignments.json` | Question → sub-section mapping |
| `_classify/guide_terms.json` | Mined term meanings |
| `archive/` | Earlier iterations (first-pass organisers, PDF builders, superseded classifiers) kept for reference only |

## How the questions were organised

1. **Classification.** Every question was placed in a sub-section: curated within-domain
   keyword rules first, then the uncertain ones reviewed question-by-question against the
   official outline, then consistency corrections (for example unifying TCSEC / Common
   Criteria / reference-monitor questions into 3.4).
2. **Text repair.** The source PDF extraction split words ("th e", "technolo gy", "ofa",
   "classificati on") and lost spaces ("ofobjects", "noneed", "thetcb"). A repair engine
   using a 370 k-word clean English dictionary and the reference books' own vocabularies
   repaired **all 3.6 MB of text**:
   - joined split words (guarded by dictionary + corpus attestation)
   - split glued words (split into dictionary words with corpus attestation)
   - fixed mispunctuation (commas/periods after function words, doubled words, possessives)
   - applied 50+ explicit FIXES for stubborn proper nouns (ElGamal, Kerberos, Rivest, etc.)
   - repaired 7,600+ joins, 5,300+ splits, 3,200+ punctuation fixes, 80 carries — converged to
     **0 residual split-word pairs** and **198 remaining broken-word suspects** (all false
     positives like "a long", "I am").
3. **Answer integrity.** Options beyond letter D, offset option labels (E–H while the answer
   key refers to position) and "?" bullet lists were parsed correctly, leaving **0 questions
   without an answer and 0 with fewer than two options**.

## Regenerating the data

```bash
python classify_subsections4.py     # rule-based labels
python merge_adjudication.py        # merge reviewed labels + corrections
python enrich_guides.py             # mine key-term meanings (needs the reference books)
python build_web_data2.py           # rebuild cissp-data.js
python textrepair.py --write        # run the text repair on the rebuilt data
node smoke_test2.js                 # verify
```

`extract_books.py` re-creates the plain-text extracts of the reference study guide and exam
companion; those extracts are intentionally not committed (they are licensed material).
It also accepts an explicit input and output path for additional locally owned references:

```bash
python extract_books.py "path/to/reference.pdf" "_books/reference.txt"
```

The glossary also includes original, paraphrased definitions selected from *CISSP For
Dummies*, 8th edition (Miller & Gregory, 2024). The raw book extract remains local and is
excluded from version control.

To run the text repair yourself, download the dictionary once:

```bash
curl -L -o _words_alpha.txt https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt
```

## Verification

`node smoke_test2.js` checks question integrity, sub-section coverage, glossary quality and
every portal view. All checks pass.

Run `python detect_text_defects.py` to scan for residual artefacts (198 suspects, all false
positives like "a long", "I am").

## Notes

- Sub-section boundaries are occasionally fuzzy in the CBK (physical security spans 3.9 and
  7.14; DR processes 7.11 versus DR testing 7.12), so a few questions sit in the closer of
  the two.
- A handful of sub-sections are naturally sparse in this question bank (2.3 has none,
  6.3/6.4 have one each); their study guides still describe what they cover.
- The reference books (Chapple OSG 10th ed 2024, CISSP Exam Certification Companion
  1000+ questions) are licensed material and are intentionally not committed; regenerate their
  text extracts with `extract_books.py` if you have them.
