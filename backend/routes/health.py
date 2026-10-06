import requests
import pytesseract
from fastapi import APIRouter

from common.config import OLLAMA_URL, OLLAMA_MODEL, TESSERACT_CMD, DB_PATH
from knowledge import store

router = APIRouter()


@router.get("/health")
def health():
    db_ok = False
    ollama_ok = False
    tesseract_ok = False

    # Check SQLite
    try:
        store.init_db()
        db_ok = True
    except Exception:
        db_ok = False

    # Check Ollama
    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=3
        )
        ollama_ok = response.ok
    except Exception:
        ollama_ok = False

    # Check Tesseract
    try:
        if TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
        pytesseract.get_tesseract_version()
        tesseract_ok = True
    except Exception:
        tesseract_ok = False

    # Check classifier
    try:
        from ml.classifier import classify
        result = classify([])
        classifier = result.method
    except Exception:
        classifier = "fallback_rules"

    return {
        "status": "ok",
        "db": db_ok,
        "ollama": ollama_ok,
        "model": OLLAMA_MODEL,
        "tesseract": tesseract_ok,
        "classifier": classifier,
    }