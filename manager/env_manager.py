from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / "runtime" / ".env")

OPENAI_API_KEY = os.getenv("OPENAI")
DEFAULT_USER = os.getenv("USER")
SMALL_OPENAI_MODEL = os.getenv("SMALL_OPENAI_MODEL")
LARGE_OPENAI_MODEL = os.getenv("LARGE_OPENAI_MODEL")