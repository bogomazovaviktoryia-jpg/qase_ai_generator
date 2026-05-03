import json
import re
from pathlib import Path

from app.llm.prompts import get_prompt


def build_manual_prompt(documents_text: str, profile: str = "general") -> str:
    system_prompt, user_template = get_prompt(profile)

    prompt_body = user_template.replace("{documents}", documents_text)

    return f"{system_prompt.strip()}\n\n{prompt_body.strip()}\n"


def save_manual_prompt(
    documents_text: str,
    output_path: Path,
    profile: str = "general",
) -> None:
    prompt = build_manual_prompt(documents_text, profile)
    output_path.write_text(prompt, encoding="utf-8")


def extract_json_block(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0).strip()

    return text


def parse_cases(raw_json: str) -> dict:
    cleaned = extract_json_block(raw_json)
    return json.loads(cleaned)