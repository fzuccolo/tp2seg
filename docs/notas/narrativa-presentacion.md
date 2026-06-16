# Narrativa de presentación

Esta guía es el guion de defensa para presentar la PPTX y hacer la demo del tablero. La idea no es memorizar palabra por palabra, sino entender el hilo: **TP1 -> medición ISO -> diagnóstico -> brechas -> plan -> trazabilidad**.

## Slide 1: Carátula

**Mensaje principal:** Presentar el trabajo como un tablero de gobierno: inventario, diagnóstico, brechas y plan.

**Narrativa oral:** Abrir diciendo que no se va a mostrar una planilla sino una forma de convertir el relevamiento del TP1 en decisiones de seguridad. El relato completo es: primero entendimos el contexto operativo, después medimos controles ISO, luego identificamos brechas y finalmente armamos un plan trazable.

**Datos concretos:**

- Caso: TecnoHogar S.A.
- Estándar: ISO/IEC 27002:2022.
- Entrega: TP2 Seguridad Informática, Grupo 1.

**Puente a la siguiente slide:** Pasar al resumen ejecutivo: ahora mostramos la foto consolidada del diagnóstico.

**Preguntas esperables:**

- **P:** ¿Qué aporta el tablero frente a una planilla?
  **R:** El tablero permite leer la postura desde dirección y bajar hasta control, evidencia y proyecto sin perder trazabilidad.

**Referencias para tener a mano:**

- **Tablero de control**: instrumento para seguimiento, priorización y comunicación de indicadores.
- **ISO/IEC 27002:2022**: catálogo de controles de seguridad de la información.

## Slide 2: Resumen ejecutivo

**Mensaje principal:** La postura actual es media-baja: hay base operativa, pero falta formalización, medición y mejora continua.

**Narrativa oral:** El mensaje central es 38.4% de madurez y 61.6% de brecha. No significa que todo esté mal; significa que TecnoHogar tiene prácticas en marcha, pero todavía no están suficientemente definidas, medidas y gobernadas como para hablar de una postura optimizada.

**Datos concretos:**

- Madurez global: 38.4%.
- Brecha global: 61.6%.
- Controles evaluados: 93.
- Iniciativas: 11.
- Quick wins: 3.
- Esfuerzo total estimado: 604 jornadas.

**Puente a la siguiente slide:** Explicar el alcance: para que esos números sean defendibles, hay que mostrar qué se midió y con qué base.

**Preguntas esperables:**

- **P:** ¿Por qué confiar en un porcentaje global?
  **R:** Porque es una síntesis ejecutiva. El tablero lo descompone por capítulo, nivel CMMI, control, brecha y proyecto.
- **P:** ¿La brecha global es riesgo real?
  **R:** Es una señal de exposición y madurez pendiente. Para convertirla en riesgo operativo se cruza con activos, procesos, evidencia y prioridades.

**Referencias para tener a mano:**

- **KGI**: indicador de resultado que expresa si se alcanza un objetivo.
- **Brecha**: distancia entre el estado actual y el objetivo de madurez.

## Slide 3: Alcance y modelo de datos

**Mensaje principal:** El TP2 continúa el TP1: usa contexto, activos y responsables para medir controles y construir decisiones.

**Narrativa oral:** Remarcar que el diagnóstico no aparece de la nada. El punto de partida es el inventario y la lectura de negocio del TP1. Sobre esa base se cargan controles, niveles CMMI, hallazgos, proyectos y vínculos control-proyecto. Lo importante es separar datos observados, datos definidos para el caso y métricas derivadas.

**Datos concretos:**

- Capítulo 5: 37 controles organizativos.
- Capítulo 6: 8 controles de personas.
- Capítulo 7: 14 controles físicos.
- Capítulo 8: 34 controles tecnológicos.
- Total evaluado: 93 controles.

**Puente a la siguiente slide:** Pasar al método: una vez definido el alcance, mostramos cómo se convierte cada control en una métrica.

**Preguntas esperables:**

- **P:** ¿Los 93 controles son todos los capítulos evaluables?
  **R:** Sí. Para este tablero se trabajaron los capítulos 5, 6, 7 y 8 de ISO/IEC 27002:2022.
- **P:** ¿Qué datos son simulados?
  **R:** El caso toma el contexto de TecnoHogar del TP1 y define niveles, hallazgos y proyectos para completar el diagnóstico del TP2.

**Referencias para tener a mano:**

- **CID**: confidencialidad, integridad y disponibilidad.
- **Trazabilidad**: vínculo entre dato de entrada, control, métrica y decisión.

## Slide 4: Método de medición

**Mensaje principal:** Cada número sale de una cadena defendible: control ISO, evidencia, nivel CMMI, brecha y proyecto.

**Narrativa oral:** Esta slide es clave para responder preguntas. Hay que explicar que no se inventa un gráfico aislado: cada control tiene una evaluación de madurez, esa madurez se normaliza, se calcula una brecha, se pondera por peso del control y luego se vincula con iniciativas de mejora.

**Datos concretos:**

- Escala CMMI usada: 0 a 5.
- Madurez normalizada: nivel actual convertido a valor entre 0 y 1.
- Brecha: 1 menos madurez.
- Brecha ponderada: brecha multiplicada por peso del control.
- Prioridad de proyecto: brecha asociada y aporte esperado.

**Puente a la siguiente slide:** Pasar a resultados por capítulo: con el método claro, vemos dónde está más débil TecnoHogar.

**Preguntas esperables:**

- **P:** ¿Por qué CMMI?
  **R:** Porque permite expresar madurez de procesos y controles en una escala simple y comparable.
- **P:** ¿Brecha ponderada es lo mismo que brecha porcentual?
  **R:** No. La brecha porcentual sale del nivel CMMI; la ponderada incorpora el peso relativo del control.

**Referencias para tener a mano:**

- **Medida**: dato observado o asignado.
- **Métrica**: cálculo o interpretación sobre medidas.
- **KPI**: indicador para seguimiento de desempeño.

## Slide 5: Madurez por capítulo ISO

**Mensaje principal:** La brecha es generalizada, pero tecnología y personas requieren atención temprana.

**Narrativa oral:** Mostrar primero el capítulo más débil: 8 - Controles Tecnológicos con 36.5% de madurez. Luego aclarar que el capítulo más fuerte, 5 - Controles Organizativos con 40.4%, también está lejos de optimizado. La lectura es de madurez media-baja, no de un único problema aislado.

**Datos concretos:**

- Más débil: 8 - Controles Tecnológicos (36.5%).
- Más fuerte: 5 - Controles Organizativos (40.4%).
- Brecha global: 61.6%.

**Puente a la siguiente slide:** Pasar a la distribución CMMI para mostrar si el promedio sale de pocos controles o de muchos niveles bajos.

**Preguntas esperables:**

- **P:** ¿El capítulo más débil define solo el plan?
  **R:** No. Define una alerta. El plan final combina capítulo, brecha ponderada, capacidad, esfuerzo y proyecto.

**Referencias para tener a mano:**

- **Capítulo ISO**: agrupación del catálogo de controles.
- **Madurez promedio ponderada**: promedio que considera peso de controles.

## Slide 6: Distribución CMMI

**Mensaje principal:** El promedio global se explica por muchos controles en niveles iniciales o gestionados parcialmente.

**Narrativa oral:** Explicar que la distribución muestra la forma del diagnóstico. 45 controles están en niveles 0 a 2, mientras que 6 controles llegan a niveles 4 o 5. Esto respalda la idea de que hay prácticas, pero todavía falta medición formal y mejora sistemática.

**Datos concretos:**

- Controles en CMMI 0 a 2: 45.
- Controles en CMMI 4 a 5: 6.
- Total: 93 controles.

**Puente a la siguiente slide:** Pasar a brechas: después de entender niveles de madurez, corresponde ordenar qué controles pesan más.

**Preguntas esperables:**

- **P:** ¿Por qué varios controles pueden tener la misma brecha?
  **R:** Porque tienen el mismo nivel CMMI. La diferencia ejecutiva aparece al ponderar por peso del control.

**Referencias para tener a mano:**

- **CMMI 0..5**: inexistente, inicial, gestionado, definido, cuantitativo y optimizado.
- **Optimizado**: control medido, gestionado y mejorado de forma continua.

## Slide 7: Brechas principales

**Mensaje principal:** La priorización se hace por brecha ponderada, no por intuición ni por orden del estándar.

**Narrativa oral:** Mostrar el primer control del ranking: 6.1 - Verificación de antecedentes (screening), con brecha ponderada 2.66. Aclarar que el Pareto ayuda a decidir por dónde empezar, porque un mismo 85% de brecha no pesa igual si el control tiene distinto peso o distinta relación con proyectos.

**Datos concretos:**

- Control crítico: 6.1.
- Brecha ponderada máxima: 2.66.
- Capítulo asociado: 6 - Controles de Personas.

**Puente a la siguiente slide:** Pasar al perfil operacional: ya sabemos qué controles pesan más; ahora vemos qué capacidades de gestión están afectadas.

**Preguntas esperables:**

- **P:** ¿Por qué usar Pareto?
  **R:** Porque permite concentrar la discusión en los controles que más explican la brecha total.
- **P:** ¿La brecha ponderada reemplaza al juicio profesional?
  **R:** No. Ordena la conversación; después se valida con contexto, esfuerzo y dependencias.

**Referencias para tener a mano:**

- **Pareto**: técnica para encontrar los factores que concentran mayor impacto.
- **Peso del control**: importancia relativa asignada para priorizar.

## Slide 8: Perfil de seguridad

**Mensaje principal:** El tablero traduce controles ISO a capacidades operacionales que se pueden gestionar.

**Narrativa oral:** Explicar que las capacidades ayudan a pasar del lenguaje del estándar al lenguaje de gestión. En TecnoHogar, la capacidad más débil es Amenazas y vulnerabilidades con 5.0%. Esa lectura justifica proyectos de vulnerabilidades, monitoreo, hardening, accesos o gobierno, según corresponda.

**Datos concretos:**

- Capacidad más débil: Amenazas y vulnerabilidades.
- Madurez de esa capacidad: 5.0%.
- Función más débil: Recuperacion.

**Puente a la siguiente slide:** Pasar al plan: si las capacidades muestran dónde duele, el plan muestra cómo se corrige.

**Preguntas esperables:**

- **P:** ¿Las capacidades son capítulos de ISO?
  **R:** No. Son una vista operacional construida para interpretar los controles y orientar decisiones.

**Referencias para tener a mano:**

- **Capacidad operacional**: conjunto de controles que expresan una práctica gestionable.
- **Perfil de seguridad**: lectura transversal de fortalezas y debilidades.

## Slide 9: Plan de acción priorizado

**Mensaje principal:** El diagnóstico se convierte en una cartera de iniciativas con impacto, esfuerzo, plazo y trazabilidad.

**Narrativa oral:** Mostrar que el plan no es una lista genérica. Tiene 11 iniciativas, 3 quick wins y 604 jornadas. La prioridad más alta es PR-10 - Concientizacion y ciclo de vida RRHH. También se puede mencionar el primer quick win: PR-10 - Concientizacion y ciclo de vida RRHH.

**Datos concretos:**

- Iniciativas: 11.
- Quick wins: 3.
- Esfuerzo total: 604 jornadas.
- Proyecto prioritario: PR-10 - Concientizacion y ciclo de vida RRHH.

**Puente a la siguiente slide:** Pasar a la demo: ahora que el plan está claro, mostramos cómo navegar el tablero publicado.

**Preguntas esperables:**

- **P:** ¿Quick win significa poco importante?
  **R:** No. Significa alto impacto con esfuerzo relativo bajo frente al resto de la cartera.
- **P:** ¿Las jornadas son presupuesto final?
  **R:** No. Son una estimación de planificación para comparar esfuerzo y secuenciar trabajo.

**Referencias para tener a mano:**

- **Matriz impacto/esfuerzo**: prioriza iniciativas por retorno relativo.
- **Tratamiento de riesgo**: acciones para reducir, transferir, aceptar o evitar exposición.

## Slide 10: Tablero publicado

**Mensaje principal:** La demo debe mostrar una historia: Ejecutivo, Mapa ISO, Brechas, Plan y Trazabilidad.

**Narrativa oral:** No navegar libremente. Hacer una demo corta y dirigida: primero la foto ejecutiva, después el mapa ISO para demostrar cobertura, luego brechas para justificar prioridades, plan para explicar acciones y trazabilidad para cerrar la defensa técnica.

**Datos concretos:**

- URL: https://tp2seg.streamlit.app/
- Ruta sugerida: Ejecutivo -> Mapa ISO -> Brechas -> Plan -> Trazabilidad.
- Plan B: PPTX más screenshots de docs/notas si Streamlit pide login o falla.

**Puente a la siguiente slide:** Pasar al cierre: después de mostrar la herramienta, remarcar el valor de gobierno y mejora continua.

**Preguntas esperables:**

- **P:** ¿Qué mostrar si hay poco tiempo?
  **R:** Ejecutivo, Pareto de brechas, matriz impacto/esfuerzo y Sankey de trazabilidad.
- **P:** ¿Qué pasa si Streamlit falla?
  **R:** Usar la PPTX y la guía de gráficos generada con screenshots reales del tablero.

**Referencias para tener a mano:**

- **Demo en vivo**: validación de que el tablero es navegable y no solo un entregable estático.
- **CI/CD**: generación reproducible de tablero, informe y presentación.

## Slide 11: Conclusiones y próximos pasos

**Mensaje principal:** El tablero es un instrumento de gobierno de seguridad, no solo una visualización.

**Narrativa oral:** Cerrar con tres ideas: el diagnóstico es trazable, el plan está priorizado y el tablero permite seguimiento periódico. La conclusión profesional es aprobar quick wins, formalizar responsables, medir avances y usar la misma estructura para futuras iteraciones.

**Datos concretos:**

- Controles evaluados: 93.
- Iniciativas priorizadas: 11.
- Esfuerzo estimado: 604 jornadas.
- Salida esperada: ciclo de medición y mejora continua.

**Puente a la siguiente slide:** Cerrar invitando preguntas sobre método, gráficos o trazabilidad de proyectos.

**Preguntas esperables:**

- **P:** ¿Qué harían después de aprobar el plan?
  **R:** Validar evidencias reales, asignar responsables, definir periodicidad de medición y controlar avance por tablero.

**Referencias para tener a mano:**

- **SGSI**: sistema de gestión de seguridad de la información.
- **Mejora continua**: medir, ejecutar, revisar y ajustar el plan de seguridad.
