# TP2 - Tablero de Control de Seguridad

Repositorio reproducible para el TP2 de Seguridad Informatica.

El objetivo es mantener el trabajo como codigo: datos versionados, metricas calculadas, tablero interactivo, informe y slides generados por pipeline.

## Stack

- Python + pandas para lectura y calculo.
- Streamlit + Plotly para el tablero.
- Quarto para informe y presentacion.
- GitHub Actions para validar y generar artifacts.

## Estructura

```text
datos/      Datos del estandar y de cada empresa
motor/      Logica reutilizable de carga y metricas
tablero/    App Streamlit
scripts/    Comandos de validacion y generacion
informe/    Informe Quarto por empresa
slides/     Presentacion Quarto por empresa
salidas/    Archivos generados
```

## Uso local

Crear un entorno e instalar dependencias:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Validar datos:

```bash
make validate
```

Generar salidas:

```bash
make build
```

Ejecutar tests:

```bash
make test
```

Levantar el tablero:

```bash
make app
```

## Entregables generados

Luego de `make build`, las salidas quedan en:

```text
salidas/tecnohogar/
  metricas.csv
  capitulos.csv
  proyectos_priorizados.csv
  resumen.json
  informe/informe.html
  slides/presentacion.html
```

## CI

El workflow `.github/workflows/ci.yml` corre en cada push a `main`:

1. Instala Python y dependencias.
2. Instala Quarto.
3. Valida los datos.
4. Ejecuta tests.
5. Genera informe, slides y metricas.
6. Publica `salidas/` como artifact descargable.

## Deploy del tablero

El entrypoint para Streamlit Community Cloud es:

```text
tablero/app.py
```

Cuando el repo privado este conectado a Streamlit, los pushes a `main` actualizan el tablero. La URL final se configura desde Streamlit Community Cloud.

## Base academica

Esta primera version usa una seleccion reducida de controles ISO/IEC 27002:2022 y escala CMMI, siguiendo la forma del material de catedra:

- TP2: tablero, metricas, graficos, presentacion e informe.
- Clase GESI-C6: metricas, KPIs, tablero y plan de acciones.
- Ejemplo G1: diagnostico ISO 27001/27002:2022 con madurez CMMI y plan de mejora.
- TP1: TecnoHogar S.A. como caso principal.
