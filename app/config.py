from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "data" / "input"
OUTPUT_DIR = BASE_DIR / "data" / "output"
TEMPLATE_DIR = BASE_DIR / "data" / "templates"

OPENAI_MODE = os.getenv("OPENAI_MODE", "manual").strip().lower()

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".docx", ".xlsx"}
MAX_DOCUMENT_CHARS = 120_000
CHUNK_SIZE = 8_000
CHUNK_OVERLAP = 500