PYTHON ?= $(shell if [ -x .venv/bin/python ]; then printf ".venv/bin/python"; else printf "python3"; fi)

.PHONY: validate build notas test app ci

validate:
	$(PYTHON) scripts/validar_datos.py

build:
	$(PYTHON) scripts/generar_salidas.py

notas:
	$(PYTHON) scripts/generar_notas.py

test:
	$(PYTHON) -m pytest

app:
	$(PYTHON) -m streamlit run app/app.py

ci: validate test notas build
