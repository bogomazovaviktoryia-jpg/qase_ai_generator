from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
TEMPLATES_DIR = DATA_DIR / "templates"

OPENAI_MODE = os.getenv("OPENAI_MODE", "manual").strip().lower()
PROMPT_PROFILE = os.getenv("PROMPT_PROFILE", "general").strip().lower()

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".docx", ".xlsx"}
MAX_DOCUMENT_CHARS = 120_000
CHUNK_SIZE = 8_000
CHUNK_OVERLAP = 500