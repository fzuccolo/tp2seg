from streamlit.testing.v1 import AppTest


def test_tablero_streamlit_renderiza_sin_excepciones():
    app = AppTest.from_file("app/app.py")
    app.run(timeout=60)

    assert not app.exception
    assert app.title[0].value == "Tablero de Control de Seguridad - TecnoHogar S.A."
    assert app.selectbox[0].value == "tecnohogar"
    assert len(app.get("plotly_chart")) >= 20
    assert len(app.dataframe) >= 4
