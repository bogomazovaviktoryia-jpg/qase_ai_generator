from __future__ import annotations

import json
from pathlib import Path

from app.config import (
    INPUT_DIR,
    OUTPUT_DIR,
    TEMPLATE_DIR,
    SUPPORTED_EXTENSIONS,
    MAX_DOCUMENT_CHARS,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    OPENAI_MODE,
)
from app.utils import clean_text, chunk_text, ensure_dir, normalize_title
from app.readers.text_reader import read_txt
from app.readers.pdf_reader import read_pdf
from app.readers.docx_reader import read_docx
from app.readers.xlsx_reader import read_xlsx
from app.llm.generator import save_manual_prompt, parse_cases
from app.exporters.qase_csv import export_to_qase_csv


def read_any(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return read_txt(path)
    if suffix == ".pdf":
        return read_pdf(path)
    if suffix == ".docx":
        return read_docx(path)
    if suffix == ".xlsx":
        return read_xlsx(path)
    return ""


def collect_documents() -> tuple[str, list[str]]:
    parts = []
    used_files = []

    for path in sorted(INPUT_DIR.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        raw_text = read_any(path)
        raw_text = clean_text(raw_text)
        if not raw_text:
            continue

        used_files.append(path.name)
        chunks = chunk_text(raw_text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)

        for index, chunk in enumerate(chunks, start=1):
            parts.append(f"FILE: {path.name}\nCHUNK: {index}\n{chunk}")

    merged = "\n\n" + ("\n\n---\n\n".join(parts))
    return merged[:MAX_DOCUMENT_CHARS], used_files


def deduplicate_cases(test_cases: list[dict]) -> list[dict]:
    seen = set()
    result = []

    for case in test_cases:
        title = normalize_title(case.get("title", ""))
        if not title:
            continue

        key = title.lower()
        if key in seen:
            continue
        seen.add(key)

        result.append({
            "title": title,
            "priority": case.get("priority", "Not Set")
        })

    return result


def run_manual_prepare(documents_text: str) -> None:
    prompt_path = OUTPUT_DIR / "prompt_for_chatgpt.txt"
    preview_path = OUTPUT_DIR / "source_preview.txt"

    save_manual_prompt(documents_text, prompt_path)
    preview_path.write_text(documents_text, encoding="utf-8")

    print("\nManual mode enabled.")
    print(f"Prompt saved to:   {prompt_path}")
    print(f"Source saved to:   {preview_path}")
    print("\nNext steps:")
    print("1. Open prompt_for_chatgpt.txt")
    print("2. Copy all text into ChatGPT")
    print("3. Save model response as data/output/manual_response.json")
    print("4. Run: python -m app.main")


def run_manual_finalize() -> None:
    manual_json_path = OUTPUT_DIR / "manual_response.json"
    if not manual_json_path.exists():
        print("\nmanual_response.json not found.")
        print("Create data/output/manual_response.json with the JSON from ChatGPT.")
        return

    raw_json = manual_json_path.read_text(encoding="utf-8")
    parsed = parse_cases(raw_json)

    test_cases = deduplicate_cases(parsed.get("test_cases", []))

    json_path = OUTPUT_DIR / "generated_cases.json"
    csv_path = OUTPUT_DIR / "qase_import.csv"
    template_csv = TEMPLATE_DIR / "qase_template.csv"

    json_path.write_text(
        json.dumps(
            {
                "test_cases": test_cases,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    export_to_qase_csv(test_cases, template_csv, csv_path)

    print(f"Saved JSON:   {json_path}")
    print(f"Saved CSV:    {csv_path}")


def run_pipeline() -> None:
    ensure_dir(OUTPUT_DIR)

    documents_text, _ = collect_documents()
    if not documents_text.strip():
        raise ValueError("No supported files found in data/input")

    if OPENAI_MODE == "manual":
        manual_json_path = OUTPUT_DIR / "manual_response.json"
        if manual_json_path.exists():
            run_manual_finalize()
        else:
            run_manual_prepare(documents_text)
        return

    raise ValueError("Only OPENAI_MODE=manual is configured in this version.")