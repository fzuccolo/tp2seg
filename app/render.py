from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from app.metricas import MetricResult


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

    with (output_dir / "resumen.json").open("w", encoding="utf-8") as fh:
        json.dump(result.resumen, fh, ensure_ascii=False, indent=2)

    (output_dir / "resumen_informe.md").write_text(render_report_summary(result), encoding="utf-8")
    (output_dir / "resumen_slides.md").write_text(render_slides_summary(result), encoding="utf-8")


def render_report_summary(result: MetricResult) -> str:
    resumen = result.resumen
    capitulos = result.capitulos.copy()
    capitulos["madurez_pct"] = capitulos["madurez_pct"].round(1)
    capitulos["brecha_pct"] = capitulos["brecha_pct"].round(1)

    top = result.top_brechas.copy()
    top["brecha_pct"] = top["brecha_pct"].round(1)

    proyectos = result.proyectos.copy()
    proyectos["prioridad"] = proyectos["prioridad"].round(3)

    return "\n\n".join(
        [
            "## Resumen generado",
            f"Empresa evaluada: **{resumen['empresa_nombre']}**.",
            f"Estandar usado: **{resumen['estandar_id']}**.",
            f"Madurez global: **{resumen['madurez_global_pct']}%**.",
            f"Brecha global: **{resumen['brecha_global_pct']}%**.",
            f"Controles evaluados: **{resumen['controles_evaluados']}**.",
            f"Capitulo mas debil: **{resumen['capitulo_mas_debil']}**.",
            f"Capacidad operacional mas debil: **{resumen['capacidad_mas_debil']}**.",
            "### Madurez por capitulo",
            _markdown_table(
                capitulos,
                ["capitulo", "controles", "madurez_pct", "brecha_pct"],
                ["Capitulo", "Controles", "Madurez %", "Brecha %"],
            ),
            "### Top brechas",
            _markdown_table(
                top,
                ["control_id", "control_nombre", "capitulo", "brecha_pct"],
                ["Control", "Nombre", "Capitulo", "Brecha %"],
                rows=8,
            ),
            "### Proyectos priorizados",
            _markdown_table(
                proyectos,
                ["proyecto_id", "titulo", "plazo", "esfuerzo_jornadas", "controles_relacionados", "prioridad"],
                ["Proyecto", "Titulo", "Plazo", "Jornadas", "Controles", "Prioridad"],
            ),
            "### Capacidad operacional",
            _markdown_table(
                result.capacidad_operacional.assign(madurez_pct=result.capacidad_operacional["madurez_pct"].round(1)),
                ["atributo", "controles", "madurez_pct"],
                ["Capacidad", "Controles", "Madurez %"],
                rows=8,
            )
            if not result.capacidad_operacional.empty
            else "Sin datos de capacidad operacional.",
        ]
    )


def render_slides_summary(result: MetricResult) -> str:
    resumen = result.resumen
    top = result.top_brechas.copy()
    top["brecha_pct"] = top["brecha_pct"].round(1)
    proyectos = result.proyectos.copy()
    proyectos["prioridad"] = proyectos["prioridad"].round(3)

    return "\n\n".join(
        [
            f"- Madurez global: **{resumen['madurez_global_pct']}%**",
            f"- Brecha global: **{resumen['brecha_global_pct']}%**",
            f"- Controles evaluados: **{resumen['controles_evaluados']}**",
            f"- Capitulo mas debil: **{resumen['capitulo_mas_debil']}**",
            f"- Capacidad mas debil: **{resumen['capacidad_mas_debil']}**",
            "## Brechas principales",
            _markdown_table(
                top,
                ["control_id", "control_nombre", "brecha_pct"],
                ["Control", "Nombre", "Brecha %"],
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
