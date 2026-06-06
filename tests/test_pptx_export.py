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
        slide1 = archive.read("ppt/slides/slide1.xml").decode("utf-8")
        visible_slides = "\n".join(
            archive.read(name).decode("utf-8")
            for name in sorted(names)
            if name.startswith("ppt/slides/slide") and name.endswith(".xml")
        )
        slide_rels = "\n".join(
            archive.read(name).decode("utf-8")
            for name in sorted(names)
            if name.startswith("ppt/slides/_rels/slide") and name.endswith(".xml.rels")
        )
        notes1 = archive.read("ppt/notesSlides/notesSlide1.xml").decode("utf-8")
    assert "ppt/presentation.xml" in names
    assert "ppt/notesSlides/notesSlide1.xml" in names
    assert "ppt/notesMasters/notesMaster1.xml" in names
    assert len([name for name in names if name.startswith("ppt/notesSlides/notesSlide") and name.endswith(".xml")]) == 11
    assert any(name.startswith("ppt/charts/chart") for name in names)
    assert "Grupo 1" in slide1
    assert "https://tp2seg.streamlit.app/" in visible_slides
    assert "https://tp2seg.streamlit.app/" in slide_rels
    assert "Argumento de defensa" not in visible_slides
    assert "Guion de presentacion" not in visible_slides
    assert "Cierre" not in visible_slides
    assert "Narrativa" in notes1
