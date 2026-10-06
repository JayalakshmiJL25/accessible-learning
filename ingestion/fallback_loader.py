import json

from common.models import AcademicContent


def load_fallback(
    path="data/classroom_fallback/manifest.json",
) -> list[AcademicContent]:
    with open(path, encoding="utf-8") as file:
        data = json.load(file)

    return [AcademicContent(**item) for item in data]