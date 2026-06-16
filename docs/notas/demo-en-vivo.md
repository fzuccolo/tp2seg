# Demo en vivo

## Objetivo

Mostrar que el tablero permite ir desde una lectura ejecutiva hasta controles y proyectos trazables. La demo tiene que ser corta, guiada y conectada con la narrativa de la PPTX.

## Recorrido recomendado

1. Abrir `https://tp2seg.streamlit.app/` y verificar que el caso seleccionado sea `tecnohogar`.
2. Tab **Ejecutivo**: mostrar madurez global **38.4%**, brecha **61.6%**, **93 controles**, **3 quick wins** y radar de capacidades.
3. Tab **Mapa ISO**: mostrar que están los capítulos 5, 6, 7 y 8 y que los cuadrados representan controles evaluados.
4. Tab **Brechas**: mostrar el Pareto y explicar que la priorización usa brecha ponderada.
5. Tab **Plan**: mostrar las **11 iniciativas**, la matriz impacto/esfuerzo y el roadmap de **604 jornadas**.
6. Tab **Trazabilidad**: cerrar con el Sankey y la tabla control-proyecto para demostrar que cada decisión se puede defender.

## Qué no conviene hacer

- No navegar sin rumbo por todas las tablas.
- No intentar explicar cada control uno por uno.
- No presentar el porcentaje global como única verdad.
- No decir que "todo está mal"; la lectura correcta es base operativa con brecha de formalización, medición y seguimiento.

## Plan B si Streamlit falla

1. Usar la PPTX generada.
2. Abrir `docs/notas/guia-graficos.md`.
3. Mostrar los screenshots de `docs/notas/assets/graficos/`.
4. Explicar que esos PNG fueron generados desde las mismas funciones Plotly que usa el tablero, con datos de TecnoHogar.

## Cierre sugerido

El tablero transforma el diagnóstico en gobierno: permite medir, priorizar, justificar proyectos y seguir la mejora de seguridad en el tiempo.
