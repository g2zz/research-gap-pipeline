# CNKI Query Templates

## Core Syntax

- Journal/source: `LY='期刊名'`
- Date range: `FT='YYYY-MM-DD' TO 'YYYY-MM-DD'`
- Fuzzy match: `FIELD%'term'`
- Exact match: `FIELD='term'`
- Synonyms: `OR`
- Different dimensions: `AND`
- Exclusion: `AND NOT FIELD%'term'`
- Citation count: `CF>=n`

Use half-width parentheses, quotes, and operators.

## Broad Template

```text
(LY='期刊A' OR LY='期刊B') AND FT='YYYY-MM-DD' TO 'YYYY-MM-DD' AND (TKA%'主题1' OR TKA%'主题2') AND (TKA%'方法1' OR TKA%'方法2') AND NOT TKA%'排除词' AND CF>=n
```

## Exact Keyword Template

```text
(LY='期刊A' OR LY='期刊B') AND FT='YYYY-MM-DD' TO 'YYYY-MM-DD' AND (KY='关键词1' OR KY='关键词2')
```

## No Journal Constraint

```text
FT='YYYY-MM-DD' TO 'YYYY-MM-DD' AND (TKA%'主题1' OR TKA%'主题2')
```

## Communication Core Preset Example

```text
(LY='新闻与传播研究' OR LY='国际新闻界' OR LY='新闻大学' OR LY='现代传播(中国传媒大学学报)')
```

## Communication CSSCI Extension Example

```text
(LY='新闻与传播研究' OR LY='国际新闻界' OR LY='新闻大学' OR LY='现代传播(中国传媒大学学报)' OR LY='当代传播' OR LY='新闻界' OR LY='新闻记者' OR LY='全球传媒学刊' OR LY='新闻与传播评论' OR LY='新闻与写作')
```

## Invalid Patterns

Do not use:

- `+`
- `*`
- bare `-`
- Chinese full-width punctuation for operators
- unbalanced parentheses
