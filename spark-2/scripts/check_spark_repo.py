#!/usr/bin/env python3
"""Lightweight Spark 2.0 repository health check."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys


def status(kind: str, message: str) -> None:
    print(f"{kind}: {message}")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def same_resolved_path(a: Path, b: Path) -> bool:
    try:
        return os.path.normcase(str(a.resolve())) == os.path.normcase(str(b.resolve()))
    except OSError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a Spark 2.0 repo checkout.")
    parser.add_argument("repo", nargs="?", default=".", help="Path to the Spark repo")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    failures: list[str] = []
    warnings: list[str] = []

    package_json = repo / "package.json"
    if not package_json.exists():
        failures.append(f"missing {package_json}")
    else:
        package = load_json(package_json)
        if package.get("name") != "@sparkjsdev/spark":
            warnings.append(f"unexpected package name: {package.get('name')!r}")
        scripts = package.get("scripts", {})
        for script in ["build", "build:wasm", "build-lod", "start", "test"]:
            if script not in scripts:
                failures.append(f"missing npm script: {script}")
        deps = {}
        deps.update(package.get("dependencies", {}))
        deps.update(package.get("devDependencies", {}))
        for dep in ["three", "vite", "spark-rs", "spark-worker-rs"]:
            if dep not in deps:
                failures.append(f"missing dependency: {dep}")

    required_files = [
        "src/index.ts",
        "src/SparkRenderer.ts",
        "src/SplatMesh.ts",
        "vite.config.ts",
        "examples/streaming-lod/index.html",
        "docs/docs/spark-renderer.md",
        "rust/Cargo.toml",
    ]
    for rel in required_files:
        if not (repo / rel).exists():
            failures.append(f"missing {rel}")

    for rel in ["rust/spark-rs/pkg/package.json", "rust/spark-worker-rs/pkg/package.json"]:
        if not (repo / rel).exists():
            failures.append(f"missing generated wasm package {rel}")

    for name, target_rel in [
        ("spark-rs", "rust/spark-rs/pkg"),
        ("spark-worker-rs", "rust/spark-worker-rs/pkg"),
    ]:
        link = repo / "node_modules" / name
        target = repo / target_rel
        if not link.exists():
            warnings.append(f"node_modules/{name} is missing; run npm install after wasm packages exist")
        elif not same_resolved_path(link, target):
            failures.append(f"node_modules/{name} points to {link.resolve()} instead of {target}")

    for rel in ["dist/spark.module.js", "dist/spark.cjs.js", "dist/types/index.d.ts"]:
        if not (repo / rel).exists():
            warnings.append(f"missing build output {rel}; run npm run build before serving examples")

    examples = sorted((repo / "examples").glob("**/index.html")) if (repo / "examples").exists() else []
    if len(examples) < 10:
        warnings.append(f"found only {len(examples)} example index files")

    if failures:
        for item in failures:
            status("FAIL", item)
    if warnings:
        for item in warnings:
            status("WARN", item)
    if not failures and not warnings:
        status("OK", f"{repo} looks like a ready Spark 2.0 checkout")
    elif not failures:
        status("OK", f"{repo} passed hard checks with {len(warnings)} warning(s)")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
