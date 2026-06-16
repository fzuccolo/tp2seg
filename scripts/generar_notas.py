from __future__ import annotations

import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.datos import load_dataset, repo_root
from app.defensa import narrativa_markdown
from app.graficos import ChartGuide, chart_guides
from app.metricas import MetricResult, compute_metrics


ROOT = repo_root()
CASE_ID = "tecnohogar"
NOTES_DIR = ROOT / "docs" / "notas"
GRAPHICS_DIR = NOTES_DIR / "assets" / "graficos"


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def export_graphics(result: MetricResult, guides: list[ChartGuide]) -> None:
    GRAPHICS_DIR.mkdir(parents=True, exist_ok=True)
    for guide in guides:
        fig = guide.factory(result, None)
        fig.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff")
        output = GRAPHICS_DIR / guide.filename
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                fig.write_image(str(output), width=1280, height=720, scale=2)
        except Exception as exc:
            raise RuntimeError(
                "No se pudieron exportar los gráficos. Ejecutá `pip install -r requirements.txt` "
                "para instalar Kaleido y volvé a correr `make notas`."
            ) from exc


def render_graph_guide(result: MetricResult, guides: list[ChartGuide]) -> str:
    resumen = result.resumen
    effort = int(resumen["esfuerzo_total"])
    lines = [
        "# Guía de gráficos del tablero",
        "",
        "Esta guía explica cada gráfico visual del tablero de TecnoHogar. Cada screenshot se genera desde las mismas funciones Plotly que usa Streamlit, por eso sirve como plan B para la defensa si la demo en vivo falla.",
        "",
        f"Valores base del caso: **{resumen['controles_evaluados']} controles**, **{resumen['madurez_global_pct']}% madurez**, **{resumen['brecha_global_pct']}% brecha**, **{resumen['proyectos']} iniciativas**, **{resumen['quick_wins']} quick wins** y **{effort} jornadas**.",
        "",
    ]
    for guide in guides:
        lines.extend(
            [
                f"## {guide.title}",
                "",
                f"![{guide.title}](assets/graficos/{guide.filename})",
                "",
                f"**Dónde aparece:** Tab {guide.tab}, sección {guide.section}.",
                "",
                f"**Para qué sirve:** {guide.purpose}",
                "",
                f"**Base teórica:** {guide.theory}",
                "",
                f"**Cómo se lee:** {guide.reading}",
                "",
                f"**Qué dicen los datos de TecnoHogar:** {guide.insight(result)}",
                "",
                f"**Cómo explicarlo en la defensa:** {guide.defense}",
                "",
                f"**Pregunta probable:** {guide.question}",
                "",
                f"**Respuesta sugerida:** {guide.answer}",
                "",
            ]
        )
    return "\n".join(lines)


def render_readme(result: MetricResult, guides: list[ChartGuide]) -> str:
    resumen = result.resumen
    effort = int(resumen["esfuerzo_total"])
    return f"""# Notas de defensa TP2

Este directorio es el paquete de estudio para defender el tablero de control de seguridad. Está pensado para preparar la presentación, entender cada gráfico y tener un plan B si la demo en vivo no funciona.

## Orden recomendado

1. Leer `conceptos-clave.md` para repasar la teoría mínima: métricas, KPI/KGI, CMMI, brecha, riesgo, CID, quick wins y trazabilidad.
2. Leer `narrativa-presentacion.md` para practicar la historia slide por slide.
3. Leer `guia-graficos.md` para entender qué dice cada gráfico y cómo responder preguntas.
4. Leer `demo-en-vivo.md` para practicar el recorrido del tablero y preparar el plan B.

## Números que conviene recordar

- Madurez global: **{resumen['madurez_global_pct']}%**.
- Brecha global: **{resumen['brecha_global_pct']}%**.
- Controles evaluados: **{resumen['controles_evaluados']}**.
- Iniciativas del plan: **{resumen['proyectos']}**.
- Quick wins: **{resumen['quick_wins']}**.
- Esfuerzo total estimado: **{effort} jornadas**.
- Gráficos documentados: **{len(guides)}**.

## Idea central de la defensa

El tablero no es solamente una visualización. Es una forma de convertir el contexto de TecnoHogar en una cadena defendible: **activo y proceso -> control ISO -> evidencia -> nivel CMMI -> brecha -> proyecto -> seguimiento**.
"""


def render_concepts(result: MetricResult) -> str:
    resumen = result.resumen
    return f"""# Conceptos clave

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

En TecnoHogar, la madurez global es **{resumen['madurez_global_pct']}%** y la brecha global es **{resumen['brecha_global_pct']}%**.

## ISO/IEC 27002:2022 capítulos 5, 6, 7 y 8

El tablero usa los cuatro capítulos evaluables del catálogo: **5 Organizativos**, **6 Personas**, **7 Físicos** y **8 Tecnológicos**. En total se evaluaron **{resumen['controles_evaluados']} controles**.

## CID

**Confidencialidad** protege contra acceso no autorizado. **Integridad** protege contra modificación incorrecta. **Disponibilidad** protege la continuidad de acceso y uso. En el TP1 se usó CID para activos; en el TP2 se usa también para leer controles asociados a esas propiedades.

## Riesgo, tratamiento y priorización

El diagnóstico muestra exposición o debilidad; el tratamiento define qué hacer. La priorización combina brecha, peso, esfuerzo, aporte esperado y plazo. Por eso el plan no se ordena solo por intuición.

## Pareto de brechas

El Pareto ordena controles por brecha ponderada y muestra el acumulado. Sirve para explicar qué controles concentran mayor impacto de mejora.

## Matriz impacto / esfuerzo

Cruza prioridad contra esfuerzo. El cuadrante de alto impacto y bajo esfuerzo contiene quick wins. Los proyectos de alto impacto y alto esfuerzo suelen ser estratégicos.

## Quick win

Un quick win no es una acción menor. Es una acción con buen retorno inicial: impacto alto y esfuerzo relativo bajo frente al resto de la cartera. TecnoHogar tiene **{resumen['quick_wins']} quick wins**.

## Trazabilidad control -> evidencia -> proyecto

La trazabilidad permite responder de dónde sale cada número y por qué existe cada proyecto. En la defensa, esta es la parte que muestra que el tablero es auditable y no una colección de gráficos sueltos.

## SGSI y mejora continua

Un SGSI busca gestionar seguridad de forma sistemática. El tablero puede ser usado como instrumento de mejora continua: medir, priorizar, ejecutar, revisar y ajustar.
"""


def render_demo(result: MetricResult) -> str:
    resumen = result.resumen
    effort = int(resumen["esfuerzo_total"])
    return f"""# Demo en vivo

## Objetivo

Mostrar que el tablero permite ir desde una lectura ejecutiva hasta controles y proyectos trazables. La demo tiene que ser corta, guiada y conectada con la narrativa de la PPTX.

## Recorrido recomendado

1. Abrir `https://tp2seg.streamlit.app/` y verificar que el caso seleccionado sea `tecnohogar`.
2. Tab **Ejecutivo**: mostrar madurez global **{resumen['madurez_global_pct']}%**, brecha **{resumen['brecha_global_pct']}%**, **{resumen['controles_evaluados']} controles**, **{resumen['quick_wins']} quick wins** y radar de capacidades.
3. Tab **Mapa ISO**: mostrar que están los capítulos 5, 6, 7 y 8 y que los cuadrados representan controles evaluados.
4. Tab **Brechas**: mostrar el Pareto y explicar que la priorización usa brecha ponderada.
5. Tab **Plan**: mostrar las **{resumen['proyectos']} iniciativas**, la matriz impacto/esfuerzo y el roadmap de **{effort} jornadas**.
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
"""


def main() -> int:
    dataset = load_dataset(CASE_ID, ROOT)
    result = compute_metrics(dataset)
    guides = chart_guides()

    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    export_graphics(result, guides)
    write_file(NOTES_DIR / "README.md", render_readme(result, guides))
    write_file(NOTES_DIR / "narrativa-presentacion.md", narrativa_markdown(result))
    write_file(NOTES_DIR / "guia-graficos.md", render_graph_guide(result, guides))
    write_file(NOTES_DIR / "conceptos-clave.md", render_concepts(result))
    write_file(NOTES_DIR / "demo-en-vivo.md", render_demo(result))

    print(f"Generadas notas de defensa en {NOTES_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
