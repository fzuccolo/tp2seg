# Conceptos clave

## Métrica vs medida

Una **medida** es un dato puntual: por ejemplo, nivel CMMI asignado a un control, peso del control o cantidad de jornadas. Una **métrica** es el cálculo que permite interpretar medidas: por ejemplo, madurez global, brecha ponderada o prioridad de proyecto.

## KPI, KGI y CSF

Un **KPI** mide desempeño durante la gestión, como avance de proyectos o brecha por capítulo. Un **KGI** mide resultado frente a un objetivo, como la madurez global. Un **CSF** es un factor crítico de éxito: algo que tiene que funcionar para que la gestión de seguridad logre su objetivo.

## Criterios SMART para indicadores

Un buen indicador debe ser específico, medible, alcanzable, relevante y temporal. En este trabajo los indicadores se apoyan en CSV, fórmulas reproducibles y generación automática para evitar depender de edición manual.

## Tablero de control de seguridad

Es una herramienta para resumir, priorizar y comunicar el estado de seguridad. Debe permitir una lectura ejecutiva y también bajar al detalle de controles, brechas, evidencias y proyectos.

## CMMI 0 a 5

- **0 - Inexistente:** no hay práctica identificable.
- **1 - Inicial:** existe de forma informal o reactiva.
- **2 - Gestionado:** hay práctica repetible pero todavía limitada.
- **3 - Definido:** existe proceso documentado y consistente.
- **4 - Cuantitativo:** se mide y controla con indicadores.
- **5 - Optimizado:** se mejora de forma continua.

## Madurez, brecha y brecha ponderada

La **madurez** es el nivel actual normalizado. La **brecha** es la distancia hasta el objetivo. La **brecha ponderada** multiplica esa brecha por el peso del control, para que dos controles con igual nivel CMMI no tengan necesariamente la misma prioridad ejecutiva.

En TecnoHogar, la madurez global es **38.4%** y la brecha global es **61.6%**.

## ISO/IEC 27002:2022 capítulos 5, 6, 7 y 8

El tablero usa los cuatro capítulos evaluables del catálogo: **5 Organizativos**, **6 Personas**, **7 Físicos** y **8 Tecnológicos**. En total se evaluaron **93 controles**.

## CID

**Confidencialidad** protege contra acceso no autorizado. **Integridad** protege contra modificación incorrecta. **Disponibilidad** protege la continuidad de acceso y uso. En el TP1 se usó CID para activos; en el TP2 se usa también para leer controles asociados a esas propiedades.

## Riesgo, tratamiento y priorización

El diagnóstico muestra exposición o debilidad; el tratamiento define qué hacer. La priorización combina brecha, peso, esfuerzo, aporte esperado y plazo. Por eso el plan no se ordena solo por intuición.

## Pareto de brechas

El Pareto ordena controles por brecha ponderada y muestra el acumulado. Sirve para explicar qué controles concentran mayor impacto de mejora.

## Matriz impacto / esfuerzo

Cruza prioridad contra esfuerzo. El cuadrante de alto impacto y bajo esfuerzo contiene quick wins. Los proyectos de alto impacto y alto esfuerzo suelen ser estratégicos.

## Quick win

Un quick win no es una acción menor. Es una acción con buen retorno inicial: impacto alto y esfuerzo relativo bajo frente al resto de la cartera. TecnoHogar tiene **3 quick wins**.

## Trazabilidad control -> evidencia -> proyecto

La trazabilidad permite responder de dónde sale cada número y por qué existe cada proyecto. En la defensa, esta es la parte que muestra que el tablero es auditable y no una colección de gráficos sueltos.

## SGSI y mejora continua

Un SGSI busca gestionar seguridad de forma sistemática. El tablero puede ser usado como instrumento de mejora continua: medir, priorizar, ejecutar, revisar y ajustar.
