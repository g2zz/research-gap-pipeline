# Per-Paper Coding Schema

Each article coding must be one JSON object.

## Required Fields

```json
{
  "article_id": 1,
  "title": "",
  "source": "",
  "year": "",
  "primary_theme": "",
  "secondary_themes": [],
  "research_object": "",
  "research_context": "",
  "theoretical_lens": [],
  "method_inferred": "",
  "data_materials": [],
  "core_question": "",
  "core_claim": "",
  "mechanism_or_relation": "",
  "innovation_axis": "",
  "implicit_limits": "",
  "extendable_gap": "",
  "degree_feasibility": 1,
  "risk_for_thesis": "",
  "keywords": [],
  "evidence_from_abstract": "",
  "confidence": 0.0
}
```

## Coding Rules

- Use the article's `article_id` unchanged.
- If the abstract does not explicitly state method, theory, or data, prefix the field with `据摘要推断：`.
- Keep arrays as arrays.
- `degree_feasibility` is 1-5.
- `confidence` is 0-1.
- Avoid inventing full-text findings from an abstract.

## Prompt Template

```text
你是严谨的学术研究编码员。请只根据题名、摘要和元数据，对这篇论文做用于寻找研究 gap 的结构化编码。

规则：
1. 不能编造摘要之外的信息。
2. 摘要未明说的方法、理论、材料，必须标注“据摘要推断：”。
3. 输出严格 JSON，不要 Markdown。
4. 字段必须完整。
5. 数组字段保持数组。

输入：
article_id: ...
title: ...
authors: ...
source: ...
year/date: ...
keywords: ...
abstract: ...

输出 schema:
[paste required fields]
```
