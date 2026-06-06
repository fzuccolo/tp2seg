from zipfile import ZipFile

from app.datos import load_dataset
from app.metricas import compute_metrics
from app.pptx_export import write_pptx


def test_exporta_presentacion_pptx(tmp_path):
    result = compute_metrics(load_dataset("tecnohogar"))
    output = tmp_path / "presentacion.pptx"

    write_pptx(result, output)

    assert output.exists()
    assert output.stat().st_size > 20_000
    with ZipFile(output) as archive:
        names = set(archive.namelist())
    assert "ppt/presentation.xml" in names
    assert any(name.startswith("ppt/charts/chart") for name in names)
