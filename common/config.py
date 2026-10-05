import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")

DB_PATH = os.getenv("DB_PATH", "data/db/knowledge.db")

TESSERACT_CMD = os.getenv("TESSERACT_CMD", "")

CLIENT_FILE = os.getenv("GOOGLE_CLIENT_FILE", "credentials.json")
TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "token.json")

DOWNLOAD_DIR = "data/downloads"
AUDIO_DIR = "data/audio"