from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert "db" in data
    assert "ollama" in data
    assert "tesseract" in data
    assert "classifier" in data


def test_sync_fallback():
    response = client.post(
        "/sync",
        json={"force_fallback": True}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["mode"] == "fallback"
    assert data["count"] > 0
    assert isinstance(data["items"], list)


def test_documents():
    response = client.get("/documents")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_document_detail():
    response = client.get(
        "/documents/local_sample_announcement"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "local_sample_announcement"
    assert data["title"] == "Computer Networks Internal Assessment"
    assert data["status"] == "synced"