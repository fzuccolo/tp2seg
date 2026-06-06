from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from app.datos import list_cases, load_dataset, repo_root
from app.metricas import compute_metrics


ROOT = repo_root()
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
DEFAULT_COMPANY = "tecnohogar"
DASHBOARD_CACHE_VERSION = "story-dashboard-v7"
PLOTLY_CONFIG = {"responsive": True, "displayModeBar": "hover", "displaylogo": False, "scrollZoom": True}


@st.cache_data
def get_result(empresa_id: str, cache_version: str):
    _ = cache_version
    dataset = load_dataset(empresa_id, ROOT)
    return compute_metrics(dataset)


def pct(value: float | int) -> str:
    return f"{float(value):.1f}%"


def num(value: float | int) -> str:
    return f"{float(value):,.0f}".replace(",", ".")


def short_text(value: str, limit: int = 48) -> str:
    text = str(value)
    return text if len(text) <= limit else text[: limit - 1] + "…"


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


def show_chart(fig: go.Figure) -> None:
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


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


def section_title(title: str, detail: str = "") -> None:
    suffix = f'<span class="section-detail">{detail}</span>' if detail else ""
    st.markdown(f'<div class="section-title">{title}{suffix}</div>', unsafe_allow_html=True)


def metric_card(label: str, value: str, detail: str, accent: str = "#2563eb") -> None:
    label_text = escape(str(label))
    value_text = str(value)
    detail_text = escape(str(detail))
    value_class = "metric-value"
    if any(char.isalpha() for char in value_text) or len(value_text) > 14:
        value_class += " metric-value-text"
    if len(value_text) > 26:
        value_class += " metric-value-long"
    value_html = escape(value_text)
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color:{accent}">
          <div class="metric-label">{label_text}</div>
          <div class="{value_class}" title="{value_html}">{value_html}</div>
          <div class="metric-detail">{detail_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
            fillcolor=color.replace("#", "rgba(") if False else "rgba(37, 99, 235, 0.18)",
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

    chapter_links = (
        frame.groupby(["capitulo", "control_id", "control_nombre"], as_index=False)["peso_brecha"].sum()
    )
    project_links = (
        frame.groupby(["control_id", "control_nombre", "proyecto_id", "titulo"], as_index=False)["peso_brecha"].sum()
    )

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


def download_button(label: str, df: pd.DataFrame, filename: str) -> None:
    st.download_button(label, df.to_csv(index=False).encode("utf-8"), file_name=filename, mime="text/csv")


st.set_page_config(page_title="TP2 Seguridad - Tablero", layout="wide", initial_sidebar_state="collapsed")
st.markdown(
    """
    <style>
      .main .block-container { padding-top: 1rem; max-width: 1520px; }
      .metric-card {
        border: 1px solid #d8dee9;
        border-left: 5px solid #2563eb;
        border-radius: 8px;
        padding: 14px 16px;
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        min-height: 118px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
      }
      .metric-label {
        color: #475569;
        font-size: 0.76rem;
        text-transform: uppercase;
        letter-spacing: 0.02em;
        font-weight: 800;
      }
      .metric-value {
        color: #111827;
        font-size: 2rem;
        line-height: 1.08;
        font-weight: 850;
        margin-top: 7px;
      }
      .metric-value-text {
        font-size: 1.38rem;
        line-height: 1.15;
        overflow-wrap: break-word;
        word-break: normal;
      }
      .metric-value-long {
        font-size: 1.18rem;
        line-height: 1.14;
      }
      .metric-detail {
        color: #64748b;
        font-size: 0.88rem;
        margin-top: 6px;
      }
      .section-title {
        margin-top: 10px;
        margin-bottom: 8px;
        font-size: 1.05rem;
        font-weight: 850;
        color: #111827;
      }
      .section-detail {
        margin-left: 10px;
        color: #64748b;
        font-size: 0.86rem;
        font-weight: 650;
      }
      div[data-testid="stTabs"] button p { font-weight: 750; }
    </style>
    """,
    unsafe_allow_html=True,
)

cases = list_cases(ROOT)
default_idx = cases.index(DEFAULT_COMPANY) if DEFAULT_COMPANY in cases else 0
selected = st.sidebar.selectbox("Caso", cases, index=default_idx)
result = get_result(selected, DASHBOARD_CACHE_VERSION)
resumen = result.resumen
controles = result.controles.copy()

st.title(f"Tablero de Control de Seguridad - {resumen['empresa_nombre']}")
st.caption(f"Estandar: {resumen['estandar_id']} | Dataset: {selected} | Controles evaluados: {resumen['controles_evaluados']}")

available_chapters = ordered_chapters(controles[["capitulo"]].drop_duplicates())["capitulo"].tolist()
selected_chapters = st.sidebar.multiselect("Capitulos", available_chapters, default=available_chapters)
available_maturity = [label for label in MATURITY_ORDER if label in set(controles["madurez_nombre"].dropna())]
selected_maturity = st.sidebar.multiselect("Madurez", available_maturity, default=available_maturity)
available_interviewees = sorted([x for x in controles["entrevistado"].dropna().unique().tolist() if x])
selected_interviewees = st.sidebar.multiselect("Entrevistados", available_interviewees, default=available_interviewees)

filtered = controles[
    controles["capitulo"].isin(selected_chapters)
    & controles["madurez_nombre"].isin(selected_maturity)
    & controles["entrevistado"].isin(selected_interviewees if selected_interviewees else available_interviewees)
].copy()
if filtered.empty:
    st.sidebar.warning("Los filtros no devuelven controles; se muestran todos los controles.")
    visible_controls = controles.copy()
else:
    visible_controls = filtered

story_tabs = st.tabs(["1 Ejecutivo", "2 Mapa ISO", "3 Perfil", "4 Brechas", "5 Plan", "6 Trazabilidad", "7 Descargas"])
tab_resumen, tab_mapa, tab_perfil, tab_brechas, tab_plan, tab_trazabilidad, tab_descargas = story_tabs

with tab_resumen:
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        metric_card("Madurez global", pct(resumen["madurez_global_pct"]), "Promedio ponderado", "#2563eb")
    with k2:
        metric_card("Brecha global", pct(resumen["brecha_global_pct"]), "Distancia a optimizado", "#dc2626")
    with k3:
        metric_card("Control critico", resumen["control_mas_critico"], "Mayor brecha ponderada", "#f59e0b")
    with k4:
        metric_card("Capacidad debil", resumen["capacidad_mas_debil"], "Menor madurez", "#7c3aed")
    with k5:
        metric_card("Quick wins", str(resumen["quick_wins"]), "Impacto alto / esfuerzo bajo", "#16a34a")

    left, center, right = st.columns([1, 1.3, 1.1])
    with left:
        section_title("Postura general")
        show_chart(gauge_chart(resumen["madurez_global_pct"], "Madurez global"))
    with center:
        section_title("Madurez por capitulo")
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
        show_chart(chart_layout(fig, height=330, showlegend=False))
    with right:
        section_title("Distribucion CMMI")
        dist = result.madurez_distribucion.copy()
        fig = px.pie(
            dist,
            names="madurez_nombre",
            values="controles",
            hole=0.58,
            color="madurez_nombre",
            color_discrete_map=MATURITY_COLORS,
        )
        show_chart(chart_layout(fig, height=330))

    r1, r2 = st.columns(2)
    with r1:
        section_title("Radar ejecutivo")
        caps_radar = ordered_chapters(result.capitulos.copy())
        show_chart(radar_chart(caps_radar, "capitulo", "madurez_pct", "Madurez por capitulo", "#2563eb"))
    with r2:
        section_title("Capacidades operacionales")
        show_chart(
            radar_chart(
                result.capacidad_operacional.sort_values("madurez_pct").head(12),
                "atributo",
                "madurez_pct",
                "Capacidad operacional",
                "#7c3aed",
            )
        )

with tab_mapa:
    m1, m2 = st.columns([1.25, 1])
    with m1:
        section_title("Mapa de madurez ISO")
        matrix = ordered_chapters(result.matriz_madurez.copy())
        maturity_cols = [col for col in MATURITY_ORDER if col in matrix.columns]
        fig = px.imshow(
            matrix[maturity_cols],
            x=maturity_cols,
            y=matrix["capitulo"],
            text_auto=True,
            color_continuous_scale="Blues",
            labels={"x": "Nivel CMMI", "y": "Capitulo", "color": "Controles"},
        )
        show_chart(chart_layout(fig, height=440, showlegend=False))
    with m2:
        section_title("CMMI por capitulo")
        stacked = maturity_stack(ordered_chapters(result.matriz_madurez.copy()))
        fig = px.bar(
            stacked,
            x="capitulo",
            y="controles",
            color="madurez",
            color_discrete_map=MATURITY_COLORS,
            labels={"capitulo": "", "controles": "Controles", "madurez": "Madurez"},
        )
        show_chart(chart_layout(fig, height=440))

    section_title("Superficie de controles")
    treemap_df = visible_controls.copy()
    treemap_df["control_label"] = treemap_df.apply(lambda row: treemap_label(row["control_id"], row["control_nombre"]), axis=1)
    fig = px.treemap(
        treemap_df,
        path=["capitulo", "control_label"],
        values="peso",
        color="cumplimiento_pct",
        color_continuous_scale=["#dc2626", "#f59e0b", "#16a34a"],
        range_color=[0, 100],
        hover_data=["madurez_nombre", "peso_brecha", "entrevistado"],
    )
    show_chart(style_treemap(fig, "Controles por capitulo coloreados por madurez", height=590))

with tab_perfil:
    p1, p2 = st.columns([1, 1.2])
    with p1:
        section_title("Funciones de ciberseguridad")
        show_chart(radar_chart(result.ciberfunciones, "atributo", "madurez_pct", "Funciones", "#0891b2"))
    with p2:
        section_title("Capacidad operacional")
        cap = result.capacidad_operacional.sort_values("madurez_pct", ascending=True)
        fig = px.bar(
            cap,
            x="madurez_pct",
            y="atributo",
            orientation="h",
            color="brecha_pct",
            text=cap["madurez_pct"].round(1),
            color_continuous_scale=["#16a34a", "#f59e0b", "#dc2626"],
            range_x=[0, 100],
            labels={"madurez_pct": "Madurez %", "atributo": "", "brecha_pct": "Brecha %"},
        )
        fig.update_traces(texttemplate="%{text:.1f}%")
        show_chart(chart_layout(fig, height=520, showlegend=False))

    s1, s2, s3 = st.columns(3)
    with s1:
        section_title("CID")
        fig = px.bar(
            result.propiedades_seguridad,
            x="madurez_pct",
            y="atributo",
            orientation="h",
            color="atributo",
            text=result.propiedades_seguridad["madurez_pct"].round(1) if not result.propiedades_seguridad.empty else None,
            color_discrete_sequence=PALETTE,
            range_x=[0, 100],
            labels={"madurez_pct": "Madurez %", "atributo": ""},
        )
        show_chart(chart_layout(fig, height=390, showlegend=False))
    with s2:
        section_title("Tipo de control")
        fig = px.bar(
            result.tipo_control,
            x="madurez_pct",
            y="atributo",
            orientation="h",
            color="atributo",
            text=result.tipo_control["madurez_pct"].round(1) if not result.tipo_control.empty else None,
            color_discrete_sequence=PALETTE,
            range_x=[0, 100],
            labels={"madurez_pct": "Madurez %", "atributo": ""},
        )
        show_chart(chart_layout(fig, height=390, showlegend=False))
    with s3:
        section_title("Dominios")
        fig = px.bar(
            result.dominios_seguridad,
            x="madurez_pct",
            y="atributo",
            orientation="h",
            color="atributo",
            text=result.dominios_seguridad["madurez_pct"].round(1) if not result.dominios_seguridad.empty else None,
            color_discrete_sequence=PALETTE,
            range_x=[0, 100],
            labels={"madurez_pct": "Madurez %", "atributo": ""},
        )
        show_chart(chart_layout(fig, height=390, showlegend=False))

with tab_brechas:
    section_title("Pareto de brechas")
    show_chart(pareto_chart(visible_controls, "Controles que explican la brecha"))

    b1, b2 = st.columns([1.05, 1])
    with b1:
        section_title("Concentracion de riesgo")
        risk_df = visible_controls.copy()
        risk_df["control_label"] = risk_df.apply(lambda row: treemap_label(row["control_id"], row["control_nombre"]), axis=1)
        fig = px.treemap(
            risk_df.sort_values("peso_brecha", ascending=False).head(35),
            path=["capitulo", "control_label"],
            values="peso_brecha",
            color="brecha_pct",
            color_continuous_scale=["#fef3c7", "#f97316", "#991b1b"],
            hover_data=["madurez_nombre", "hallazgo", "entrevistado"],
        )
        show_chart(style_treemap(fig, "Brecha por capitulo y control", height=560))
    with b2:
        section_title("Madurez vs brecha")
        fig = px.scatter(
            visible_controls,
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
        show_chart(chart_layout(fig, height=520))

    table_cols = [
        "control_id",
        "capitulo",
        "control_nombre",
        "madurez_nombre",
        "cumplimiento_pct",
        "peso_brecha",
        "entrevistado",
        "hallazgo",
        "observaciones",
    ]
    st.dataframe(visible_controls[table_cols].sort_values("peso_brecha", ascending=False), width="stretch", hide_index=True)

with tab_plan:
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        metric_card("Proyectos", str(resumen["proyectos"]), "Cartera total", "#2563eb")
    with q2:
        metric_card("Esfuerzo", num(resumen["esfuerzo_total"]), "Jornadas estimadas", "#7c3aed")
    with q3:
        metric_card("Quick wins", str(resumen["quick_wins"]), "Prioridad alta / bajo esfuerzo", "#16a34a")
    with q4:
        metric_card("Proyecto lider", resumen["proyecto_prioritario"], "Mayor prioridad", "#f59e0b")

    p1, p2, p3 = st.columns([1.05, 1, 1])
    with p1:
        section_title("Plan por plazo")
        plazo = result.proyectos_plazo.copy()
        fig = px.bar(
            plazo,
            x="plazo",
            y="prioridad",
            color="plazo",
            text=plazo["prioridad"].round(2) if not plazo.empty else None,
            color_discrete_map={"Corto": "#16a34a", "Medio": "#f59e0b", "Largo": "#dc2626", "": "#64748b"},
            labels={"prioridad": "Prioridad acumulada", "plazo": "Plazo"},
        )
        show_chart(chart_layout(fig, height=380, showlegend=False))
    with p2:
        section_title("Compromiso por plazo")
        fig = px.pie(plazo, names="plazo", values="proyectos", hole=0.5, color="plazo", color_discrete_sequence=PALETTE)
        show_chart(chart_layout(fig, height=380))
    with p3:
        section_title("Tipo de proyecto")
        fig = px.pie(result.proyectos_tipo, names="tipo", values="controles", hole=0.5, color_discrete_sequence=PALETTE)
        show_chart(chart_layout(fig, height=380))

    p4, p5 = st.columns([1, 1.1])
    with p4:
        section_title("Plan por capitulo")
        cap_plan = ordered_chapters(result.proyectos_capitulo.copy())
        fig = px.bar(
            cap_plan,
            x="capitulo",
            y="prioridad",
            color="capitulo",
            text=cap_plan["proyectos"] if not cap_plan.empty else None,
            color_discrete_map=CHAPTER_COLORS,
            labels={"prioridad": "Prioridad", "capitulo": ""},
        )
        show_chart(chart_layout(fig, height=430, showlegend=False))
    with p5:
        section_title("Plan por capacidad operacional")
        cap_plan_radar = result.proyectos_capacidad.sort_values("prioridad", ascending=False).head(12)
        show_chart(radar_chart(cap_plan_radar, "capacidad", "prioridad_pct", "Prioridad relativa por capacidad", "#0891b2"))

    e1, e2 = st.columns([1.05, 1])
    with e1:
        section_title("Roadmap de esfuerzo")
        show_chart(roadmap_chart(result.esfuerzo_roadmap))
    with e2:
        section_title("Quick wins")
        show_chart(impact_matrix(result.quick_wins))

    section_title("Esfuerzo por proyecto")
    effort = result.proyectos.sort_values("esfuerzo_jornadas", ascending=False).head(18).copy()
    effort["label"] = effort["proyecto_id"].astype(str) + " · " + effort["titulo"].map(lambda x: short_text(x, 34))
    fig = px.bar(
        effort.sort_values("esfuerzo_jornadas"),
        x="esfuerzo_jornadas",
        y="label",
        orientation="h",
        color="plazo",
        hover_data=["prioridad", "controles_relacionados", "tipo_seguridad"],
        color_discrete_sequence=PALETTE,
        labels={"esfuerzo_jornadas": "Jornadas", "label": ""},
    )
    show_chart(chart_layout(fig, height=560))

    project_table = result.quick_wins[
        [
            "proyecto_id",
            "titulo",
            "cuadrante",
            "plazo",
            "tipo_seguridad",
            "esfuerzo_jornadas",
            "controles_relacionados",
            "brecha_asociada",
            "prioridad",
            "descripcion",
        ]
    ].copy()
    st.dataframe(project_table, width="stretch", hide_index=True)

with tab_trazabilidad:
    section_title("Cadena de decision")
    show_chart(sankey_chart(result.trazabilidad))

    t1, t2 = st.columns([1, 1.1])
    with t1:
        section_title("Entrevistas")
        if result.entrevistas.empty:
            st.info("No hay entrevistas registradas para este caso.")
        else:
            st.dataframe(result.entrevistas, width="stretch", hide_index=True)
    with t2:
        section_title("Fuentes")
        source_rows = [
            {"archivo": "datos/estandares/iso27002_2022/catalogo_controles.csv", "contenido": "Catalogo ISO 27002:2022 y atributos de control"},
            {"archivo": f"datos/casos/{selected}/diagnostico.csv", "contenido": "Evaluacion de madurez por control"},
            {"archivo": f"datos/casos/{selected}/proyectos.csv", "contenido": "Plan de mejora y esfuerzo estimado"},
            {"archivo": f"datos/casos/{selected}/proyecto_control.csv", "contenido": "Relacion control-proyecto"},
            {"archivo": f"datos/casos/{selected}/entrevistas.csv", "contenido": "Entrevistados, cuando existe"},
        ]
        st.dataframe(pd.DataFrame(source_rows), width="stretch", hide_index=True)

    section_title("Relacion control-proyecto")
    trace_cols = ["capitulo", "control_id", "control_nombre", "proyecto_id", "titulo", "plazo", "peso_brecha", "prioridad"]
    st.dataframe(result.trazabilidad[trace_cols].sort_values("peso_brecha", ascending=False), width="stretch", hide_index=True)

with tab_descargas:
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        download_button("metricas.csv", result.controles, f"{selected}_metricas.csv")
        download_button("capitulos.csv", result.capitulos, f"{selected}_capitulos.csv")
        download_button("madurez_distribucion.csv", result.madurez_distribucion, f"{selected}_madurez_distribucion.csv")
    with d2:
        download_button("matriz_madurez.csv", result.matriz_madurez, f"{selected}_matriz_madurez.csv")
        download_button("capacidad_operacional.csv", result.capacidad_operacional, f"{selected}_capacidad_operacional.csv")
        download_button("ciberfunciones.csv", result.ciberfunciones, f"{selected}_ciberfunciones.csv")
    with d3:
        download_button("proyectos_priorizados.csv", result.proyectos, f"{selected}_proyectos.csv")
        download_button("proyectos_por_capitulo.csv", result.proyectos_capitulo, f"{selected}_proyectos_por_capitulo.csv")
        download_button("proyectos_por_capacidad.csv", result.proyectos_capacidad, f"{selected}_proyectos_por_capacidad.csv")
    with d4:
        download_button("quick_wins.csv", result.quick_wins, f"{selected}_quick_wins.csv")
        download_button("trazabilidad.csv", result.trazabilidad, f"{selected}_trazabilidad.csv")
        resumen_json = json.dumps(result.resumen, ensure_ascii=False, indent=2).encode("utf-8")
        st.download_button("resumen.json", resumen_json, file_name=f"{selected}_resumen.json", mime="application/json")

    output_dir = Path(".build") / selected
    if output_dir.exists():
        st.info(f"Build local disponible en {output_dir}")
