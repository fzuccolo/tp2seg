# ISO 27002:2022

Catalogo comun usado por los datasets del TP2.

## Archivos

- `catalogo_controles.csv`: 93 controles distribuidos en los 4 capitulos de ISO/IEC 27002:2022 trabajados en la materia.
- `parametros_madurez.csv`: escala CMMI de 0 a 5, normalizada a valores entre 0 y 1 para calcular porcentajes.

## Distribucion esperada

| Capitulo | Controles |
| --- | ---: |
| 5 - Controles Organizativos | 37 |
| 6 - Controles de Personas | 8 |
| 7 - Controles Físicos | 14 |
| 8 - Controles Tecnológicos | 34 |

## Columnas principales del catalogo

- Identificacion: `control_id`, `capitulo`, `control_nombre`, `control_descripcion`.
- Evaluacion: `pregunta`, `proposito`, `aplica`, `peso`.
- Tipo de control: `tipo_preventivo`, `tipo_detectivo`, `tipo_correctivo`.
- Propiedades CID: `prop_confidencialidad`, `prop_integridad`, `prop_disponibilidad`.
- Funciones de ciberseguridad: identificacion, proteccion, deteccion, respuesta y recuperacion.
- Capacidades operacionales: columnas `cap_*`.
- Dominios de seguridad: columnas `dom_*`.
- Plan de mejora de referencia: `tipo_seguridad`, `proyecto_sugerido`, `plazo_sugerido`.

## Fuente

El catalogo inicial se importa desde la hoja `Ctrl_Anexo` del archivo de referencia de la catedra `REF G1 - Metricas_ISO_27002_2022_Grupo2_FINAL.xlsx`. No se copia texto normativo oficial de ISO; el repo usa el material academico disponible para el TP.
