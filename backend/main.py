"""Minimal API for the AI Lara prototype."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from generator.spec_builder import build_spec

app = FastAPI(
    title="AI Lara API",
    version="0.1.0",
    description=(
        "Prototype API that turns a natural-language app idea into a structured "
        "specification. It does not generate source code or APKs yet."
    ),
)


class SpecRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=2000)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ai-lara-api"}


@app.post("/generate-spec")
def generate_spec(body: SpecRequest) -> dict:
    try:
        return build_spec(body.prompt)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
