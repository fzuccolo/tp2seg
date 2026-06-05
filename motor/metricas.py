from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class MetricResult:
    empresa: dict[str, Any]
    controles: pd.DataFrame
    capitulos: pd.DataFrame
    proyectos: pd.DataFrame
    top_brechas: pd.DataFrame
    resumen: dict[str, Any]


def _weighted_average(df: pd.DataFrame, value_col: str, weight_col: str) -> float:
    total_weight = float(df[weight_col].sum())
    if total_weight == 0:
        return 0.0
    return float((df[value_col] * df[weight_col]).sum() / total_weight)


def compute_metrics(dataset: dict[str, Any]) -> MetricResult:
    catalogo = dataset["catalogo"].copy()
    diagnostico = dataset["diagnostico"].copy()
    madurez = dataset["madurez"].copy()
    proyectos = dataset["proyectos"].copy()
    proyecto_control = dataset["proyecto_control"].copy()

    madurez["nivel"] = madurez["nivel"].astype(int)
    diagnostico["nivel_madurez"] = diagnostico["nivel_madurez"].astype(int)
    catalogo["peso"] = catalogo["peso"].astype(float)
    catalogo["aplica"] = catalogo["aplica"].astype(int)

    controles = catalogo.merge(diagnostico, on="control_id", how="left")
    controles = controles.merge(
        madurez.rename(columns={"nivel": "nivel_madurez", "nombre": "madurez_nombre", "valor": "madurez_valor"}),
        on="nivel_madurez",
        how="left",
    )
    controles = controles[controles["aplica"] == 1].copy()
    controles["madurez_valor"] = controles["madurez_valor"].fillna(0.0).astype(float)
    controles["brecha"] = 1.0 - controles["madurez_valor"]
    controles["peso_brecha"] = controles["brecha"] * controles["peso"]
    controles["cumplimiento_pct"] = controles["madurez_valor"] * 100
    controles["brecha_pct"] = controles["brecha"] * 100

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
    capitulos = capitulos.sort_values("madurez", ascending=True)

    top_brechas = controles.sort_values(["peso_brecha", "peso"], ascending=False).head(10).copy()

    proyectos = proyectos.copy()
    proyectos["esfuerzo_jornadas"] = proyectos["esfuerzo_jornadas"].astype(float)
    proyectos["aporte_seguridad"] = proyectos["aporte_seguridad"].astype(float)
    linked = proyecto_control.merge(
        controles[["control_id", "control_nombre", "capitulo", "peso_brecha"]],
        on="control_id",
        how="left",
    )
    project_gaps = (
        linked.groupby("proyecto_id", as_index=False)
        .agg(
            brecha_asociada=("peso_brecha", "sum"),
            controles_relacionados=("control_id", "nunique"),
        )
    )
    proyectos = proyectos.merge(project_gaps, on="proyecto_id", how="left")
    proyectos["brecha_asociada"] = proyectos["brecha_asociada"].fillna(0.0)
    proyectos["controles_relacionados"] = proyectos["controles_relacionados"].fillna(0).astype(int)
    proyectos["prioridad"] = proyectos["brecha_asociada"] * proyectos["aporte_seguridad"]
    proyectos = proyectos.sort_values(["prioridad", "aporte_seguridad"], ascending=False)

    resumen = {
        "empresa_id": dataset["empresa_id"],
        "empresa_nombre": dataset["empresa"].get("nombre", dataset["empresa_id"]),
        "estandar_id": dataset["estandar_id"],
        "controles_evaluados": int(len(controles)),
        "capitulos_evaluados": int(capitulos["capitulo"].nunique()),
        "proyectos": int(len(proyectos)),
        "madurez_global": round(madurez_global, 4),
        "madurez_global_pct": round(madurez_global * 100, 1),
        "brecha_global": round(brecha_global, 4),
        "brecha_global_pct": round(brecha_global * 100, 1),
        "capitulo_mas_debil": str(capitulos.iloc[0]["capitulo"]) if not capitulos.empty else "",
        "control_mas_critico": str(top_brechas.iloc[0]["control_id"]) if not top_brechas.empty else "",
        "proyecto_prioritario": str(proyectos.iloc[0]["proyecto_id"]) if not proyectos.empty else "",
    }

    return MetricResult(
        empresa=dataset["empresa"],
        controles=controles,
        capitulos=capitulos,
        proyectos=proyectos,
        top_brechas=top_brechas,
        resumen=resumen,
    )
