import sys

from app.pipeline import run_pipeline
from app.config import OUTPUT_DIR


def clean_output():
    for file in OUTPUT_DIR.glob("*"):
        if file.name == ".gitkeep":
            continue
        if file.is_file():
            file.unlink()
    print("Output folder cleaned.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "clean":
            clean_output()
        else:
            print(f"Unknown command: {command}")
    else:
        run_pipeline()