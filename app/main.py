"""Punto de entrada de la aplicación FastAPI."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="¿Qué clase de BG3 te sirve?")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(router)
