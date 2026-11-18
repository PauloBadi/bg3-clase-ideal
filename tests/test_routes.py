"""Pruebas de las rutas de FastAPI con TestClient."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

FORM_TANQUE = {"p1": "0", "p2": "0", "p3": "0", "p4": "0",
               "p5": "3", "p6": "1", "p7": "1", "p8": "0"}


def test_pagina_inicio_responde_con_el_cuestionario():
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert "Encuentra tu clase" in respuesta.text
    assert 'name="p8"' in respuesta.text


def test_envio_valido_muestra_la_clase_recomendada():
    respuesta = client.post("/resultado", data=FORM_TANQUE)
    assert respuesta.status_code == 200
    assert "Tu clase ideal" in respuesta.text
    assert any(n in respuesta.text for n in ("Bárbaro", "Guerrero", "Paladín"))


def test_envio_incompleto_devuelve_400_con_mensaje():
    datos = dict(FORM_TANQUE)
    del datos["p5"]
    respuesta = client.post("/resultado", data=datos)
    assert respuesta.status_code == 400
    assert "Falta responder la pregunta 5" in respuesta.text


def test_envio_con_valor_invalido_devuelve_400():
    datos = dict(FORM_TANQUE, p2="99")
    respuesta = client.post("/resultado", data=datos)
    assert respuesta.status_code == 400
    assert "no existe" in respuesta.text


def test_lista_de_clases_muestra_las_12():
    respuesta = client.get("/clases")
    assert respuesta.status_code == 200
    assert respuesta.text.count("/clases/") == 12


def test_clase_inexistente_devuelve_404():
    respuesta = client.get("/clases/dragon")
    assert respuesta.status_code == 404
