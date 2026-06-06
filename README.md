# Tablero de Control de Seguridad - TecnoHogar

Generación del tablero de seguridad para TecnoHogar basado en ISO/IEC 27002:2022.

## Resumen

* Tablero: https://tp2seg.streamlit.app/
* Datos fuente: [datos](./datos)
* Presentacion PPTX: https://github.com/fzuccolo/tp2seg/releases/latest/download/tp2-tecnohogar-presentacion.pptx
* Informe PDF: https://github.com/fzuccolo/tp2seg/releases/latest/download/tp2-tecnohogar-informe.pdf
* ZIP PPTX + PDF: https://github.com/fzuccolo/tp2seg/releases/latest/download/tp2-tecnohogar-entregables.zip

## Estructura

```text
datos/      Datos del estandar y de cada caso
app/        App Streamlit y logica reutilizable de carga/metricas/render
scripts/    Comandos de validacion y generacion
docs/       Fuentes Quarto de informes y presentaciones
```

## CI

El workflow `.github/workflows/ci.yml` corre en cada push a `main` y tambien se puede ejecutar manualmente desde GitHub Actions:

1. Instala Python y dependencias.
2. Valida los datos.
3. Ejecuta tests.
4. Genera PPTX, informe PDF y ZIP.
5. Deploya tablero en https://tp2seg.streamlit.app/
6. Publica una GitHub Release fechada con links permanentes.

Las URLs de la seccion Resumen siempre apuntan a la ultima Release. Cada Release queda versionada con fecha y hora UTC en el tag `entregables-YYYYMMDD-HHMMSS`.


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
