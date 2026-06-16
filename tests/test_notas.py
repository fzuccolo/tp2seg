from app.datos import load_dataset
from app.defensa import speaker_note_texts
from app.graficos import chart_guides
from app.metricas import compute_metrics


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
