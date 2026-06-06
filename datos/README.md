# Datos

Esta carpeta contiene las fuentes del tablero, del informe y de la presentacion. Primero definimos el estandar comun, despues definimos un caso concreto, y finalmente el motor calcula metricas, graficos y entregables.

El objetivo es evitar cargar celdas a mano. Los CSV/YAML son la fuente visible del trabajo y los scripts explican como se generan o actualizan.

## 1. Estandar

Solo usamos `iso27002_2022`. Es el catalogo de controles contra el que se evalua cualquier caso.

`catalogo_controles.csv` contiene los 93 controles de ISO/IEC 27002:2022 que se trabajan en la materia:

| Capitulo | Controles |
| --- | ---: |
| 5 - Controles Organizativos | 37 |
| 6 - Controles de Personas | 8 |
| 7 - Controles Fisicos | 14 |
| 8 - Controles Tecnologicos | 34 |

Para cada control se guarda lo necesario para calcular y graficar:

- `control_id`, `capitulo`, `control_nombre`: identifican el control.
- `pregunta` y `proposito`: ayudan a entender que se evalua.
- `peso`: importancia relativa para calcular brecha ponderada.
- columnas de tipo de control: preventivo, detectivo, correctivo.
- columnas CID: confidencialidad, integridad, disponibilidad.
- columnas de funcion: identificacion, proteccion, deteccion, respuesta, recuperacion.
- capacidades y dominios: se usan para graficos de perfil y mapa ISO.
- proyecto/plazo sugerido: referencia para armar el plan de mejora.

El repositorio usa `catalogo_controles.csv` como version operativa del estandar para el TP. No incluye la norma ISO completa; solo el catalogo necesario para evaluar, calcular metricas y presentar resultados.

`parametros_madurez.csv` define como se traduce la madurez CMMI a numero:

| Nivel | Lectura simple | Valor |
| ---: | --- | ---: |
| 0 | No existe evidencia | 0.00 |
| 1 | Practica inicial o reactiva | 0.05 |
| 2 | Gestion parcial | 0.15 |
| 3 | Definido/documentado | 0.60 |
| 4 | Medido con indicadores | 0.85 |
| 5 | Optimizado/mejora continua | 1.00 |

Ese valor es el que usa el tablero para calcular madurez, brecha y prioridades.

## 2. Caso

Un caso es una organizacion, escenario o dataset evaluable. Puede ser una empresa real, una empresa ficticia, un organismo, una unidad de negocio o un caso de practica.

Cada caso vive en `datos/casos/<caso_id>/`.

`caso.yml` define el contexto minimo:

- `id`: identificador usado por scripts y tablero.
- `nombre`: nombre visible en tablero, informe y slides.
- `descripcion`: alcance resumido.
- `industria`: contexto del caso.
- `estandar`: para este TP debe ser `iso27002_2022`.

Este archivo no calcula nada. Sirve para dejar claro que se esta evaluando.

## 3. Activos

`activos.csv` define sobre que realidad operativa se interpreta la seguridad. Sin activos, el diagnostico ISO queda demasiado abstracto.

Campos principales:

- `activo_id`: codigo estable del activo.
- `tipo`: proceso, informacion, aplicacion, servidor u otra categoria.
- `nombre`: nombre visible.
- `criticidad_cid`: criticidad usada por el tablero.
- `propietario`, `custodio`, `area`: responsables.
- `proceso`: proceso de negocio asociado.
- `confidencialidad`, `integridad`, `disponibilidad`: valores CID cuando aplican.

Uso en el tablero:

- da contexto a la postura de seguridad;
- permite explicar por que ciertos controles importan mas;
- ayuda a justificar proyectos y prioridades.

## 4. Entrevistas

`entrevistas.csv` registra las fuentes humanas o roles usados para justificar la evidencia.

Campos principales:

- `entrevista_id`
- `nombre`
- `area`
- `empresa`
- `cargo`
- `fecha`
- `fuente`

No intenta ser una transcripcion. Su funcion es que cada evidencia tenga una fuente defendible.

## 5. Diagnostico

`diagnostico.csv` es el archivo central. Tiene una fila por control ISO evaluado. Para este TP deben ser 93 filas por caso.

Campos principales:

- `control_id`: se cruza con `catalogo_controles.csv`.
- `nivel_madurez`: nivel CMMI 0..5 asignado por el grupo.
- `valor`: valor numerico normalizado del nivel.
- `evidencia`: que se observo.
- `hallazgo`: lectura ejecutiva del problema o estado.
- `observaciones`: que falta mejorar.
- `entrevistado`: referente o rol asociado a la evidencia.
- `fuente`: referencia corta del origen o contexto de la evidencia cuando aplica.
- `fecha`: fecha de corte.
- `objetivo_negocio`: para explicar por que importa.
- `interpretacion`: texto de apoyo para defender el grafico.

Regla practica para asignar niveles:

- 0: no hay evidencia.
- 1: existe algo informal o reactivo.
- 2: hay gestion parcial, pero incompleta.
- 3: esta definido y documentado.
- 4: se mide con indicadores o revision periodica.
- 5: se mejora sistematicamente.

Para defender un numero hay que poder responder: que vimos, que falta, quien lo informo y por que ese nivel es razonable.

## 6. Proyectos

`proyectos.csv` convierte brechas en acciones.

Campos principales:

- `proyecto_id`
- `titulo`
- `plazo`
- `esfuerzo_jornadas`
- `aporte_seguridad`
- `descripcion`
- `dependencias`
- `tipo_seguridad`

Algunos valores son decisiones del grupo. Por ejemplo, esfuerzo, plazo y aporte de seguridad no salen automaticamente de los activos: se estiman segun brecha, impacto, criticidad y dependencia entre iniciativas.

Uso en el tablero:

- priorizacion esfuerzo/impacto;
- roadmap;
- quick wins;
- costo y esfuerzo acumulado.

## 7. Relacion proyecto-control

`proyecto_control.csv` une proyectos con controles ISO.

Campos:

- `proyecto_id`
- `control_id`

Esta relacion es clave. Si un control debil no tiene proyecto asociado, el plan queda incompleto. Si un proyecto no mejora controles con brecha, queda dificil de justificar.

## 8. Caso: TecnoHogar

TecnoHogar es el caso principal del TP2 y esta basado en el TP1.

La informacion del caso esta definida en los CSV de `datos/casos/tecnohogar/`. Para otros casos, esos CSV podrian salir de otra fuente o cargarse manualmente. Lo importante es que el tablero consume siempre la misma estructura.

`activos.csv` contiene el inventario operativo del caso: procesos, activos de informacion, aplicaciones, servidores, responsables, criticidad y valores CID cuando aplican.

`entrevistas.csv` contiene los roles usados como fuente de evidencia para el diagnostico.

`diagnostico.csv` contiene la evaluacion de los 93 controles ISO: nivel de madurez, evidencia, hallazgo, observaciones, fuente y lectura de negocio.

`proyectos.csv` contiene la cartera de mejora propuesta para cerrar brechas: titulo, plazo, esfuerzo, aporte de seguridad, dependencias y tipo de seguridad.

`proyecto_control.csv` conecta cada proyecto con los controles ISO que ayuda a mejorar.

## 9. Como leer los graficos

- Ejecutivo: resume madurez, brecha, control critico, capacidad debil y quick wins.
- Mapa ISO: muestra los cuatro capitulos y la distribucion CMMI de los 93 controles.
- Perfil: agrupa controles por funciones, dominios, CID, tipo y capacidades.
- Brechas: ordena controles por brecha ponderada.
- Plan: muestra proyectos, esfuerzo, prioridad y roadmap.
- Trazabilidad: conecta capitulo, control, proyecto y evidencia.
