import os
from backend.errors import ApiError
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from knowledge import store
from backend.routes import health, sync, documents, generate


os.makedirs("data/audio", exist_ok=True)

app = FastAPI(title="Accessible Learning API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/audio",
    StaticFiles(directory="data/audio"),
    name="audio",
)

for r in (health, sync, documents, generate):
    app.include_router(r.router)


@app.on_event("startup")
def _startup():
    store.init_db()



@app.exception_handler(ApiError)
async def _api_error(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status,
        content={
            "error": exc.code,
            "detail": exc.detail,
        },
    )


@app.exception_handler(Exception)
async def _unhandled(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "detail": str(exc),
        },
    )