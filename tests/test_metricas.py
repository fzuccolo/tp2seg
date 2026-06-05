from app.datos import load_dataset
from app.metricas import compute_metrics


def test_madurez_global_esta_en_rango():
    result = compute_metrics(load_dataset("tecnohogar"))
    assert 0 <= result.resumen["madurez_global"] <= 1
    assert 0 <= result.resumen["brecha_global"] <= 1


def test_control_mas_critico_tiene_brecha():
    result = compute_metrics(load_dataset("tecnohogar"))
    assert not result.top_brechas.empty
    assert result.top_brechas.iloc[0]["brecha"] > 0


def test_proyectos_tienen_prioridad_calculada():
    result = compute_metrics(load_dataset("tecnohogar"))
    assert "prioridad" in result.proyectos.columns
    assert result.proyectos["prioridad"].max() > 0
