from __future__ import annotations

import json
import shutil
import subprocess
import sys
import os
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.datos import list_cases, load_config, load_dataset, repo_root
from app.metricas import compute_metrics
from app.pptx_export import write_pptx
from app.render import write_outputs


ROOT = repo_root()
DELIVERABLE_CASE = "tecnohogar"


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


def render_quarto_pdf(input_file: Path, output_file: Path) -> None:
    if not input_file.exists():
        return
    if shutil.which("quarto") is None:
        raise RuntimeError("No se encontro quarto en PATH")

    generated_name = f"{output_file.parent.parent.name}-{output_file.name}"
    generated = ROOT / generated_name
    if generated.exists():
        generated.unlink()

    cache_dir = ROOT / ".cache" / "quarto"
    deno_dir = ROOT / ".cache" / "deno"
    cache_dir.mkdir(parents=True, exist_ok=True)
    deno_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["XDG_CACHE_HOME"] = str(cache_dir)
    env["DENO_DIR"] = str(deno_dir)

    input_arg = input_file.relative_to(ROOT)
    subprocess.run(
        ["quarto", "render", str(input_arg), "--to", "typst", "--output", generated_name],
        cwd=ROOT,
        env=env,
        check=True,
    )
    if not generated.exists():
        raise RuntimeError(f"No se genero {generated}")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    if output_file.exists():
        output_file.unlink()
    shutil.move(str(generated), output_file)


def package_deliverables(caso_id: str) -> None:
    build_dir = ROOT / ".build" / caso_id
    pptx = build_dir / "slides" / "presentacion.pptx"
    pdf = build_dir / "informe" / "informe.pdf"
    if not pptx.exists() or not pdf.exists():
        missing = [str(path.relative_to(ROOT)) for path in [pptx, pdf] if not path.exists()]
        raise RuntimeError(f"No se pueden empaquetar entregables; faltan {missing}")

    timestamp = os.environ.get("BUILD_TIMESTAMP") or datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    output_dir = ROOT / ".build" / "entregables"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    stable_pptx = output_dir / "tp2-tecnohogar-presentacion.pptx"
    stable_pdf = output_dir / "tp2-tecnohogar-informe.pdf"
    stable_zip = output_dir / "tp2-tecnohogar-entregables.zip"
    manifest = output_dir / "manifest.json"

    shutil.copy2(pptx, stable_pptx)
    shutil.copy2(pdf, stable_pdf)
    manifest.write_text(
        json.dumps(
            {
                "caso": caso_id,
                "generated_at_utc": timestamp,
                "files": [stable_pptx.name, stable_pdf.name, stable_zip.name],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    with zipfile.ZipFile(stable_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(stable_pptx, stable_pptx.name)
        archive.write(stable_pdf, stable_pdf.name)
        archive.write(manifest, manifest.name)


def main() -> int:
    config = load_config(ROOT)
    deliverable_case = str(config.get("caso_default") or DELIVERABLE_CASE)

    for caso_id in list_cases(ROOT):
        dataset = load_dataset(caso_id, ROOT)
        result = compute_metrics(dataset)
        company_output = ROOT / ".build" / caso_id
        if company_output.exists():
            shutil.rmtree(company_output)
        write_outputs(result, company_output)

        render_quarto(ROOT / "docs" / "informe" / caso_id / "informe.qmd", company_output / "informe")
        render_quarto_pdf(ROOT / "docs" / "informe" / caso_id / "informe.qmd", company_output / "informe" / "informe.pdf")
        render_quarto(ROOT / "docs" / "slides" / caso_id / "presentacion.qmd", company_output / "slides")
        write_pptx(result, company_output / "slides" / "presentacion.pptx")

        print(f"Generadas salidas para {caso_id}: {company_output}")

    package_deliverables(deliverable_case)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
