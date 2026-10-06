from fastapi import APIRouter

from knowledge import store
from backend.errors import ApiError


router = APIRouter()


@router.get("/documents")
def list_documents():
    return store.list_documents()


@router.get("/documents/{document_id}")
def get_document(document_id: str):
    document = store.get_detail(document_id)

    if document is None:
        raise ApiError(
            404,
            "not_found",
            f"Document '{document_id}' not found",
        )

    return document