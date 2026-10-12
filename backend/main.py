"""Minimal API for the AI Lara prototype."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from generator.project_builder import build_android_sources
from generator.spec_builder import build_spec

app = FastAPI(
    title="AI Lara API",
    version="0.2.0",
    description=(
        "Prototype API that turns a natural-language app idea into a specification "
        "and starter Android source files. It does not compile APKs."
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


@app.post("/generate-project")
def generate_project(body: SpecRequest) -> dict:
    """Generate starter Android source files; this endpoint does not build an APK."""
    try:
        spec = build_spec(body.prompt)
        files = build_android_sources(spec)
        return {
            "project_name": spec["project_name"],
            "platform": "android",
            "build_status": "source_generated_not_built",
            "files": files,
            "notice": "Kode sumber awal dibuat. File ini belum dikompilasi menjadi APK.",
        }
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
