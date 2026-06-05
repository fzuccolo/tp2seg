# Empresas

Cada subcarpeta representa un dataset independiente que puede visualizarse en el tablero y compilarse en CI.

## Archivos requeridos

- `empresa.yml`: metadata del caso y estandar utilizado.
- `activos.csv`: activos o procesos principales del alcance.
- `diagnostico.csv`: madurez por control, evidencia, entrevistado, fecha y observaciones.
- `proyectos.csv`: cartera de iniciativas de mejora.
- `proyecto_control.csv`: trazabilidad entre proyectos y controles ISO.

## Archivos opcionales

- `entrevistas.csv`: registro de entrevistados usado como fuente de evidencia.

## Convencion

El nombre de carpeta es el identificador de empresa. Ejemplos:

- `ejemplo`: dataset de referencia importado desde el Excel del trabajo G1.
- `tecnohogar`: caso del TP2, que debe convertirse en el entregable final.
