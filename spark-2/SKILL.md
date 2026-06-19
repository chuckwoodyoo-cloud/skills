---
name: spark-2
description: Build, debug, extend, verify, or migrate Spark 2.0 / @sparkjsdev/spark Gaussian Splatting apps and official examples. Use when working with SparkRenderer, SplatMesh, PackedSplats, ExtSplats, RAD/LoD/paged streaming, Dyno shader graphs, SplatEdit, SparkControls, SparkXr, raycasting, procedural splats, black-canvas/debugging issues, or this Spark repo's src/examples/docs/Rust WASM tooling.
---

# Spark 2.0

Use this skill for Spark 2.0 work in the `@sparkjsdev/spark` repo or in apps that consume it. Favor current source and official examples over remembered API details.

## First Checks

- Inspect `package.json`, `src/index.ts`, and the target example/docs before changing code.
- Treat docs that mention `NewSparkRenderer` as older wording in this repo. Current exports and official examples use `SparkRenderer`.
- If an example and source disagree, trust `src/` and `dist/types/` after a successful build, then fix or call out the example drift.
- Add `new SparkRenderer({ renderer })` to the scene hierarchy. Spark apps render no splats without it.
- Build examples against `dist/spark.module.js`; run the library build before judging local examples.

## Reference Routing

- Read `references/project-map.md` for repo layout, install/build commands, Rust/WASM, assets, and common setup failures.
- Read `references/api-patterns.md` for common Spark 2.0 snippets: minimal scene, loading, LoD/streaming, Dyno, procedural splats, edits, raycasting, controls, XR, and cleanup.
- Read `references/api-symbols.md` when deciding which exported class/function/namespace to use or when an import fails.
- Read `references/examples-catalog.md` to choose which official example to copy or compare before implementing a feature.
- Read `references/recipes.md` for end-to-end workflows such as new examples, streaming RAD worlds, prebuilt LoD assets, Dyno effects, picking/painting, XR, and migration.
- Read `references/troubleshooting.md` for black canvas, import/build, CORS/Range, LoD quality, performance, Dyno, and interaction failures.
- Run `scripts/check_spark_repo.py <repo>` when setup state is unclear or Vite/build errors suggest stale dist, missing WASM packages, or broken local dependency links.

## Workflow

1. Classify the request:
   - Setup/build/package problem: load `project-map.md`.
   - Debugging/black-canvas/import/performance problem: load `troubleshooting.md`, then `project-map.md` if setup is involved.
   - API/import/symbol-selection question: load `api-symbols.md`, then verify against `src/index.ts`.
   - App/example implementation: load `recipes.md`, `api-patterns.md`, and `examples-catalog.md`.
   - LoD, RAD, huge scenes, or streaming: load `recipes.md`, `api-patterns.md`, `examples-catalog.md`, and `project-map.md`.
   - Dyno shader effects, splat edits, raycasting, XR, portals, or viewer/editor features: load `api-patterns.md` and the matching rows in `examples-catalog.md`.
   - Migration from Spark 0.1 or older examples: load `recipes.md`, `project-map.md`, and inspect `src/index.ts`.
2. Read the closest official example file before writing new code. Prefer adapting a working example over inventing Spark plumbing from scratch.
3. Keep Three.js and Spark lifecycles explicit: create scene/camera/renderer, add `SparkRenderer`, create and transform `SplatMesh` or procedural sources, update controls/uniforms, then call `renderer.render(scene, camera)` inside `setAnimationLoop`.
4. For Dyno graph changes, use `dyno.*` operations instead of JavaScript arithmetic inside graphs. Use uniforms for per-frame values and call `mesh.updateVersion()` for value changes or `mesh.updateGenerator()` when graph structure changes.
5. Validate with the smallest command that exercises the change. For repo changes, prefer `npm test`, `npm run build`, and a Vite/browser check of the affected example. For visual examples, inspect the page in a browser and confirm the canvas is nonblank and interactive.

## Output Standards

- Mention exact example or source files used as references.
- Explain Spark-specific tradeoffs when relevant: packed vs extended encoding, on-demand LoD vs prebuilt RAD, paged streaming memory budget, sort mode, and GPU/CPU readback cost.
- Do not promise that browser streaming works from `file://`; use a local HTTP server for assets and Range requests.
- When fixing setup on Windows, account for PowerShell execution policy and local `file:` dependencies to Rust-generated `pkg` folders.
