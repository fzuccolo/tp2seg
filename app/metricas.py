from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


TYPE_CONTROL = {
    "tipo_preventivo": "Preventivo",
    "tipo_detectivo": "Detectivo",
    "tipo_correctivo": "Correctivo",
}

SECURITY_PROPERTIES = {
    "prop_confidencialidad": "Confidencialidad",
    "prop_integridad": "Integridad",
    "prop_disponibilidad": "Disponibilidad",
}

CYBER_FUNCTIONS = {
    "func_identificacion": "Identificacion",
    "func_proteccion": "Proteccion",
    "func_deteccion": "Deteccion",
    "func_respuesta": "Respuesta",
    "func_recuperacion": "Recuperacion",
}

OPERATIONAL_CAPABILITIES = {
    "cap_gobernanza": "Gobernanza",
    "cap_gestion_activos": "Gestion de activos",
    "cap_proteccion_informacion": "Proteccion de informacion",
    "cap_seguridad_rrhh": "Seguridad de RRHH",
    "cap_seguridad_fisica": "Seguridad fisica",
    "cap_seguridad_redes_sistemas": "Redes y sistemas",
    "cap_seguridad_aplicaciones": "Seguridad en aplicaciones",
    "cap_configuraciones_seguras": "Configuraciones seguras",
    "cap_gestion_accesos_identidades": "Accesos e identidades",
    "cap_gestion_amenazas_vulnerabilidades": "Amenazas y vulnerabilidades",
    "cap_continuidad": "Continuidad",
    "cap_seguridad_proveedores": "Proveedores",
    "cap_cumplimiento_legalidad": "Cumplimiento y legalidad",
    "cap_gestion_eventos_si": "Eventos de SI",
    "cap_garantizar_si": "Garantizar SI",
}

SECURITY_DOMAINS = {
    "dom_gobernanza_ecosistema": "Gobernanza y ecosistema",
    "dom_proteccion": "Proteccion",
    "dom_defensa": "Defensa",
    "dom_resiliencia": "Resiliencia",
}

PROJECT_TYPES = {
    "logica": "Logica",
    "fisica": "Fisica",
    "organizativa": "Organizativa",
    "legal": "Legal",
}

MATURITY_LABELS = {
    0: "0 - Inexistente",
    1: "1 - Inicial",
    2: "2 - Gestionado",
    3: "3 - Definido",
    4: "4 - Cuantitativo",
    5: "5 - Optimizado",
}

PLAZO_ORDER = {"Corto": 1, "Medio": 2, "Largo": 3, "": 4}


@dataclass(frozen=True)
class MetricResult:
    empresa: dict[str, Any]
    controles: pd.DataFrame
    capitulos: pd.DataFrame
    proyectos: pd.DataFrame
    top_brechas: pd.DataFrame
    madurez_distribucion: pd.DataFrame
    matriz_madurez: pd.DataFrame
    tipo_control: pd.DataFrame
    propiedades_seguridad: pd.DataFrame
    ciberfunciones: pd.DataFrame
    capacidad_operacional: pd.DataFrame
    dominios_seguridad: pd.DataFrame
    proyectos_plazo: pd.DataFrame
    proyectos_tipo: pd.DataFrame
    proyectos_capitulo: pd.DataFrame
    proyectos_capacidad: pd.DataFrame
    esfuerzo_roadmap: pd.DataFrame
    quick_wins: pd.DataFrame
    trazabilidad: pd.DataFrame
    entrevistas: pd.DataFrame
    resumen: dict[str, Any]


def _weighted_average(df: pd.DataFrame, value_col: str, weight_col: str) -> float:
    total_weight = float(df[weight_col].sum())
    if total_weight == 0:
        return 0.0
    return float((df[value_col] * df[weight_col]).sum() / total_weight)


def _ensure_numeric(df: pd.DataFrame, column: str, default: float = 0.0) -> None:
    if column not in df.columns:
        df[column] = default
    df[column] = pd.to_numeric(df[column], errors="coerce").fillna(default)


def _ensure_text(df: pd.DataFrame, column: str, default: str = "") -> None:
    if column not in df.columns:
        df[column] = default
    df[column] = df[column].fillna(default).astype(str)


def _attribute_scores(controles: pd.DataFrame, mapping: dict[str, str], group_name: str) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    for column, label in mapping.items():
        if column not in controles.columns:
            continue
        values = pd.to_numeric(controles[column], errors="coerce").fillna(0)
        subset = controles[values > 0].copy()
        if subset.empty:
            continue
        madurez = _weighted_average(subset, "madurez_valor", "peso")
        records.append(
            {
                "grupo": group_name,
                "atributo": label,
                "controles": int(len(subset)),
                "madurez": madurez,
                "madurez_pct": madurez * 100,
                "brecha": 1.0 - madurez,
                "brecha_pct": (1.0 - madurez) * 100,
            }
        )
    return pd.DataFrame(records).sort_values("madurez", ascending=True) if records else pd.DataFrame()


def _maturity_distribution(controles: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        controles.groupby(["nivel_madurez", "madurez_nombre"], as_index=False)
        .agg(controles=("control_id", "nunique"), peso_total=("peso", "sum"))
        .sort_values("nivel_madurez")
    )
    total = max(int(grouped["controles"].sum()), 1)
    grouped["porcentaje"] = grouped["controles"] / total * 100
    return grouped


def _maturity_matrix(controles: pd.DataFrame) -> pd.DataFrame:
    matrix = (
        controles.assign(madurez_orden=controles["nivel_madurez"].astype(int))
        .pivot_table(
            index="capitulo",
            columns="madurez_nombre",
            values="control_id",
            aggfunc="nunique",
            fill_value=0,
        )
        .reset_index()
    )
    ordered_columns = ["capitulo"] + [label for label in MATURITY_LABELS.values() if label in matrix.columns]
    return matrix.loc[:, ordered_columns]


def _pct_of_max(series: pd.Series) -> pd.Series:
    max_value = float(series.max()) if not series.empty else 0.0
    if max_value <= 0:
        return pd.Series([0.0] * len(series), index=series.index)
    return series / max_value * 100


def _project_chapter_summary(trazabilidad: pd.DataFrame) -> pd.DataFrame:
    if trazabilidad.empty or "capitulo" not in trazabilidad.columns:
        return pd.DataFrame()
    base = trazabilidad[trazabilidad["capitulo"].notna()].copy()
    if base.empty:
        return pd.DataFrame()

    control_summary = (
        base.groupby("capitulo", as_index=False)
        .agg(controles=("control_id", "nunique"), brecha_asociada=("peso_brecha", "sum"))
    )
    project_summary = (
        base.drop_duplicates(["capitulo", "proyecto_id"])
        .groupby("capitulo", as_index=False)
        .agg(
            proyectos=("proyecto_id", "nunique"),
            esfuerzo_jornadas=("esfuerzo_jornadas", "sum"),
            prioridad=("prioridad", "sum"),
        )
    )
    summary = control_summary.merge(project_summary, on="capitulo", how="outer").fillna(0)
    summary["prioridad_pct"] = _pct_of_max(summary["prioridad"])
    return summary.sort_values("prioridad", ascending=False)


def _project_capacity_summary(trazabilidad: pd.DataFrame) -> pd.DataFrame:
    if trazabilidad.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for column, label in OPERATIONAL_CAPABILITIES.items():
        if column not in trazabilidad.columns:
            continue
        values = pd.to_numeric(trazabilidad[column], errors="coerce").fillna(0)
        subset = trazabilidad[values > 0].copy()
        if subset.empty:
            continue
        project_once = subset.drop_duplicates("proyecto_id")
        rows.append(
            {
                "capacidad": label,
                "controles": int(subset["control_id"].nunique()),
                "proyectos": int(project_once["proyecto_id"].nunique()),
                "esfuerzo_jornadas": float(project_once["esfuerzo_jornadas"].sum()),
                "prioridad": float(project_once["prioridad"].sum()),
                "brecha_asociada": float(subset["peso_brecha"].sum()),
            }
        )
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["prioridad_pct"] = _pct_of_max(df["prioridad"])
    return df.sort_values("prioridad", ascending=False)


def _effort_roadmap(proyectos: pd.DataFrame) -> pd.DataFrame:
    if proyectos.empty:
        return pd.DataFrame()
    roadmap = proyectos.copy()
    roadmap["plazo_orden"] = roadmap["plazo"].map(PLAZO_ORDER).fillna(4).astype(int)
    roadmap = roadmap.sort_values(["plazo_orden", "prioridad", "esfuerzo_jornadas"], ascending=[True, False, True]).reset_index(drop=True)
    roadmap["secuencia"] = roadmap.index + 1
    roadmap["esfuerzo_acumulado"] = roadmap["esfuerzo_jornadas"].cumsum()
    roadmap["prioridad_acumulada"] = roadmap["prioridad"].cumsum()
    total_effort = max(float(roadmap["esfuerzo_jornadas"].sum()), 1.0)
    roadmap["avance_esfuerzo_pct"] = roadmap["esfuerzo_acumulado"] / total_effort * 100
    return roadmap


def _quick_wins(proyectos: pd.DataFrame) -> pd.DataFrame:
    if proyectos.empty:
        return pd.DataFrame()
    df = proyectos.copy()
    effort_positive = df.loc[df["esfuerzo_jornadas"] > 0, "esfuerzo_jornadas"]
    priority_positive = df.loc[df["prioridad"] > 0, "prioridad"]
    effort_threshold = float(effort_positive.median()) if not effort_positive.empty else 0.0
    priority_threshold = float(priority_positive.median()) if not priority_positive.empty else 0.0

    def classify(row: pd.Series) -> str:
        high_priority = row["prioridad"] >= priority_threshold
        low_effort = row["esfuerzo_jornadas"] <= effort_threshold or effort_threshold == 0
        if high_priority and low_effort:
            return "Quick win"
        if high_priority and not low_effort:
            return "Proyecto estrategico"
        if not high_priority and low_effort:
            return "Mejora tactica"
        return "Diferir"

    df["cuadrante"] = df.apply(classify, axis=1)
    order = {"Quick win": 0, "Proyecto estrategico": 1, "Mejora tactica": 2, "Diferir": 3}
    df["cuadrante_orden"] = df["cuadrante"].map(order).fillna(9).astype(int)
    return df.sort_values(["cuadrante_orden", "prioridad"], ascending=[True, False])


def compute_metrics(dataset: dict[str, Any]) -> MetricResult:
    catalogo = dataset["catalogo"].copy()
    diagnostico = dataset["diagnostico"].copy()
    madurez = dataset["madurez"].copy()
    proyectos = dataset["proyectos"].copy()
    proyecto_control = dataset["proyecto_control"].copy()
    entrevistas = dataset.get("entrevistas", pd.DataFrame()).copy()

    madurez["nivel"] = madurez["nivel"].astype(int)
    diagnostico["nivel_madurez"] = diagnostico["nivel_madurez"].astype(int)
    _ensure_numeric(catalogo, "peso", 1.0)
    _ensure_numeric(catalogo, "aplica", 1.0)

    controles = catalogo.merge(diagnostico, on="control_id", how="left")
    controles = controles[pd.to_numeric(controles["aplica"], errors="coerce").fillna(1).astype(int) == 1].copy()
    controles = controles[controles["nivel_madurez"].notna()].copy()
    controles["nivel_madurez"] = controles["nivel_madurez"].astype(int)
    controles = controles.merge(
        madurez.rename(columns={"nivel": "nivel_madurez", "nombre": "madurez_nombre_escala", "valor": "madurez_valor_escala"}),
        on="nivel_madurez",
        how="left",
    )

    if "valor" in controles.columns:
        maturity_value = pd.to_numeric(controles["valor"], errors="coerce")
    else:
        maturity_value = pd.Series(index=controles.index, dtype="float64")
    controles["madurez_valor_escala"] = pd.to_numeric(controles["madurez_valor_escala"], errors="coerce").fillna(0.0)
    controles["madurez_valor"] = maturity_value.where(maturity_value.notna(), controles["madurez_valor_escala"]).fillna(0.0).astype(float)
    controles["madurez_nombre"] = controles.get("madurez_desc", pd.Series(index=controles.index, dtype=object)).fillna(
        controles["madurez_nombre_escala"]
    )
    controles["madurez_nombre"] = controles["madurez_nombre"].fillna(controles["nivel_madurez"].map(MATURITY_LABELS))
    controles["brecha"] = 1.0 - controles["madurez_valor"]
    controles["peso_brecha"] = controles["brecha"] * controles["peso"]
    controles["cumplimiento_pct"] = controles["madurez_valor"] * 100
    controles["brecha_pct"] = controles["brecha"] * 100
    _ensure_text(controles, "entrevistado")
    _ensure_text(controles, "hallazgo")
    _ensure_text(controles, "observaciones")
    _ensure_text(controles, "tipo_seguridad")
    _ensure_text(controles, "plazo_sugerido")

    madurez_global = _weighted_average(controles, "madurez_valor", "peso")
    brecha_global = 1.0 - madurez_global

    capitulos = (
        controles.groupby("capitulo", as_index=False)
        .apply(
            lambda group: pd.Series(
                {
                    "controles": int(len(group)),
                    "peso_total": float(group["peso"].sum()),
                    "madurez": _weighted_average(group, "madurez_valor", "peso"),
                    "brecha": 1.0 - _weighted_average(group, "madurez_valor", "peso"),
                }
            ),
            include_groups=False,
        )
        .reset_index(drop=True)
    )
    capitulos["madurez_pct"] = capitulos["madurez"] * 100
    capitulos["brecha_pct"] = capitulos["brecha"] * 100
    if "controles" in capitulos.columns:
        capitulos["controles"] = capitulos["controles"].astype(int)
    capitulos = capitulos.sort_values("madurez", ascending=True)

    top_brechas = controles.sort_values(["peso_brecha", "peso"], ascending=False).head(10).copy()
    madurez_distribucion = _maturity_distribution(controles)
    matriz_madurez = _maturity_matrix(controles)
    tipo_control = _attribute_scores(controles, TYPE_CONTROL, "Tipo de control")
    propiedades_seguridad = _attribute_scores(controles, SECURITY_PROPERTIES, "Propiedad de seguridad")
    ciberfunciones = _attribute_scores(controles, CYBER_FUNCTIONS, "Funcion de ciberseguridad")
    capacidad_operacional = _attribute_scores(controles, OPERATIONAL_CAPABILITIES, "Capacidad operacional")
    dominios_seguridad = _attribute_scores(controles, SECURITY_DOMAINS, "Dominio de seguridad")

    proyectos = proyectos.copy()
    _ensure_numeric(proyectos, "esfuerzo_jornadas")
    _ensure_numeric(proyectos, "aporte_seguridad")
    _ensure_text(proyectos, "plazo")
    _ensure_text(proyectos, "tipo_seguridad")
    for column in PROJECT_TYPES:
        _ensure_numeric(proyectos, column)

    control_link_columns = [
        "control_id",
        "control_nombre",
        "capitulo",
        "peso_brecha",
        "madurez_valor",
        "brecha",
        *OPERATIONAL_CAPABILITIES.keys(),
    ]
    linked = proyecto_control.merge(controles[control_link_columns], on="control_id", how="left")
    project_gaps = (
        linked.groupby("proyecto_id", as_index=False)
        .agg(
            brecha_asociada=("peso_brecha", "sum"),
            controles_relacionados=("control_id", "nunique"),
            madurez_promedio=("madurez_valor", "mean"),
        )
    )
    proyectos = proyectos.merge(project_gaps, on="proyecto_id", how="left")
    proyectos["brecha_asociada"] = proyectos["brecha_asociada"].fillna(0.0)
    proyectos["controles_relacionados"] = proyectos["controles_relacionados"].fillna(0).astype(int)
    proyectos["madurez_promedio"] = proyectos["madurez_promedio"].fillna(0.0)
    proyectos["prioridad"] = proyectos["brecha_asociada"] * (1 + proyectos["aporte_seguridad"])
    proyectos = proyectos.sort_values(["prioridad", "controles_relacionados"], ascending=False)

    project_cols = ["proyecto_id", "titulo", "plazo", "tipo_seguridad", "esfuerzo_jornadas", "aporte_seguridad", "prioridad"]
    trazabilidad = linked.merge(proyectos[project_cols], on="proyecto_id", how="left", suffixes=("_control", "_proyecto"))
    for column in ["plazo", "tipo_seguridad"]:
        project_column = f"{column}_proyecto"
        control_column = f"{column}_control"
        if project_column in trazabilidad.columns:
            fallback = trazabilidad[control_column] if control_column in trazabilidad.columns else ""
            trazabilidad[column] = trazabilidad[project_column].fillna(fallback)
        elif control_column in trazabilidad.columns:
            trazabilidad[column] = trazabilidad[control_column]
        else:
            trazabilidad[column] = ""
    trazabilidad["peso_brecha"] = trazabilidad["peso_brecha"].fillna(0.0)
    trazabilidad["prioridad"] = trazabilidad["prioridad"].fillna(0.0)
    trazabilidad["esfuerzo_jornadas"] = trazabilidad["esfuerzo_jornadas"].fillna(0.0)

    proyectos_plazo = (
        proyectos.groupby("plazo", as_index=False)
        .agg(
            proyectos=("proyecto_id", "nunique"),
            esfuerzo_jornadas=("esfuerzo_jornadas", "sum"),
            prioridad=("prioridad", "sum"),
            controles_relacionados=("controles_relacionados", "sum"),
        )
        .sort_values("prioridad", ascending=False)
    )

    project_type_rows: list[dict[str, Any]] = []
    for column, label in PROJECT_TYPES.items():
        project_type_rows.append(
            {
                "tipo": label,
                "controles": float(proyectos[column].sum()),
                "proyectos": int((proyectos[column] > 0).sum()),
                "prioridad": float(proyectos.loc[proyectos[column] > 0, "prioridad"].sum()),
            }
        )
    proyectos_tipo = pd.DataFrame(project_type_rows).sort_values("controles", ascending=False)
    proyectos_capitulo = _project_chapter_summary(trazabilidad)
    proyectos_capacidad = _project_capacity_summary(trazabilidad)
    esfuerzo_roadmap = _effort_roadmap(proyectos)
    quick_wins = _quick_wins(proyectos)

    resumen = {
        "empresa_id": dataset["empresa_id"],
        "empresa_nombre": dataset["empresa"].get("nombre", dataset["empresa_id"]),
        "estandar_id": dataset["estandar_id"],
        "controles_evaluados": int(len(controles)),
        "capitulos_evaluados": int(capitulos["capitulo"].nunique()),
        "proyectos": int(len(proyectos)),
        "entrevistas": int(len(entrevistas)),
        "quick_wins": int((quick_wins["cuadrante"] == "Quick win").sum()) if not quick_wins.empty else 0,
        "esfuerzo_total": round(float(proyectos["esfuerzo_jornadas"].sum()), 1) if not proyectos.empty else 0,
        "madurez_global": round(madurez_global, 4),
        "madurez_global_pct": round(madurez_global * 100, 1),
        "brecha_global": round(brecha_global, 4),
        "brecha_global_pct": round(brecha_global * 100, 1),
        "capitulo_mas_debil": str(capitulos.iloc[0]["capitulo"]) if not capitulos.empty else "",
        "control_mas_critico": str(top_brechas.iloc[0]["control_id"]) if not top_brechas.empty else "",
        "proyecto_prioritario": str(proyectos.iloc[0]["proyecto_id"]) if not proyectos.empty else "",
        "capacidad_mas_debil": str(capacidad_operacional.iloc[0]["atributo"]) if not capacidad_operacional.empty else "",
        "funcion_mas_debil": str(ciberfunciones.iloc[0]["atributo"]) if not ciberfunciones.empty else "",
    }

    return MetricResult(
        empresa=dataset["empresa"],
        controles=controles,
        capitulos=capitulos,
        proyectos=proyectos,
        top_brechas=top_brechas,
        madurez_distribucion=madurez_distribucion,
        matriz_madurez=matriz_madurez,
        tipo_control=tipo_control,
        propiedades_seguridad=propiedades_seguridad,
        ciberfunciones=ciberfunciones,
        capacidad_operacional=capacidad_operacional,
        dominios_seguridad=dominios_seguridad,
        proyectos_plazo=proyectos_plazo,
        proyectos_tipo=proyectos_tipo,
        proyectos_capitulo=proyectos_capitulo,
        proyectos_capacidad=proyectos_capacidad,
        esfuerzo_roadmap=esfuerzo_roadmap,
        quick_wins=quick_wins,
        trazabilidad=trazabilidad,
        entrevistas=entrevistas,
        resumen=resumen,
    )
