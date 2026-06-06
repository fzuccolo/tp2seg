# TP2 - Tablero de Control de Seguridad

El objetivo es mantener el trabajo como codigo: datos versionados, metricas calculadas, tablero interactivo, informe y slides generados por pipeline.

## Stack

- Python + pandas para lectura y calculo.
- Streamlit + Plotly para el tablero.
- Quarto para informe y presentacion.
- GitHub Actions para validar y generar artifacts.

## Estructura

```text
datos/      Datos del estandar y de cada empresa
app/        App Streamlit y logica reutilizable de carga/metricas/render
scripts/    Comandos de validacion y generacion
docs/       Fuentes Quarto de informes y presentaciones
.build/     Archivos generados localmente, ignorados por git
```

## Empresas

- `ejemplo`: dataset importado desde el trabajo de referencia G1 para calibrar el formato, el tablero y los graficos.
- `tecnohogar`: caso principal del TP2, derivado del TP1 y cubriendo los 93 controles ISO/IEC 27002:2022.

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

Reimportar el caso ejemplo desde los Excel de la catedra:

```bash
make import-example
```

Regenerar el caso TecnoHogar desde el inventario del TP1 y el catalogo ISO:

```bash
make generate-tecnohogar
```

Si el Excel TP1 esta en otra ruta:

```bash
TP1_TECNOHOGAR_XLSX=/ruta/TP1_Inventario_TecnoHogar_v2.xlsx make generate-tecnohogar
```

Levantar el tablero:

```bash
make app
```

## Entregables generados

Luego de `make build`, las salidas quedan en:

```text
.build/<empresa>/
  metricas.csv
  capitulos.csv
  madurez_distribucion.csv
  matriz_madurez.csv
  capacidad_operacional.csv
  ciberfunciones.csv
  proyectos_por_plazo.csv
  proyectos_por_tipo.csv
  proyectos_priorizados.csv
  resumen.json
  informe/informe.html
  slides/presentacion.html
```

## CI

El workflow `.github/workflows/ci.yml` corre en cada push a `main` y tambien se puede ejecutar manualmente desde GitHub Actions:

1. Instala Python y dependencias.
2. Instala Quarto.
3. Valida los datos.
4. Ejecuta tests.
5. Genera informe, slides y metricas.
6. Publica artifacts descargables.

Artifacts principales:

- `tp2-tecnohogar-presentacion`: presentacion HTML y `presentacion.pptx` editable en PowerPoint.
- `tp2-tecnohogar-informe-ejecutivo`: informe ejecutivo HTML.
- `tp2-build-completo`: metricas, CSV, informe, slides y salidas completas.

Para descargarlos en GitHub:

1. Entrar a **Actions**.
2. Abrir la ultima corrida de **CI y Entregables TP2**.
3. Bajar hasta **Artifacts**.
4. Descargar `tp2-tecnohogar-presentacion` o `tp2-tecnohogar-informe-ejecutivo`.

## Deploy del tablero

El entrypoint para Streamlit Community Cloud es:

```text
app/app.py
```

Los pushes a `main` actualizan el tablero. La URL final se configura desde Streamlit Community Cloud.

## Base academica

Esta version usa los 93 controles ISO/IEC 27002:2022 trabajados en el material de catedra y escala CMMI:

- TP2: tablero, metricas, graficos, presentacion e informe.
- Clase GESI-C6: metricas, KPIs, tablero y plan de acciones.
- Ejemplo G1: diagnostico ISO 27001/27002:2022 con madurez CMMI y plan de mejora.
- TP1: TecnoHogar S.A. como caso principal.
