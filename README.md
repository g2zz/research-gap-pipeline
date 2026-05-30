<div align="center">

# Research Gap Pipeline.skill

### 面向文献综述与论文选题的研究空白发现流水线

把“文献表”一步步整理成可追溯的主题、研究 Gap 和候选论文选题。

<p>
  <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111111?style=flat-square">
  <img alt="Research Gap" src="https://img.shields.io/badge/Research-Gap-0f766e?style=flat-square">
  <img alt="Literature Review" src="https://img.shields.io/badge/Literature-Review-2563eb?style=flat-square">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-3776ab?style=flat-square">
  <img alt="Output" src="https://img.shields.io/badge/Output-CSV%20%7C%20JSONL%20%7C%20Markdown-f59e0b?style=flat-square">
</p>

[一句话](#一句话) · [能做什么](#能做什么) · [工作流程](#工作流程) · [快速开始](#快速开始) · [目录结构](#目录结构)

</div>

---

## 一句话

人工整理文献时，最烦的是线索散；让 AI 代劳时，最怕的是结论没来源。

这个 skill 把文献检索、表格清洗、逐篇编码、编码校验、主题归纳、研究 Gap 识别和候选选题包装拆成一套可复核的流程。每一个主题、Gap 和选题，都应该能回溯到具体文献 ID。

> 少拍脑袋，多留证据。

## 能做什么

| 场景 | 输出 |
| --- | --- |
| 从 CNKI、arXiv 或其他数据库导出的文献表中找研究空白 | 清洗后的文献表、逐篇编码、Gap 表 |
| 为本科、硕士、博士论文或课题申请生成候选选题 | 带来源依据的候选题目清单 |
| 搭建可复核的文献综述工作流 | 中间产物、校验报告、最终报告 |
| 对比主题、方法、理论、对象和数据来源 | 拥挤区、空白区、可行选题方向 |

## 核心原则

- 不伪装自动化 CNKI：CNKI 检索和导出需要人工完成。
- 不把一堆摘要一次性丢给模型总结：先逐篇编码，再综合分析。
- 不接受没有来源的 Gap：主题、Gap、选题都要指向文献 ID 或来源组。
- 不把摘要当全文：摘要没有明说的方法、理论、材料，需要标注为推断。
- 不只给最终报告：保留清洗表、编码 JSONL、主题表、Gap 表等过程产物。

## 工作流程

```mermaid
flowchart LR
    A[检索并导出文献表] --> B[标准化字段与 article_id]
    B --> C[生成逐篇编码提示]
    C --> D[LLM 逐篇编码]
    D --> E[校验编码结果]
    E --> F[归纳主题与拥挤区]
    F --> G[识别研究 Gap]
    G --> H[生成候选论文选题]
```

## 快速开始

### 1. 准备环境

建议使用 Python 3.10+。

```bash
pip install pandas openpyxl lxml
```

如果只处理 CSV 文件，通常只需要 `pandas`；如果要读取 Excel 或 HTML 表格导出文件，可能需要 `openpyxl` 或 `lxml`。

### 2. 准备原始文献表

文献表至少建议包含：

- 题名
- 作者
- 来源或期刊
- 年份或日期
- 摘要
- 关键词
- 被引次数
- DOI 或 URL，如果有

字段要求可参考：

```text
references/export_field_requirements.md
```

假设原始文件为：

```text
01_raw_literature.xlsx
```

### 3. 标准化文献表

```bash
python scripts/normalize_literature_table.py 01_raw_literature.xlsx --output 02_clean_literature.csv
```

输出文件会包含稳定的 `article_id`，后续所有编码、主题和 Gap 都应基于这个 ID 追踪。

### 4. 生成逐篇编码提示

```bash
python scripts/build_article_coding_prompts.py 02_clean_literature.csv --output 03_article_coding_prompts.jsonl --degree master --discipline "传播学"
```

输出的 JSONL 每一行对应一篇文献的 LLM 调用消息。

### 5. 调用 LLM 并保存编码结果

将每篇文献的提示独立发送给选定的大模型，输出结果保存为：

```text
04_article_codings.jsonl
```

每一行必须是一个完整 JSON 对象，并符合：

```text
references/coding_schema.md
```

### 6. 校验编码结果

```bash
python scripts/validate_article_codings.py 02_clean_literature.csv 04_article_codings.jsonl --review-csv 04_article_codings_review.csv
```

校验内容包括：

- 是否有文献缺失编码
- 是否有重复 `article_id`
- 是否有未知 `article_id`
- 是否缺少必要字段
- 是否能导出便于人工检查的 CSV

## 默认产物

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

## 好的 Gap 长什么样

一个合格的候选选题，至少应该能回答：

- 研究对象是什么？
- 经验场景是什么？
- 要解释的机制是什么？
- 数据从哪里来？
- 与已有研究相比，具体空白在哪里？
- 为什么这个题目对目标学位层级可行？

如果一个题目只能说“已有研究很多，但还可以继续研究”，通常不算合格的研究 Gap。

更好的 Gap 表述类似：

```text
已有研究主要关注 A，但对 B 场景中 C 机制如何发生仍解释不足。
```

## 目录结构

```text
.
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- references/
|   |-- arxiv_source.md
|   |-- cnki_manual_sop.md
|   |-- cnki_query_templates.md
|   |-- coding_schema.md
|   |-- export_field_requirements.md
|   |-- gap_rubric.md
|   |-- output_templates.md
|   `-- workflow.md
`-- scripts/
    |-- build_article_coding_prompts.py
    |-- normalize_literature_table.py
    `-- validate_article_codings.py
```

## 注意事项

- 本项目不包含 CNKI 自动爬取功能。
- 摘要不能替代全文；严格综述应在关键文献阶段补充全文阅读。
- LLM 编码结果需要人工抽查，尤其是方法、理论、数据材料和研究结论。
- 公开仓库前请确认没有上传未授权论文全文、个人隐私数据、API Key 或内部资料。

## License

当前仓库尚未声明许可证。公开复用前建议补充 `LICENSE` 文件。
