import importlib
import sqlite3
import sys

import requests


ok = True


def check(name, fn):
    global ok

    try:
        print(f"[ OK ] {name}: {fn()}")
    except Exception as e:
        ok = False
        print(f"[FAIL] {name}: {e}")


for m in [
    "fastapi",
    "uvicorn",
    "streamlit",
    "fitz",
    "pytesseract",
    "PIL",
    "nltk",
    "spacy",
    "tensorflow",
    "pyttsx3",
    "googleapiclient",
    "pydantic",
]:
    check(
        f"import {m}",
        lambda m=m: importlib.import_module(m).__name__,
    )


check(
    "python>=3.10",
    lambda: (
        sys.version.split()[0]
        if sys.version_info >= (3, 10)
        else 1 / 0
    ),
)


def _nltk():
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords

    return (
        len(word_tokenize("a b c")),
        len(stopwords.words("english")),
    )


check("nltk data", _nltk)


check(
    "spacy model",
    lambda: __import__("spacy")
    .load("en_core_web_sm")
    .meta["version"],
)


def _tess():
    import os
    import pytesseract

    if os.getenv("TESSERACT_CMD"):
        pytesseract.pytesseract.tesseract_cmd = os.getenv(
            "TESSERACT_CMD"
        )

    return pytesseract.get_tesseract_version()


check("tesseract", _tess)


check(
    "sqlite",
    lambda: sqlite3.sqlite_version,
)


check(
    "ollama (optional on non-demo laptops)",
    lambda: [
        m["name"]
        for m in requests.get(
            "http://localhost:11434/api/tags",
            timeout=3,
        ).json()["models"]
    ],
)


print(
    "\nALL GREEN"
    if ok
    else "\nFIX THE FAILS ABOVE BEFORE CONTINUING"
)