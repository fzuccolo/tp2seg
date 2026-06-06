PYTHON ?= $(shell if [ -x .venv/bin/python ]; then printf ".venv/bin/python"; else printf "python3"; fi)

.PHONY: validate build test app import-example generate-tecnohogar ci

validate:
	$(PYTHON) scripts/validar_datos.py

build:
	$(PYTHON) scripts/generar_salidas.py

test:
	$(PYTHON) -m pytest

app:
	$(PYTHON) -m streamlit run app/app.py

import-example:
	$(PYTHON) scripts/importar_ejemplo.py

generate-tecnohogar:
	$(PYTHON) scripts/generar_tecnohogar.py

ci: validate test build
