from __future__ import annotations

from dataclasses import dataclass

from app.metricas import MetricResult


@dataclass(frozen=True)
class SlideDefense:
    number: int
    title: str
    main_message: str
    narrative: str
    data_points: list[str]
    transition: str
    questions: list[tuple[str, str]]
    references: list[str]


def _pct(value: object) -> str:
    return f"{float(value):.1f}%"


def _top_gap(result: MetricResult):
    return result.top_brechas.sort_values("peso_brecha", ascending=False).iloc[0]


def _top_project(result: MetricResult):
    return result.proyectos.sort_values("prioridad", ascending=False).iloc[0]


def _weakest_chapter(result: MetricResult):
    return result.capitulos.sort_values("madurez_pct").iloc[0]


def _strongest_chapter(result: MetricResult):
    return result.capitulos.sort_values("madurez_pct").iloc[-1]


def _weakest_capacity(result: MetricResult):
    return result.capacidad_operacional.sort_values("madurez_pct").iloc[0]


def slide_defense_notes(result: MetricResult) -> list[SlideDefense]:
    resumen = result.resumen
    effort = int(resumen["esfuerzo_total"])
    gap = _top_gap(result)
    project = _top_project(result)
    weak_chapter = _weakest_chapter(result)
    strong_chapter = _strongest_chapter(result)
    weak_capacity = _weakest_capacity(result)
    low_cmmi = int(result.madurez_distribucion.loc[result.madurez_distribucion["nivel_madurez"].isin([0, 1, 2]), "controles"].sum())
    measured_cmmi = int(result.madurez_distribucion.loc[result.madurez_distribucion["nivel_madurez"].isin([4, 5]), "controles"].sum())
    quick_wins = result.quick_wins[result.quick_wins["cuadrante"] == "Quick win"]
    first_quick = quick_wins.sort_values("prioridad", ascending=False).iloc[0]

    return [
        SlideDefense(
            1,
            "Carátula",
            "Presentar el trabajo como un tablero de gobierno: inventario, diagnóstico, brechas y plan.",
            "Abrir diciendo que no se va a mostrar una planilla sino una forma de convertir el relevamiento del TP1 en decisiones de seguridad. El relato completo es: primero entendimos el contexto operativo, después medimos controles ISO, luego identificamos brechas y finalmente armamos un plan trazable.",
            [
                "Caso: TecnoHogar S.A.",
                "Estándar: ISO/IEC 27002:2022.",
                "Entrega: TP2 Seguridad Informática, Grupo 1.",
            ],
            "Pasar al resumen ejecutivo: ahora mostramos la foto consolidada del diagnóstico.",
            [
                (
                    "¿Qué aporta el tablero frente a una planilla?",
                    "El tablero permite leer la postura desde dirección y bajar hasta control, evidencia y proyecto sin perder trazabilidad.",
                )
            ],
            [
                "**Tablero de control**: instrumento para seguimiento, priorización y comunicación de indicadores.",
                "**ISO/IEC 27002:2022**: catálogo de controles de seguridad de la información.",
            ],
        ),
        SlideDefense(
            2,
            "Resumen ejecutivo",
            "La postura actual es media-baja: hay base operativa, pero falta formalización, medición y mejora continua.",
            f"El mensaje central es {resumen['madurez_global_pct']}% de madurez y {resumen['brecha_global_pct']}% de brecha. No significa que todo esté mal; significa que TecnoHogar tiene prácticas en marcha, pero todavía no están suficientemente definidas, medidas y gobernadas como para hablar de una postura optimizada.",
            [
                f"Madurez global: {_pct(resumen['madurez_global_pct'])}.",
                f"Brecha global: {_pct(resumen['brecha_global_pct'])}.",
                f"Controles evaluados: {resumen['controles_evaluados']}.",
                f"Iniciativas: {resumen['proyectos']}.",
                f"Quick wins: {resumen['quick_wins']}.",
                f"Esfuerzo total estimado: {effort} jornadas.",
            ],
            "Explicar el alcance: para que esos números sean defendibles, hay que mostrar qué se midió y con qué base.",
            [
                (
                    "¿Por qué confiar en un porcentaje global?",
                    "Porque es una síntesis ejecutiva. El tablero lo descompone por capítulo, nivel CMMI, control, brecha y proyecto.",
                ),
                (
                    "¿La brecha global es riesgo real?",
                    "Es una señal de exposición y madurez pendiente. Para convertirla en riesgo operativo se cruza con activos, procesos, evidencia y prioridades.",
                ),
            ],
            [
                "**KGI**: indicador de resultado que expresa si se alcanza un objetivo.",
                "**Brecha**: distancia entre el estado actual y el objetivo de madurez.",
            ],
        ),
        SlideDefense(
            3,
            "Alcance y modelo de datos",
            "El TP2 continúa el TP1: usa contexto, activos y responsables para medir controles y construir decisiones.",
            "Remarcar que el diagnóstico no aparece de la nada. El punto de partida es el inventario y la lectura de negocio del TP1. Sobre esa base se cargan controles, niveles CMMI, hallazgos, proyectos y vínculos control-proyecto. Lo importante es separar datos observados, datos definidos para el caso y métricas derivadas.",
            [
                "Capítulo 5: 37 controles organizativos.",
                "Capítulo 6: 8 controles de personas.",
                "Capítulo 7: 14 controles físicos.",
                "Capítulo 8: 34 controles tecnológicos.",
                f"Total evaluado: {resumen['controles_evaluados']} controles.",
            ],
            "Pasar al método: una vez definido el alcance, mostramos cómo se convierte cada control en una métrica.",
            [
                (
                    "¿Los 93 controles son todos los capítulos evaluables?",
                    "Sí. Para este tablero se trabajaron los capítulos 5, 6, 7 y 8 de ISO/IEC 27002:2022.",
                ),
                (
                    "¿Qué datos son simulados?",
                    "El caso toma el contexto de TecnoHogar del TP1 y define niveles, hallazgos y proyectos para completar el diagnóstico del TP2.",
                ),
            ],
            [
                "**CID**: confidencialidad, integridad y disponibilidad.",
                "**Trazabilidad**: vínculo entre dato de entrada, control, métrica y decisión.",
            ],
        ),
        SlideDefense(
            4,
            "Método de medición",
            "Cada número sale de una cadena defendible: control ISO, evidencia, nivel CMMI, brecha y proyecto.",
            "Esta slide es clave para responder preguntas. Hay que explicar que no se inventa un gráfico aislado: cada control tiene una evaluación de madurez, esa madurez se normaliza, se calcula una brecha, se pondera por peso del control y luego se vincula con iniciativas de mejora.",
            [
                "Escala CMMI usada: 0 a 5.",
                "Madurez normalizada: nivel actual convertido a valor entre 0 y 1.",
                "Brecha: 1 menos madurez.",
                "Brecha ponderada: brecha multiplicada por peso del control.",
                "Prioridad de proyecto: brecha asociada y aporte esperado.",
            ],
            "Pasar a resultados por capítulo: con el método claro, vemos dónde está más débil TecnoHogar.",
            [
                (
                    "¿Por qué CMMI?",
                    "Porque permite expresar madurez de procesos y controles en una escala simple y comparable.",
                ),
                (
                    "¿Brecha ponderada es lo mismo que brecha porcentual?",
                    "No. La brecha porcentual sale del nivel CMMI; la ponderada incorpora el peso relativo del control.",
                ),
            ],
            [
                "**Medida**: dato observado o asignado.",
                "**Métrica**: cálculo o interpretación sobre medidas.",
                "**KPI**: indicador para seguimiento de desempeño.",
            ],
        ),
        SlideDefense(
            5,
            "Madurez por capítulo ISO",
            "La brecha es generalizada, pero tecnología y personas requieren atención temprana.",
            f"Mostrar primero el capítulo más débil: {weak_chapter['capitulo']} con {float(weak_chapter['madurez_pct']):.1f}% de madurez. Luego aclarar que el capítulo más fuerte, {strong_chapter['capitulo']} con {float(strong_chapter['madurez_pct']):.1f}%, también está lejos de optimizado. La lectura es de madurez media-baja, no de un único problema aislado.",
            [
                f"Más débil: {weak_chapter['capitulo']} ({float(weak_chapter['madurez_pct']):.1f}%).",
                f"Más fuerte: {strong_chapter['capitulo']} ({float(strong_chapter['madurez_pct']):.1f}%).",
                f"Brecha global: {_pct(resumen['brecha_global_pct'])}.",
            ],
            "Pasar a la distribución CMMI para mostrar si el promedio sale de pocos controles o de muchos niveles bajos.",
            [
                (
                    "¿El capítulo más débil define solo el plan?",
                    "No. Define una alerta. El plan final combina capítulo, brecha ponderada, capacidad, esfuerzo y proyecto.",
                )
            ],
            [
                "**Capítulo ISO**: agrupación del catálogo de controles.",
                "**Madurez promedio ponderada**: promedio que considera peso de controles.",
            ],
        ),
        SlideDefense(
            6,
            "Distribución CMMI",
            "El promedio global se explica por muchos controles en niveles iniciales o gestionados parcialmente.",
            f"Explicar que la distribución muestra la forma del diagnóstico. {low_cmmi} controles están en niveles 0 a 2, mientras que {measured_cmmi} controles llegan a niveles 4 o 5. Esto respalda la idea de que hay prácticas, pero todavía falta medición formal y mejora sistemática.",
            [
                f"Controles en CMMI 0 a 2: {low_cmmi}.",
                f"Controles en CMMI 4 a 5: {measured_cmmi}.",
                f"Total: {resumen['controles_evaluados']} controles.",
            ],
            "Pasar a brechas: después de entender niveles de madurez, corresponde ordenar qué controles pesan más.",
            [
                (
                    "¿Por qué varios controles pueden tener la misma brecha?",
                    "Porque tienen el mismo nivel CMMI. La diferencia ejecutiva aparece al ponderar por peso del control.",
                )
            ],
            [
                "**CMMI 0..5**: inexistente, inicial, gestionado, definido, cuantitativo y optimizado.",
                "**Optimizado**: control medido, gestionado y mejorado de forma continua.",
            ],
        ),
        SlideDefense(
            7,
            "Brechas principales",
            "La priorización se hace por brecha ponderada, no por intuición ni por orden del estándar.",
            f"Mostrar el primer control del ranking: {gap['control_id']} - {gap['control_nombre']}, con brecha ponderada {float(gap['peso_brecha']):.2f}. Aclarar que el Pareto ayuda a decidir por dónde empezar, porque un mismo 85% de brecha no pesa igual si el control tiene distinto peso o distinta relación con proyectos.",
            [
                f"Control crítico: {gap['control_id']}.",
                f"Brecha ponderada máxima: {float(gap['peso_brecha']):.2f}.",
                f"Capítulo asociado: {gap['capitulo']}.",
            ],
            "Pasar al perfil operacional: ya sabemos qué controles pesan más; ahora vemos qué capacidades de gestión están afectadas.",
            [
                (
                    "¿Por qué usar Pareto?",
                    "Porque permite concentrar la discusión en los controles que más explican la brecha total.",
                ),
                (
                    "¿La brecha ponderada reemplaza al juicio profesional?",
                    "No. Ordena la conversación; después se valida con contexto, esfuerzo y dependencias.",
                ),
            ],
            [
                "**Pareto**: técnica para encontrar los factores que concentran mayor impacto.",
                "**Peso del control**: importancia relativa asignada para priorizar.",
            ],
        ),
        SlideDefense(
            8,
            "Perfil de seguridad",
            "El tablero traduce controles ISO a capacidades operacionales que se pueden gestionar.",
            f"Explicar que las capacidades ayudan a pasar del lenguaje del estándar al lenguaje de gestión. En TecnoHogar, la capacidad más débil es {weak_capacity['atributo']} con {float(weak_capacity['madurez_pct']):.1f}%. Esa lectura justifica proyectos de vulnerabilidades, monitoreo, hardening, accesos o gobierno, según corresponda.",
            [
                f"Capacidad más débil: {weak_capacity['atributo']}.",
                f"Madurez de esa capacidad: {float(weak_capacity['madurez_pct']):.1f}%.",
                f"Función más débil: {resumen['funcion_mas_debil']}.",
            ],
            "Pasar al plan: si las capacidades muestran dónde duele, el plan muestra cómo se corrige.",
            [
                (
                    "¿Las capacidades son capítulos de ISO?",
                    "No. Son una vista operacional construida para interpretar los controles y orientar decisiones.",
                )
            ],
            [
                "**Capacidad operacional**: conjunto de controles que expresan una práctica gestionable.",
                "**Perfil de seguridad**: lectura transversal de fortalezas y debilidades.",
            ],
        ),
        SlideDefense(
            9,
            "Plan de acción priorizado",
            "El diagnóstico se convierte en una cartera de iniciativas con impacto, esfuerzo, plazo y trazabilidad.",
            f"Mostrar que el plan no es una lista genérica. Tiene {resumen['proyectos']} iniciativas, {resumen['quick_wins']} quick wins y {effort} jornadas. La prioridad más alta es {project['proyecto_id']} - {project['titulo']}. También se puede mencionar el primer quick win: {first_quick['proyecto_id']} - {first_quick['titulo']}.",
            [
                f"Iniciativas: {resumen['proyectos']}.",
                f"Quick wins: {resumen['quick_wins']}.",
                f"Esfuerzo total: {effort} jornadas.",
                f"Proyecto prioritario: {project['proyecto_id']} - {project['titulo']}.",
            ],
            "Pasar a la demo: ahora que el plan está claro, mostramos cómo navegar el tablero publicado.",
            [
                (
                    "¿Quick win significa poco importante?",
                    "No. Significa alto impacto con esfuerzo relativo bajo frente al resto de la cartera.",
                ),
                (
                    "¿Las jornadas son presupuesto final?",
                    "No. Son una estimación de planificación para comparar esfuerzo y secuenciar trabajo.",
                ),
            ],
            [
                "**Matriz impacto/esfuerzo**: prioriza iniciativas por retorno relativo.",
                "**Tratamiento de riesgo**: acciones para reducir, transferir, aceptar o evitar exposición.",
            ],
        ),
        SlideDefense(
            10,
            "Tablero publicado",
            "La demo debe mostrar una historia: Ejecutivo, Mapa ISO, Brechas, Plan y Trazabilidad.",
            "No navegar libremente. Hacer una demo corta y dirigida: primero la foto ejecutiva, después el mapa ISO para demostrar cobertura, luego brechas para justificar prioridades, plan para explicar acciones y trazabilidad para cerrar la defensa técnica.",
            [
                "URL: https://tp2seg.streamlit.app/",
                "Ruta sugerida: Ejecutivo -> Mapa ISO -> Brechas -> Plan -> Trazabilidad.",
                "Plan B: PPTX más screenshots de docs/notas si Streamlit pide login o falla.",
            ],
            "Pasar al cierre: después de mostrar la herramienta, remarcar el valor de gobierno y mejora continua.",
            [
                (
                    "¿Qué mostrar si hay poco tiempo?",
                    "Ejecutivo, Pareto de brechas, matriz impacto/esfuerzo y Sankey de trazabilidad.",
                ),
                (
                    "¿Qué pasa si Streamlit falla?",
                    "Usar la PPTX y la guía de gráficos generada con screenshots reales del tablero.",
                ),
            ],
            [
                "**Demo en vivo**: validación de que el tablero es navegable y no solo un entregable estático.",
                "**CI/CD**: generación reproducible de tablero, informe y presentación.",
            ],
        ),
        SlideDefense(
            11,
            "Conclusiones y próximos pasos",
            "El tablero es un instrumento de gobierno de seguridad, no solo una visualización.",
            "Cerrar con tres ideas: el diagnóstico es trazable, el plan está priorizado y el tablero permite seguimiento periódico. La conclusión profesional es aprobar quick wins, formalizar responsables, medir avances y usar la misma estructura para futuras iteraciones.",
            [
                f"Controles evaluados: {resumen['controles_evaluados']}.",
                f"Iniciativas priorizadas: {resumen['proyectos']}.",
                f"Esfuerzo estimado: {effort} jornadas.",
                "Salida esperada: ciclo de medición y mejora continua.",
            ],
            "Cerrar invitando preguntas sobre método, gráficos o trazabilidad de proyectos.",
            [
                (
                    "¿Qué harían después de aprobar el plan?",
                    "Validar evidencias reales, asignar responsables, definir periodicidad de medición y controlar avance por tablero.",
                )
            ],
            [
                "**SGSI**: sistema de gestión de seguridad de la información.",
                "**Mejora continua**: medir, ejecutar, revisar y ajustar el plan de seguridad.",
            ],
        ),
    ]


def speaker_note_texts(result: MetricResult) -> list[str]:
    return [_speaker_note_text(note) for note in slide_defense_notes(result)]


def _speaker_note_text(note: SlideDefense) -> str:
    questions = "\n".join(f"- P: {question}\n  R: {answer}" for question, answer in note.questions)
    data_points = "\n".join(f"- {item}" for item in note.data_points)
    references = "\n".join(f"- {item}" for item in note.references)
    return "\n\n".join(
        [
            "Mensaje principal:",
            note.main_message,
            "Narrativa:",
            note.narrative,
            "Datos concretos:",
            data_points,
            "Puente:",
            note.transition,
            "Preguntas esperables:",
            questions,
            "Referencias:",
            references,
        ]
    )


def narrativa_markdown(result: MetricResult) -> str:
    sections = [
        "# Narrativa de presentación",
        "",
        "Esta guía es el guion de defensa para presentar la PPTX y hacer la demo del tablero. La idea no es memorizar palabra por palabra, sino entender el hilo: **TP1 -> medición ISO -> diagnóstico -> brechas -> plan -> trazabilidad**.",
        "",
    ]
    for note in slide_defense_notes(result):
        sections.extend(
            [
                f"## Slide {note.number}: {note.title}",
                "",
                f"**Mensaje principal:** {note.main_message}",
                "",
                f"**Narrativa oral:** {note.narrative}",
                "",
                "**Datos concretos:**",
                "",
                *[f"- {item}" for item in note.data_points],
                "",
                f"**Puente a la siguiente slide:** {note.transition}",
                "",
                "**Preguntas esperables:**",
                "",
                *[f"- **P:** {question}\n  **R:** {answer}" for question, answer in note.questions],
                "",
                "**Referencias para tener a mano:**",
                "",
                *[f"- {item}" for item in note.references],
                "",
            ]
        )
    return "\n".join(sections).rstrip() + "\n"
