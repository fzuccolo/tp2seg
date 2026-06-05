# Datos

Esta carpeta contiene todas las fuentes versionadas del tablero. La regla de trabajo es que el tablero, los informes y las salidas se regeneren desde CSV/YAML, sin completar celdas manualmente en Excel.

## Estructura

```text
datos/
  estandares/       Catalogos y escalas comunes.
  empresas/         Datasets separados por empresa/caso.
```

Cada empresa vive en su propia carpeta para poder cambiar el dataset desplegado sin mezclar evidencias. El tablero permite seleccionar la empresa y el pipeline genera salidas para todas las carpetas disponibles.

## Origen de datos

- `estandares/iso27002_2022/catalogo_controles.csv`: catalogo comun de controles, atributos, funciones, capacidades y dominios.
- `estandares/iso27002_2022/parametros_madurez.csv`: escala CMMI 0..5 usada por la catedra.
- `empresas/ejemplo`: importacion programatica del trabajo de referencia G1.
- `empresas/tecnohogar`: caso propio del TP2; por ahora es semilla parcial y se completa en la etapa siguiente.

## Reproduccion

El dataset `ejemplo` se regenera con:

```bash
make import-example
```

La validacion de integridad se ejecuta con:

```bash
make validate
```
