#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import pandas as pd


REQUIRED_FIELDS = {
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
}

ALIASES = {
    "article_id": ["id"],
    "research_context": ["media_context"],
    "degree_feasibility": ["masters_feasibility"],
}


def normalize_item(item: dict) -> dict:
    item = dict(item)
    for canonical, aliases in ALIASES.items():
        if canonical not in item:
            for alias in aliases:
                if alias in item:
                    item[canonical] = item[alias]
                    break
    if "article_id" in item:
        item["article_id"] = int(item["article_id"])
    item.setdefault("year", "")
    return item


def load_jsonl(path: Path) -> list[dict]:
    items = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                items.append(normalize_item(json.loads(line)))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON at line {line_no}: {exc}") from exc
    return items


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate per-paper coding JSONL coverage and schema.")
    parser.add_argument("clean_csv", type=Path)
    parser.add_argument("codings_jsonl", type=Path)
    parser.add_argument("--review-csv", type=Path)
    args = parser.parse_args()

    source = pd.read_csv(args.clean_csv).fillna("")
    expected = set(int(x) for x in source["article_id"])
    items = load_jsonl(args.codings_jsonl)
    ids = [int(x.get("article_id", -1)) for x in items]
    counts = Counter(ids)
    missing_ids = sorted(expected - set(ids))
    duplicate_ids = sorted(k for k, v in counts.items() if v > 1)
    unknown_ids = sorted(set(ids) - expected)

    schema_errors = []
    for item in items:
        item_id = item.get("article_id")
        missing = sorted(REQUIRED_FIELDS - set(item))
        if missing:
            schema_errors.append({"article_id": item_id, "missing_fields": missing})

    report = {
        "source_articles": len(source),
        "coded_articles": len(items),
        "missing_ids": missing_ids,
        "duplicate_ids": duplicate_ids,
        "unknown_ids": unknown_ids,
        "schema_error_count": len(schema_errors),
        "schema_errors": schema_errors[:20],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if args.review_csv:
        flat = []
        for item in sorted(items, key=lambda x: int(x.get("article_id", 0))):
            row = item.copy()
            for key in ["secondary_themes", "theoretical_lens", "data_materials", "keywords"]:
                if isinstance(row.get(key), list):
                    row[key] = "；".join(map(str, row[key]))
            flat.append(row)
        pd.DataFrame(flat).to_csv(args.review_csv, index=False, encoding="utf-8-sig")

    if missing_ids or duplicate_ids or unknown_ids or schema_errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
