# TecnoHogar

Dataset principal del TP2. Representa un diagnostico defendible de TecnoHogar S.A. sobre ISO/IEC 27002:2022, usando como base el inventario y la clasificacion del TP1.

## Fuentes

- `Entregas/TP1/TP1_Inventario_TecnoHogar_v2.xlsx`: caso TecnoHogar, 6 procesos, 41 activos, roles, dependencias y clasificacion CID.
- `datos/estandares/iso27002_2022/catalogo_controles.csv`: catalogo de 93 controles trabajado desde el ejemplo de la catedra.
- Material GESI-C6 de la catedra: criterio de tablero, KPI/KGI, madurez CMMI y plan de acciones.
- Ejemplo G1: referencia de estructura de diagnostico, madurez, proyectos y trazabilidad.

## Archivos

- `activos.csv`: 41 activos del TP1 con tipo, proceso, responsable, criticidad CID y, para datos/informacion, C/I/D y marco aplicable.
- `entrevistas.csv`: responsables usados como fuente de evidencia.
- `diagnostico.csv`: 93 controles ISO evaluados con nivel CMMI, valor normalizado, evidencia, hallazgo, observacion, fuente y objetivo de negocio.
- `proyectos.csv`: cartera de 11 iniciativas priorizables.
- `proyecto_control.csv`: relacion entre controles y proyectos.

## Criterio de numeros

La madurez global queda deliberadamente por debajo del ejemplo bancario: TecnoHogar tiene inventario, clasificacion y algunos controles operativos, pero todavia no tiene un SGSI medido y optimizado. La escala usada es CMMI 0..5:

- 0: inexistente.
- 1: inicial y reactivo.
- 2: gestionado parcialmente.
- 3: definido/documentado.
- 4: medido con indicadores.
- 5: optimizado.

## Guia para explicar graficos

- Ejecutivo: resume madurez, brecha, control mas critico, capacidad mas debil y quick wins.
- Mapa ISO: muestra cobertura de los 4 capitulos y distribucion CMMI de los 93 controles.
- Perfil: agrupa controles por funciones, dominios, CID, tipo y capacidad operacional.
- Brechas: prioriza controles por brecha ponderada; sirve para justificar el plan.
- Plan: traduce brechas a proyectos con esfuerzo, plazo, tipo de seguridad y quick wins.
- Trazabilidad: muestra la cadena capitulo -> control -> proyecto -> evidencia.

## Regeneracion

```bash
make generate-tecnohogar
```

Si el Excel TP1 esta en otra ubicacion:

```bash
TP1_TECNOHOGAR_XLSX=/ruta/TP1_Inventario_TecnoHogar_v2.xlsx make generate-tecnohogar
```
