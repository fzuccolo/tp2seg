from app.datos import load_dataset
from app.metricas import compute_metrics


def test_ejemplo_cubre_catalogo_iso_27002_completo():
    result = compute_metrics(load_dataset("ejemplo"))
    counts = result.controles.groupby("capitulo")["control_id"].nunique().to_dict()

    assert result.resumen["controles_evaluados"] == 93
    assert counts == {
        "5 - Controles Organizativos": 37,
        "6 - Controles de Personas": 8,
        "7 - Controles Físicos": 14,
        "8 - Controles Tecnológicos": 34,
    }


def test_ejemplo_genera_dimensiones_del_tablero():
    result = compute_metrics(load_dataset("ejemplo"))

    assert result.resumen["entrevistas"] == 7
    assert result.resumen["proyectos"] == 45
    assert not result.matriz_madurez.empty
    assert not result.capacidad_operacional.empty
    assert not result.ciberfunciones.empty
    assert not result.proyectos_plazo.empty
    assert not result.proyectos_capitulo.empty
    assert not result.proyectos_capacidad.empty
    assert not result.esfuerzo_roadmap.empty
    assert not result.quick_wins.empty
    assert not result.trazabilidad.empty


def test_madurez_global_esta_en_rango():
    result = compute_metrics(load_dataset("tecnohogar"))
    assert 0 <= result.resumen["madurez_global"] <= 1
    assert 0 <= result.resumen["brecha_global"] <= 1
    assert 0 < result.resumen["controles_evaluados"] <= 93


def test_control_mas_critico_tiene_brecha():
    result = compute_metrics(load_dataset("tecnohogar"))
    assert not result.top_brechas.empty
    assert result.top_brechas.iloc[0]["brecha"] > 0


def test_proyectos_tienen_prioridad_calculada():
    result = compute_metrics(load_dataset("tecnohogar"))
    assert "prioridad" in result.proyectos.columns
    assert result.proyectos["prioridad"].max() > 0
