# Datos

Esta carpeta contiene las fuentes versionadas del tablero, el informe y la
presentacion. La regla del proyecto es que las salidas se puedan regenerar desde
CSV/YAML y scripts, sin completar celdas manualmente en Excel.

El objetivo no es solo "tener numeros": cada dato debe poder explicarse. Para
eso se separan tres tipos de informacion:

- Datos observados: salen del TP1, de entrevistas, de inventarios o de material
  provisto por la catedra.
- Datos derivados: se calculan automaticamente desde otros datos versionados.
- Datos definidos por el grupo: son criterios de evaluacion, priorizacion o
  estimacion. Tienen que quedar explicitados en el script generador, en el
  README de la empresa o en el informe.

## Estructura

```text
datos/
  estandares/
    iso27002_2022/
      catalogo_controles.csv
      parametros_madurez.csv
  empresas/
    ejemplo/
      empresa.yml
      activos.csv
      entrevistas.csv
      diagnostico.csv
      proyectos.csv
      proyecto_control.csv
    tecnohogar/
      empresa.yml
      activos.csv
      entrevistas.csv
      diagnostico.csv
      proyectos.csv
      proyecto_control.csv
```

Cada empresa vive en su propia carpeta. Eso permite desplegar el mismo tablero
con distintos datasets sin mezclar evidencia, supuestos ni entregables.

## Capa 1: estandar comun

`datos/estandares/iso27002_2022/catalogo_controles.csv` es el catalogo comun de
controles ISO/IEC 27002:2022 usado por todas las empresas.

Contiene los 93 controles de los capitulos evaluables:

| Capitulo | Controles |
| --- | ---: |
| 5 - Controles Organizativos | 37 |
| 6 - Controles de Personas | 8 |
| 7 - Controles Fisicos | 14 |
| 8 - Controles Tecnologicos | 34 |

El catalogo incluye:

- Identificacion del control: `control_id`, `capitulo`, `control_nombre`.
- Pregunta/proposito usados para evaluar el control.
- Peso relativo del control dentro del tablero: `peso`.
- Tipo de control: preventivo, detectivo, correctivo.
- Propiedades CID: confidencialidad, integridad, disponibilidad.
- Funciones de ciberseguridad: identificacion, proteccion, deteccion, respuesta
  y recuperacion.
- Capacidades operacionales y dominios de seguridad usados para agrupar
  graficos.
- Proyecto/plazo sugerido desde el material de referencia.

Fuente: se importa desde el ejemplo de la catedra
`REF G1 - Metricas_ISO_27002_2022_Grupo2_FINAL.xlsx`. No se descarga ni copia la
norma oficial ISO completa; el repo trabaja con el material academico disponible
para el TP.

`parametros_madurez.csv` define la escala CMMI usada para transformar niveles
0..5 en valores numericos:

| Nivel | Nombre | Valor |
| ---: | --- | ---: |
| 0 | Inexistente | 0.00 |
| 1 | Inicial | 0.05 |
| 2 | Gestionado | 0.15 |
| 3 | Definido | 0.60 |
| 4 | Cuantitativo | 0.85 |
| 5 | Optimizado | 1.00 |

## Capa 2: metadata de empresa

Cada empresa tiene un `empresa.yml` con datos de contexto:

- Nombre de la empresa/caso.
- Estandar usado.
- Descripcion del alcance.
- Metadata que aparece en tablero, informe y slides.

Este archivo no calcula metricas, pero fija el contexto. Si cambia el alcance,
tambien debe revisarse el diagnostico porque no todos los controles se
interpretan igual para todas las organizaciones.

## Capa 3: activos

`activos.csv` representa el alcance operativo sobre el que se evalua seguridad.
Para TecnoHogar se genera desde el Excel del TP1:

```text
Entregas/TP1/TP1_Inventario_TecnoHogar_v2.xlsx
```

Datos observados desde TP1:

- `activo_id`
- `tipo`
- `nombre`
- `capa`
- `nivel_evo`
- `detalle`
- `descripcion`
- `propietario`
- `custodio`
- `area`
- `padre_principal`
- `origen`
- valores CID para activos de informacion cuando estan relevados
- justificacion CID y marco aplicable

Datos derivados:

- `criticidad_cid`: para activos de informacion sale del TP1; para procesos,
  aplicaciones y servidores se hereda desde activos relacionados.
- `proceso`: se infiere recorriendo relaciones padre/hijo hasta el proceso de
  negocio principal.

Datos definidos por el grupo:

- No deberia haber datos definidos manualmente dentro de `activos.csv` salvo que
  se agregue una fuente nueva de relevamiento. Si se modifica un activo, lo
  correcto es ajustar el TP1 fuente o documentar la excepcion en el README de la
  empresa.

## Capa 4: entrevistas

`entrevistas.csv` registra las personas usadas como fuente de evidencia.

Datos observados:

- Nombres, areas y responsabilidades salen del caso TP1 o de la narrativa del
  relevamiento.

Datos definidos por el grupo:

- `entrevista_id`
- fecha de corte del relevamiento
- asignacion de cada responsable como fuente principal para un conjunto de
  controles

Este archivo no pretende simular entrevistas completas. Su funcion es hacer
trazable de donde sale la evidencia usada en `diagnostico.csv`.

## Capa 5: diagnostico ISO

`diagnostico.csv` es el archivo central del TP2. Debe tener una fila por control
ISO aplicable. Para TecnoHogar son 93 filas.

Datos que vienen del catalogo comun:

- `control_id`
- capitulo, nombre, pregunta, peso y atributos del control se agregan en runtime
  al unir `diagnostico.csv` con `catalogo_controles.csv`.

Datos definidos por evaluacion del grupo:

- `nivel_madurez`: nivel CMMI 0..5 asignado al estado actual del control.
- `evidencia`: razon concreta que justifica el nivel.
- `hallazgo`: lectura ejecutiva de la situacion del control.
- `observaciones`: que falta o que deberia fortalecerse.
- `entrevistado`: fuente principal de la evidencia.
- `fecha`: fecha de corte del diagnostico.
- `objetivo_negocio`: objetivo que ayuda a interpretar el control en el caso.
- `interpretacion`: lectura sugerida para explicar el grafico.

Datos derivados:

- `valor`: valor numerico normalizado de la escala CMMI. El tablero usa este
  campo para calcular madurez y brecha.
- `madurez_desc` y `aspecto_clave`: descripcion legible del nivel.
- `cumplimiento`: se mantiene por compatibilidad con el ejemplo de catedra; la
  madurez efectiva del tablero sale de `valor`.

Regla de evaluacion:

- Nivel 0: no hay evidencia de implementacion.
- Nivel 1: existe una practica reactiva, informal o dependiente de personas.
- Nivel 2: hay gestion parcial, pero falta formalizacion, cobertura o evidencia.
- Nivel 3: el control esta definido/documentado para el alcance principal.
- Nivel 4: el control se mide con indicadores o revisiones periodicas.
- Nivel 5: hay mejora continua demostrable.

Para defender el numero, no alcanza con decir "cumple" o "no cumple". Cada fila
debe poder contestar: que vimos, que falta, quien lo informo y por que ese nivel
es razonable.

## Capa 6: proyectos

`proyectos.csv` traduce las brechas en una cartera de iniciativas.

Datos definidos por el grupo:

- `proyecto_id`
- `titulo`
- `plazo`
- `esfuerzo_jornadas`
- `aporte_seguridad`
- `descripcion`
- `dependencias`
- `tipo_seguridad`

Datos derivados:

- `controles_esperados`: cantidad de controles vinculados al proyecto.
- columnas `logica`, `fisica`, `organizativa`, `legal`: clasificacion del
  proyecto para graficos.
- `costo`: estimacion calculada como `esfuerzo_jornadas * 150000`.
- `meses`: duracion aproximada calculada como `esfuerzo_jornadas / 22`.

Los proyectos no salen literalmente del TP1. Son una decision profesional del
grupo basada en:

- brechas ISO detectadas;
- criticidad de activos y procesos del TP1;
- material de la catedra sobre tablero, KPI/KGI y plan de acciones;
- ejemplo G1 como referencia de estructura.

## Capa 7: trazabilidad proyecto-control

`proyecto_control.csv` vincula cada proyecto con los controles ISO que ayuda a
mejorar.

Datos definidos por el grupo:

- relacion `proyecto_id` -> `control_id`.

Datos derivados en el tablero:

- prioridad por proyecto;
- brecha asociada;
- esfuerzo acumulado;
- quick wins;
- graficos de trazabilidad capitulo -> control -> proyecto.

Esta relacion es clave para defender el plan. Si un proyecto no esta conectado a
controles con brecha, queda debil. Si un control critico no tiene proyecto
asociado, queda una brecha sin tratamiento.

## Flujo incremental de generacion

### 1. Importar base academica y caso ejemplo

```bash
make import-example
```

Este paso importa:

- catalogo ISO usado por el tablero;
- parametros comunes;
- dataset `empresas/ejemplo` desde el trabajo G1.

Sirve para tener una referencia funcional y comparar si TecnoHogar queda
razonable frente a un caso ya armado.

### 2. Generar dataset TecnoHogar desde TP1

```bash
make generate-tecnohogar
```

Por defecto toma:

```text
../../udemm_sistemas/seguridad_informatica/Entregas/TP1/TP1_Inventario_TecnoHogar_v2.xlsx
```

Si el Excel esta en otra ruta:

```bash
TP1_TECNOHOGAR_XLSX=/ruta/TP1_Inventario_TecnoHogar_v2.xlsx make generate-tecnohogar
```

Este paso genera:

- `datos/empresas/tecnohogar/activos.csv`
- `datos/empresas/tecnohogar/entrevistas.csv`
- `datos/empresas/tecnohogar/diagnostico.csv`
- `datos/empresas/tecnohogar/proyectos.csv`
- `datos/empresas/tecnohogar/proyecto_control.csv`

El script combina datos observados del TP1 con criterios definidos en codigo:

- niveles de madurez por control;
- evidencias destacadas;
- responsables entrevistados;
- cartera de proyectos;
- vinculos proyecto-control.

### 3. Validar integridad

```bash
make validate
```

La validacion controla que:

- existan los archivos requeridos;
- los controles del diagnostico existan en el catalogo;
- los niveles de madurez esten en rango;
- los vinculos proyecto-control sean validos;
- TecnoHogar tenga los 93 controles y los activos esperados;
- las brechas debiles tengan hallazgo, observacion y proyecto asociado.

### 4. Calcular tablero y salidas

```bash
make build
```

El motor de metricas calcula:

- madurez global ponderada;
- brecha global;
- madurez por capitulo;
- distribucion CMMI;
- brechas ponderadas por control;
- capacidades operacionales;
- dominios de seguridad;
- prioridad de proyectos;
- quick wins;
- trazabilidad.

En CI se ejecuta:

```bash
make ci
```

que equivale a validar datos, correr tests y generar salidas.

## Como se calculan los graficos principales

- Madurez de control: `valor` del nivel CMMI.
- Brecha de control: `1 - valor`.
- Brecha ponderada: `brecha * peso`.
- Madurez global: promedio ponderado de `valor` por `peso`.
- Madurez por capitulo: promedio ponderado dentro de cada capitulo ISO.
- Mapa ISO: distribucion de los 93 controles por capitulo y nivel CMMI.
- Treemap de controles: superficie de controles coloreada por madurez.
- Pareto de brechas: controles ordenados por `peso_brecha`.
- Plan: proyectos priorizados por brecha asociada, aporte y esfuerzo.
- Quick wins: proyectos de prioridad alta y esfuerzo relativo bajo.
- Trazabilidad: union entre catalogo, diagnostico, proyectos y vinculos.

## Criterio para agregar o cambiar datos

1. Primero identificar la fuente: TP1, material de catedra, entrevista,
   inferencia o criterio del grupo.
2. Si el dato viene de una fuente estructurada, preferir un script generador.
3. Si el dato es criterio del grupo, dejarlo explicito y consistente.
4. Si cambia un nivel de madurez, actualizar tambien evidencia, hallazgo y
   observaciones.
5. Si cambia una brecha relevante, revisar el proyecto asociado.
6. Ejecutar `make validate` antes de usar el tablero o generar entregables.

La pregunta guia es: si el profesor senala un grafico, deberiamos poder llegar
desde ese punto hasta el control ISO, la evidencia, el activo/proceso afectado y
el proyecto propuesto.
