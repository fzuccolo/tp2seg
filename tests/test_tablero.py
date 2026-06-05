from streamlit.testing.v1 import AppTest


def test_tablero_streamlit_renderiza_sin_excepciones():
    app = AppTest.from_file("app/app.py")
    app.run(timeout=60)

    assert not app.exception
