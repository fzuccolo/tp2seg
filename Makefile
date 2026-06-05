PYTHON ?= python3

.PHONY: validate build test app ci

validate:
	$(PYTHON) scripts/validar_datos.py

build:
	$(PYTHON) scripts/generar_salidas.py

test:
	$(PYTHON) -m pytest

app:
	streamlit run tablero/app.py

ci: validate test build
