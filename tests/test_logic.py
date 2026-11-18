"""Pruebas de la lógica principal (no dependen de FastAPI)."""
import pytest

from app import logic
from app.data import CLASES, HABILIDADES, PREGUNTAS

# Respuestas = índice de la opción elegida en cada pregunta (1..8)
PERFIL_TANQUE = {1: 0, 2: 0, 3: 0, 4: 0, 5: 3, 6: 1, 7: 1, 8: 0}
PERFIL_MAGO = {1: 1, 2: 1, 3: 2, 4: 2, 5: 0, 6: 0, 7: 3, 8: 3}
PERFIL_SIGILO = {1: 2, 2: 2, 3: 1, 4: 1, 5: 2, 6: 3, 7: 2, 8: 2}


def test_perfil_tanque_recomienda_clase_facil_cuerpo_a_cuerpo():
    resultado = logic.recomendar(PERFIL_TANQUE)
    assert resultado.principal.clase.slug in {"barbaro", "guerrero", "paladin"}
    assert resultado.principal.clase.dificultad == 1


def test_perfil_magico_recomienda_lanzador():
    resultado = logic.recomendar(PERFIL_MAGO)
    assert resultado.principal.clase.slug in {"mago", "hechicero", "brujo"}


def test_perfil_sigilo_recomienda_picaro():
    assert logic.recomendar(PERFIL_SIGILO).principal.clase.slug == "picaro"


def test_resultado_tiene_dos_alternativas_y_porcentaje_valido():
    resultado = logic.recomendar(PERFIL_TANQUE)
    assert len(resultado.alternativas) == 2
    assert 0 <= resultado.principal.compatibilidad <= 100
    assert resultado.principal.puntaje >= resultado.alternativas[0].puntaje


def test_todas_las_clases_cumplen_reglas_de_27_puntos():
    for clase in CLASES:
        habilidades = logic.asignar_habilidades(clase)
        assert set(habilidades) == set(HABILIDADES)
        assert logic.costo_total(habilidades) == logic.PUNTOS_TOTALES
        assert all(logic.VALOR_MIN <= v <= logic.VALOR_MAX for v in habilidades.values())


def test_falta_una_respuesta_lanza_error():
    incompleto = dict(PERFIL_TANQUE)
    del incompleto[3]
    with pytest.raises(logic.RespuestasInvalidas):
        logic.recomendar(incompleto)


def test_opcion_fuera_de_rango_lanza_error():
    invalido = dict(PERFIL_TANQUE)
    invalido[1] = len(PREGUNTAS[0].opciones)  # una opción más de las que existen
    with pytest.raises(logic.RespuestasInvalidas):
        logic.recomendar(invalido)


def test_parsear_formulario_rechaza_texto_no_numerico():
    with pytest.raises(logic.RespuestasInvalidas):
        logic.parsear_formulario({"p1": "abc"})
