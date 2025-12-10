from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.v1.word import router as word_router

app = FastAPI(title="Vocab App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(word_router, prefix="/api/v1")

__all__ = ["app"]

