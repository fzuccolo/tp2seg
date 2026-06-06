from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.datos import load_config, load_yaml, repo_root


ROOT = repo_root()


REQUIRED = {
    "catalogo_controles.csv": {"control_id", "capitulo", "control_nombre", "pregunta", "aplica", "peso"},
    "parametros_madurez.csv": {"nivel", "nombre", "valor"},
    "activos.csv": {"activo_id", "tipo", "nombre", "criticidad_cid", "propietario", "proceso"},
    "diagnostico.csv": {"control_id", "nivel_madurez", "evidencia", "entrevistado", "fecha", "observaciones"},
    "proyectos.csv": {"proyecto_id", "titulo", "plazo", "esfuerzo_jornadas", "aporte_seguridad", "descripcion", "dependencias"},
    "proyecto_control.csv": {"proyecto_id", "control_id"},
    "entrevistas.csv": {"entrevista_id", "nombre", "area", "empresa", "cargo"},
}

ISO_27002_2022_CHAPTER_COUNTS = {
    "5 - Controles Organizativos": 37,
    "6 - Controles de Personas": 8,
    "7 - Controles Físicos": 14,
    "8 - Controles Tecnológicos": 34,
}

EXTENDED_CATALOG_COLUMNS = {
    "proposito",
    "tipo_preventivo",
    "tipo_detectivo",
    "tipo_correctivo",
    "prop_confidencialidad",
    "prop_integridad",
    "prop_disponibilidad",
    "func_identificacion",
    "func_proteccion",
    "func_deteccion",
    "func_respuesta",
    "func_recuperacion",
    "tipo_seguridad",
    "proyecto_sugerido",
    "plazo_sugerido",
}

BINARY_CATALOG_COLUMNS = {
    "tipo_preventivo",
    "tipo_detectivo",
    "tipo_correctivo",
    "prop_confidencialidad",
    "prop_integridad",
    "prop_disponibilidad",
    "func_identificacion",
    "func_proteccion",
    "func_deteccion",
    "func_respuesta",
    "func_recuperacion",
}


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise ValueError(f"Falta archivo: {path}")
    df = pd.read_csv(path, dtype={"control_id": str, "proyecto_id": str})
    missing = REQUIRED[path.name] - set(df.columns)
    if missing:
        raise ValueError(f"{path} no tiene columnas requeridas: {sorted(missing)}")
    return df


def validate_standard(standard_dir: Path) -> tuple[pd.DataFrame, set[int]]:
    catalogo = read_csv(standard_dir / "catalogo_controles.csv")
    madurez = read_csv(standard_dir / "parametros_madurez.csv")

    if catalogo["control_id"].duplicated().any():
        raise ValueError(f"{standard_dir}: control_id duplicado")
    missing_extended = EXTENDED_CATALOG_COLUMNS - set(catalogo.columns)
    if missing_extended:
        raise ValueError(f"{standard_dir}: catalogo sin columnas extendidas {sorted(missing_extended)}")

    if standard_dir.name == "iso27002_2022":
        counts = catalogo.groupby("capitulo")["control_id"].nunique().to_dict()
        if counts != ISO_27002_2022_CHAPTER_COUNTS:
            raise ValueError(f"{standard_dir}: distribucion ISO 27002:2022 inesperada {counts}")

    for column in BINARY_CATALOG_COLUMNS & set(catalogo.columns):
        values = pd.to_numeric(catalogo[column], errors="coerce").dropna()
        invalid = set(values.astype(int)) - {0, 1}
        if invalid:
            raise ValueError(f"{standard_dir}: {column} debe ser binario 0/1")

    madurez["nivel"] = madurez["nivel"].astype(int)
    levels = set(madurez["nivel"])
    if levels != {0, 1, 2, 3, 4, 5}:
        raise ValueError(f"{standard_dir}: parametros_madurez debe tener niveles 0..5")

    if not madurez["valor"].between(0, 1).all():
        raise ValueError(f"{standard_dir}: valores de madurez fuera de rango")

    return catalogo, levels


def validate_company(company_dir: Path, standards_dir: Path) -> None:
    empresa = load_yaml(company_dir / "empresa.yml")
    standard_id = empresa.get("estandar")
    if not standard_id:
        raise ValueError(f"{company_dir}: empresa.yml debe declarar estandar")

    catalogo, valid_levels = validate_standard(standards_dir / str(standard_id))
    known_controls = set(catalogo["control_id"].astype(str))

    activos = read_csv(company_dir / "activos.csv")
    diagnostico = read_csv(company_dir / "diagnostico.csv")
    proyectos = read_csv(company_dir / "proyectos.csv")
    proyecto_control = read_csv(company_dir / "proyecto_control.csv")
    entrevistas_path = company_dir / "entrevistas.csv"
    entrevistas = read_csv(entrevistas_path) if entrevistas_path.exists() else pd.DataFrame()

    diag_controls = set(diagnostico["control_id"].astype(str))
    if diagnostico["control_id"].duplicated().any():
        raise ValueError(f"{company_dir}: diagnostico tiene controles duplicados")
    unknown_diag = diag_controls - known_controls
    if unknown_diag:
        raise ValueError(f"{company_dir}: diagnostico referencia controles inexistentes {sorted(unknown_diag)}")

    levels = set(diagnostico["nivel_madurez"].astype(int))
    invalid_levels = levels - valid_levels
    if invalid_levels:
        raise ValueError(f"{company_dir}: niveles de madurez invalidos {sorted(invalid_levels)}")

    known_projects = set(proyectos["proyecto_id"].astype(str))
    unknown_projects = set(proyecto_control["proyecto_id"].astype(str)) - known_projects
    if unknown_projects:
        raise ValueError(f"{company_dir}: proyecto_control referencia proyectos inexistentes {sorted(unknown_projects)}")

    unknown_controls = set(proyecto_control["control_id"].astype(str)) - known_controls
    if unknown_controls:
        raise ValueError(f"{company_dir}: proyecto_control referencia controles inexistentes {sorted(unknown_controls)}")

    if company_dir.name == "ejemplo":
        missing_diag = known_controls - diag_controls
        if len(diagnostico) != 93 or missing_diag:
            raise ValueError(f"{company_dir}: ejemplo debe cubrir los 93 controles ISO, faltan {sorted(missing_diag)}")
        if len(entrevistas) != 7:
            raise ValueError(f"{company_dir}: ejemplo debe conservar 7 entrevistas de la fuente")
        if len(proyectos) != 45:
            raise ValueError(f"{company_dir}: ejemplo debe conservar 45 proyectos de referencia")
        if len(proyecto_control) != 93:
            raise ValueError(f"{company_dir}: ejemplo debe conservar 93 vinculos control-proyecto")

    if company_dir.name == "tecnohogar":
        missing_diag = known_controls - diag_controls
        if len(diagnostico) != 93 or missing_diag:
            raise ValueError(f"{company_dir}: tecnohogar debe cubrir los 93 controles ISO, faltan {sorted(missing_diag)}")
        if len(activos) != 41:
            raise ValueError(f"{company_dir}: tecnohogar debe conservar los 41 activos del TP1")
        if len(entrevistas) < 6:
            raise ValueError(f"{company_dir}: tecnohogar debe registrar las 6 entrevistas/fuentes principales")

        required_asset_detail = {"confidencialidad", "integridad", "disponibilidad"}
        missing_asset_detail = required_asset_detail - set(activos.columns)
        if missing_asset_detail:
            raise ValueError(f"{company_dir}: activos.csv sin columnas CID {sorted(missing_asset_detail)}")

        info_assets = activos[activos["tipo"].astype(str).str.lower() == "informacion"].copy()
        if len(info_assets) != 13:
            raise ValueError(f"{company_dir}: tecnohogar debe conservar 13 activos de informacion del TP1")
        for column in required_asset_detail | {"criticidad_cid"}:
            values = pd.to_numeric(info_assets[column], errors="coerce")
            if values.isna().any() or not values.between(1, 5).all():
                raise ValueError(f"{company_dir}: {column} debe estar completo con valores 1..5 para activos de informacion")

        weak = diagnostico[pd.to_numeric(diagnostico["nivel_madurez"], errors="coerce").fillna(0).astype(int) <= 2].copy()
        for column in ["hallazgo", "observaciones"]:
            if column not in weak.columns or weak[column].fillna("").astype(str).str.strip().eq("").any():
                raise ValueError(f"{company_dir}: controles debiles deben tener {column}")
        linked_controls = set(proyecto_control["control_id"].astype(str))
        weak_without_project = set(weak["control_id"].astype(str)) - linked_controls
        if weak_without_project:
            raise ValueError(f"{company_dir}: controles debiles sin proyecto asociado {sorted(weak_without_project)}")


def main() -> int:
    errors: list[str] = []
    try:
        config = load_config(ROOT)
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1

    standards_dir = ROOT / "datos" / "estandares"
    companies_dir = ROOT / "datos" / "empresas"

    if not (companies_dir / str(config["empresa_default"])).exists():
        errors.append("empresa_default no existe")
    if not (standards_dir / str(config["estandar_default"])).exists():
        errors.append("estandar_default no existe")

    for company_dir in sorted(path for path in companies_dir.iterdir() if path.is_dir()):
        try:
            validate_company(company_dir, standards_dir)
        except Exception as exc:
            errors.append(str(exc))

    if errors:
        print("Validacion fallida:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validacion OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
