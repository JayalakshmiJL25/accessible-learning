import os

from common.config import CLIENT_FILE
from ingestion.fallback_loader import load_fallback


def sync(force_fallback: bool = False) -> dict:
    if not force_fallback and os.path.exists(CLIENT_FILE):
        try:
            from ingestion.classroom_client import fetch_items

            items = fetch_items()

            if items:
                return {
                    "mode": "classroom",
                    "items": items,
                    "error": None,
                }

        except Exception as exc:
            return {
                "mode": "fallback",
                "items": load_fallback(),
                "error": f"Classroom failed: {exc}",
            }

    return {
        "mode": "fallback",
        "items": load_fallback(),
        "error": None if force_fallback else "No credentials.json",
    }


if __name__ == "__main__":
    result = sync()

    print(result["mode"], len(result["items"]), result["error"])

    for item in result["items"]:
        print(
            "-",
            item.id,
            "|",
            item.title,
            "|",
            item.file_path,
        )