# CNKI Manual SOP

CNKI is a manual source. Do not claim that the agent can log in, search, click, download, or export CNKI automatically unless the user explicitly operates the browser and provides files.

## Manual Steps For The Human

1. Open CNKI advanced/professional search.
2. Select the target database and source type.
3. Paste the professional search expression.
4. Confirm source/journal constraints and date range.
5. Inspect result count. Adjust terms if result count is too high or too low.
6. Export records.
7. Include at least title, authors, source, year/date, abstract, keywords, citation count if available.
8. Save the exported file as `01_raw_literature.xlsx`, `.xls`, `.csv`, or `.txt`.
9. Give the file to the agent for normalization and downstream analysis.

## What The Agent Can Do

- Help define top-journal/source pool.
- Generate CNKI professional search expressions.
- Check syntax against known rules.
- Tell the human what fields to export.
- Normalize the exported file.
- Run per-paper LLM coding and gap analysis after export.

## What The Agent Must Not Claim

- Automatic CNKI login.
- Automatic CNKI crawling.
- Automatic export from CNKI.
- Complete full-text coverage unless the user provides full text.
