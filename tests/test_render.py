from app.datos import load_dataset
from app.metricas import compute_metrics
from app.render import write_outputs


def test_write_outputs_genera_graficos_para_informe(tmp_path):
    result = compute_metrics(load_dataset("tecnohogar"))

    write_outputs(result, tmp_path)

    assets = tmp_path / "report_assets"
    assert (assets / "postura.svg").exists()
    assert (assets / "madurez-capitulos.svg").exists()
    assert (assets / "brechas-principales.svg").exists()

    summary = (tmp_path / "resumen_informe.md").read_text(encoding="utf-8")
    assert "report_assets/postura.svg" in summary
    assert "Resumen ejecutivo" in summary
