#!/usr/bin/env python3
"""
Render helper for Human Image.

The intelligence stays in Claude: it writes the visual prompt and chooses the
creative direction. This script only checks Higgsfield CLI/login, submits the
prompt, waits for the result, and downloads the generated image.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
URL_RE = re.compile(r"https://[^ \"']+\.(?:png|jpg|jpeg|webp)(?:\?[^ \"']*)?", re.I)

ASPECT_RATIOS = {"auto", "1:1", "3:2", "2:3", "4:3", "3:4", "4:5", "5:4", "9:16", "16:9", "21:9"}
RESOLUTIONS = {"1k", "2k", "4k"}


def now_slug() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def model_name() -> str:
    return os.environ.get("HIGGSFIELD_IMAGE_MODEL", "nano_banana_2")


def run_cmd(args: list[str], timeout: int = 1800) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )


def parse_first_uuid(text: str) -> str | None:
    match = UUID_RE.search(text)
    return match.group(0) if match else None


def parse_first_url(text: str) -> str | None:
    match = URL_RE.search(text)
    return match.group(0) if match else None


def upload_reference(path: Path) -> str | None:
    result = run_cmd(["higgsfield", "upload", "create", str(path)], timeout=300)
    uuid = parse_first_uuid(result.stdout)
    if not uuid:
        print(f"ERRO: nao consegui extrair UUID do upload de referencia {path.name}. Saida: {result.stdout[:800]}", file=sys.stderr)
    return uuid


def check_cli() -> int:
    if not shutil.which("higgsfield"):
        print(json.dumps({
            "status": "missing",
            "message": "Higgsfield CLI nao encontrado. Instale com: npm install -g @higgsfield/cli",
        }, ensure_ascii=False))
        return 1

    result = run_cmd(["higgsfield", "account", "status"], timeout=60)
    if result.returncode == 0:
        print(json.dumps({
            "status": "ok",
            "message": "Higgsfield CLI instalado e autenticado.",
            "detail": result.stdout.strip()[:800],
        }, ensure_ascii=False))
        return 0

    print(json.dumps({
        "status": "login_required",
        "message": "Higgsfield CLI existe, mas precisa de login. Rode higgsfield auth login.",
        "detail": result.stdout.strip()[:800],
    }, ensure_ascii=False))
    return 2


def render(prompt_file: str, aspect_ratio: str, resolution: str, output_dir: str | None, output_name: str | None, reference_images: list[str]) -> int:
    if aspect_ratio not in ASPECT_RATIOS:
        print(f"ERRO: aspect_ratio invalido: {aspect_ratio}. Use: {', '.join(sorted(ASPECT_RATIOS))}", file=sys.stderr)
        return 1

    if resolution not in RESOLUTIONS:
        print(f"ERRO: resolution invalida: {resolution}. Use: 1k, 2k ou 4k.", file=sys.stderr)
        return 1

    check = check_cli()
    if check != 0:
        return check

    prompt_path = Path(prompt_file).expanduser().resolve()
    if not prompt_path.exists():
        print(f"ERRO: prompt-file nao existe: {prompt_path}", file=sys.stderr)
        return 1

    prompt = prompt_path.read_text(encoding="utf-8")
    out_dir = Path(output_dir).expanduser().resolve() if output_dir else ROOT / "output" / now_slug()
    out_dir.mkdir(parents=True, exist_ok=True)
    logs_dir = out_dir / "_logs"
    logs_dir.mkdir(exist_ok=True)

    model = model_name()
    uploaded_refs: list[str] = []
    for ref in reference_images:
        ref_path = Path(ref).expanduser().resolve()
        if not ref_path.exists():
            print(f"ERRO: referencia nao existe: {ref_path}", file=sys.stderr)
            return 1
        uuid = upload_reference(ref_path)
        if uuid:
            uploaded_refs.append(uuid)

    args = [
        "higgsfield", "generate", "create", model,
        "--prompt", prompt,
        "--aspect_ratio", aspect_ratio,
        "--resolution", resolution,
        "--json",
    ]

    for ref in uploaded_refs:
        args.extend(["--image", ref])

    create = run_cmd(args, timeout=300)
    job_id = parse_first_uuid(create.stdout)
    if not job_id:
        print(f"ERRO: Higgsfield nao retornou job_id. Saida: {create.stdout[:1200]}", file=sys.stderr)
        return 1

    wait = run_cmd(["higgsfield", "generate", "wait", job_id, "--wait-timeout", "30m", "--json"], timeout=2100)
    combined = create.stdout + "\n" + wait.stdout
    out_url = parse_first_url(combined)
    if not out_url:
        print(f"ERRO: Higgsfield nao retornou URL de imagem. Saida: {combined[:1600]}", file=sys.stderr)
        return 1

    out_path = out_dir / (output_name or "image.png")
    try:
        with urllib.request.urlopen(out_url, timeout=120) as resp:
            img_bytes = resp.read()
        out_path.write_bytes(img_bytes)
    except (urllib.error.HTTPError, urllib.error.URLError) as exc:
        print(f"ERRO ao baixar imagem gerada: {exc}", file=sys.stderr)
        return 1

    metadata = {
        "status": "ok",
        "created_at": now_iso(),
        "provider": "higgsfield_cli",
        "model": model,
        "job_id": job_id,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "prompt_file": str(prompt_path),
        "output_path": str(out_path),
        "output_size_kb": len(img_bytes) // 1024,
        "higgsfield_url": out_url,
        "references": [str(Path(ref).expanduser().resolve()) for ref in reference_images],
        "reference_uuids": uploaded_refs,
    }
    (out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    (logs_dir / f"{out_path.stem}.json").write_text(json.dumps({
        "stdout": combined[-5000:],
        **metadata,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(metadata, indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="render_image.py", description="Render Human Image via Higgsfield CLI.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check-cli", help="valida Higgsfield CLI/login")

    p_render = sub.add_parser("render", help="renderiza uma imagem via Higgsfield CLI")
    p_render.add_argument("prompt_file")
    p_render.add_argument("--aspect-ratio", default="1:1", choices=sorted(ASPECT_RATIOS))
    p_render.add_argument("--resolution", default="2k", choices=sorted(RESOLUTIONS))
    p_render.add_argument("--output-dir", default=None)
    p_render.add_argument("--output-name", default=None)
    p_render.add_argument("--reference", action="append", default=[])

    args = parser.parse_args(argv)
    if args.cmd == "check-cli":
        return check_cli()
    if args.cmd == "render":
        return render(args.prompt_file, args.aspect_ratio, args.resolution, args.output_dir, args.output_name, args.reference)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
