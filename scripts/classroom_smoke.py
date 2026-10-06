import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ingestion.sync import sync


def main():
    result = sync()

    print("mode:", result["mode"])
    print("count:", len(result["items"]))
    print("error:", result["error"])

    for item in result["items"]:
        print(
            "-",
            item.id,
            "|",
            item.title,
            "|",
            item.source,
            "|",
            item.file_path,
        )


if __name__ == "__main__":
    main()