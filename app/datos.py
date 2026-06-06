from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml


ROOT = Path(__file__).resolve().parents[1]


def repo_root() -> Path:
    return ROOT


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} debe contener un objeto YAML")
    return data


def load_config(root: Path | None = None) -> dict[str, Any]:
    base = root or ROOT
    return load_yaml(base / "config.yml")


def list_cases(root: Path | None = None) -> list[str]:
    base = root or ROOT
    casos_dir = base / "datos" / "casos"
    return sorted(path.name for path in casos_dir.iterdir() if path.is_dir())


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path, dtype={"control_id": str, "proyecto_id": str})


def read_optional_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return read_csv(path)


def load_dataset(caso_id: str | None = None, root: Path | None = None) -> dict[str, Any]:
    base = root or ROOT
    config = load_config(base)
    default_case = config.get("caso_default")
    if caso_id is None and not default_case:
        raise ValueError("config.yml debe declarar caso_default")
    selected = caso_id or str(default_case)
    caso_dir = base / "datos" / "casos" / selected
    empresa = load_yaml(caso_dir / "caso.yml")
    estandar_id = str(empresa.get("estandar") or config["estandar_default"])
    estandar_dir = base / "datos" / "estandares" / estandar_id

    return {
        "root": base,
        "config": config,
        "empresa_id": selected,
        "empresa": empresa,
        "estandar_id": estandar_id,
        "catalogo": read_csv(estandar_dir / "catalogo_controles.csv"),
        "madurez": read_csv(estandar_dir / "parametros_madurez.csv"),
        "activos": read_csv(caso_dir / "activos.csv"),
        "diagnostico": read_csv(caso_dir / "diagnostico.csv"),
        "proyectos": read_csv(caso_dir / "proyectos.csv"),
        "proyecto_control": read_csv(caso_dir / "proyecto_control.csv"),
        "entrevistas": read_optional_csv(caso_dir / "entrevistas.csv"),
    }
