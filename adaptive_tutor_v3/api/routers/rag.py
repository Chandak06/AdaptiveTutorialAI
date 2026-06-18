from __future__ import annotations

from fastapi import APIRouter

from config import settings
from rag.chain import RAGChain

router = APIRouter()
chain = RAGChain()


@router.post("/ingest")
def ingest(docs: list[dict]):
    chain.ingest(docs)
    return {"ingested": len(docs)}


@router.get("/ask")
def ask(question: str):
    return chain.answer(question)
