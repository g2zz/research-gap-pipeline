# Research Gap Pipeline

一个用于“研究空白发现”和“论文选题生成”的可审计流水线工具包。

它的目标不是一次性把大量摘要丢给大模型做总结，而是把文献检索、表格清洗、逐篇编码、编码校验、主题归纳、研究 gap 识别和候选选题包装拆成可追踪的步骤。每一个主题、gap 和候选题目都应该能回溯到具体文献 ID。

## 适用场景

- 从 CNKI、arXiv 或其他数据库导出的文献中寻找研究空白
- 为本科、硕士、博士论文或课题申请生成候选选题
- 建立可复核的文献综述工作流
- 将论文标题、摘要、关键词等元数据整理成结构化编码
- 对比不同主题、方法、理论、研究对象和数据来源的拥挤区与空白区

## 核心原则

- 不伪装自动化 CNKI：CNKI 检索和导出需要人工完成。
- 不用一次大模型调用总结全部文献：先逐篇编码，再综合分析。
- 保留可追溯性：主题、gap、选题都要指向文献 ID 或来源组。
- 把摘要视为不完整证据：摘要中没有明说的方法、理论、材料需要标注为推断。
- 产出中间文件：不要只给最终报告，要保留清洗表、编码 JSONL、主题表、gap 表等过程产物。

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

## 工作流程

1. 明确研究任务：学科、方向、学位层级、语言范围、时间范围、数据可得性。
2. 确定文献来源：例如 CNKI/CSSCI/核心期刊、arXiv、Web of Science、Scopus、PubMed 或自定义文件。
3. 检索并导出文献表：CNKI 按 `references/cnki_manual_sop.md` 和 `references/cnki_query_templates.md` 手动操作。
4. 标准化文献表：生成稳定的 `article_id`。
5. 生成逐篇 LLM 编码提示。
6. 对每篇文献分别调用 LLM，保存 JSONL 编码结果。
7. 校验编码覆盖率、重复 ID、缺失字段和异常记录。
8. 根据编码结果综合主题、拥挤区、研究空白和候选选题。
9. 输出最终报告和可复核的中间产物。

## 环境准备

建议使用 Python 3.10+。

安装依赖：

```bash
pip install pandas openpyxl lxml
```

如果只处理 CSV 文件，通常只需要 `pandas`；如果读取 Excel 或 HTML 表格导出文件，可能需要 `openpyxl` 或 `lxml`。

## 快速开始

### 1. 准备原始文献表

文献表至少应包含：

- 题名
- 作者
- 来源/期刊
- 年份或日期
- 摘要
- 关键词
- 被引次数
- DOI 或 URL，若有

字段要求可参考：

```text
references/export_field_requirements.md
```

假设原始文件为：

```text
01_raw_literature.xlsx
```

### 2. 标准化文献表

```bash
python scripts/normalize_literature_table.py 01_raw_literature.xlsx --output 02_clean_literature.csv
```

输出文件会包含稳定的 `article_id`，后续所有编码、主题和 gap 都应基于这个 ID 追踪。

### 3. 生成逐篇编码提示

```bash
python scripts/build_article_coding_prompts.py 02_clean_literature.csv --output 03_article_coding_prompts.jsonl --degree master --discipline "传播学"
```

输出的 JSONL 每一行对应一篇文献的 LLM 调用消息。

### 4. 调用 LLM 并保存编码结果

将每篇文献的提示独立发送给选定的大模型，输出结果保存为：

```text
04_article_codings.jsonl
```

每一行必须是一个完整 JSON 对象，并符合：

```text
references/coding_schema.md
```

### 5. 校验编码结果

```bash
python scripts/validate_article_codings.py 02_clean_literature.csv 04_article_codings.jsonl --review-csv 04_article_codings_review.csv
```

校验内容包括：

- 是否有文献缺失编码
- 是否有重复 `article_id`
- 是否有未知 `article_id`
- 是否缺少必要字段
- 是否能导出便于人工检查的 CSV

### 6. 综合主题和研究空白

根据编码结果，结合以下参考文件进行综合：

```text
references/gap_rubric.md
references/output_templates.md
references/workflow.md
```

重点寻找：

- 已经拥挤的主题
- 研究对象不足
- 场景不足
- 方法单一
- 理论和方法不匹配
- 数据可得性强但解释不足的问题
- 失败、拒绝、协商、崩解、副作用等反向机制

## 默认产物命名

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

## 候选选题筛选标准

最终候选选题至少要能回答：

- 研究对象是什么？
- 经验场景是什么？
- 要解释的机制是什么？
- 数据从哪里来？
- 与已有研究相比，具体空白在哪里？
- 为什么这个题目对目标学位层级可行？

如果一个题目只能说“已有研究很多，但还可以继续研究”，通常不算合格的研究 gap。

更好的 gap 表述应类似：

```text
已有研究主要关注 A，但对 B 场景下 C 机制如何发生仍解释不足。
```

## 注意事项

- CNKI 数据需要人工检索和导出，本项目不包含 CNKI 自动爬取功能。
- 摘要不能替代全文。若要做严格综述，应在关键文献阶段补充全文阅读。
- LLM 编码结果需要人工抽查，尤其是方法、理论、数据材料和研究结论。
- 公开仓库前请确认没有上传未授权论文全文、个人隐私数据、API Key 或内部资料。

## 许可证

当前仓库尚未声明许可证。公开复用前建议补充 `LICENSE` 文件。
