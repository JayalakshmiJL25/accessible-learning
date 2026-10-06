from fastapi import APIRouter
from pydantic import BaseModel

from ingestion.sync import sync
from knowledge import store


router = APIRouter()


class SyncRequest(BaseModel):
    force_fallback: bool = False


@router.post("/sync")
def do_sync(req: SyncRequest = SyncRequest()):
    r = sync(req.force_fallback)

    for a in r["items"]:
        store.upsert_document(a)

    return {
        "mode": r["mode"],
        "count": len(r["items"]),
        "error": r["error"],
        "items": [a.model_dump() for a in r["items"]],
    }