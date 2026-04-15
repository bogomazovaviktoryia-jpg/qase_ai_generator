from __future__ import annotations

from pathlib import Path
import pandas as pd


def normalize_priority(value: str | None) -> str:
    if not value:
        return "Not Set"

    value = value.strip().lower()

    mapping = {
        "high": "High",
        "medium": "Medium",
        "med": "Medium",
        "low": "Low",
        "not set": "Not Set",
        "none": "Not Set",
        "unset": "Not Set",
    }
    return mapping.get(value, "Not Set")


def export_to_qase_csv(test_cases: list[dict], template_csv: Path, output_csv: Path) -> None:
    template_df = pd.read_csv(template_csv)
    columns = list(template_df.columns)

    rows = []
    for case in test_cases:
        row = {col: "" for col in columns}

        for col in columns:
            low = col.strip().lower()

            if low == "title":
                row[col] = (case.get("title") or "").strip()
            elif low == "priority":
                row[col] = normalize_priority(case.get("priority"))

        rows.append(row)

    output_df = pd.DataFrame(rows, columns=columns)
    output_df.to_csv(output_csv, index=False, encoding="utf-8-sig")