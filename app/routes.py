"""Rutas de FastAPI: reciben las solicitudes y delegan la lógica en logic.py."""
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app import logic
from app.data import CLASES, PREGUNTAS

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    return templates.TemplateResponse(
        request, "index.html", {"preguntas": PREGUNTAS, "previas": {}, "error": None}
    )


@router.post("/resultado", response_class=HTMLResponse)
async def resultado(request: Request):
    form = await request.form()
    try:
        respuestas = logic.parsear_formulario(form)
        datos = logic.recomendar(respuestas)
    except logic.RespuestasInvalidas as exc:
        # Entrada incorrecta: se vuelve a mostrar el formulario con el mensaje.
        return templates.TemplateResponse(
            request,
            "index.html",
            {"preguntas": PREGUNTAS, "previas": dict(form), "error": str(exc)},
            status_code=400,
        )
    return templates.TemplateResponse(request, "resultado.html", {"r": datos})


@router.get("/clases", response_class=HTMLResponse)
def lista_clases(request: Request):
    return templates.TemplateResponse(request, "clases.html", {"clases": CLASES})


@router.get("/clases/{slug}", response_class=HTMLResponse)
def detalle_clase(request: Request, slug: str):
    try:
        clase = logic.obtener_clase(slug)
    except KeyError as exc:
        return templates.TemplateResponse(
            request, "error.html", {"mensaje": exc.args[0]}, status_code=404
        )
    return templates.TemplateResponse(request, "clase.html", {"clase": clase})
