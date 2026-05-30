# Export Field Requirements

## Minimum Fields

- title
- authors
- source/journal
- year or date
- abstract

## Strongly Recommended Fields

- keywords
- citation count
- DOI
- URL
- fund/project
- institution
- publication type

## Accepted File Types

- `.xlsx`
- `.xls`
- `.csv`
- `.tsv`
- HTML table exported as `.xls`

## Normalized Output Columns

```text
article_id
title
authors
source
year
date
abstract
keywords
citation_count
doi
url
raw_source_file
```

If a field is missing, keep the column and leave it blank. Do not silently drop expected columns.
