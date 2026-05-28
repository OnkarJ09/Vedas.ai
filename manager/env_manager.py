from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / "runtime" / ".env")

# PERSONAL INFORMATION
DEFAULT_USER = os.getenv("USER")

# API KEYS
OPENAI_API_KEY = os.getenv("OPENAI")
OPEN_WEATHER_API_KEY = str(os.getenv("OPEN_WEATHER"))
GEOCODING_API_KEY = str(os.getenv("GEOCODING"))

# MODEL NAMES
SMALL_OPENAI_MODEL = os.getenv("SMALL_OPENAI_MODEL")
LARGE_OPENAI_MODEL = os.getenv("LARGE_OPENAI_MODEL")

# DEFAULTS
DEFAULT_VOICE = os.getenv("DEFAULT_VOICE")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE")
DEFAULT_LANGUAGE_CODE = os.getenv("DEFAULT_LANGUAGE_CODE")
DEFAULT_CITY = str(os.getenv("DEFAULT_CITY"))
DEFAULT_COUNTRY = str(os.getenv("DEFAULT_COUNTRY"))
DEFAULT_WEATHER_UNIT = str(os.getenv("DEFAULT_WEATHER_UNIT"))
DEFAULT_LATITUDE = str(os.getenv("DEFAULT_LATITUDE"))
DEFAULT_LONGITUDE = str(os.getenv("DEFAULT_LONGITUDE"))