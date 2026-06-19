# Official Examples Catalog

Use this catalog to pick a working example before implementing Spark 2.0 behavior. Always open the file before copying details.

## Minimal Loading And Scene Setup

| Example | Use When |
| --- | --- |
| `examples/hello-world/index.html` | Minimal SparkRenderer plus one SplatMesh. Best starting point for a blank app. |
| `examples/hello-world/carousel.html` | Multiple splats with OrbitControls and simple layout. |
| `examples/multiple-splats/index.html` | Reuse one `PackedSplats` source across several `SplatMesh` instances. |
| `examples/sogs/index.html` | Loading SOG/SOGS-style assets. |
| `examples/viewer/index.html` | File upload, URL loading, `transcodeSpz`, progress/UI handling. |
| `examples/editor/index.html` | Heavier viewer/editor behavior: URL parsing, CORS handling, transform controls, export paths. |

## LoD, RAD, And Huge Worlds

| Example | Use When |
| --- | --- |
| `examples/streaming-lod/index.html` | Paged `.rad` streaming, `pagedExtSplats`, foveation, GUI LoD control. This matches the local browser page `/examples/streaming-lod/`. |
| `examples/multi-lod/index.html` | Many paged RAD objects sharing a renderer/paged pool; demonstrates `maxPagedSplats`. |
| `examples/lod/index.html` | LoD comparison, OldSparkRenderer fallback, toggles, and mixed LoD options. |
| `examples/lod-on-demand/index.html` | On-demand LoD and custom RGBA/readback style paths. |
| `examples/nonlod/index.html` | Non-LoD rendering and Dyno comparison patterns. |

## Dyno Shader Effects And VFX

| Example | Use When |
| --- | --- |
| `examples/glsl/index.html` | Custom shader/Dyno basics with SparkControls. |
| `examples/debug-color/index.html` | Debug color modifiers and packed source reuse. |
| `examples/splat-shader-effects/index.html` | Large custom GLSL effects inside Dyno blocks. |
| `examples/splat-reveal-effects/index.html` | Time-based reveal effects and effect switching. |
| `examples/splat-dissolve-effects/index.html` | Dissolve-style object modifier. |
| `examples/splat-flow/index.html` | Flowing Dyno effects across loaded splats. |
| `examples/splat-transitions/*` | Modular transition effects split across companion JS files. |
| `examples/interactive-deform/main.js` | Pointer-driven deformation with uniforms. |
| `examples/interactive-ripples/main.js` | Ripple interaction pattern. |
| `examples/interactive-holes/index.html` | Dyno plus SplatEdit and raycast interaction. |

## Procedural And Particle Splats

| Example | Use When |
| --- | --- |
| `examples/procedural-splats/index.html` | `constructSplats`, `textSplats`, `imageSplats`, and generated geometry. |
| `examples/particle-simulation/index.html` | GPU-ish particle simulation patterns. |
| `examples/particle-animation/index.html` | Animated procedural splat clouds. |
| `examples/lofi/index.html` | Combined world loading, XR, controls, generators, snow/rain, and Dyno modifiers. |

## Editing, Painting, And Picking

| Example | Use When |
| --- | --- |
| `examples/raycasting/index.html` | Three.js Raycaster against SplatMesh and recolor feedback. |
| `examples/splat-painter/index.html` | `RgbaArray`, painting, readback, and baking colors. |
| `examples/dynamic-lighting/index.html` | SDF edit layers for lighting-like effects. Verify blend enum names against source before copying. |
| `examples/interactivity/index.html` | Splat objects mixed with GLTF/EXR scene assets and UI choices. |

## Advanced Rendering

| Example | Use When |
| --- | --- |
| `examples/envmap/index.html` | Offscreen SparkRenderer and `renderEnvMap` for image-based lighting. |
| `examples/render-cube-depth/index.html` | Cube/depth rendering and custom Dyno encoding. |
| `examples/multiple-viewpoints/index.html` | Multiple camera/viewpoint style rendering. |
| `examples/portal/index.html` | Complex portal rendering with multiple renderers and edits. |
| `examples/newportal/index.html` | `SparkPortals` API usage. |
| `examples/splat-portal/main.js` | Manual portal math with two SparkRenderers. |

## XR And Mobile

| Example | Use When |
| --- | --- |
| `examples/basic-xr/index.html` | XR controls, SparkXr, hands, and richer scene setup. |
| `examples/webxr/index.html` | Minimal WebXR hand-tracking with SplatEdit SDFs. |
| `examples/mobile-joystick/index.html` | Mobile joystick controls and SparkControls integration. |

## Legacy Or Fallback

| Example | Use When |
| --- | --- |
| `examples/stochastic/index.html` | Old stochastic renderer behavior; uses `OldSparkRenderer`. |
| `examples/splat-texture/index.html` | Deprecated splat texture path; uses `OldSparkRenderer`. |

## Example Selection Heuristics

- Start from `hello-world` for any new app.
- Start from `streaming-lod` for any `.rad`, `paged`, huge-world, or foveated LoD request.
- Start from `splat-shader-effects` or `splat-reveal-effects` for custom Dyno/GLSL visual effects.
- Start from `procedural-splats` for generated text/images/grids or point clouds.
- Start from `raycasting`, `splat-painter`, or `interactive-holes` for click/touch editing.
- Start from `webxr` or `basic-xr` for VR/AR/hand-tracking.
