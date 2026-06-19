# Spark 2.0 Project Map

## Source Of Truth

- Package: `package.json` names `@sparkjsdev/spark` at version `2.0.0`.
- Public exports: `src/index.ts`.
- Most reliable examples: `examples/**/index.html` and companion `.js` files.
- Documentation: `docs/docs/*.md`; useful, but verify names against `src/index.ts`.
- Current renderer name in this repo: `SparkRenderer`. Some docs still say `NewSparkRenderer`; do not use that name unless source exports it.

## Layout

- `src/`: TypeScript library source.
  - `SparkRenderer.ts`: scene-level renderer, LoD driver, offscreen targets, env maps, paged splat pool.
  - `SplatMesh.ts`: high-level `THREE.Object3D` for splat files, procedural splats, LoD, raycasting, edits, and modifiers.
  - `PackedSplats.ts`: compact 16-byte/splat storage and GPU generation.
  - `ExtSplats.ts`: 32-byte/splat extended precision storage for huge coordinate ranges.
  - `SplatLoader.ts`: file format detection and loading.
  - `SplatEdit.ts`: SDF-based RGBA/displacement editing.
  - `controls.ts`, `SparkXr.ts`, `SparkPortals.ts`: navigation, XR, and portals.
  - `dyno/`: typed shader graph blocks compiled to GLSL.
- `examples/`: official Vite-served examples. Import maps point at `../../dist/spark.module.js`, so build first.
- `docs/docs/`: public docs and guides.
- `rust/`: Rust workspace.
  - `spark-rs` and `spark-worker-rs`: wasm-pack packages consumed as local `file:` dependencies.
  - `spark-lib`: decoders, encoders, LoD algorithms, RAD/SPZ/PLY/SOGS logic.
  - `build-lod`: CLI for prebuilding LoD `.rad` files.
- `scripts/`: asset download/compression and docs/site utilities.

## Install And Build

- Package manager: npm, with `package-lock.json`.
- Normal install: `npm install`.
- WASM build: `npm run build:wasm`, which runs `rust/build_wasm.js`.
- Library build: `npm run build`, which runs production and dev Vite builds into `dist/`.
- Tests: `npm test`.
- Local examples: `npm start`, then open `/examples/...` on the Vite server.
- Optional assets: `npm run assets:download`; otherwise examples fetch from remote URLs.
- Docs: `npm run docs` after installing MkDocs Material.
- LoD CLI: `npm run build-lod -- input.ply input.spz --quality`.

## Rust And WASM Notes

- `build:wasm` requires `rustup`, `cargo`, target `wasm32-unknown-unknown`, and `wasm-pack`.
- `rust/build_rust_wasm.ps1` installs the wasm target and `wasm-pack` if missing, then builds `rust/spark-worker-rs/pkg` and `rust/spark-rs/pkg`.
- The root package has local dependencies `spark-rs: file:rust/spark-rs/pkg` and `spark-worker-rs: file:rust/spark-worker-rs/pkg`.
- If a checkout is moved and Vite cannot resolve `spark-rs` or `spark-worker-rs`, rerun `npm install` after WASM pkg folders exist, or repair the `node_modules` junctions/symlinks to point at the current checkout.

## Runtime Requirements And Gotchas

- Use Three.js r180 or newer for this repo unless the consuming app has a tested compatible peer version.
- Spark targets WebGL2. Create `THREE.WebGLRenderer` normally; WebGL antialiasing is not useful for Gaussian splats and can hurt performance.
- Local example import maps use `/examples/js/vendor/...`, served by a Vite middleware alias to `node_modules`.
- Paged `.rad` streaming should be served over HTTP with Range request support. Do not rely on `file://`.
- `.splat` and `.ksplat` cannot always be content-detected; provide `fileType` or a filename/URL extension.
- `.sog`/`.zip` SOGS support expects a zipped package, not a remote `manifest.json` with separate relative image URLs.
- PowerShell may block `.ps1` shims in `node_modules/.bin`; use `.cmd`, npm scripts, or the package JS entry when necessary.

## Validation Shortcuts

- API/package sanity: `npm test`.
- Build output and declarations: `npm run build`.
- Example smoke test: start Vite, open the changed example, check console errors, canvas content, resize behavior, and interaction.
- LoD/RAD changes: test both small on-demand `lod: true` and prebuilt `.rad`/`paged: true` paths when feasible.
