from __future__ import annotations

import shutil
import subprocess
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.datos import list_companies, load_dataset, repo_root
from app.metricas import compute_metrics
from app.render import write_outputs


ROOT = repo_root()


def render_quarto(input_file: Path, output_dir: Path) -> None:
    if not input_file.exists():
        return
    if shutil.which("quarto") is None:
        raise RuntimeError("No se encontro quarto en PATH")

    temp_root = ROOT / ".build" / ".quarto_tmp" / input_file.parent.relative_to(ROOT)
    temp_dir = temp_root / output_dir.name
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    cache_dir = ROOT / ".cache" / "quarto"
    deno_dir = ROOT / ".cache" / "deno"
    cache_dir.mkdir(parents=True, exist_ok=True)
    deno_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["XDG_CACHE_HOME"] = str(cache_dir)
    env["DENO_DIR"] = str(deno_dir)
    input_arg = input_file.relative_to(ROOT)
    subprocess.run(
        ["quarto", "render", str(input_arg), "--output-dir", str(temp_dir)],
        cwd=ROOT,
        env=env,
        check=True,
    )

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(temp_dir, output_dir)
    shutil.rmtree(temp_root)


def main() -> int:
    for empresa_id in list_companies(ROOT):
        dataset = load_dataset(empresa_id, ROOT)
        result = compute_metrics(dataset)
        company_output = ROOT / ".build" / empresa_id
        if company_output.exists():
            shutil.rmtree(company_output)
        write_outputs(result, company_output)

        render_quarto(ROOT / "docs" / "informe" / empresa_id / "informe.qmd", company_output / "informe")
        render_quarto(ROOT / "docs" / "slides" / empresa_id / "presentacion.qmd", company_output / "slides")

        print(f"Generadas salidas para {empresa_id}: {company_output}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
