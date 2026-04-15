from __future__ import annotations

import json
from pathlib import Path

from app.llm.prompts import SYSTEM_PROMPT, USER_TEMPLATE


QASE_SCHEMA = {
    "type": "object",
    "properties": {
        "test_cases": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "priority": {"type": "string"}
                },
                "required": ["title", "priority"],
                "additionalProperties": False
            }
        }
    },
    "required": ["test_cases"],
    "additionalProperties": False
}


def build_manual_prompt(documents_text: str) -> str:
    prompt_body = USER_TEMPLATE.replace("{documents}", documents_text)
    return f"{SYSTEM_PROMPT.strip()}\n\n{prompt_body.strip()}\n"


def save_manual_prompt(documents_text: str, output_path: Path) -> None:
    prompt = build_manual_prompt(documents_text)
    output_path.write_text(prompt, encoding="utf-8")


def parse_cases(raw_json: str) -> dict:
    return json.loads(raw_json)