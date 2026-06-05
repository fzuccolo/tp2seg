from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app.datos import list_companies, load_dataset, repo_root
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
PALETTE = ["#2563eb", "#16a34a", "#f59e0b", "#dc2626", "#7c3aed", "#0891b2", "#be123c"]


@st.cache_data
def get_result(empresa_id: str):
    dataset = load_dataset(empresa_id, ROOT)
    return compute_metrics(dataset)


def pct(value: float | int) -> str:
    return f"{float(value):.1f}%"


def short_chapter(value: str) -> str:
    return value.replace("Controles ", "").replace("6 - ", "6 - ").replace("7 - ", "7 - ").replace("8 - ", "8 - ")


def ordered_chapters(df: pd.DataFrame) -> pd.DataFrame:
    if "capitulo" not in df.columns:
        return df
    order = {name: index for index, name in enumerate(CHAPTER_ORDER)}
    return df.assign(_orden=df["capitulo"].map(order).fillna(99)).sort_values("_orden").drop(columns=["_orden"])


def metric_card(label: str, value: str, detail: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-detail">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def gauge_chart(value: float, title: str) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": "%", "font": {"size": 42}},
            title={"text": title, "font": {"size": 16}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563eb"},
                "bgcolor": "#eef2ff",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 30], "color": "#fee2e2"},
                    {"range": [30, 70], "color": "#fef3c7"},
                    {"range": [70, 100], "color": "#dcfce7"},
                ],
            },
        )
    )
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
    return fig


def radar_chart(df: pd.DataFrame, label_col: str, value_col: str, title: str) -> go.Figure:
    if df.empty:
        return go.Figure()
    labels = df[label_col].astype(str).tolist()
    values = df[value_col].astype(float).round(1).tolist()
    labels_closed = labels + labels[:1]
    values_closed = values + values[:1]
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values_closed,
            theta=labels_closed,
            fill="toself",
            name=title,
            line={"color": "#2563eb", "width": 2},
            fillcolor="rgba(37, 99, 235, 0.22)",
        )
    )
    fig.update_layout(
        title=title,
        polar={"radialaxis": {"visible": True, "range": [0, 100]}},
        showlegend=False,
        height=430,
        margin=dict(l=40, r=40, t=60, b=30),
    )
    return fig


def download_button(label: str, df: pd.DataFrame, filename: str) -> None:
    st.download_button(label, df.to_csv(index=False).encode("utf-8"), file_name=filename, mime="text/csv")


st.set_page_config(page_title="TP2 Seguridad - Tablero", layout="wide")
st.markdown(
    """
    <style>
      .main .block-container { padding-top: 1.1rem; }
      .metric-card {
        border: 1px solid #d8dee9;
        border-left: 4px solid #2563eb;
        border-radius: 8px;
        padding: 14px 16px;
        background: #ffffff;
        min-height: 116px;
      }
      .metric-label {
        color: #4b5563;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.02em;
        font-weight: 700;
      }
      .metric-value {
        color: #111827;
        font-size: 2.05rem;
        line-height: 1.1;
        font-weight: 800;
        margin-top: 6px;
      }
      .metric-detail {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 5px;
      }
      .section-title {
        margin-top: 8px;
        margin-bottom: 2px;
        font-size: 1.05rem;
        font-weight: 800;
        color: #111827;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

companies = list_companies(ROOT)
default_idx = companies.index("ejemplo") if "ejemplo" in companies else 0
selected = st.sidebar.selectbox("Empresa", companies, index=default_idx)
result = get_result(selected)
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

tab_resumen, tab_madurez, tab_brechas, tab_plan, tab_fuentes, tab_descargas = st.tabs(
    ["Resumen Ejecutivo", "Madurez ISO", "Brechas", "Plan de Mejora", "Fuentes", "Descargas"]
)

with tab_resumen:
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        metric_card("Madurez global", pct(resumen["madurez_global_pct"]), "Promedio ponderado")
    with k2:
        metric_card("Brecha global", pct(resumen["brecha_global_pct"]), "Distancia a optimizado")
    with k3:
        metric_card("Controles", str(resumen["controles_evaluados"]), "ISO 27002:2022")
    with k4:
        metric_card("Capitulo debil", resumen["capitulo_mas_debil"].split(" - ", 1)[0], resumen["capitulo_mas_debil"])
    with k5:
        metric_card("Proyecto prioritario", resumen["proyecto_prioritario"], "Mayor impacto calculado")

    left, center, right = st.columns([1.05, 1.25, 1.2])
    with left:
        st.plotly_chart(gauge_chart(resumen["madurez_global_pct"], "Madurez global"), width="stretch")
    with center:
        caps = ordered_chapters(result.capitulos.copy())
        fig = px.bar(
            caps,
            x="capitulo",
            y="madurez_pct",
            color="capitulo",
            text=caps["madurez_pct"].round(1),
            color_discrete_sequence=PALETTE,
            labels={"madurez_pct": "Madurez %", "capitulo": ""},
            range_y=[0, 100],
        )
        fig.update_layout(showlegend=False, height=300, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, width="stretch")
    with right:
        dist = result.madurez_distribucion.copy()
        fig = px.pie(
            dist,
            names="madurez_nombre",
            values="controles",
            hole=0.58,
            color="madurez_nombre",
            color_discrete_sequence=PALETTE,
        )
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, width="stretch")

    r1, r2 = st.columns(2)
    with r1:
        caps_radar = ordered_chapters(result.capitulos.copy())
        st.plotly_chart(radar_chart(caps_radar, "capitulo", "madurez_pct", "Madurez por capitulo"), width="stretch")
    with r2:
        st.plotly_chart(
            radar_chart(result.capacidad_operacional.sort_values("madurez_pct").head(12), "atributo", "madurez_pct", "Capacidad operacional"),
            width="stretch",
        )

with tab_madurez:
    m1, m2 = st.columns([1.25, 1])
    with m1:
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
        fig.update_layout(height=430, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, width="stretch")
    with m2:
        fig = px.bar(
            result.madurez_distribucion,
            x="madurez_nombre",
            y="controles",
            color="madurez_nombre",
            text="controles",
            color_discrete_sequence=PALETTE,
            labels={"madurez_nombre": "Nivel", "controles": "Controles"},
        )
        fig.update_layout(showlegend=False, height=430, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, width="stretch")

    a1, a2, a3 = st.columns(3)
    with a1:
        st.plotly_chart(radar_chart(result.ciberfunciones, "atributo", "madurez_pct", "Funciones de ciberseguridad"), width="stretch")
    with a2:
        fig = px.bar(
            result.propiedades_seguridad,
            x="madurez_pct",
            y="atributo",
            orientation="h",
            color="atributo",
            text=result.propiedades_seguridad["madurez_pct"].round(1) if not result.propiedades_seguridad.empty else None,
            color_discrete_sequence=PALETTE,
            range_x=[0, 100],
        )
        fig.update_layout(showlegend=False, height=430, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, width="stretch")
    with a3:
        fig = px.bar(
            result.tipo_control,
            x="madurez_pct",
            y="atributo",
            orientation="h",
            color="atributo",
            text=result.tipo_control["madurez_pct"].round(1) if not result.tipo_control.empty else None,
            color_discrete_sequence=PALETTE,
            range_x=[0, 100],
        )
        fig.update_layout(showlegend=False, height=430, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, width="stretch")

with tab_brechas:
    top_filtered = filtered.sort_values(["peso_brecha", "peso"], ascending=False).head(15).copy()
    b1, b2 = st.columns([1.25, 1])
    with b1:
        fig = px.bar(
            top_filtered.sort_values("peso_brecha"),
            x="peso_brecha",
            y="control_id",
            orientation="h",
            color="capitulo",
            hover_data=["control_nombre", "madurez_nombre", "hallazgo"],
            labels={"peso_brecha": "Brecha ponderada", "control_id": "Control"},
            color_discrete_sequence=PALETTE,
        )
        fig.update_layout(height=520, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, width="stretch")
    with b2:
        fig = px.scatter(
            filtered,
            x="cumplimiento_pct",
            y="peso_brecha",
            color="capitulo",
            size="peso",
            hover_name="control_id",
            hover_data=["control_nombre", "madurez_nombre", "entrevistado"],
            labels={"cumplimiento_pct": "Madurez %", "peso_brecha": "Brecha ponderada"},
            color_discrete_sequence=PALETTE,
        )
        fig.update_layout(height=520, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, width="stretch")

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
    st.dataframe(filtered[table_cols].sort_values("peso_brecha", ascending=False), width="stretch", hide_index=True)

with tab_plan:
    p1, p2, p3 = st.columns([1.1, 1, 1])
    with p1:
        fig = px.bar(
            result.proyectos_plazo,
            x="plazo",
            y="prioridad",
            color="plazo",
            text=result.proyectos_plazo["prioridad"].round(2) if not result.proyectos_plazo.empty else None,
            color_discrete_sequence=PALETTE,
            labels={"prioridad": "Prioridad acumulada", "plazo": "Plazo"},
        )
        fig.update_layout(showlegend=False, height=360, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, width="stretch")
    with p2:
        fig = px.pie(
            result.proyectos_tipo,
            names="tipo",
            values="controles",
            hole=0.5,
            color_discrete_sequence=PALETTE,
        )
        fig.update_layout(height=360, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, width="stretch")
    with p3:
        fig = px.scatter(
            result.proyectos,
            x="esfuerzo_jornadas",
            y="prioridad",
            size="controles_relacionados",
            color="plazo",
            hover_name="titulo",
            hover_data=["proyecto_id", "tipo_seguridad", "controles_relacionados"],
            color_discrete_sequence=PALETTE,
            labels={"esfuerzo_jornadas": "Esfuerzo jornadas", "prioridad": "Prioridad"},
        )
        fig.update_layout(height=360, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, width="stretch")

    project_table = result.proyectos[
        [
            "proyecto_id",
            "titulo",
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

with tab_fuentes:
    c1, c2 = st.columns([1, 1.1])
    with c1:
        st.markdown('<div class="section-title">Metadata del dataset</div>', unsafe_allow_html=True)
        st.json(result.empresa)
        st.markdown('<div class="section-title">Entrevistas</div>', unsafe_allow_html=True)
        if result.entrevistas.empty:
            st.info("No hay entrevistas registradas para esta empresa.")
        else:
            st.dataframe(result.entrevistas, width="stretch", hide_index=True)
    with c2:
        st.markdown('<div class="section-title">Trazabilidad de fuentes</div>', unsafe_allow_html=True)
        source_rows = [
            {"archivo": "datos/estandares/iso27002_2022/catalogo_controles.csv", "contenido": "Catalogo ISO 27002:2022 y atributos de control"},
            {"archivo": f"datos/empresas/{selected}/diagnostico.csv", "contenido": "Evaluacion de madurez por control"},
            {"archivo": f"datos/empresas/{selected}/proyectos.csv", "contenido": "Plan de mejora y esfuerzo estimado"},
            {"archivo": f"datos/empresas/{selected}/proyecto_control.csv", "contenido": "Relacion control-proyecto"},
            {"archivo": f"datos/empresas/{selected}/entrevistas.csv", "contenido": "Entrevistados, cuando existe"},
        ]
        st.dataframe(pd.DataFrame(source_rows), width="stretch", hide_index=True)
        st.markdown('<div class="section-title">Resumen de cobertura</div>', unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame(
                [
                    {"dimension": "Capitulos ISO", "valor": str(resumen["capitulos_evaluados"])},
                    {"dimension": "Controles evaluados", "valor": str(resumen["controles_evaluados"])},
                    {"dimension": "Entrevistas", "valor": str(resumen["entrevistas"])},
                    {"dimension": "Proyectos", "valor": str(resumen["proyectos"])},
                    {"dimension": "Capacidad mas debil", "valor": str(resumen["capacidad_mas_debil"])},
                    {"dimension": "Funcion mas debil", "valor": str(resumen["funcion_mas_debil"])},
                ]
            ),
            width="stretch",
            hide_index=True,
        )

with tab_descargas:
    d1, d2, d3 = st.columns(3)
    with d1:
        download_button("metricas.csv", result.controles, f"{selected}_metricas.csv")
        download_button("capitulos.csv", result.capitulos, f"{selected}_capitulos.csv")
        download_button("madurez_distribucion.csv", result.madurez_distribucion, f"{selected}_madurez_distribucion.csv")
    with d2:
        download_button("capacidad_operacional.csv", result.capacidad_operacional, f"{selected}_capacidad_operacional.csv")
        download_button("ciberfunciones.csv", result.ciberfunciones, f"{selected}_ciberfunciones.csv")
        download_button("matriz_madurez.csv", result.matriz_madurez, f"{selected}_matriz_madurez.csv")
    with d3:
        download_button("proyectos_priorizados.csv", result.proyectos, f"{selected}_proyectos.csv")
        download_button("proyectos_por_plazo.csv", result.proyectos_plazo, f"{selected}_proyectos_por_plazo.csv")
        resumen_json = json.dumps(result.resumen, ensure_ascii=False, indent=2).encode("utf-8")
        st.download_button("resumen.json", resumen_json, file_name=f"{selected}_resumen.json", mime="application/json")

    output_dir = Path("salidas") / selected
    if output_dir.exists():
        st.info(f"Salidas locales disponibles en {output_dir}")
