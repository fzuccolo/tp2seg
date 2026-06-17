from app.datos import load_dataset
from app.defensa import speaker_note_texts
from app.graficos import chart_guides
from app.metricas import compute_metrics
from scripts.generar_notas import render_iso_guide


def test_catalogo_graficos_de_defensa_es_completo():
    guides = chart_guides()
    filenames = [guide.filename for guide in guides]

    assert len(guides) >= 25
    assert len(filenames) == len(set(filenames))
    assert all(filename.endswith(".png") for filename in filenames)


def test_notas_presentador_mencionan_numeros_clave():
    result = compute_metrics(load_dataset("tecnohogar"))
    notes = "\n".join(speaker_note_texts(result))

    assert len(speaker_note_texts(result)) == 11
    for value in ["38.4%", "61.6%", "93", "11", "3", "604"]:
        assert value in notes
    assert "Mensaje principal" in notes
    assert "Preguntas esperables" in notes


def test_guia_iso_resume_norma_y_aplicacion():
    result = compute_metrics(load_dataset("tecnohogar"))
    guide = render_iso_guide(result)

    for value in ["ISO/IEC 27002:2022", "ISO/IEC 27001", "93 controles", "5 Organizativos", "6 Personas", "7 Físicos", "8 Tecnológicos"]:
        assert value in guide
    assert "ISO 27002 aporta el catálogo" in guide
    assert "CMMI" in guide
    assert "control -> hallazgo -> brecha -> proyecto" in guide
