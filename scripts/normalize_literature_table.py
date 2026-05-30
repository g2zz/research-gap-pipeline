#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


TARGET_COLUMNS = [
    "article_id",
    "title",
    "authors",
    "source",
    "year",
    "date",
    "abstract",
    "keywords",
    "citation_count",
    "doi",
    "url",
    "raw_source_file",
]

ALIASES = {
    "title": ["title", "题名", "篇名", "文献题名", "Title-题名", "TI"],
    "authors": ["authors", "author", "作者", "Author-作者", "AU"],
    "source": ["source", "journal", "来源", "文献来源", "Source-文献来源", "刊名", "LY"],
    "year": ["year", "年份", "年", "发表年度"],
    "date": ["date", "发表时间", "发表日期", "出版日期", "FT"],
    "abstract": ["abstract", "summary", "摘要", "Summary-摘要", "AB"],
    "keywords": ["keywords", "keyword", "关键词", "KY"],
    "citation_count": ["citation_count", "cited", "被引", "被引频次", "CF"],
    "doi": ["doi", "DOI"],
    "url": ["url", "URL", "链接"],
}


def read_input(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        try:
            return pd.read_excel(path)
        except Exception:
            tables = pd.read_html(str(path), encoding="utf-8")
            if not tables:
                raise
            df = tables[0]
            if not df.empty:
                df.columns = df.iloc[0]
                df = df.iloc[1:].reset_index(drop=True)
            return df
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix == ".tsv":
        return pd.read_csv(path, sep="\t")
    raise ValueError(f"Unsupported file type: {suffix}")


def pick_column(df: pd.DataFrame, canonical: str) -> str | None:
    normalized = {str(col).strip().lower(): col for col in df.columns}
    for alias in ALIASES[canonical]:
        key = alias.strip().lower()
        if key in normalized:
            return normalized[key]
    return None


def normalize(path: Path) -> pd.DataFrame:
    raw = read_input(path)
    raw = raw.dropna(how="all").reset_index(drop=True)
    out = pd.DataFrame()
    out["article_id"] = range(1, len(raw) + 1)
    for col in TARGET_COLUMNS:
        if col in {"article_id", "raw_source_file"}:
            continue
        source_col = pick_column(raw, col)
        out[col] = raw[source_col].fillna("").astype(str) if source_col is not None else ""
    out["raw_source_file"] = str(path)

    if out["year"].eq("").all() and not out["date"].eq("").all():
        out["year"] = out["date"].str.extract(r"(\d{4})", expand=False).fillna("")
    if out["title"].eq("").all():
        raise ValueError("No title column found. Check export fields.")
    if out["abstract"].eq("").all():
        raise ValueError("No abstract column found. Export abstracts before running gap analysis.")
    return out[TARGET_COLUMNS]


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize exported literature tables.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("02_clean_literature.csv"))
    args = parser.parse_args()
    df = normalize(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(f"wrote {args.output} rows={len(df)}")


if __name__ == "__main__":
    main()
