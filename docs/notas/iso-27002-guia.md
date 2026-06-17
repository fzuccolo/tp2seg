# Guía ISO/IEC 27002:2022 para la defensa

Esta guía resume lo que conviene saber de ISO/IEC 27002:2022 para defender el tablero. No reemplaza a la norma oficial: sirve para explicar qué es, qué parte usamos y cómo se tradujo en métricas, brechas y proyectos dentro del caso TecnoHogar. Para siglas y abreviaturas, usar `glosario-abreviaturas.md`.

## Qué tenés que poder decir en 30 segundos

ISO/IEC 27002:2022 es un catálogo de controles de seguridad de la información. En este TP la usamos como **estructura de referencia**: cada control se convirtió en una unidad evaluable, se le asignó una madurez CMMI, se calculó una brecha y se vinculó con proyectos de mejora. Para TecnoHogar se evaluaron los **93 controles** de los capítulos **5 Organizativos**, **6 Personas**, **7 Físicos** y **8 Tecnológicos**.

## ISO 27001 vs ISO 27002

- **ISO/IEC 27001** define requisitos para un SGSI y es la norma típica contra la que una organización puede certificarse.
- **ISO/IEC 27002** es una guía/catálogo de controles. No certifica por sí sola; ayuda a seleccionar, implementar e interpretar controles.
- En este trabajo no hacemos una certificación. Hacemos un **tablero de control** basado en controles ISO 27002, con medición de madurez y plan de mejora.

## Qué parte de ISO aplicamos

- Estándar del tablero: **iso27002_2022**.
- Caso principal: **TecnoHogar S.A.**.
- Controles evaluados: **93**.
- Capítulos evaluados: **4**.
- Unidad de análisis: cada control ISO es una métrica/control evaluable.
- Capa de medición agregada por nosotros: nivel Capability Maturity Model Integration (CMMI), madurez, brecha, peso, brecha ponderada, hallazgo, evidencia y proyecto asociado.
- Atributos usados para vistas transversales: tipo preventivo/detectivo/correctivo, confidencialidad, integridad y disponibilidad (CID), funciones de ciberseguridad, capacidades operacionales y dominios ejecutivos.

## Resumen por capítulo

| Capítulo | Controles | Madurez | Brecha | Qué representa |
| --- | ---: | ---: | ---: | --- |
| 5 - Controles Organizativos | 37 | 40.4% | 59.6% | gobierno, políticas, roles, activos, proveedores, incidentes, continuidad, cumplimiento y mejora. |
| 6 - Controles de Personas | 8 | 37.5% | 62.5% | ciclo de vida laboral, concientización, confidencialidad, trabajo remoto, desvinculación y reporte de eventos. |
| 7 - Controles Físicos | 14 | 39.3% | 60.7% | perímetros, ingresos, oficinas, salas, instalaciones, equipamiento, cableado, almacenamiento y mantenimiento. |
| 8 - Controles Tecnológicos | 34 | 36.5% | 63.5% | endpoints, accesos privilegiados, autenticación, malware, vulnerabilidades, configuración, backup, logs, redes, criptografía y desarrollo seguro. |

## Cómo defender cada capítulo

### 5 - Controles Organizativos

**Qué cubre:** gobierno, políticas, roles, activos, proveedores, incidentes, continuidad, cumplimiento y mejora.

**Qué aplicamos en TecnoHogar:** se usó para evaluar si TecnoHogar tiene responsabilidades claras, inventario y clasificación de información, gestión de accesos, relación con proveedores, preparación ante incidentes, continuidad y cumplimiento.

**Lectura del tablero:** 37 controles, madurez **40.4%** y brecha **59.6%**.

**Cómo explicarlo:** este capítulo explica la parte de gobierno del tablero: sin políticas, roles, activos y responsables, los controles técnicos quedan aislados.

**Controles concretos para tener presentes:**

- **5.7 - Inteligencia de amenazas:** madurez 5.0%, brecha ponderada 0.64. Hallazgo: Control inicial y reactivo; alta dependencia de personas y bajo respaldo documental.
- **5.24 - Planificación y preparación para la gestión de incidentes de SI:** madurez 5.0%, brecha ponderada 0.64. Hallazgo: Control inicial y reactivo; alta dependencia de personas y bajo respaldo documental.
- **5.27 - Aprendizaje de los incidentes de SI:** madurez 5.0%, brecha ponderada 0.64. Hallazgo: Control inicial y reactivo; alta dependencia de personas y bajo respaldo documental.
- **5.28 - Recolección de evidencia:** madurez 5.0%, brecha ponderada 0.64. Hallazgo: Control inicial y reactivo; alta dependencia de personas y bajo respaldo documental.
- **5.3 - Segregación de tareas:** madurez 15.0%, brecha ponderada 0.57. Hallazgo: Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo.

### 6 - Controles de Personas

**Qué cubre:** ciclo de vida laboral, concientización, confidencialidad, trabajo remoto, desvinculación y reporte de eventos.

**Qué aplicamos en TecnoHogar:** se usó para medir prácticas de Recursos Humanos (RRHH) y usuarios: verificación de antecedentes, términos de empleo, capacitación, acuerdos de confidencialidad, teletrabajo y canales de reporte.

**Lectura del tablero:** 8 controles, madurez **37.5%** y brecha **62.5%**.

**Cómo explicarlo:** este capítulo muestra que seguridad no es sólo tecnología; las personas pueden reducir o amplificar la exposición del negocio.

**Controles concretos para tener presentes:**

- **6.1 - Verificación de antecedentes (screening):** madurez 15.0%, brecha ponderada 2.66. Hallazgo: Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo.
- **6.3 - Concientización, educación y entrenamiento en SI:** madurez 15.0%, brecha ponderada 2.66. Hallazgo: Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo.
- **6.7 - Trabajo remoto:** madurez 15.0%, brecha ponderada 2.66. Hallazgo: Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo.
- **6.5 - Responsabilidades tras la desvinculación o cambio de empleo:** madurez 15.0%, brecha ponderada 2.66. Hallazgo: Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo.
- **6.4 - Proceso disciplinario:** madurez 60.0%, brecha ponderada 1.25. Hallazgo: Control definido, con oportunidad de medicion y cobertura transversal.

### 7 - Controles Físicos

**Qué cubre:** perímetros, ingresos, oficinas, salas, instalaciones, equipamiento, cableado, almacenamiento y mantenimiento.

**Qué aplicamos en TecnoHogar:** se usó para evaluar oficinas, depósito, centros de distribución, protección de equipos, control de ingreso físico, áreas seguras y soporte ambiental.

**Lectura del tablero:** 14 controles, madurez **39.3%** y brecha **60.7%**.

**Cómo explicarlo:** este capítulo conecta seguridad de la información con el mundo físico: si se comprometen equipos, medios o instalaciones, también se compromete la información.

**Controles concretos para tener presentes:**

- **7.5 - Protección contra amenazas físicas y ambientales:** madurez 15.0%, brecha ponderada 1.52. Hallazgo: Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo.
- **7.4 - Monitoreo de seguridad física:** madurez 15.0%, brecha ponderada 1.52. Hallazgo: Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo.
- **7.6 - Trabajo en áreas seguras:** madurez 15.0%, brecha ponderada 1.52. Hallazgo: Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo.
- **7.10 - Medios de almacenamiento:** madurez 15.0%, brecha ponderada 1.52. Hallazgo: Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo.
- **7.9 - Seguridad de los activos fuera de las instalaciones:** madurez 15.0%, brecha ponderada 1.52. Hallazgo: Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo.

### 8 - Controles Tecnológicos

**Qué cubre:** endpoints, accesos privilegiados, autenticación, malware, vulnerabilidades, configuración, backup, logs, redes, criptografía y desarrollo seguro.

**Qué aplicamos en TecnoHogar:** se usó para medir la postura técnica del e-commerce y la operación: hardening, gestión de identidades y accesos (IAM), autenticación multifactor (MFA), registros, monitoreo, vulnerabilidades, segregación de redes, ciclo de vida de desarrollo seguro (SDLC seguro) y protección de aplicaciones.

**Lectura del tablero:** 34 controles, madurez **36.5%** y brecha **63.5%**.

**Cómo explicarlo:** este capítulo concentra muchos controles operativos y por eso es clave para explicar brechas técnicas, monitoreo, vulnerabilidades y seguridad de aplicaciones.

**Controles concretos para tener presentes:**

- **8.2 - Derechos de acceso privilegiado:** madurez 5.0%, brecha ponderada 0.70. Hallazgo: Control inicial y reactivo; alta dependencia de personas y bajo respaldo documental.
- **8.8 - Gestión de vulnerabilidades técnicas:** madurez 5.0%, brecha ponderada 0.70. Hallazgo: Control inicial y reactivo; alta dependencia de personas y bajo respaldo documental.
- **8.16 - Monitoreo de actividades:** madurez 5.0%, brecha ponderada 0.70. Hallazgo: Control inicial y reactivo; alta dependencia de personas y bajo respaldo documental.
- **8.18 - Uso de programas utilitarios privilegiados:** madurez 5.0%, brecha ponderada 0.70. Hallazgo: Control inicial y reactivo; alta dependencia de personas y bajo respaldo documental.
- **8.12 - Prevención de fuga de datos:** madurez 5.0%, brecha ponderada 0.70. Hallazgo: Control inicial y reactivo; alta dependencia de personas y bajo respaldo documental.

## Controles que más tenés que saber explicar

Estos son los controles que aparecen arriba en el ranking de brecha ponderada. No son los únicos importantes, pero sí los más probables para preguntas porque justifican prioridades del plan.

| Control | Capítulo | Madurez | Brecha ponderada | Interpretación |
| --- | --- | ---: | ---: | --- |
| 6.1 - Verificación de antecedentes (screening) | 6 - Controles de Personas | 15.0% | 2.66 | Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo. |
| 6.3 - Concientización, educación y entrenamiento en SI | 6 - Controles de Personas | 15.0% | 2.66 | Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo. |
| 6.5 - Responsabilidades tras la desvinculación o cambio de empleo | 6 - Controles de Personas | 15.0% | 2.66 | Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo. |
| 6.7 - Trabajo remoto | 6 - Controles de Personas | 15.0% | 2.66 | Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo. |
| 7.4 - Monitoreo de seguridad física | 7 - Controles Físicos | 15.0% | 1.52 | Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo. |
| 7.5 - Protección contra amenazas físicas y ambientales | 7 - Controles Físicos | 15.0% | 1.52 | Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo. |
| 7.6 - Trabajo en áreas seguras | 7 - Controles Físicos | 15.0% | 1.52 | Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo. |
| 7.7 - Escritorio despejado y pantalla limpia | 7 - Controles Físicos | 15.0% | 1.52 | Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo. |
| 7.9 - Seguridad de los activos fuera de las instalaciones | 7 - Controles Físicos | 15.0% | 1.52 | Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo. |
| 7.10 - Medios de almacenamiento | 7 - Controles Físicos | 15.0% | 1.52 | Control gestionado de forma parcial; falta formalizacion, evidencia o alcance completo. |

## Cómo convertimos ISO en datos

1. **Catálogo:** `datos/estandares/iso27002_2022/catalogo_controles.csv` define los controles, capítulo, nombre, propósito, pregunta de evaluación, atributos, peso y mapeos auxiliares.
2. **Diagnóstico:** `datos/casos/tecnohogar/diagnostico.csv` asigna nivel Capability Maturity Model Integration (CMMI), hallazgo, observaciones, fuente y entrevistado por control.
3. **Métrica:** el motor calcula madurez, brecha y brecha ponderada.
4. **Plan:** `datos/casos/tecnohogar/proyectos.csv` define iniciativas, esfuerzo, plazo y aporte esperado.
5. **Trazabilidad:** `datos/casos/tecnohogar/proyecto_control.csv` vincula controles ISO con proyectos concretos.

## Cómo se relaciona ISO con CMMI

ISO 27002 aporta el catálogo y dice **qué controles mirar**. Capability Maturity Model Integration (CMMI) nos da una escala para expresar **qué tan maduro está cada control**. Por eso no decimos que ISO tenga niveles 0 a 5; esa escala la agregamos nosotros para transformar el catálogo en indicadores de tablero.

## Qué significa aplicar un control

En este tablero, aplicar un control no significa que TecnoHogar ya lo cumple. Significa que el control es relevante para el caso, fue incluido en el universo evaluado y recibió una medición de madurez. Después, si la madurez es baja, aparece como brecha y puede disparar un proyecto.

## Qué NO conviene decir

- No decir que ISO 27002 certifica a TecnoHogar.
- No decir que el tablero demuestra cumplimiento legal completo.
- No decir que CMMI es parte textual de ISO 27002.
- No decir que todos los controles tienen la misma importancia: por eso usamos peso y brecha ponderada.
- No recitar los 93 controles: conviene explicar estructura, capítulos, controles críticos y trazabilidad.

## Preguntas probables sobre ISO

**¿Por qué eligieron ISO 27002?**

Porque es un catálogo reconocido de controles de seguridad de la información y permite cubrir gobierno, personas, seguridad física y tecnología en una misma estructura.

**¿Evaluaron toda la norma?**

Para el tablero se evaluaron los 93 controles cargados de los capítulos 5 a 8 de ISO/IEC 27002:2022. Es el universo definido para este TP.

**¿Esto es una auditoría ISO?**

No. Es un diagnóstico académico/profesional basado en controles ISO. Una auditoría formal requeriría evidencia real validada, alcance aprobado, criterios de auditoría y posiblemente ISO 27001 si se busca certificación del SGSI.

**¿Por qué no muestran todos los controles en la presentación?**

Porque la presentación cuenta una historia ejecutiva. Los 93 controles están en el tablero y en la trazabilidad; las slides muestran los patrones y prioridades.

**¿Dónde se ve qué aplicaron de cada control?**

En el tablero: Mapa ISO muestra controles por capítulo, Brechas muestra los controles con mayor distancia, Trazabilidad conecta control con proyecto y Descargas permite bajar los CSV.

**¿Qué pasa si cambia el estándar o el caso?**

El repo separa estándar, caso, diagnóstico y proyectos. Para otro caso se cargan nuevos CSV con el mismo formato y se regeneran tablero, informe, slides y notas.

## Checklist de estudio antes de defender

- Saber explicar la diferencia entre ISO 27001 e ISO 27002.
- Saber nombrar los cuatro capítulos usados: 5 Organizativos, 6 Personas, 7 Físicos y 8 Tecnológicos.
- Saber decir que ISO aporta el catálogo y CMMI aporta la escala de madurez.
- Saber explicar por qué hay 93 controles y dónde se ven en el tablero.
- Saber conectar capítulo -> control -> hallazgo -> brecha -> proyecto.
- Saber defender que la brecha ponderada prioriza mejor que mirar sólo porcentaje de brecha.
- Saber decir que el tablero no certifica, pero sí ordena diagnóstico, priorización y seguimiento.
