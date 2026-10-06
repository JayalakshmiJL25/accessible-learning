from ingestion.fallback_loader import load_fallback
from ingestion.sync import sync


def test_fallback_loader():
    items = load_fallback()

    assert isinstance(items, list)
    assert len(items) > 0

    item = items[0]

    assert item.id
    assert item.title
    assert item.content


def test_sync_fallback():
    result = sync(force_fallback=True)

    assert isinstance(result, dict)
    assert result["mode"] == "fallback"
    assert isinstance(result["items"], list)
    assert len(result["items"]) > 0