# Conceptos clave

Esta nota está escrita para estudiar desde cero. La idea es entender primero la lógica general y después conectar cada concepto con el tablero de TecnoHogar.

Para siglas y abreviaturas, leer también `glosario-abreviaturas.md`.

## 1. Qué estamos tratando de proteger

La seguridad de la información busca proteger la información que una organización necesita para operar. En TecnoHogar eso incluye datos de clientes, ventas, e-commerce, inventario, proveedores, accesos, sistemas internos y continuidad del negocio.

La forma clásica de explicar esa protección es **CID**:

- **Confidencialidad:** que la información no sea vista por quien no corresponde.
- **Integridad:** que la información no sea modificada de forma indebida o accidental.
- **Disponibilidad:** que la información y los sistemas estén accesibles cuando el negocio los necesita.

En el TP1 usamos CID para entender activos. En el TP2 usamos controles ISO para medir qué tan protegida está esa información.

## 2. Qué es ISO/IEC 27002:2022 en este trabajo

**ISO/IEC 27002:2022** es un catálogo de controles de seguridad de la información. No lo usamos como certificación, sino como lista ordenada de cosas que conviene mirar.

La idea simple es:

1. ISO 27002 nos dice **qué controles evaluar**.
2. El caso TecnoHogar nos da contexto de negocio.
3. Nosotros asignamos un nivel de madurez a cada control.
4. El tablero calcula brechas, prioridades y proyectos.

Para TecnoHogar evaluamos **93 controles** de los capítulos:

- **5 - Organizativos:** gobierno, políticas, roles, proveedores, incidentes, continuidad y cumplimiento.
- **6 - Personas:** empleados, capacitación, confidencialidad, trabajo remoto y desvinculación.
- **7 - Físicos:** oficinas, accesos físicos, equipos, salas, instalaciones y soportes.
- **8 - Tecnológicos:** endpoints, accesos, redes, logs, vulnerabilidades, backup, criptografía y desarrollo seguro.

La explicación completa de ISO está en `iso-27002-guia.md`.

## 3. Qué es un control

Un **control** es una práctica, proceso, medida técnica o regla de gestión que ayuda a reducir una exposición de seguridad.

Ejemplos:

- Tener política de seguridad.
- Revisar accesos de usuarios.
- Hacer backups.
- Registrar eventos en logs.
- Capacitar a empleados.
- Proteger físicamente oficinas y equipos.

En el tablero, cada control ISO se convirtió en una unidad evaluable. Por eso cuando decimos “93 controles” estamos diciendo que medimos 93 puntos concretos del catálogo.

## 4. Qué significa madurez

La **madurez** responde esta pregunta: “qué tan instalado y controlado está este control en la organización”.

No alcanza con que algo exista de forma informal. Un control maduro debería estar definido, repetirse, tener responsables, evidencia, medición y mejora.

Usamos una escala tipo **CMMI** de 0 a 5:

- **0 - Inexistente:** no hay práctica identificable.
- **1 - Inicial:** existe algo informal o reactivo.
- **2 - Gestionado:** se hace de forma repetible, pero todavía limitada.
- **3 - Definido:** hay proceso documentado y más consistente.
- **4 - Cuantitativo:** se mide con indicadores.
- **5 - Optimizado:** se revisa y mejora de forma continua.

Importante para defender: CMMI no es “la ISO”. ISO nos da los controles; CMMI es la escala que usamos para medirlos.

## 5. Qué es una medida y qué es una métrica

Una **medida** es un dato base. Por ejemplo:

- nivel CMMI de un control;
- peso del control;
- cantidad de controles evaluados;
- esfuerzo estimado en jornadas;
- cantidad de proyectos.

Una **métrica** es un cálculo o lectura que se obtiene usando medidas. Por ejemplo:

- madurez global;
- brecha global;
- brecha ponderada;
- prioridad de proyecto;
- madurez por capítulo.

Ejemplo simple: si un control tiene nivel CMMI bajo, eso es una medida. Cuando calculamos cuánto falta para llegar al objetivo, eso ya es una métrica de brecha.

## 6. Qué es brecha

La **brecha** es la distancia entre la situación actual y el objetivo esperado.

En el tablero usamos esta idea:

- si un control está muy maduro, la brecha es baja;
- si un control está poco maduro, la brecha es alta.

En TecnoHogar, la madurez global es **38.4%** y la brecha global es **61.6%**.

Cómo explicarlo en voz alta:

“No estamos diciendo que TecnoHogar no tenga nada. Estamos diciendo que, frente a un objetivo optimizado, todavía falta formalización, medición y mejora continua”.

## 7. Qué es brecha ponderada

La **brecha ponderada** evita tratar todos los controles como si pesaran igual.

Dos controles pueden tener la misma brecha porcentual, pero no necesariamente tienen el mismo impacto para el diagnóstico. Por eso multiplicamos la brecha por un peso del control.

Idea simple:

```text
brecha ponderada = brecha * peso del control
```

Esto ayuda a ordenar prioridades. En vez de mirar solamente “qué control está peor”, miramos “qué control combina mala madurez con mayor peso relativo”.

## 8. Qué son KPI, KGI y CSF

Estas siglas aparecen mucho cuando se habla de métricas y tablero:

- **KPI - Key Performance Indicator:** indicador clave de desempeño. Sirve para seguir cómo viene la gestión. Ejemplo: brecha por capítulo o avance de proyectos.
- **KGI - Key Goal Indicator:** indicador clave de resultado. Sirve para ver si se alcanzó un objetivo. Ejemplo: madurez global.
- **CSF - Critical Success Factor:** factor crítico de éxito. Es algo que debe funcionar para que el objetivo se cumpla. Ejemplo: que haya responsables definidos para sostener el plan.

Forma fácil de recordarlo:

- KPI mira el camino.
- KGI mira el resultado.
- CSF marca condiciones necesarias para que el camino funcione.

## 9. Qué significa SMART

SMART es una regla práctica para armar buenos indicadores:

- **Specific - específico:** debe decir claramente qué mide.
- **Measurable - medible:** debe poder calcularse.
- **Achievable - alcanzable:** debe ser realista.
- **Relevant - relevante:** debe importar para la gestión.
- **Time-bound - temporal:** debe poder revisarse en un período.

En este repo intentamos que los indicadores sean defendibles porque salen de CSV, fórmulas y generación automática, no de celdas editadas a mano.

## 10. Qué es un tablero de control de seguridad

Un **tablero de control de seguridad** sirve para convertir muchos datos técnicos en una lectura útil para decidir.

Debe permitir dos movimientos:

1. **Subir a una lectura ejecutiva:** madurez global, brecha global, quick wins, plan.
2. **Bajar al detalle:** capítulo, control, hallazgo, evidencia, proyecto y trazabilidad.

Por eso el tablero no es solamente “gráficos lindos”. Es una herramienta para gobernar seguridad: mirar estado, priorizar, ejecutar y volver a medir.

## 11. Qué es riesgo

El **riesgo** aparece cuando hay algo valioso que puede verse afectado por una amenaza aprovechando una debilidad.

En forma simple:

```text
activo importante + amenaza + vulnerabilidad = riesgo
```

El tablero no calcula riesgo formal con probabilidad e impacto monetario. Lo que hace es mostrar señales de exposición: controles débiles, brechas ponderadas y capacidades poco maduras.

Esa lectura ayuda a decidir tratamientos.

## 12. Qué es tratamiento de riesgo

El **tratamiento** es qué hacemos frente a un riesgo o debilidad.

Opciones típicas:

- **Reducir:** implementar controles o mejorar procesos.
- **Transferir:** pasar parte del impacto a un tercero, por ejemplo seguro o contrato.
- **Aceptar:** asumir el riesgo si está dentro del apetito de la organización.
- **Evitar:** dejar de hacer la actividad que genera el riesgo.

En nuestro TP, el foco está en **reducir** brechas mediante proyectos de mejora.

## 13. Qué es Pareto de brechas

El **Pareto** ordena los controles que más explican la brecha ponderada.

Sirve para responder:

“Si no puedo mejorar todo al mismo tiempo, ¿por dónde empiezo?”

En el gráfico, las barras muestran brecha ponderada y la línea muestra acumulado. La idea es encontrar los controles que más aportan al problema total.

## 14. Qué es matriz impacto / esfuerzo

La matriz impacto / esfuerzo ayuda a priorizar proyectos.

- Alto impacto y bajo esfuerzo: **quick win**.
- Alto impacto y alto esfuerzo: proyecto estratégico.
- Bajo impacto y bajo esfuerzo: mejora táctica.
- Bajo impacto y alto esfuerzo: diferir o revisar.

Esto evita que el plan sea una lista arbitraria. Ordena acciones según valor esperado y capacidad de ejecución.

## 15. Qué es un quick win

Un **quick win** no es una acción menor ni cosmética. Es una acción con buen retorno inicial: aporta mucho frente al esfuerzo relativo que requiere.

TecnoHogar tiene **3 quick wins**.

Cómo explicarlo:

“Elegimos quick wins para mostrar avance temprano y reducir brechas visibles, pero el plan también incluye proyectos más estructurales”.

## 16. Qué es trazabilidad

La **trazabilidad** es poder seguir el camino completo de una decisión.

En el tablero, la cadena es:

```text
control ISO -> evidencia/hallazgo -> madurez -> brecha -> proyecto
```

Esto es clave para defender el trabajo. Si el profesor pregunta “¿por qué existe este proyecto?”, la respuesta no debería ser “porque nos pareció”. Debería ser: “porque cubre estos controles, que tienen estas brechas, con estos hallazgos”.

## 17. Qué es SGSI

**SGSI** significa Sistema de Gestión de Seguridad de la Información.

Es una forma organizada de gestionar seguridad: definir alcance, políticas, responsables, controles, medición, revisión y mejora.

El tablero no implementa un SGSI completo, pero sí ayuda a operar una lógica de SGSI:

1. medir estado actual;
2. detectar brechas;
3. priorizar acciones;
4. ejecutar mejoras;
5. volver a medir.

## 18. Cómo contar todo junto en la defensa

Una forma simple de explicarlo:

“Tomamos el contexto de TecnoHogar y usamos ISO/IEC 27002:2022 como catálogo de controles. A cada control le asignamos una madurez CMMI. Con eso calculamos brechas y brechas ponderadas. Luego vinculamos esas brechas con proyectos de mejora. El tablero permite ver el resumen ejecutivo, bajar al detalle por control y justificar el plan con trazabilidad”.

## 19. Frases cortas para responder preguntas

- **ISO 27002 no certifica:** nos da un catálogo de controles.
- **CMMI no es la ISO:** es la escala que usamos para medir madurez.
- **Brecha no significa ausencia total:** significa distancia al objetivo.
- **Brecha ponderada prioriza mejor:** combina distancia y peso del control.
- **Quick win no es algo menor:** es alto impacto con esfuerzo relativo bajo.
- **El tablero no es sólo visual:** sirve para gobernar, priorizar y seguir mejoras.
- **La trazabilidad defiende el plan:** cada proyecto se conecta con controles y hallazgos.
