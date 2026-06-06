from __future__ import annotations

import json
from html import escape
from pathlib import Path

import pandas as pd

from app.metricas import MetricResult


BLUE = "#2563eb"
GREEN = "#16a34a"
RED = "#dc2626"
AMBER = "#f59e0b"
PURPLE = "#7c3aed"
CYAN = "#0891b2"
NAVY = "#0f172a"
SLATE = "#475569"
MUTED = "#64748b"
LIGHT = "#f8fafc"
BORDER = "#dbe3ef"


def _markdown_table(df: pd.DataFrame, columns: list[str], headers: list[str], rows: int | None = None) -> str:
    selected = df.loc[:, columns].copy()
    if rows is not None:
        selected = selected.head(rows)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in selected.iterrows():
        values = [str(row[col]) for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def _report_spacer(height: str = "1.25em") -> str:
    return "\n\n".join(
        [
            f"```{{=typst}}\n#v({height})\n```",
            '```{=html}\n<div style="height: 0.75rem;"></div>\n```',
        ]
    )


def _weighted_gaps_list(df: pd.DataFrame, rows: int = 5) -> str:
    lines = []
    for row in df.head(rows).itertuples(index=False):
        lines.append(
            f"- **{row.control_id} - {row.control_nombre}:** brecha ponderada {float(row.peso_brecha):.2f}; {row.capitulo}."
        )
    return "\n\n".join(lines)


def _pretty_project_title(title: object) -> str:
    text = str(title)
    replacements = {
        "Concientizacion": "Concientización",
        "fisica": "física",
        "distribucion": "distribución",
        "politicas": "políticas",
        "Auditoria": "Auditoría",
        "metricas": "métricas",
        "segregacion": "segregación",
        "recuperacion": "recuperación",
        "clasificacion": "clasificación",
        "Gestion": "Gestión",
    }
    for source, replacement in replacements.items():
        text = text.replace(source, replacement)
    return text


def _projects_list(df: pd.DataFrame, rows: int = 5) -> str:
    lines = []
    for row in df.head(rows).itertuples(index=False):
        lines.append(
            f"- **{row.proyecto_id} - {_pretty_project_title(row.titulo)}:** {row.plazo}, {int(row.esfuerzo_jornadas)} jornadas, {int(row.controles_relacionados)} controles, prioridad {float(row.prioridad):.2f}."
        )
    return "\n\n".join(lines)


def _short(value: object, limit: int = 44) -> str:
    text = str(value)
    return text if len(text) <= limit else text[: limit - 1] + "..."


def _svg_text(x: float, y: float, text: object, size: int = 14, color: str = NAVY, weight: int = 400, anchor: str = "start") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(str(text))}</text>'
    )


def _svg_card(x: float, y: float, w: float, h: float, accent: str, label: str, value: str, detail: str) -> str:
    return "\n".join(
        [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#ffffff" stroke="{BORDER}"/>',
            f'<rect x="{x}" y="{y}" width="6" height="{h}" rx="3" fill="{accent}"/>',
            _svg_text(x + 22, y + 35, value, 26, NAVY, 700),
            _svg_text(x + 22, y + 62, label.upper(), 11, SLATE, 700),
            _svg_text(x + 22, y + 86, detail, 12, MUTED, 400),
        ]
    )


def _svg_bar_chart(
    title: str,
    rows: list[tuple[str, float, str]],
    color: str,
    width: int = 900,
    value_suffix: str = "%",
    value_decimals: int = 1,
) -> str:
    height = 92 + len(rows) * 50
    label_x = 36
    bar_x = 290
    bar_w = width - bar_x - 120
    max_value = max([value for _, value, _ in rows] + [1.0])
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        _svg_text(28, 36, title, 22, NAVY, 700),
        f'<line x1="28" y1="58" x2="{width - 28}" y2="58" stroke="{BORDER}"/>',
    ]
    for idx, (label, value, detail) in enumerate(rows):
        y = 92 + idx * 50
        pct = 0 if max_value == 0 else max(0, min(value / max_value, 1))
        lines.extend(
            [
                _svg_text(label_x, y + 16, _short(label, 34), 13, NAVY, 700),
                _svg_text(label_x, y + 35, _short(detail, 40), 11, MUTED, 400),
                f'<rect x="{bar_x}" y="{y}" width="{bar_w}" height="18" rx="9" fill="{LIGHT}" stroke="{BORDER}"/>',
                f'<rect x="{bar_x}" y="{y}" width="{bar_w * pct:.1f}" height="18" rx="9" fill="{color}"/>',
                _svg_text(bar_x + bar_w + 18, y + 15, f"{value:.{value_decimals}f}{value_suffix}", 13, NAVY, 700),
            ]
        )
    lines.append("</svg>")
    return "\n".join(lines)


def _posture_svg(result: MetricResult) -> str:
    resumen = result.resumen
    maturity = float(resumen["madurez_global_pct"])
    gap = float(resumen["brecha_global_pct"])
    width, height = 900, 310
    bar_x, bar_y, bar_w, bar_h = 44, 230, 812, 28
    maturity_w = bar_w * maturity / 100
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
            _svg_text(32, 42, "Postura ejecutiva", 24, NAVY, 700),
            _svg_text(32, 68, "Lectura consolidada de madurez, brecha, alcance y esfuerzo estimado.", 13, MUTED, 400),
            _svg_card(32, 94, 192, 100, BLUE, "Madurez global", f"{maturity:.1f}%", "promedio ponderado"),
            _svg_card(244, 94, 192, 100, RED, "Brecha global", f"{gap:.1f}%", "distancia al objetivo"),
            _svg_card(456, 94, 192, 100, CYAN, "Controles", str(resumen["controles_evaluados"]), "capitulos 5 a 8"),
            _svg_card(668, 94, 192, 100, PURPLE, "Proyectos", str(resumen["proyectos"]), "cartera priorizada"),
            _svg_text(44, 220, "Madurez vs brecha", 13, NAVY, 700),
            f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="14" fill="{RED}"/>',
            f'<rect x="{bar_x}" y="{bar_y}" width="{maturity_w:.1f}" height="{bar_h}" rx="14" fill="{GREEN}"/>',
            _svg_text(bar_x, bar_y + 52, f"Madurez {maturity:.1f}%", 13, GREEN, 700),
            _svg_text(bar_x + bar_w, bar_y + 52, f"Brecha {gap:.1f}%", 13, RED, 700, "end"),
            "</svg>",
        ]
    )


def _chapters_svg(result: MetricResult) -> str:
    frame = result.capitulos.copy().sort_values("madurez_pct", ascending=True)
    rows = [
        (str(row["capitulo"]), float(row["madurez_pct"]), f"Brecha {float(row['brecha_pct']):.1f}%")
        for _, row in frame.iterrows()
    ]
    return _svg_bar_chart("Madurez por capitulo ISO", rows, BLUE)


def _maturity_svg(result: MetricResult) -> str:
    frame = result.madurez_distribucion.copy()
    width, height = 900, 330
    chart_x, chart_y, chart_w, chart_h = 62, 86, 770, 170
    max_value = max([float(value) for value in frame["controles"]] + [1.0])
    col_w = chart_w / max(len(frame), 1)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        _svg_text(32, 42, "Distribucion CMMI", 24, NAVY, 700),
        _svg_text(32, 68, "Cantidad de controles segun nivel de madurez.", 13, MUTED, 400),
        f'<line x1="{chart_x}" y1="{chart_y + chart_h}" x2="{chart_x + chart_w}" y2="{chart_y + chart_h}" stroke="{BORDER}"/>',
    ]
    colors = {1: RED, 2: AMBER, 3: BLUE, 4: GREEN, 5: GREEN, 0: RED}
    for idx, row in enumerate(frame.itertuples(index=False)):
        value = float(row.controles)
        x = chart_x + idx * col_w + col_w * 0.2
        h = chart_h * value / max_value
        y = chart_y + chart_h - h
        color = colors.get(int(row.nivel_madurez), CYAN)
        lines.extend(
            [
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{col_w * 0.6:.1f}" height="{h:.1f}" rx="8" fill="{color}"/>',
                _svg_text(x + col_w * 0.3, y - 8, int(value), 13, NAVY, 700, "middle"),
                _svg_text(x + col_w * 0.3, chart_y + chart_h + 26, str(row.nivel_madurez), 13, NAVY, 700, "middle"),
                _svg_text(x + col_w * 0.3, chart_y + chart_h + 45, _short(str(row.madurez_nombre).split(" - ", 1)[-1], 14), 10, MUTED, 400, "middle"),
            ]
        )
    lines.append("</svg>")
    return "\n".join(lines)


def _gaps_svg(result: MetricResult) -> str:
    frame = result.top_brechas.copy().head(8)
    rows = [
        (
            f"{row.control_id} {row.control_nombre}",
            float(row.peso_brecha),
            f"Brecha cruda {float(row.brecha_pct):.0f}% | {row.capitulo}",
        )
        for row in frame.itertuples(index=False)
    ]
    return _svg_bar_chart("Controles con mayor brecha ponderada", rows, RED, value_suffix="", value_decimals=2)


def _projects_svg(result: MetricResult) -> str:
    frame = result.proyectos.copy().head(8)
    rows = [
        (f"{row.proyecto_id} {row.titulo}", float(row.prioridad), f"{row.plazo} | {int(row.esfuerzo_jornadas)} jornadas")
        for row in frame.itertuples(index=False)
    ]
    return _svg_bar_chart("Proyectos priorizados", rows, GREEN, value_suffix="", value_decimals=2)


def write_report_assets(result: MetricResult, output_dir: Path) -> None:
    assets_dir = output_dir / "report_assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    assets = {
        "postura.svg": _posture_svg(result),
        "madurez-capitulos.svg": _chapters_svg(result),
        "distribucion-cmmi.svg": _maturity_svg(result),
        "brechas-principales.svg": _gaps_svg(result),
        "proyectos-priorizados.svg": _projects_svg(result),
    }
    for filename, content in assets.items():
        (assets_dir / filename).write_text(content + "\n", encoding="utf-8")


def write_outputs(result: MetricResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    result.controles.to_csv(output_dir / "metricas.csv", index=False)
    result.capitulos.to_csv(output_dir / "capitulos.csv", index=False)
    result.proyectos.to_csv(output_dir / "proyectos_priorizados.csv", index=False)
    result.madurez_distribucion.to_csv(output_dir / "madurez_distribucion.csv", index=False)
    result.matriz_madurez.to_csv(output_dir / "matriz_madurez.csv", index=False)
    result.capacidad_operacional.to_csv(output_dir / "capacidad_operacional.csv", index=False)
    result.ciberfunciones.to_csv(output_dir / "ciberfunciones.csv", index=False)
    result.proyectos_plazo.to_csv(output_dir / "proyectos_por_plazo.csv", index=False)
    result.proyectos_tipo.to_csv(output_dir / "proyectos_por_tipo.csv", index=False)
    result.proyectos_capitulo.to_csv(output_dir / "proyectos_por_capitulo.csv", index=False)
    result.proyectos_capacidad.to_csv(output_dir / "proyectos_por_capacidad.csv", index=False)
    result.esfuerzo_roadmap.to_csv(output_dir / "esfuerzo_roadmap.csv", index=False)
    result.quick_wins.to_csv(output_dir / "quick_wins.csv", index=False)
    result.trazabilidad.to_csv(output_dir / "trazabilidad_control_proyecto.csv", index=False)

    write_report_assets(result, output_dir)

    with (output_dir / "resumen.json").open("w", encoding="utf-8") as fh:
        json.dump(result.resumen, fh, ensure_ascii=False, indent=2)

    (output_dir / "resumen_informe.md").write_text(render_report_summary(result), encoding="utf-8")
    (output_dir / "resumen_slides.md").write_text(render_slides_summary(result), encoding="utf-8")


def render_report_summary(result: MetricResult) -> str:
    resumen = result.resumen
    caso_id = str(resumen["empresa_id"])
    assets = "report_assets"

    capitulos = result.capitulos.copy()
    capitulos["madurez_pct"] = capitulos["madurez_pct"].round(1)
    capitulos["brecha_pct"] = capitulos["brecha_pct"].round(1)

    top = result.top_brechas.copy()
    top["brecha_pct"] = top["brecha_pct"].round(1)
    top["peso_brecha"] = top["peso_brecha"].round(2)

    proyectos = result.proyectos.copy()
    proyectos["prioridad"] = proyectos["prioridad"].round(2)

    return "\n\n".join(
        [
            "## Resumen ejecutivo",
            f"TecnoHogar registra una **madurez global de {resumen['madurez_global_pct']}%** y una **brecha global de {resumen['brecha_global_pct']}%** sobre 93 controles ISO/IEC 27002:2022. El resultado muestra una base operativa existente, pero con oportunidades relevantes de formalización, medición y seguimiento.",
            f"![]({assets}/postura.svg){'{'}width=100%{'}'}",
            f"El capítulo con menor madurez es **{resumen['capitulo_mas_debil']}** y la capacidad más comprometida es **{resumen['capacidad_mas_debil']}**. La recomendación es iniciar por las iniciativas con mejor relación entre impacto y esfuerzo, manteniendo trazabilidad entre brecha, control, evidencia e iniciativa.",
            "## Diagnóstico visual",
            f"![]({assets}/madurez-capitulos.svg){'{'}width=100%{'}'}",
            f"![]({assets}/distribucion-cmmi.svg){'{'}width=100%{'}'}",
            "La distribución CMMI indica que la organización no parte de cero: existen prácticas definidas y algunos controles medidos. Sin embargo, una proporción relevante permanece en niveles iniciales o gestionados parcialmente, lo que limita la previsibilidad y la mejora continua.",
            "## Brechas que explican el plan",
            f"![]({assets}/brechas-principales.svg){'{'}width=100%{'}'}",
            "El ranking ejecutivo utiliza **brecha ponderada** para evitar una lectura plana de controles con el mismo nivel de madurez. De esta forma, la priorización incorpora el peso relativo de cada control y no solo la distancia porcentual al objetivo.",
            _report_spacer(),
            _weighted_gaps_list(top, rows=6),
            "Las brechas principales no se concentran en un único frente. Combinan aspectos de personas, seguridad física, eventos, continuidad y tecnología; por lo tanto, el plan recomendado integra gobierno, operación y controles técnicos.",
            "## Plan de acción recomendado",
            f"![]({assets}/proyectos-priorizados.svg){'{'}width=100%{'}'}",
            _report_spacer(),
            _projects_list(proyectos, rows=6),
            f"La cartera completa incluye **{resumen['proyectos']} iniciativas**, **{resumen['quick_wins']} quick wins** y un esfuerzo total estimado de **{resumen['esfuerzo_total']} jornadas**. El objetivo inicial es reducir brechas visibles, ordenar responsables y dejar instalado un ciclo de medición periódica.",
            "## Conclusión ejecutiva",
            "La recomendación es utilizar el tablero como instrumento de gobierno de seguridad: aprobar quick wins, formalizar responsables, medir avances y sostener la trazabilidad entre evidencia, control ISO e iniciativa de mejora.",
            "## Referencias metodológicas",
            "- **Madurez:** valor normalizado del nivel CMMI asignado a cada control.",
            "- **Brecha:** distancia entre la madurez actual y el objetivo optimizado.",
            "- **Brecha ponderada:** brecha multiplicada por el peso relativo del control.",
            "- **Quick win:** iniciativa con impacto alto y esfuerzo relativo bajo.",
            "- **Trazabilidad:** relación control ISO -> evidencia -> brecha -> iniciativa.",
        ]
    )


def render_slides_summary(result: MetricResult) -> str:
    resumen = result.resumen
    top = result.top_brechas.copy()
    top["brecha_pct"] = top["brecha_pct"].round(1)
    top["peso_brecha"] = top["peso_brecha"].round(2)
    proyectos = result.proyectos.copy()
    proyectos["prioridad"] = proyectos["prioridad"].round(3)

    return "\n\n".join(
        [
            f"- Madurez global: **{resumen['madurez_global_pct']}%**",
            f"- Brecha global: **{resumen['brecha_global_pct']}%**",
            f"- Controles evaluados: **{resumen['controles_evaluados']}**",
            f"- Quick wins: **{resumen['quick_wins']}**",
            f"- Esfuerzo total: **{resumen['esfuerzo_total']} jornadas**",
            f"- Capitulo mas debil: **{resumen['capitulo_mas_debil']}**",
            f"- Capacidad mas debil: **{resumen['capacidad_mas_debil']}**",
            "## Brechas principales",
            _markdown_table(
                top,
                ["control_id", "control_nombre", "peso_brecha"],
                ["Control", "Nombre", "Brecha ponderada"],
                rows=5,
            ),
            "## Plan de mejora",
            _markdown_table(
                proyectos,
                ["proyecto_id", "titulo", "plazo", "prioridad"],
                ["Proyecto", "Titulo", "Plazo", "Prioridad"],
                rows=5,
            ),
        ]
    )
