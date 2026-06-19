# Spark 2.0 Troubleshooting

## Black Canvas Or No Splats

- Confirm a `SparkRenderer` exists in the rendered scene hierarchy.
- Confirm the example/app imports a fresh `dist/spark.module.js`; run `npm run build`.
- Check the browser console for failed asset loads, CORS errors, MIME errors, or missing WASM chunks.
- Await `splatMesh.initialized` before querying bounding boxes or loaded data.
- Verify camera near/far and object transform. Many examples reorient splats with `quaternion.set(1, 0, 0, 0)` and place them at negative Z.
- Confirm WebGL2 is available.

## Import Or Build Failures

- `Rollup failed to resolve import "spark-rs"` or `"spark-worker-rs"`:
  - Verify `rust/spark-rs/pkg/package.json` and `rust/spark-worker-rs/pkg/package.json` exist.
  - Rerun `npm install` after those pkg folders exist.
  - If the checkout moved, repair `node_modules/spark-rs` and `node_modules/spark-worker-rs` links/junctions to the current repo.
- PowerShell refuses `node_modules/.bin/*.ps1`:
  - Use npm scripts, `.cmd` shims, or direct JS entrypoints such as `node node_modules/vite/bin/vite.js`.
- Missing Rust/WASM:
  - Install `rustup`, add target `wasm32-unknown-unknown`, then run `npm run build:wasm`.
  - `rust/build_rust_wasm.ps1` can install `wasm-pack` through `cargo install wasm-pack`.
- Docs mention `NewSparkRenderer`:
  - Current repo exports `SparkRenderer`; check `src/index.ts`.

## Asset Loading, CORS, And Streaming

- Do not test examples through `file://`.
- Use Vite or another HTTP server.
- Remote splat URLs need CORS headers.
- Paged `.rad` streaming needs HTTP Range support.
- For chunked RAD, the `.rad` header and `.radc` chunks must be deployed together with matching paths.
- `.splat` and `.ksplat` often need a visible extension or `fileType`.
- PC-SOGS should be loaded as `.sog`/`.zip`; Spark 2.0 loaders do not support a remote manifest that fetches relative image files separately.

## LoD Looks Bad Or Updates Slowly

- Start with `spark.lodSplatScale`; raise for detail, lower for frame rate.
- Use foveation controls (`coneFov0`, `coneFov`, `coneFoveate`, `behindFoveate`) for huge scenes.
- Use per-object `splatMesh.lodScale` for important objects.
- Use prebuilt `.rad` for production; on-demand `lod: true` is convenient but can take seconds to minutes for large inputs.
- For large-coordinate striping or quantization artifacts:
  - Use `new SplatMesh({ url, extSplats: true })` for non-paged loads.
  - Use `new SparkRenderer({ renderer, pagedExtSplats: true })` for paged loads.
  - Consider `accumExtSplats: true` only when intermediate accumulation precision is the problem.

## Performance Problems

- Platform rough budgets:
  - Quest 3: up to about 1M splats.
  - Android phone: about 1-2M splats.
  - iPhone: about 1-3M splats.
  - Desktop: about 1-5M splats, more on strong GPUs.
- Keep `THREE.WebGLRenderer({ antialias: false })` unless there is a specific non-splat reason.
- Consider lowering `SparkRenderer.maxStdDev`; VR examples use `Math.sqrt(5)`.
- Avoid high `renderer.setPixelRatio(window.devicePixelRatio)` on splat-heavy scenes unless worth the cost.
- Avoid raycasting or CPU readback every frame against large splat sets.
- Dispose removed `SplatMesh` and secondary `SparkRenderer` objects.

## Dyno Problems

- Do not use `+`, `*`, `Math.sin`, or normal JavaScript conditionals on `DynoVal`s inside a graph.
- Use `dyno.add`, `dyno.mul`, `dyno.sin`, `dyno.select`, `dyno.splitGsplat`, and `dyno.combineGsplat`.
- Use uniforms (`dyno.dynoFloat`, `dyno.dynoVec3`, etc.) for values that change every frame.
- Call `mesh.updateVersion()` when uniform values change.
- Call `mesh.updateGenerator()` after changing graph structure, modifier arrays, selected effect constants, or `maxSh`.
- For custom GLSL, always use generated input/output variable names from `statements({ inputs, outputs })`.

## Interaction Problems

- Use `canvas.getBoundingClientRect()` when converting pointer coordinates to normalized device coordinates.
- Use `raycaster.intersectObjects(scene.children, true)` when splats may be nested.
- Check `raycastable` and `minRaycastOpacity`.
- Raycasting is synchronous and can visibly pause on multi-million-splat meshes.
- If edits affect unintended objects, scope `SplatEdit` as a child of the target `SplatMesh` or assign explicit edit lists.

## Visual QA Checklist

- Open the changed page through Vite.
- Confirm no console errors.
- Confirm the canvas is nonblank after a few frames.
- Resize once and verify aspect/renderer size update.
- Test the primary interaction: controls, picking, GUI, XR button, asset switch, or streaming world switch.
- For streaming pages, watch network requests for `.rad`/`.radc` and Range behavior.
