# End-to-End Workflow

## 1. Clarify The Research Task

Collect:

- discipline and subfield
- degree level: undergraduate, master, PhD, grant proposal
- language scope: Chinese, English, both
- source scope: CNKI/CSSCI/core journals, arXiv, Web of Science, Scopus, PubMed, custom files
- time range
- preferred methods and constraints
- available data access: interviews, scraping, experiments, archives, surveys

## 2. Build The Source Pool

For any discipline, first define what "top literature" means. Use one or more:

- official core/CSSCI/SSCI/SCI journal lists
- supervisor-recognized top journals
- field-specific conferences
- discipline databases
- high-citation threshold
- recent-year window

Do not begin LLM gap generation before the source pool is explicit.

## 3. Retrieve Literature

CNKI is manual-first:

- create professional search expressions
- user runs CNKI search
- user exports results
- agent resumes from the exported file

arXiv is API-enabled:

- use arXiv search skill
- export metadata and abstracts
- optionally download PDFs if needed

## 4. Normalize Exported Literature

Run:

```bash
python3 scripts/normalize_literature_table.py input.xlsx --output 02_clean_literature.csv
```

The output must include stable `article_id` values.

## 5. Per-Paper LLM Coding

Run:

```bash
python3 scripts/build_article_coding_prompts.py 02_clean_literature.csv --output 03_article_coding_prompts.jsonl
```

Send each prompt to the selected LLM independently. Save strict JSON lines to:

```text
04_article_codings.jsonl
```

Do not replace this with one large summarization call.

## 6. Validate Coverage

Run:

```bash
python3 scripts/validate_article_codings.py 02_clean_literature.csv 04_article_codings.jsonl
```

Fix missing, duplicate, or invalid records before synthesis.

## 7. Synthesize Themes And Gaps

Group coded papers by theme, object, method, theory, data source, and scene.

Look for:

- crowded themes
- underexplored objects
- underexplored scenes
- method imbalance
- theory-method mismatch
- strong topic but weak empirical access
- reverse mechanisms: failure, refusal, breakdown, negotiation, unintended consequence

## 8. Package Candidate Topics

Each candidate topic must include:

- title
- problem consciousness
- research gap statement
- RQ1-RQ3
- object and sample
- method design
- data path
- theoretical contribution
- feasibility score
- innovation score
- risks
- first-week validation tasks

## 9. Final Deliverables

Produce:

- clean literature table
- article coding JSONL and review CSV
- theme map
- gap table
- candidate topic table
- final report
- optional workbook
