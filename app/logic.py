"""Lógica de la aplicación (sin dependencias de FastAPI ni de Jinja2).

Flujo: respuestas -> validación -> puntaje por clase -> ranking -> hoja de personaje.
"""
from dataclasses import dataclass
from typing import Mapping

from app.data import CLASES, CLASES_POR_SLUG, HABILIDADES, PREGUNTAS, Clase

# Reglas de creación de personaje de BG3: 27 puntos, valores entre 8 y 15.
PUNTOS_TOTALES = 27
VALOR_MIN, VALOR_MAX = 8, 15
COSTO_PUNTOS = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
# Reparto recomendado: se asigna según el orden de prioridad de cada clase.
REPARTO_BASE = (15, 14, 13, 12, 10, 8)


class RespuestasInvalidas(ValueError):
    """Cuestionario incompleto o con valores fuera de rango."""


@dataclass(frozen=True)
class Recomendacion:
    clase: Clase
    puntaje: int
    compatibilidad: int  # porcentaje 0-100


@dataclass(frozen=True)
class Resultado:
    principal: Recomendacion
    alternativas: tuple
    habilidades: tuple  # ((nombre, valor), ...) de la clase principal
    puntos_usados: int


def parsear_formulario(form: Mapping) -> dict:
    """Convierte los campos p1..pN del formulario en {id_pregunta: indice_opcion}."""
    respuestas = {}
    for pregunta in PREGUNTAS:
        valor = form.get(f"p{pregunta.id}")
        if valor is None or valor == "":
            continue
        try:
            respuestas[pregunta.id] = int(valor)
        except (TypeError, ValueError):
            raise RespuestasInvalidas(
                f"La respuesta de la pregunta {pregunta.id} no es válida."
            )
    return respuestas


def validar_respuestas(respuestas: Mapping) -> None:
    for pregunta in PREGUNTAS:
        if pregunta.id not in respuestas:
            raise RespuestasInvalidas(f"Falta responder la pregunta {pregunta.id}.")
        indice = respuestas[pregunta.id]
        if not 0 <= indice < len(pregunta.opciones):
            raise RespuestasInvalidas(
                f"La opción elegida en la pregunta {pregunta.id} no existe."
            )


def _puntos_opcion(clase: Clase, opcion) -> int:
    return sum(v * clase.rasgos.get(r, 0) for r, v in opcion.rasgos.items())


def puntaje_clase(clase: Clase, respuestas: Mapping) -> int:
    return sum(
        _puntos_opcion(clase, p.opciones[respuestas[p.id]]) for p in PREGUNTAS
    )


def puntaje_maximo(clase: Clase) -> int:
    """Mejor puntaje posible de la clase (sirve para calcular el porcentaje)."""
    return sum(max(_puntos_opcion(clase, o) for o in p.opciones) for p in PREGUNTAS)


def asignar_habilidades(clase: Clase) -> dict:
    """Asigna el reparto base a las habilidades según la prioridad de la clase."""
    return dict(zip(clase.orden_habilidades, REPARTO_BASE))


def costo_total(habilidades: Mapping) -> int:
    return sum(COSTO_PUNTOS[v] for v in habilidades.values())


def recomendar(respuestas: Mapping) -> Resultado:
    validar_respuestas(respuestas)
    ranking = []
    for clase in CLASES:
        puntaje = puntaje_clase(clase, respuestas)
        maximo = puntaje_maximo(clase)
        compat = round(100 * max(puntaje, 0) / maximo) if maximo > 0 else 0
        ranking.append(Recomendacion(clase, puntaje, min(compat, 100)))
    # Desempate: mayor puntaje, luego la clase más fácil, luego orden alfabético.
    ranking.sort(key=lambda r: (-r.puntaje, r.clase.dificultad, r.clase.nombre))
    principal = ranking[0]
    habilidades = asignar_habilidades(principal.clase)
    return Resultado(
        principal=principal,
        alternativas=tuple(ranking[1:3]),
        habilidades=tuple((HABILIDADES[h], v) for h, v in habilidades.items()),
        puntos_usados=costo_total(habilidades),
    )


def obtener_clase(slug: str) -> Clase:
    try:
        return CLASES_POR_SLUG[slug]
    except KeyError:
        raise KeyError(f"La clase '{slug}' no existe.")
