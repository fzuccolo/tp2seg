from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from app.metricas import MetricResult


MATURITY_ORDER = [
    "0 - Inexistente",
    "1 - Inicial",
    "2 - Gestionado",
    "3 - Definido",
    "4 - Cuantitativo",
    "5 - Optimizado",
]
CHAPTER_ORDER = [
    "5 - Controles Organizativos",
    "6 - Controles de Personas",
    "7 - Controles Físicos",
    "8 - Controles Tecnológicos",
]
PALETTE = ["#2563eb", "#16a34a", "#f59e0b", "#dc2626", "#7c3aed", "#0891b2", "#be123c", "#475569"]
CHAPTER_COLORS = {
    "5 - Controles Organizativos": "#2563eb",
    "6 - Controles de Personas": "#16a34a",
    "7 - Controles Físicos": "#f59e0b",
    "8 - Controles Tecnológicos": "#dc2626",
}
MATURITY_COLORS = {
    "0 - Inexistente": "#991b1b",
    "1 - Inicial": "#dc2626",
    "2 - Gestionado": "#f97316",
    "3 - Definido": "#f59e0b",
    "4 - Cuantitativo": "#22c55e",
    "5 - Optimizado": "#0f766e",
}
QUADRANT_COLORS = {
    "Quick win": "#16a34a",
    "Proyecto estrategico": "#2563eb",
    "Mejora tactica": "#f59e0b",
    "Diferir": "#64748b",
}
PLOTLY_CONFIG = {"responsive": True, "displayModeBar": "hover", "displaylogo": False, "scrollZoom": True}


ChartFactory = Callable[[MetricResult, pd.DataFrame | None], go.Figure]
InsightFactory = Callable[[MetricResult], str]


@dataclass(frozen=True)
class ChartGuide:
    id: str
    filename: str
    title: str
    tab: str
    section: str
    purpose: str
    theory: str
    reading: str
    insight: InsightFactory
    defense: str
    question: str
    answer: str
    factory: ChartFactory


def short_text(value: str, limit: int = 48) -> str:
    text = str(value)
    return text if len(text) <= limit else text[: limit - 1] + "..."


def treemap_label(control_id: str, control_name: str, limit: int = 24) -> str:
    return f"{control_id}<br>{short_text(control_name, limit)}"


def ordered_chapters(df: pd.DataFrame) -> pd.DataFrame:
    if "capitulo" not in df.columns:
        return df
    order = {name: index for index, name in enumerate(CHAPTER_ORDER)}
    return df.assign(_orden=df["capitulo"].map(order).fillna(99)).sort_values("_orden").drop(columns=["_orden"])


def chart_layout(fig: go.Figure, height: int = 420, showlegend: bool = True) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=24, r=24, t=56, b=28),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, system-ui, sans-serif", "size": 12, "color": "#111827"},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
        modebar={
            "bgcolor": "rgba(255, 255, 255, 0.72)",
            "color": "rgba(71, 85, 105, 0.42)",
            "activecolor": "#2563eb",
        },
        showlegend=showlegend,
    )
    return fig


def style_treemap(fig: go.Figure, title: str, height: int = 560) -> go.Figure:
    fig.update_traces(
        textinfo="label",
        textfont={"size": 12},
        marker={"line": {"width": 1.2, "color": "#ffffff"}},
        tiling={"pad": 2},
    )
    fig.update_layout(
        title=title,
        uniformtext={"minsize": 10, "mode": "hide"},
        font={"family": "Inter, system-ui, sans-serif", "size": 12, "color": "#111827"},
    )
    return chart_layout(fig, height=height, showlegend=False)


def _hex_to_rgba(color: str, alpha: float) -> str:
    value = color.lstrip("#")
    if len(value) != 6:
        return f"rgba(37, 99, 235, {alpha})"
    red = int(value[0:2], 16)
    green = int(value[2:4], 16)
    blue = int(value[4:6], 16)
    return f"rgba({red}, {green}, {blue}, {alpha})"


def gauge_chart(value: float, title: str) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": "%", "font": {"size": 44, "color": "#111827"}},
            title={"text": title, "font": {"size": 16, "color": "#374151"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 0},
                "bar": {"color": "#2563eb", "thickness": 0.28},
                "bgcolor": "#f8fafc",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 30], "color": "#fee2e2"},
                    {"range": [30, 70], "color": "#fef3c7"},
                    {"range": [70, 100], "color": "#dcfce7"},
                ],
            },
        )
    )
    return chart_layout(fig, height=310, showlegend=False)


def radar_chart(df: pd.DataFrame, label_col: str, value_col: str, title: str, color: str = "#2563eb") -> go.Figure:
    if df.empty:
        return chart_layout(go.Figure(), height=430, showlegend=False)
    frame = df.copy()
    labels = frame[label_col].astype(str).tolist()
    values = frame[value_col].astype(float).clip(0, 100).round(1).tolist()
    labels_closed = labels + labels[:1]
    values_closed = values + values[:1]
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values_closed,
            theta=labels_closed,
            fill="toself",
            name=title,
            line={"color": color, "width": 2},
            fillcolor=_hex_to_rgba(color, 0.18),
        )
    )
    fig.update_layout(title=title, polar={"radialaxis": {"visible": True, "range": [0, 100]}}, showlegend=False)
    return chart_layout(fig, height=440, showlegend=False)


def maturity_stack(matrix: pd.DataFrame) -> pd.DataFrame:
    if matrix.empty:
        return pd.DataFrame()
    maturity_cols = [col for col in MATURITY_ORDER if col in matrix.columns]
    return matrix.melt(id_vars="capitulo", value_vars=maturity_cols, var_name="madurez", value_name="controles")


def pareto_chart(df: pd.DataFrame, title: str) -> go.Figure:
    if df.empty:
        return chart_layout(go.Figure(), height=520, showlegend=False)
    pareto = df.sort_values("peso_brecha", ascending=False).head(20).copy()
    total = max(float(pareto["peso_brecha"].sum()), 1.0)
    pareto["brecha_acum_pct"] = pareto["peso_brecha"].cumsum() / total * 100
    pareto["control_label"] = pareto["control_id"].astype(str) + " · " + pareto["control_nombre"].map(lambda x: short_text(x, 34))

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=pareto["control_label"],
            y=pareto["peso_brecha"],
            marker_color=pareto["capitulo"].map(CHAPTER_COLORS).fillna("#64748b"),
            name="Brecha ponderada",
            hovertext=pareto["hallazgo"],
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=pareto["control_label"],
            y=pareto["brecha_acum_pct"],
            mode="lines+markers",
            marker={"color": "#111827", "size": 7},
            line={"color": "#111827", "width": 2},
            name="Acumulado %",
        ),
        secondary_y=True,
    )
    fig.update_xaxes(tickangle=-35)
    fig.update_yaxes(title_text="Brecha ponderada", secondary_y=False)
    fig.update_yaxes(title_text="Acumulado %", range=[0, 105], secondary_y=True)
    fig.update_layout(title=title)
    return chart_layout(fig, height=540)


def impact_matrix(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return chart_layout(go.Figure(), height=440, showlegend=False)
    frame = df.copy()
    effort_threshold = frame.loc[frame["esfuerzo_jornadas"] > 0, "esfuerzo_jornadas"].median()
    priority_threshold = frame.loc[frame["prioridad"] > 0, "prioridad"].median()
    effort_threshold = float(effort_threshold) if pd.notna(effort_threshold) else 0.0
    priority_threshold = float(priority_threshold) if pd.notna(priority_threshold) else 0.0
    fig = px.scatter(
        frame,
        x="esfuerzo_jornadas",
        y="prioridad",
        size="controles_relacionados",
        color="cuadrante",
        hover_name="titulo",
        hover_data=["proyecto_id", "plazo", "tipo_seguridad", "controles_relacionados"],
        color_discrete_map=QUADRANT_COLORS,
        labels={"esfuerzo_jornadas": "Esfuerzo (jornadas)", "prioridad": "Impacto / prioridad"},
    )
    fig.add_vline(x=effort_threshold, line_width=1, line_dash="dash", line_color="#94a3b8")
    fig.add_hline(y=priority_threshold, line_width=1, line_dash="dash", line_color="#94a3b8")
    fig.update_layout(title="Matriz esfuerzo / impacto")
    return chart_layout(fig, height=470)


def roadmap_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return chart_layout(go.Figure(), height=430, showlegend=False)
    frame = df.head(20).copy()
    frame["label"] = frame["proyecto_id"].astype(str) + " · " + frame["titulo"].map(lambda x: short_text(x, 28))
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=frame["label"],
            y=frame["esfuerzo_jornadas"],
            marker_color=frame["plazo"].map({"Corto": "#16a34a", "Medio": "#f59e0b", "Largo": "#dc2626"}).fillna("#64748b"),
            name="Esfuerzo",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=frame["label"],
            y=frame["esfuerzo_acumulado"],
            fill="tozeroy",
            mode="lines+markers",
            marker={"color": "#7c3aed", "size": 6},
            line={"color": "#7c3aed", "width": 2},
            name="Esfuerzo acumulado",
        ),
        secondary_y=True,
    )
    fig.update_xaxes(tickangle=-35)
    fig.update_yaxes(title_text="Jornadas", secondary_y=False)
    fig.update_yaxes(title_text="Jornadas acumuladas", secondary_y=True)
    fig.update_layout(title="Esfuerzo a optimizado")
    return chart_layout(fig, height=500)


def sankey_chart(trazabilidad: pd.DataFrame) -> go.Figure:
    if trazabilidad.empty:
        return chart_layout(go.Figure(), height=520, showlegend=False)
    top_controls = (
        trazabilidad.groupby(["capitulo", "control_id", "control_nombre"], as_index=False)["peso_brecha"]
        .sum()
        .sort_values("peso_brecha", ascending=False)
        .head(16)
    )
    frame = trazabilidad.merge(top_controls[["control_id"]], on="control_id", how="inner")
    frame = frame[frame["proyecto_id"].notna()].copy()
    if frame.empty:
        return chart_layout(go.Figure(), height=520, showlegend=False)

    chapter_links = frame.groupby(["capitulo", "control_id", "control_nombre"], as_index=False)["peso_brecha"].sum()
    project_links = frame.groupby(["control_id", "control_nombre", "proyecto_id", "titulo"], as_index=False)["peso_brecha"].sum()

    labels: list[str] = []
    colors: list[str] = []
    index: dict[str, int] = {}

    def node(key: str, label: str, color: str) -> int:
        if key not in index:
            index[key] = len(labels)
            labels.append(label)
            colors.append(color)
        return index[key]

    sources: list[int] = []
    targets: list[int] = []
    values: list[float] = []

    for _, row in chapter_links.iterrows():
        chapter_key = f"cap:{row['capitulo']}"
        control_key = f"ctrl:{row['control_id']}"
        sources.append(node(chapter_key, str(row["capitulo"]), CHAPTER_COLORS.get(row["capitulo"], "#64748b")))
        targets.append(node(control_key, f"{row['control_id']} · {short_text(row['control_nombre'], 26)}", "#94a3b8"))
        values.append(max(float(row["peso_brecha"]), 0.01))

    for _, row in project_links.iterrows():
        control_key = f"ctrl:{row['control_id']}"
        project_key = f"proy:{row['proyecto_id']}"
        sources.append(node(control_key, f"{row['control_id']} · {short_text(row['control_nombre'], 26)}", "#94a3b8"))
        targets.append(node(project_key, f"{row['proyecto_id']} · {short_text(row['titulo'], 28)}", "#0f766e"))
        values.append(max(float(row["peso_brecha"]), 0.01))

    fig = go.Figure(
        data=[
            go.Sankey(
                node={"pad": 12, "thickness": 14, "line": {"color": "#e5e7eb", "width": 0.5}, "label": labels, "color": colors},
                link={"source": sources, "target": targets, "value": values, "color": "rgba(37, 99, 235, 0.18)"},
            )
        ]
    )
    fig.update_layout(title="Trazabilidad capítulo → control → proyecto")
    return chart_layout(fig, height=560, showlegend=False)


def _controls(result: MetricResult, visible_controls: pd.DataFrame | None) -> pd.DataFrame:
    return visible_controls.copy() if visible_controls is not None else result.controles.copy()


def fig_ejecutivo_madurez_global(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    return gauge_chart(result.resumen["madurez_global_pct"], "Madurez global")


def fig_ejecutivo_madurez_capitulo(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    caps = ordered_chapters(result.capitulos.copy())
    fig = px.bar(
        caps,
        x="capitulo",
        y="madurez_pct",
        color="capitulo",
        text=caps["madurez_pct"].round(1),
        color_discrete_map=CHAPTER_COLORS,
        labels={"madurez_pct": "Madurez %", "capitulo": ""},
        range_y=[0, 100],
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    return chart_layout(fig, height=330, showlegend=False)


def fig_ejecutivo_distribucion_cmmi(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    dist = result.madurez_distribucion.copy()
    fig = px.pie(
        dist,
        names="madurez_nombre",
        values="controles",
        hole=0.58,
        color="madurez_nombre",
        color_discrete_map=MATURITY_COLORS,
    )
    return chart_layout(fig, height=330)


def fig_ejecutivo_radar_capitulos(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    return radar_chart(ordered_chapters(result.capitulos.copy()), "capitulo", "madurez_pct", "Madurez por capítulo", "#2563eb")


def fig_ejecutivo_capacidades(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    frame = result.capacidad_operacional.sort_values("madurez_pct").head(12)
    return radar_chart(frame, "atributo", "madurez_pct", "Capacidad operacional", "#7c3aed")


def fig_mapa_matriz_cmmi(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    matrix = ordered_chapters(result.matriz_madurez.copy())
    maturity_cols = [col for col in MATURITY_ORDER if col in matrix.columns]
    fig = px.imshow(
        matrix[maturity_cols],
        x=maturity_cols,
        y=matrix["capitulo"],
        text_auto=True,
        color_continuous_scale="Blues",
        labels={"x": "Nivel CMMI", "y": "Capítulo", "color": "Controles"},
    )
    return chart_layout(fig, height=440, showlegend=False)


def fig_mapa_cmmi_capitulo(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    stacked = maturity_stack(ordered_chapters(result.matriz_madurez.copy()))
    fig = px.bar(
        stacked,
        x="capitulo",
        y="controles",
        color="madurez",
        color_discrete_map=MATURITY_COLORS,
        labels={"capitulo": "", "controles": "Controles", "madurez": "Madurez"},
    )
    return chart_layout(fig, height=440)


def fig_mapa_superficie_controles(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    frame = _controls(result, visible_controls)
    frame["control_label"] = frame.apply(lambda row: treemap_label(row["control_id"], row["control_nombre"]), axis=1)
    fig = px.treemap(
        frame,
        path=["capitulo", "control_label"],
        values="peso",
        color="cumplimiento_pct",
        color_continuous_scale=["#dc2626", "#f59e0b", "#16a34a"],
        range_color=[0, 100],
        hover_data=["madurez_nombre", "peso_brecha", "entrevistado"],
    )
    return style_treemap(fig, "Controles por capítulo coloreados por madurez", height=590)


def fig_perfil_funciones(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    return radar_chart(result.ciberfunciones, "atributo", "madurez_pct", "Funciones", "#0891b2")


def fig_perfil_capacidad_operacional(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    frame = result.capacidad_operacional.sort_values("madurez_pct", ascending=True)
    fig = px.bar(
        frame,
        x="madurez_pct",
        y="atributo",
        orientation="h",
        color="brecha_pct",
        text=frame["madurez_pct"].round(1) if not frame.empty else None,
        color_continuous_scale=["#16a34a", "#f59e0b", "#dc2626"],
        range_x=[0, 100],
        labels={"madurez_pct": "Madurez %", "atributo": "", "brecha_pct": "Brecha %"},
    )
    fig.update_traces(texttemplate="%{text:.1f}%")
    return chart_layout(fig, height=520, showlegend=False)


def _attribute_bar(frame: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        frame,
        x="madurez_pct",
        y="atributo",
        orientation="h",
        color="atributo",
        text=frame["madurez_pct"].round(1) if not frame.empty else None,
        color_discrete_sequence=PALETTE,
        range_x=[0, 100],
        labels={"madurez_pct": "Madurez %", "atributo": ""},
    )
    fig.update_traces(texttemplate="%{text:.1f}%")
    return chart_layout(fig, height=390, showlegend=False)


def fig_perfil_cid(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    return _attribute_bar(result.propiedades_seguridad)


def fig_perfil_tipo_control(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    return _attribute_bar(result.tipo_control)


def fig_perfil_dominios(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    return _attribute_bar(result.dominios_seguridad)


def fig_brechas_pareto(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    return pareto_chart(_controls(result, visible_controls), "Controles que explican la brecha")


def fig_brechas_treemap(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    frame = _controls(result, visible_controls)
    frame["control_label"] = frame.apply(lambda row: treemap_label(row["control_id"], row["control_nombre"]), axis=1)
    fig = px.treemap(
        frame.sort_values("peso_brecha", ascending=False).head(35),
        path=["capitulo", "control_label"],
        values="peso_brecha",
        color="brecha_pct",
        color_continuous_scale=["#fef3c7", "#f97316", "#991b1b"],
        hover_data=["madurez_nombre", "hallazgo", "entrevistado"],
    )
    return style_treemap(fig, "Brecha por capítulo y control", height=560)


def fig_brechas_madurez_vs_brecha(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    frame = _controls(result, visible_controls)
    fig = px.scatter(
        frame,
        x="cumplimiento_pct",
        y="peso_brecha",
        color="capitulo",
        size="peso",
        hover_name="control_id",
        hover_data=["control_nombre", "madurez_nombre", "entrevistado"],
        labels={"cumplimiento_pct": "Madurez %", "peso_brecha": "Brecha ponderada"},
        color_discrete_map=CHAPTER_COLORS,
    )
    fig.add_vline(x=70, line_width=1, line_dash="dash", line_color="#94a3b8")
    return chart_layout(fig, height=520)


def fig_plan_plazo(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    frame = result.proyectos_plazo.copy()
    fig = px.bar(
        frame,
        x="plazo",
        y="prioridad",
        color="plazo",
        text=frame["prioridad"].round(2) if not frame.empty else None,
        color_discrete_map={"Corto": "#16a34a", "Medio": "#f59e0b", "Largo": "#dc2626", "": "#64748b"},
        labels={"prioridad": "Prioridad acumulada", "plazo": "Plazo"},
    )
    return chart_layout(fig, height=380, showlegend=False)


def fig_plan_compromiso_plazo(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    frame = result.proyectos_plazo.copy()
    fig = px.pie(frame, names="plazo", values="proyectos", hole=0.5, color="plazo", color_discrete_sequence=PALETTE)
    return chart_layout(fig, height=380)


def fig_plan_tipo_proyecto(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    fig = px.pie(result.proyectos_tipo, names="tipo", values="controles", hole=0.5, color_discrete_sequence=PALETTE)
    return chart_layout(fig, height=380)


def fig_plan_capitulo(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    frame = ordered_chapters(result.proyectos_capitulo.copy())
    fig = px.bar(
        frame,
        x="capitulo",
        y="prioridad",
        color="capitulo",
        text=frame["proyectos"] if not frame.empty else None,
        color_discrete_map=CHAPTER_COLORS,
        labels={"prioridad": "Prioridad", "capitulo": ""},
    )
    return chart_layout(fig, height=430, showlegend=False)


def fig_plan_capacidad(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    frame = result.proyectos_capacidad.sort_values("prioridad", ascending=False).head(12)
    return radar_chart(frame, "capacidad", "prioridad_pct", "Prioridad relativa por capacidad", "#0891b2")


def fig_plan_roadmap(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    return roadmap_chart(result.esfuerzo_roadmap)


def fig_plan_quick_wins(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    return impact_matrix(result.quick_wins)


def fig_plan_esfuerzo_proyecto(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    frame = result.proyectos.sort_values("esfuerzo_jornadas", ascending=False).head(18).copy()
    frame["label"] = frame["proyecto_id"].astype(str) + " · " + frame["titulo"].map(lambda x: short_text(x, 34))
    fig = px.bar(
        frame.sort_values("esfuerzo_jornadas"),
        x="esfuerzo_jornadas",
        y="label",
        orientation="h",
        color="plazo",
        hover_data=["prioridad", "controles_relacionados", "tipo_seguridad"],
        color_discrete_sequence=PALETTE,
        labels={"esfuerzo_jornadas": "Jornadas", "label": ""},
    )
    return chart_layout(fig, height=560)


def fig_trazabilidad_sankey(result: MetricResult, visible_controls: pd.DataFrame | None = None) -> go.Figure:
    return sankey_chart(result.trazabilidad)


def _weakest_chapter(result: MetricResult) -> pd.Series:
    return result.capitulos.sort_values("madurez_pct").iloc[0]


def _strongest_chapter(result: MetricResult) -> pd.Series:
    return result.capitulos.sort_values("madurez_pct").iloc[-1]


def _weakest_attr(frame: pd.DataFrame) -> pd.Series:
    return frame.sort_values("madurez_pct").iloc[0]


def _top_gap(result: MetricResult) -> pd.Series:
    return result.top_brechas.sort_values("peso_brecha", ascending=False).iloc[0]


def _top_project(result: MetricResult) -> pd.Series:
    return result.proyectos.sort_values("prioridad", ascending=False).iloc[0]


def _top_plazo(result: MetricResult) -> pd.Series:
    return result.proyectos_plazo.sort_values("prioridad", ascending=False).iloc[0]


def _top_capacity_plan(result: MetricResult) -> pd.Series:
    return result.proyectos_capacidad.sort_values("prioridad", ascending=False).iloc[0]


def _insight_global(result: MetricResult) -> str:
    resumen = result.resumen
    return (
        f"La madurez global es {resumen['madurez_global_pct']}% y la brecha global es {resumen['brecha_global_pct']}%. "
        "La lectura defendible es que existe base operativa, pero falta formalizar, medir y sostener la mejora."
    )


def _insight_chapter(result: MetricResult) -> str:
    weak = _weakest_chapter(result)
    strong = _strongest_chapter(result)
    return (
        f"El capítulo más débil es {weak['capitulo']} con {float(weak['madurez_pct']):.1f}% de madurez. "
        f"El más fuerte es {strong['capitulo']} con {float(strong['madurez_pct']):.1f}%, pero todos quedan lejos de un nivel optimizado."
    )


def _insight_distribution(result: MetricResult) -> str:
    low = int(result.madurez_distribucion.loc[result.madurez_distribucion["nivel_madurez"].isin([0, 1, 2]), "controles"].sum())
    total = int(result.madurez_distribucion["controles"].sum())
    return f"{low} de {total} controles están en niveles 0 a 2. Esto muestra prácticas existentes pero todavía poco estandarizadas o medidas."


def _insight_capabilities(result: MetricResult) -> str:
    weak = _weakest_attr(result.capacidad_operacional)
    return f"La capacidad operacional más débil es {weak['atributo']} con {float(weak['madurez_pct']):.1f}% de madurez."


def _insight_functions(result: MetricResult) -> str:
    weak = _weakest_attr(result.ciberfunciones)
    return f"La función más débil es {weak['atributo']} con {float(weak['madurez_pct']):.1f}%, lo que orienta la conversación hacia resiliencia y seguimiento."


def _insight_attribute(frame_name: str) -> InsightFactory:
    def insight(result: MetricResult) -> str:
        frame = getattr(result, frame_name)
        weak = _weakest_attr(frame)
        strong = frame.sort_values("madurez_pct").iloc[-1]
        return f"El atributo más débil es {weak['atributo']} ({float(weak['madurez_pct']):.1f}%) y el más fuerte es {strong['atributo']} ({float(strong['madurez_pct']):.1f}%)."

    return insight


def _insight_gap(result: MetricResult) -> str:
    top = _top_gap(result)
    return (
        f"El control con mayor brecha ponderada es {top['control_id']} - {top['control_nombre']} "
        f"con peso de brecha {float(top['peso_brecha']):.2f}."
    )


def _insight_plan(result: MetricResult) -> str:
    resumen = result.resumen
    top = _top_project(result)
    return (
        f"El plan tiene {resumen['proyectos']} iniciativas, {resumen['quick_wins']} quick wins y {resumen['esfuerzo_total']} jornadas. "
        f"La prioridad más alta es {top['proyecto_id']} - {top['titulo']}."
    )


def _insight_plazo(result: MetricResult) -> str:
    top = _top_plazo(result)
    return f"El plazo con mayor prioridad acumulada es {top['plazo']}, con {int(top['proyectos'])} proyectos y prioridad {float(top['prioridad']):.2f}."


def _insight_tipo_proyecto(result: MetricResult) -> str:
    top = result.proyectos_tipo.sort_values("controles", ascending=False).iloc[0]
    return f"El tipo de proyecto con mayor cobertura de controles es {top['tipo']}, con {float(top['controles']):.0f} vínculos a controles."


def _insight_capitulo_plan(result: MetricResult) -> str:
    top = result.proyectos_capitulo.sort_values("prioridad", ascending=False).iloc[0]
    return f"El capítulo con mayor prioridad de intervención es {top['capitulo']}, con {int(top['proyectos'])} proyectos vinculados."


def _insight_capacidad_plan(result: MetricResult) -> str:
    top = _top_capacity_plan(result)
    return f"La capacidad con mayor prioridad relativa del plan es {top['capacidad']}, asociada a {int(top['proyectos'])} proyectos."


def _insight_roadmap(result: MetricResult) -> str:
    total = float(result.esfuerzo_roadmap["esfuerzo_jornadas"].sum())
    first = result.esfuerzo_roadmap.iloc[0]
    return f"El roadmap acumula {total:.0f} jornadas y comienza por {first['proyecto_id']} - {first['titulo']}."


def _insight_quick_wins(result: MetricResult) -> str:
    quick = result.quick_wins[result.quick_wins["cuadrante"] == "Quick win"]
    first = quick.sort_values("prioridad", ascending=False).iloc[0]
    return f"Hay {len(quick)} quick wins. El primero es {first['proyecto_id']} - {first['titulo']} por su combinación de impacto y esfuerzo relativo."


def _insight_esfuerzo(result: MetricResult) -> str:
    top = result.proyectos.sort_values("esfuerzo_jornadas", ascending=False).iloc[0]
    return f"El proyecto de mayor esfuerzo es {top['proyecto_id']} - {top['titulo']} con {int(top['esfuerzo_jornadas'])} jornadas."


def _insight_traceability(result: MetricResult) -> str:
    links = int(len(result.trazabilidad))
    controls = int(result.trazabilidad["control_id"].nunique())
    projects = int(result.trazabilidad["proyecto_id"].nunique())
    return f"La trazabilidad conecta {controls} controles con {projects} proyectos mediante {links} vínculos control-proyecto."


def chart_guides() -> list[ChartGuide]:
    return [
        ChartGuide(
            "ejecutivo-madurez-global",
            "01-ejecutivo-madurez-global.png",
            "Postura global",
            "1 Ejecutivo",
            "Postura general",
            "Resume la postura de seguridad en un indicador ejecutivo de madurez.",
            "Tablero de control y KGI: sintetiza el estado frente a un objetivo de gobierno.",
            "El valor central es la madurez porcentual. La escala visual ayuda a distinguir zona baja, media y alta.",
            _insight_global,
            "Usarlo como apertura: es el número que resume el diagnóstico, pero no reemplaza el análisis por capítulo y control.",
            "¿Por qué usar un indicador global si seguridad es multidimensional?",
            "Porque sirve para dirección; después se desagrega en capítulos, controles, brechas y proyectos para evitar una lectura simplista.",
            fig_ejecutivo_madurez_global,
        ),
        ChartGuide(
            "ejecutivo-madurez-capitulo",
            "02-ejecutivo-madurez-capitulo.png",
            "Madurez por capítulo",
            "1 Ejecutivo",
            "Madurez por capítulo",
            "Compara los cuatro capítulos evaluables de ISO/IEC 27002:2022.",
            "ISO 27002 organiza controles en organizativos, personas, físicos y tecnológicos.",
            "Cada barra muestra madurez promedio ponderada por capítulo. Más bajo implica mayor distancia al objetivo.",
            _insight_chapter,
            "Explicar que el diagnóstico no queda en un promedio: muestra dónde concentrar la mirada inicial.",
            "¿El capítulo más bajo es automáticamente el único prioritario?",
            "No. Marca una alerta, pero la priorización final usa brecha ponderada, capacidad afectada y proyectos vinculados.",
            fig_ejecutivo_madurez_capitulo,
        ),
        ChartGuide(
            "ejecutivo-distribucion-cmmi",
            "03-ejecutivo-distribucion-cmmi.png",
            "Distribución CMMI",
            "1 Ejecutivo",
            "Distribución CMMI",
            "Muestra cuántos controles caen en cada nivel de madurez.",
            "Escala CMMI 0 a 5: inexistente, inicial, gestionado, definido, cuantitativo y optimizado.",
            "El gráfico reparte controles por nivel. Una concentración en niveles bajos implica prácticas poco repetibles o poco medidas.",
            _insight_distribution,
            "Usarlo para defender que el promedio no oculta la forma de la distribución.",
            "¿Por qué varios controles tienen la misma brecha?",
            "Porque comparten nivel CMMI; por eso el ranking usa brecha ponderada y no solo porcentaje de brecha.",
            fig_ejecutivo_distribucion_cmmi,
        ),
        ChartGuide(
            "ejecutivo-radar-capitulos",
            "04-ejecutivo-radar-capitulos.png",
            "Radar ejecutivo",
            "1 Ejecutivo",
            "Radar ejecutivo",
            "Permite ver balance o desbalance entre capítulos ISO.",
            "Radar de KPI: útil para comparar dimensiones equivalentes en una misma escala.",
            "Cuanto más cercano al borde, mayor madurez. Un polígono irregular muestra desequilibrio de postura.",
            _insight_chapter,
            "Explicar visualmente que TecnoHogar tiene brecha generalizada y no un único punto aislado.",
            "¿El radar reemplaza a la barra por capítulo?",
            "No. La barra compara con precisión; el radar ayuda a contar balance de postura.",
            fig_ejecutivo_radar_capitulos,
        ),
        ChartGuide(
            "ejecutivo-capacidades",
            "05-ejecutivo-capacidades.png",
            "Capacidades operacionales",
            "1 Ejecutivo",
            "Capacidades operacionales",
            "Traduce controles ISO a capacidades de gestión entendibles para operar seguridad.",
            "Métrica por capacidad: conecta controles con procesos de gestión y operación.",
            "Cada eje es una capacidad. La distancia al borde indica madurez relativa.",
            _insight_capabilities,
            "Usarlo para pasar del estándar a lenguaje de gestión: qué capacidad falta desarrollar.",
            "¿Las capacidades son parte literal de ISO?",
            "No son capítulos ISO; son una agrupación operativa definida para interpretar mejor los controles.",
            fig_ejecutivo_capacidades,
        ),
        ChartGuide(
            "mapa-matriz-cmmi",
            "06-mapa-matriz-cmmi.png",
            "Matriz CMMI por capítulo",
            "2 Mapa ISO",
            "Mapa de madurez ISO",
            "Muestra la cantidad de controles de cada capítulo en cada nivel CMMI.",
            "Mapa de calor: cruza dimensiones para encontrar concentración de debilidades.",
            "Filas son capítulos, columnas son niveles CMMI y el color/celda indica cantidad de controles.",
            _insight_distribution,
            "Explicar que este es el mapa completo de madurez, no solo el promedio.",
            "¿Por qué sirve cruzar capítulo y CMMI?",
            "Porque permite ver si un capítulo tiene muchos controles bajos o pocos controles críticos.",
            fig_mapa_matriz_cmmi,
        ),
        ChartGuide(
            "mapa-cmmi-capitulo",
            "07-mapa-cmmi-capitulo.png",
            "CMMI por capítulo",
            "2 Mapa ISO",
            "CMMI por capítulo",
            "Compara la composición de niveles CMMI dentro de cada capítulo.",
            "Distribución por madurez: muestra dónde hay prácticas iniciales, definidas o medidas.",
            "Cada barra apilada acumula controles del capítulo y los colores indican nivel CMMI.",
            _insight_distribution,
            "Usarlo para mostrar que la brecha sale de controles concretos, no de percepción general.",
            "¿Se evaluaron todos los controles con la misma escala?",
            "Sí. Todos los controles aplicables usan CMMI 0 a 5 y luego se ponderan por peso.",
            fig_mapa_cmmi_capitulo,
        ),
        ChartGuide(
            "mapa-superficie-controles",
            "08-mapa-superficie-controles.png",
            "Superficie de controles",
            "2 Mapa ISO",
            "Superficie de controles",
            "Permite inspeccionar los 93 controles por capítulo y madurez.",
            "Treemap: representa jerarquía y volumen; en este caso capítulo y control.",
            "El tamaño responde al peso del control y el color al porcentaje de cumplimiento.",
            _insight_chapter,
            "Usarlo en demo para mostrar navegación granular: de capítulo a control individual.",
            "¿Están las 93 métricas en estos cuadrados?",
            "Sí, cada cuadrado representa un control evaluado; los filtros pueden cambiar qué subconjunto se ve.",
            fig_mapa_superficie_controles,
        ),
        ChartGuide(
            "perfil-funciones",
            "09-perfil-funciones.png",
            "Funciones de ciberseguridad",
            "3 Perfil",
            "Funciones de ciberseguridad",
            "Agrupa controles según funciones de identificar, proteger, detectar, responder y recuperar.",
            "Modelo funcional de seguridad: ayuda a leer postura por ciclo operativo.",
            "Cada eje representa una función; los valores más bajos muestran funciones con menor madurez.",
            _insight_functions,
            "Conectar con resiliencia: no alcanza proteger, también hay que detectar, responder y recuperar.",
            "¿Por qué usar funciones si ya tenemos capítulos ISO?",
            "Porque los capítulos explican el estándar y las funciones explican la operación diaria.",
            fig_perfil_funciones,
        ),
        ChartGuide(
            "perfil-capacidad-operacional",
            "10-perfil-capacidad-operacional.png",
            "Capacidad operacional",
            "3 Perfil",
            "Capacidad operacional",
            "Ordena capacidades de menor a mayor madurez para priorizar gestión.",
            "KPI de gestión: transforma mediciones de controles en capacidades accionables.",
            "Las barras horizontales muestran madurez; el color resalta la brecha asociada.",
            _insight_capabilities,
            "Usarlo para justificar proyectos orientados a vulnerabilidades, monitoreo, accesos o gobierno.",
            "¿Qué diferencia hay entre capacidad y proyecto?",
            "La capacidad describe qué tan madura está una práctica; el proyecto es la acción para mejorarla.",
            fig_perfil_capacidad_operacional,
        ),
        ChartGuide(
            "perfil-cid",
            "11-perfil-cid.png",
            "Perfil CID",
            "3 Perfil",
            "CID",
            "Mide cómo se comportan los controles asociados a confidencialidad, integridad y disponibilidad.",
            "CID es el eje clásico para analizar impacto de seguridad de la información.",
            "Cada barra muestra madurez promedio de controles vinculados a una propiedad CID.",
            _insight_attribute("propiedades_seguridad"),
            "Relacionar con TP1: activos y criticidad se explican por confidencialidad, integridad y disponibilidad.",
            "¿CID se mide sobre activos o controles?",
            "En TP1 se usó para activos; en este tablero se usa para leer controles asociados a esas propiedades.",
            fig_perfil_cid,
        ),
        ChartGuide(
            "perfil-tipo-control",
            "12-perfil-tipo-control.png",
            "Tipo de control",
            "3 Perfil",
            "Tipo de control",
            "Compara madurez de controles preventivos, detectivos y correctivos.",
            "Defensa en profundidad: prevenir, detectar y corregir son capas complementarias.",
            "Las barras muestran qué tipo de control tiene menor madurez relativa.",
            _insight_attribute("tipo_control"),
            "Explicar que seguridad madura no es solo prevenir: también requiere detección y respuesta.",
            "¿Qué pasa si un tipo queda más alto?",
            "No significa que alcance; indica mejor desarrollo relativo frente a los otros tipos.",
            fig_perfil_tipo_control,
        ),
        ChartGuide(
            "perfil-dominios",
            "13-perfil-dominios.png",
            "Dominios de seguridad",
            "3 Perfil",
            "Dominios",
            "Agrupa controles en dominios ejecutivos: gobierno, protección, defensa y resiliencia.",
            "Lectura de tablero: reduce complejidad para conversar con dirección.",
            "Cada barra muestra madurez promedio por dominio.",
            _insight_attribute("dominios_seguridad"),
            "Usarlo para traducir el diagnóstico técnico a una conversación de gobierno.",
            "¿Estos dominios reemplazan ISO?",
            "No. Son una vista de análisis construida encima del catálogo ISO.",
            fig_perfil_dominios,
        ),
        ChartGuide(
            "brechas-pareto",
            "14-brechas-pareto.png",
            "Pareto de brechas",
            "4 Brechas",
            "Pareto de brechas",
            "Ordena los controles que más explican la brecha ponderada.",
            "Principio de Pareto: encontrar pocos factores que concentran impacto.",
            "Las barras muestran brecha ponderada y la línea muestra acumulado porcentual.",
            _insight_gap,
            "Usarlo como puente hacia el plan: primero atender lo que más pesa en la brecha.",
            "¿Por qué no priorizar todos los controles en orden ISO?",
            "Porque el orden del estándar no indica impacto; el Pareto prioriza por brecha y peso.",
            fig_brechas_pareto,
        ),
        ChartGuide(
            "brechas-treemap",
            "15-brechas-treemap.png",
            "Treemap de brecha",
            "4 Brechas",
            "Concentración de riesgo",
            "Muestra dónde se concentra la brecha por capítulo y control.",
            "Visual de riesgo: tamaño y color ayudan a detectar concentración.",
            "El tamaño representa peso de brecha y el color la brecha porcentual.",
            _insight_gap,
            "Explicar visualmente que las brechas combinan capítulo, control y severidad.",
            "¿El cuadrado más grande siempre es el más urgente?",
            "Es candidato fuerte, pero la urgencia final también depende del proyecto, esfuerzo y contexto operativo.",
            fig_brechas_treemap,
        ),
        ChartGuide(
            "brechas-madurez-vs-brecha",
            "16-brechas-madurez-vs-brecha.png",
            "Madurez vs brecha",
            "4 Brechas",
            "Madurez vs brecha",
            "Cruza cumplimiento actual con brecha ponderada para distinguir controles bajos y pesados.",
            "Priorización por riesgo: combina probabilidad/impacto aproximado mediante madurez y peso.",
            "Eje X es madurez, eje Y brecha ponderada, tamaño es peso y color es capítulo.",
            _insight_gap,
            "Usarlo para explicar por qué un control puede ser más importante que otro con el mismo nivel CMMI.",
            "¿Qué significa la línea vertical en 70%?",
            "Es una referencia visual de madurez aceptable; no es una regla absoluta del estándar.",
            fig_brechas_madurez_vs_brecha,
        ),
        ChartGuide(
            "plan-plazo",
            "17-plan-plazo.png",
            "Plan por plazo",
            "5 Plan",
            "Plan por plazo",
            "Distribuye la prioridad del plan entre corto, medio y largo plazo.",
            "Planificación de tratamiento de riesgo: secuencia acciones según impacto y capacidad de ejecución.",
            "Cada barra acumula prioridad de proyectos por plazo.",
            _insight_plazo,
            "Mostrar que el plan tiene una secuencia, no una lista plana de deseos.",
            "¿Por qué no ejecutar todo a corto plazo?",
            "Porque hay restricciones de esfuerzo, dependencia y madurez organizacional.",
            fig_plan_plazo,
        ),
        ChartGuide(
            "plan-compromiso-plazo",
            "18-plan-compromiso-plazo.png",
            "Compromiso por plazo",
            "5 Plan",
            "Compromiso por plazo",
            "Muestra cuántos proyectos caen en cada horizonte temporal.",
            "Gestión de cartera: balancea cantidad de iniciativas y capacidad de absorción.",
            "Cada porción representa cantidad de proyectos por plazo.",
            _insight_plazo,
            "Usarlo para explicar carga de gestión y no solo prioridad técnica.",
            "¿Cantidad de proyectos equivale a esfuerzo?",
            "No. Por eso se complementa con roadmap y esfuerzo por proyecto.",
            fig_plan_compromiso_plazo,
        ),
        ChartGuide(
            "plan-tipo-proyecto",
            "19-plan-tipo-proyecto.png",
            "Tipo de proyecto",
            "5 Plan",
            "Tipo de proyecto",
            "Clasifica el plan por tipo de seguridad: lógica, física, organizativa o legal.",
            "Tratamiento de riesgo: las respuestas pueden ser técnicas, organizativas, físicas o legales.",
            "Cada porción muestra cobertura de controles por tipo de proyecto.",
            _insight_tipo_proyecto,
            "Usarlo para mostrar que el plan no es solo tecnología.",
            "¿Por qué mezclar proyectos técnicos y organizativos?",
            "Porque ISO 27002 cubre gobierno, personas, físico y tecnología; el tratamiento debe acompañar esa mezcla.",
            fig_plan_tipo_proyecto,
        ),
        ChartGuide(
            "plan-capitulo",
            "20-plan-capitulo.png",
            "Plan por capítulo",
            "5 Plan",
            "Plan por capítulo",
            "Relaciona prioridades del plan con capítulos ISO.",
            "Trazabilidad de tratamiento: cada iniciativa debe cubrir controles concretos.",
            "Las barras muestran prioridad por capítulo y las etiquetas cantidad de proyectos.",
            _insight_capitulo_plan,
            "Mostrar que el plan cubre los capítulos donde aparecen brechas relevantes.",
            "¿Un proyecto puede cubrir más de un capítulo?",
            "Sí. Por eso la trazabilidad control-proyecto es más importante que contar proyectos aislados.",
            fig_plan_capitulo,
        ),
        ChartGuide(
            "plan-capacidad",
            "21-plan-capacidad.png",
            "Plan por capacidad operacional",
            "5 Plan",
            "Plan por capacidad operacional",
            "Muestra qué capacidades reciben más prioridad relativa en el plan.",
            "Alineación entre diagnóstico y tratamiento: las debilidades deben aparecer en el plan.",
            "Cada eje indica prioridad relativa por capacidad.",
            _insight_capacidad_plan,
            "Usarlo para defender que el plan responde a capacidades débiles, no a ocurrencias sueltas.",
            "¿Qué pasa si una capacidad débil no recibe máxima prioridad?",
            "Puede pasar si el esfuerzo, dependencias o cobertura de controles cambian la secuencia recomendada.",
            fig_plan_capacidad,
        ),
        ChartGuide(
            "plan-roadmap",
            "22-plan-roadmap.png",
            "Roadmap de esfuerzo",
            "5 Plan",
            "Roadmap de esfuerzo",
            "Ordena iniciativas y muestra esfuerzo individual y acumulado.",
            "Gestión de ejecución: convierte el diagnóstico en una cartera implementable.",
            "Las barras son jornadas por proyecto y la línea/área acumula esfuerzo.",
            _insight_roadmap,
            "Usarlo para explicar costo de implementación y orden sugerido.",
            "¿Las jornadas son exactas?",
            "No son presupuesto cerrado; son estimación para priorizar y comparar esfuerzo relativo.",
            fig_plan_roadmap,
        ),
        ChartGuide(
            "plan-quick-wins",
            "23-plan-quick-wins.png",
            "Matriz impacto / esfuerzo",
            "5 Plan",
            "Quick wins",
            "Distingue quick wins, proyectos estratégicos, mejoras tácticas y acciones a diferir.",
            "Matriz impacto/esfuerzo: técnica de priorización para tratamiento de riesgos.",
            "Eje X es esfuerzo, eje Y prioridad; el cuadrante alto impacto/bajo esfuerzo son quick wins.",
            _insight_quick_wins,
            "Remarcar que quick win no significa superficial: significa buen retorno inicial.",
            "¿Por qué PR-10 aparece como quick win?",
            "Porque combina prioridad alta con esfuerzo relativo menor frente a otros proyectos de la cartera.",
            fig_plan_quick_wins,
        ),
        ChartGuide(
            "plan-esfuerzo-proyecto",
            "24-plan-esfuerzo-proyecto.png",
            "Esfuerzo por proyecto",
            "5 Plan",
            "Esfuerzo por proyecto",
            "Compara la carga estimada de las iniciativas.",
            "Gestión de recursos: priorizar requiere entender impacto y costo.",
            "Las barras horizontales muestran jornadas estimadas; el color marca plazo.",
            _insight_esfuerzo,
            "Usarlo para explicar por qué algunas iniciativas quedan para medio o largo plazo.",
            "¿Un proyecto grande puede ser quick win?",
            "Normalmente no; si el esfuerzo es alto, aunque tenga impacto, se trata como estratégico.",
            fig_plan_esfuerzo_proyecto,
        ),
        ChartGuide(
            "trazabilidad-sankey",
            "25-trazabilidad-sankey.png",
            "Sankey de trazabilidad",
            "6 Trazabilidad",
            "Cadena de decisión",
            "Muestra cómo capítulos ISO se conectan con controles y proyectos.",
            "Trazabilidad control -> evidencia -> brecha -> proyecto: sostiene la defensa técnica del tablero.",
            "Los flujos van de capítulo a control y de control a proyecto; el grosor representa peso de brecha.",
            _insight_traceability,
            "Usarlo al final para demostrar que cada decisión del plan es explicable y auditable.",
            "¿Qué aporta frente a una tabla?",
            "Permite ver visualmente qué controles alimentan cada proyecto y evita que el plan parezca arbitrario.",
            fig_trazabilidad_sankey,
        ),
    ]
