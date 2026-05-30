#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


SCHEMA_FIELDS = [
    "article_id",
    "title",
    "source",
    "year",
    "primary_theme",
    "secondary_themes",
    "research_object",
    "research_context",
    "theoretical_lens",
    "method_inferred",
    "data_materials",
    "core_question",
    "core_claim",
    "mechanism_or_relation",
    "innovation_axis",
    "implicit_limits",
    "extendable_gap",
    "degree_feasibility",
    "risk_for_thesis",
    "keywords",
    "evidence_from_abstract",
    "confidence",
]


SYSTEM_PROMPT = "你是严谨的学术研究编码员。只输出可解析 JSON。编码要服务于研究 gap 识别。"


def user_prompt(row: pd.Series, degree: str, discipline: str) -> str:
    payload = {
        "article_id": int(row["article_id"]),
        "title": str(row.get("title", "")),
        "authors": str(row.get("authors", "")),
        "source": str(row.get("source", "")),
        "year": str(row.get("year", "")),
        "date": str(row.get("date", "")),
        "keywords": str(row.get("keywords", "")),
        "abstract": str(row.get("abstract", "")),
    }
    return f"""
请只根据下面这篇论文的题名、摘要和元数据，做用于寻找研究 gap 的结构化编码。

学科：{discipline}
目标层级：{degree}

规则：
1. 不能编造摘要之外的信息。
2. 摘要未明说的方法、理论、材料，必须标注“据摘要推断：”。
3. 输出严格 JSON，不要 Markdown。
4. 字段必须完整。
5. secondary_themes、theoretical_lens、data_materials、keywords 必须是数组。
6. degree_feasibility 用 1-5 分，confidence 用 0-1 小数。

JSON 字段：
{json.dumps(SCHEMA_FIELDS, ensure_ascii=False)}

论文：
{json.dumps(payload, ensure_ascii=False, indent=2)}
""".strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build per-paper LLM coding prompts.")
    parser.add_argument("clean_csv", type=Path)
    parser.add_argument("--output", type=Path, default=Path("03_article_coding_prompts.jsonl"))
    parser.add_argument("--degree", default="master")
    parser.add_argument("--discipline", default="unspecified")
    args = parser.parse_args()

    df = pd.read_csv(args.clean_csv).fillna("")
    required = {"article_id", "title", "abstract"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            record = {
                "article_id": int(row["article_id"]),
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt(row, args.degree, args.discipline)},
                ],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"wrote {args.output} prompts={len(df)}")


if __name__ == "__main__":
    main()
