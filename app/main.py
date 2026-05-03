import sys
import subprocess
import os

from app.pipeline import run_pipeline
from app.config import OUTPUT_DIR


def clean_output():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for file in OUTPUT_DIR.glob("*"):
        if file.name == ".gitkeep":
            continue
        if file.is_file():
            file.unlink()

    print("Output folder cleaned.")


def save_response_from_clipboard():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ["pbpaste"],
        capture_output=True,
        text=True,
        check=False,
    )

    text = result.stdout.strip()

    if not text:
        raise ValueError("Clipboard is empty. Copy ChatGPT response first.")

    response_path = OUTPUT_DIR / "manual_response.json"
    response_path.write_text(text, encoding="utf-8")

    print(f"Saved ChatGPT response to: {response_path}")
    print("Generating CSV...")

    run_pipeline()


def parse_profile_arg(args: list[str]) -> str | None:
    if "--profile" not in args:
        return None

    index = args.index("--profile")
    if index + 1 >= len(args):
        raise ValueError("Missing profile after --profile")

    return args[index + 1]


if __name__ == "__main__":
    args = sys.argv[1:]

    profile = parse_profile_arg(args)
    if profile:
        os.environ["PROMPT_PROFILE"] = profile

    command_args = [arg for arg in args if arg != "--profile" and arg != profile]

    if command_args:
        command = command_args[0]

        if command == "clean":
            clean_output()
        elif command == "save-response":
            save_response_from_clipboard()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: clean, save-response")
            print("Available profiles: general, web, backend, payment, game")
    else:
        run_pipeline()