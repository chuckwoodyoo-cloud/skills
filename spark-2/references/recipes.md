# Spark 2.0 Recipes

Use these as starting workflows. Open the named source/example files before editing.

## Create A New Example

1. Start from `examples/hello-world/index.html`.
2. Keep the import map shape:
   - `three` from `../js/vendor/three/build/three.module.js`
   - `@sparkjsdev/spark` from `../../dist/spark.module.js`
3. Create `THREE.Scene`, `PerspectiveCamera`, `WebGLRenderer`, then `new SparkRenderer({ renderer })` and `scene.add(spark)`.
4. Add one `SplatMesh` or procedural source.
5. Add resize handling and `renderer.setAnimationLoop`.
6. Run `npm run build` before opening the example because examples import `dist/`.
7. Verify the page through Vite, not `file://`.

## Add A Streaming RAD World

1. Start from `examples/streaming-lod/index.html`.
2. Use a prebuilt `.rad` URL with `new SplatMesh({ url, paged: true })`.
3. Configure the renderer for precision and foveation when needed:

```js
const spark = new SparkRenderer({
  renderer,
  pagedExtSplats: true,
  coneFov0: 70,
  coneFov: 120,
  coneFoveate: 0.4,
  behindFoveate: 0.2,
});
```

4. Tune `spark.lodSplatScale` first for quality/performance.
5. Use `maxPagedSplats` only when memory budget needs explicit control; it must be a multiple of `65536`.
6. Serve `.rad`/`.radc` over HTTP with Range support.

## Prebuild RAD Assets

1. Ensure Rust, `cargo`, and the `wasm32-unknown-unknown` target exist.
2. Build the LoD CLI with release mode through npm:

```sh
npm run build-lod -- input.ply input.spz --quality
```

3. Prefer `--quality` for offline assets and the default quick mode for fast iteration.
4. Use `--max-sh=0..3` to cap spherical harmonics memory.
5. Use `--rad-chunked` for streaming output; load only the header `.rad` with `paged: true`.
6. Expect output files with `-lod.rad` suffix, and `.radc` chunks when chunked.

## Add A Dyno Visual Effect

1. Start from `examples/splat-shader-effects/index.html`, `examples/splat-reveal-effects/index.html`, or `examples/glsl/index.html`.
2. Store time and user-controlled values in Dyno uniforms:

```js
const t = dyno.dynoFloat(0);
```

3. Assign `mesh.objectModifier` or `mesh.worldModifier` with a `dyno.dynoBlock({ gsplat: dyno.Gsplat }, { gsplat: dyno.Gsplat }, ...)`.
4. Use `dyno.*` functions for graph arithmetic. JavaScript arithmetic cannot operate on `DynoVal`s.
5. For custom GLSL, wrap it in `new dyno.Dyno({ inTypes, outTypes, globals, statements })`.
6. Call `mesh.updateGenerator()` after changing graph structure.
7. Call `mesh.updateVersion()` when only uniform values or source values changed.

## Add Picking Or Painting

1. Start from `examples/raycasting/index.html` for selection, `examples/splat-painter/index.html` for painting, or `examples/interactive-holes/index.html` for raycast-driven effects.
2. Compute pointer NDC from `canvas.getBoundingClientRect()`, not from CSS-independent assumptions.
3. Use `THREE.Raycaster` and find the first hit whose `object instanceof SplatMesh`.
4. Avoid raycasting every frame against huge splat sets.
5. For persistent color changes, use `RgbaArray` and/or update `PackedSplats` then mark texture/update state as needed. Use examples as source of truth.

## Add Procedural Splats

1. Start from `examples/procedural-splats/index.html`.
2. For CPU construction, use `new SplatMesh({ constructSplats })` and push splats.
3. Reuse `THREE.Vector3`, `THREE.Quaternion`, and `THREE.Color` temporary objects in loops.
4. Use built-ins for common generated content:
   - `constructGrid`
   - `constructAxes`
   - `constructSpherePoints`
   - `textSplats`
   - `imageSplats`
5. For particle fields, inspect `examples/particle-simulation/index.html`, `examples/particle-animation/index.html`, and `generators.snowBox`.

## Add XR Or Hand Interaction

1. Start from `examples/webxr/index.html` for minimal hand tracking or `examples/basic-xr/index.html` for a richer XR app.
2. Create a movable `localFrame` group when locomotion/reference-frame compensation is needed.
3. Add `SparkRenderer` and camera under that local frame when appropriate.
4. Use `new SparkXr({ renderer, mode: "vr", enableHands: true, sessionInit })`.
5. Use `xr.updateHands({ xrFrame })` inside `setAnimationLoop`.
6. Use `SparkXr.makeJointSplats(...)` for hand visualizations.

## Add Offscreen Rendering Or Environment Maps

1. Start from `examples/envmap/index.html` or `examples/render-cube-depth/index.html`.
2. Create a secondary `SparkRenderer({ renderer, target: { width, height, doubleBuffer? } })`.
3. For synchronous output, call and await `spark.update({ scene, camera })` before `renderTarget`.
4. Use `renderEnvMap({ scene, worldCenter, ... })` for IBL-style output.
5. Dispose secondary renderers when they are no longer needed.

## Migrate Spark 0.1 Code

1. Ensure dependencies use `@sparkjsdev/spark@2.0.0` and Three r179+; this repo uses Three r180.
2. Add an explicit `SparkRenderer` to the scene.
3. Replace old viewpoint APIs with separate `SparkRenderer` instances and `target` rendering.
4. Move sort options onto `SparkRenderer` (`sortRadial`).
5. Replace `VRButton` usage with `SparkXr`.
6. Use `OldSparkRenderer` only as a temporary fallback for deprecated stochastic/splat texture paths.
