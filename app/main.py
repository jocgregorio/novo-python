"""Punto de entrada de la API de Novo Talento."""

from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(title="Novo Talento CV Orchestrator")
app.include_router(router)
