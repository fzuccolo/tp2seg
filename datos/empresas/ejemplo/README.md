# Empresa ejemplo

Dataset de calibracion basado en el trabajo de referencia G1. No es el entregable final; sirve para comprobar que el formato code-first puede reproducir un tablero rico con los mismos tipos de graficos que se ven en el Excel.

## Fuente principal

Archivo de catedra:

```text
Recursos/TP1 2025 G1/REF G1 - Metricas_ISO_27002_2022_Grupo2_FINAL.xlsx
```

Fuente complementaria para proyectos:

```text
Recursos/TP2 Material/Relacion Controles Proyectos ISO27K.xlsx
```

## Archivos generados

- `empresa.yml`: metadata del caso. La razon social se toma como caso ejemplo para identificar el dataset.
- `activos.csv`: alcance minimo de organizacion/proceso para alimentar el modelo de datos.
- `entrevistas.csv`: hoja `Entrevistas` del Excel G1.
- `diagnostico.csv`: hoja `Cuestionario`, filas de controles 5..97. Contiene nivel CMMI, valor normalizado, evidencia, entrevistado, fecha, hallazgo y observaciones.
- `proyectos.csv`: hoja `Proyectos` del archivo `Relacion Controles Proyectos ISO27K.xlsx`, filtrada/ampliada con los proyectos usados por el anexo del ejemplo.
- `proyecto_control.csv`: vinculos control-proyecto obtenidos desde `Ctrl_Anexo`.

El catalogo comun `datos/estandares/iso27002_2022/catalogo_controles.csv` tambien se regenera desde `Ctrl_Anexo`.

## Comando de importacion

```bash
make import-example
```

## Controles de calidad esperados

- 93 controles diagnosticados.
- 7 entrevistas importadas.
- 45 proyectos de referencia.
- 93 vinculos control-proyecto.
