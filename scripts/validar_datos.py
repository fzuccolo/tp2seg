from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from motor.datos import load_config, load_yaml, repo_root


ROOT = repo_root()


REQUIRED = {
    "catalogo_controles.csv": {"control_id", "capitulo", "control_nombre", "pregunta", "aplica", "peso"},
    "parametros_madurez.csv": {"nivel", "nombre", "valor"},
    "activos.csv": {"activo_id", "tipo", "nombre", "criticidad_cid", "propietario", "proceso"},
    "diagnostico.csv": {"control_id", "nivel_madurez", "evidencia", "entrevistado", "fecha", "observaciones"},
    "proyectos.csv": {"proyecto_id", "titulo", "plazo", "esfuerzo_jornadas", "aporte_seguridad", "descripcion", "dependencias"},
    "proyecto_control.csv": {"proyecto_id", "control_id"},
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

    read_csv(company_dir / "activos.csv")
    diagnostico = read_csv(company_dir / "diagnostico.csv")
    proyectos = read_csv(company_dir / "proyectos.csv")
    proyecto_control = read_csv(company_dir / "proyecto_control.csv")

    diag_controls = set(diagnostico["control_id"].astype(str))
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
