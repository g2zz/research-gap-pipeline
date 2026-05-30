---
name: research-gap-pipeline
description: Run a rigorous cross-disciplinary research topic discovery workflow from top-journal/source selection to literature export, normalization, per-paper LLM coding, theme synthesis, research-gap identification, and thesis-topic packaging. Use when the user wants to find research gaps, choose a thesis/dissertation topic, build an auditable literature review pipeline, process CNKI-exported Chinese literature, combine CNKI with arXiv, or turn many paper titles/abstracts into concrete research questions and feasible topics.
---

# Research Gap Pipeline

## Non-Negotiables

- Do not pretend to automate CNKI. CNKI retrieval/export is manual unless the user supplies an exported file.
- Do not summarize hundreds of abstracts in one LLM call for final decisions. Use per-paper coding first.
- Preserve traceability: every theme, gap, and candidate topic must point back to article IDs or source groups.
- Treat abstracts as incomplete evidence. Mark inferred methods/theories/materials as inferred.
- Produce auditable intermediate artifacts, not only a polished final report.

## Workflow

1. Define discipline, target degree level, language scope, and top-journal/source pool.
2. Prepare retrieval strategy.
   - CNKI: follow `references/cnki_manual_sop.md` and `references/cnki_query_templates.md`; the human exports the table.
   - arXiv: use the existing arXiv search skill or `references/arxiv_source.md`.
3. Require export fields from `references/export_field_requirements.md`.
4. Normalize the exported file with `scripts/normalize_literature_table.py`.
5. Build per-paper coding prompts with `scripts/build_article_coding_prompts.py`.
6. Call the chosen LLM one paper at a time or in small independent batches. Save JSONL codings.
7. Validate coding coverage with `scripts/validate_article_codings.py`.
8. Synthesize themes, crowded zones, gaps, and candidate topics using `references/gap_rubric.md` and `references/output_templates.md`.
9. Deliver final artifacts: cleaned literature table, article codings, theme map, gap table, candidate-topic table, final report, and workbook if useful.

## Default Artifact Names

```text
01_raw_literature.*
02_clean_literature.csv
03_article_coding_prompts.jsonl
04_article_codings.jsonl
05_theme_map.csv
06_research_gaps.csv
07_candidate_topics.csv
08_final_report.md
09_workbook.xlsx
```

## LLM Coding Contract

Each paper must be coded into the schema in `references/coding_schema.md`. Required input:

- `article_id`
- title
- authors
- source/journal
- year/date
- abstract
- keywords if available
- citation count if available

Required output:

- theme, object, context, theory, method, data, core question, core claim
- implicit limitations
- extendable gap
- feasibility/risk for the target degree
- evidence quoted or paraphrased from the abstract

## When The User Only Has CNKI

Give the user exact manual steps:

1. Define top journals or source categories.
2. Generate CNKI professional search expression manually from templates.
3. User runs the search in CNKI.
4. User exports at least title, authors, source, year/date, abstract, keywords, citation count.
5. Agent resumes from normalization.

## When The User Wants arXiv

Use arXiv official API through the arXiv search skill when available. Respect arXiv rate limits. Convert arXiv results into the same normalized literature schema before coding.

## Decision Gate

Before finalizing candidate topics, reject topics that fail any of these:

- no clear object
- no specific empirical scene
- no explainable mechanism
- no feasible data path
- only renames an existing hot topic
- cannot state "existing research focuses on A, but under-explains B"

Read `references/workflow.md` for the full step-by-step procedure when running a real project.
