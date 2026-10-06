import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ingestion.sync import sync


def main():
    result = sync()

    output = [
        item.model_dump()
        for item in result["items"]
    ]

    output_path = ROOT / "data" / "classroom_fallback" / "snapshot.json"

    output_path.write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )

    print(f"Exported {len(output)} items to {output_path}")


if __name__ == "__main__":
    main()