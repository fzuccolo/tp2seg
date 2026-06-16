from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st

from app.datos import list_cases, load_dataset, repo_root
from app.graficos import (
    MATURITY_ORDER,
    PLOTLY_CONFIG,
    fig_brechas_madurez_vs_brecha,
    fig_brechas_pareto,
    fig_brechas_treemap,
    fig_ejecutivo_capacidades,
    fig_ejecutivo_distribucion_cmmi,
    fig_ejecutivo_madurez_capitulo,
    fig_ejecutivo_madurez_global,
    fig_ejecutivo_radar_capitulos,
    fig_mapa_cmmi_capitulo,
    fig_mapa_matriz_cmmi,
    fig_mapa_superficie_controles,
    fig_perfil_capacidad_operacional,
    fig_perfil_cid,
    fig_perfil_dominios,
    fig_perfil_funciones,
    fig_perfil_tipo_control,
    fig_plan_capacidad,
    fig_plan_capitulo,
    fig_plan_compromiso_plazo,
    fig_plan_esfuerzo_proyecto,
    fig_plan_plazo,
    fig_plan_quick_wins,
    fig_plan_roadmap,
    fig_plan_tipo_proyecto,
    fig_trazabilidad_sankey,
    ordered_chapters,
)
from app.metricas import compute_metrics


ROOT = repo_root()
DEFAULT_COMPANY = "tecnohogar"
DASHBOARD_CACHE_VERSION = "story-dashboard-v8"


@st.cache_data
def get_result(empresa_id: str, cache_version: str):
    _ = cache_version
    dataset = load_dataset(empresa_id, ROOT)
    return compute_metrics(dataset)


def pct(value: float | int) -> str:
    return f"{float(value):.1f}%"


def num(value: float | int) -> str:
    return f"{float(value):,.0f}".replace(",", ".")


def show_chart(fig) -> None:
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


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
        show_chart(fig_ejecutivo_madurez_global(result))
    with center:
        section_title("Madurez por capitulo")
        show_chart(fig_ejecutivo_madurez_capitulo(result))
    with right:
        section_title("Distribucion CMMI")
        show_chart(fig_ejecutivo_distribucion_cmmi(result))

    r1, r2 = st.columns(2)
    with r1:
        section_title("Radar ejecutivo")
        show_chart(fig_ejecutivo_radar_capitulos(result))
    with r2:
        section_title("Capacidades operacionales")
        show_chart(fig_ejecutivo_capacidades(result))

with tab_mapa:
    m1, m2 = st.columns([1.25, 1])
    with m1:
        section_title("Mapa de madurez ISO")
        show_chart(fig_mapa_matriz_cmmi(result))
    with m2:
        section_title("CMMI por capitulo")
        show_chart(fig_mapa_cmmi_capitulo(result))

    section_title("Superficie de controles")
    show_chart(fig_mapa_superficie_controles(result, visible_controls))

with tab_perfil:
    p1, p2 = st.columns([1, 1.2])
    with p1:
        section_title("Funciones de ciberseguridad")
        show_chart(fig_perfil_funciones(result))
    with p2:
        section_title("Capacidad operacional")
        show_chart(fig_perfil_capacidad_operacional(result))

    s1, s2, s3 = st.columns(3)
    with s1:
        section_title("CID")
        show_chart(fig_perfil_cid(result))
    with s2:
        section_title("Tipo de control")
        show_chart(fig_perfil_tipo_control(result))
    with s3:
        section_title("Dominios")
        show_chart(fig_perfil_dominios(result))

with tab_brechas:
    section_title("Pareto de brechas")
    show_chart(fig_brechas_pareto(result, visible_controls))

    b1, b2 = st.columns([1.05, 1])
    with b1:
        section_title("Concentracion de riesgo")
        show_chart(fig_brechas_treemap(result, visible_controls))
    with b2:
        section_title("Madurez vs brecha")
        show_chart(fig_brechas_madurez_vs_brecha(result, visible_controls))

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
        show_chart(fig_plan_plazo(result))
    with p2:
        section_title("Compromiso por plazo")
        show_chart(fig_plan_compromiso_plazo(result))
    with p3:
        section_title("Tipo de proyecto")
        show_chart(fig_plan_tipo_proyecto(result))

    p4, p5 = st.columns([1, 1.1])
    with p4:
        section_title("Plan por capitulo")
        show_chart(fig_plan_capitulo(result))
    with p5:
        section_title("Plan por capacidad operacional")
        show_chart(fig_plan_capacidad(result))

    e1, e2 = st.columns([1.05, 1])
    with e1:
        section_title("Roadmap de esfuerzo")
        show_chart(fig_plan_roadmap(result))
    with e2:
        section_title("Quick wins")
        show_chart(fig_plan_quick_wins(result))

    section_title("Esfuerzo por proyecto")
    show_chart(fig_plan_esfuerzo_proyecto(result))

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
    show_chart(fig_trazabilidad_sankey(result))

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
