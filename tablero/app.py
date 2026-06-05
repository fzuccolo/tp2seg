from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from motor.datos import list_companies, load_dataset, repo_root
from motor.metricas import compute_metrics


ROOT = repo_root()


@st.cache_data
def get_result(empresa_id: str):
    dataset = load_dataset(empresa_id, ROOT)
    return compute_metrics(dataset)


st.set_page_config(
    page_title="TP2 Seguridad - Tablero",
    page_icon="",
    layout="wide",
)

companies = list_companies(ROOT)
selected = st.sidebar.selectbox("Empresa", companies, index=companies.index("tecnohogar") if "tecnohogar" in companies else 0)
result = get_result(selected)
resumen = result.resumen

st.title(f"Tablero de Control - {resumen['empresa_nombre']}")
st.caption(f"Estandar: {resumen['estandar_id']} | Controles evaluados: {resumen['controles_evaluados']}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Madurez global", f"{resumen['madurez_global_pct']}%")
col2.metric("Brecha global", f"{resumen['brecha_global_pct']}%")
col3.metric("Capitulos", resumen["capitulos_evaluados"])
col4.metric("Proyectos", resumen["proyectos"])

tab_global, tab_controles, tab_proyectos, tab_descargas = st.tabs(["Global", "Controles", "Proyectos", "Descargas"])

with tab_global:
    chart_data = result.capitulos.sort_values("madurez_pct")
    fig = px.bar(
        chart_data,
        x="madurez_pct",
        y="capitulo",
        orientation="h",
        text=chart_data["madurez_pct"].round(1),
        labels={"madurez_pct": "Madurez %", "capitulo": "Capitulo"},
        range_x=[0, 100],
    )
    fig.update_layout(height=430, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

with tab_controles:
    top = result.top_brechas.copy()
    top["brecha_pct"] = top["brecha_pct"].round(1)
    fig = px.bar(
        top.sort_values("brecha_pct"),
        x="brecha_pct",
        y="control_id",
        orientation="h",
        color="capitulo",
        hover_data=["control_nombre", "observaciones"],
        labels={"brecha_pct": "Brecha %", "control_id": "Control"},
    )
    fig.update_layout(height=430, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(
        result.controles[
            [
                "control_id",
                "capitulo",
                "control_nombre",
                "nivel_madurez",
                "madurez_nombre",
                "cumplimiento_pct",
                "observaciones",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

with tab_proyectos:
    projects = result.proyectos.copy()
    projects["prioridad"] = projects["prioridad"].round(3)
    fig = px.scatter(
        projects,
        x="esfuerzo_jornadas",
        y="aporte_seguridad",
        size="brecha_asociada",
        color="plazo",
        hover_name="titulo",
        hover_data=["proyecto_id", "controles_relacionados", "prioridad"],
        labels={"esfuerzo_jornadas": "Esfuerzo jornadas", "aporte_seguridad": "Aporte seguridad"},
    )
    fig.update_layout(height=430, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(
        projects[
            [
                "proyecto_id",
                "titulo",
                "plazo",
                "esfuerzo_jornadas",
                "aporte_seguridad",
                "controles_relacionados",
                "prioridad",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

with tab_descargas:
    controles_csv = result.controles.to_csv(index=False).encode("utf-8")
    capitulos_csv = result.capitulos.to_csv(index=False).encode("utf-8")
    proyectos_csv = result.proyectos.to_csv(index=False).encode("utf-8")
    resumen_json = json.dumps(result.resumen, ensure_ascii=False, indent=2).encode("utf-8")

    st.download_button("metricas.csv", controles_csv, file_name=f"{selected}_metricas.csv", mime="text/csv")
    st.download_button("capitulos.csv", capitulos_csv, file_name=f"{selected}_capitulos.csv", mime="text/csv")
    st.download_button("proyectos_priorizados.csv", proyectos_csv, file_name=f"{selected}_proyectos.csv", mime="text/csv")
    st.download_button("resumen.json", resumen_json, file_name=f"{selected}_resumen.json", mime="application/json")

    output_dir = Path("salidas") / selected
    if output_dir.exists():
        st.info(f"Salidas locales disponibles en {output_dir}")
