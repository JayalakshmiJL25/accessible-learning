from typing import Literal
from pydantic import BaseModel, Field


Category = Literal[
    "ASSIGNMENT",
    "ANNOUNCEMENT",
    "LECTURE_NOTES",
    "STUDY_MATERIAL",
    "EXAM_INFORMATION",
]


class AcademicContent(BaseModel):
    id: str
    source: str
    title: str
    content: str = ""
    file_path: str | None = None
    mime_type: str | None = None
    metadata: dict = Field(default_factory=dict)


class ExtractedDocument(BaseModel):
    document_id: str
    title: str
    text: str
    pages: int
    method: Literal["pymupdf", "tesseract", "inline_text"]
    char_count: int
    warnings: list[str] = Field(default_factory=list)


class Entity(BaseModel):
    text: str
    label: str


class ProcessedDocument(BaseModel):
    document_id: str
    tokens: list[str]
    entities: list[Entity]
    sentence_count: int


class Classification(BaseModel):
    category: Category
    confidence: float
    probabilities: dict[str, float]
    method: Literal["gru", "fallback_rules"]


class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    source: str
    title: str
    section: str
    category: Category
    text: str
    position: int


class SummaryResult(BaseModel):
    document_id: str
    summary: str
    model: str
    method: Literal["ollama", "pregenerated"]
    warnings: list[str] = Field(default_factory=list)


class AudioResult(BaseModel):
    document_id: str
    audio_path: str
    audio_url: str