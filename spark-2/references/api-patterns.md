# Spark 2.0 API Patterns

## Minimal Scene

```js
import * as THREE from "three";
import { SparkRenderer, SplatMesh } from "@sparkjsdev/spark";

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);

const spark = new SparkRenderer({ renderer });
scene.add(spark);

const splats = new SplatMesh({ url: "/assets/model.spz" });
splats.quaternion.set(1, 0, 0, 0); // common OpenCV-to-OpenGL reorientation
splats.position.set(0, 0, -3);
scene.add(splats);

addEventListener("resize", () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});

renderer.setAnimationLoop((time) => {
  renderer.render(scene, camera);
});
```

## Loading Splats

- Simple load: `new SplatMesh({ url })`.
- Raw bytes: `new SplatMesh({ fileBytes, fileName })`.
- Stream: `new SplatMesh({ stream, streamLength, fileName })`.
- Shared source: `const packedSplats = new PackedSplats({ url }); new SplatMesh({ packedSplats })`.
- Loader integration: `new SplatLoader().loadAsync(url, onProgress)`.
- File formats: `.ply`, `.spz`, `.splat`, `.ksplat`, `.sog`, `.zip`, `.rad`.
- For `.splat` and `.ksplat`, pass `fileType: SplatFileType.SPLAT` or `SplatFileType.KSPLAT` when no extension is visible.
- Await `splatMesh.initialized` before reading bounds or depending on loaded data.

## LoD, RAD, And Streaming

```js
// On-demand LoD for ordinary splat files.
scene.add(new SplatMesh({ url: "/assets/scene.spz", lod: true }));

// Prebuilt RAD, loaded normally.
scene.add(new SplatMesh({ url: "/assets/scene-lod.rad" }));

// Paged RAD streaming.
const spark = new SparkRenderer({
  renderer,
  pagedExtSplats: true,
  lodSplatScale: 1.0,
  coneFov0: 70,
  coneFov: 120,
  coneFoveate: 0.4,
  behindFoveate: 0.2,
});
scene.add(spark);
scene.add(new SplatMesh({ url: "/assets/scene-lod.rad", paged: true }));
```

- Prebuild RAD with `npm run build-lod -- input.spz --quality`.
- Use `--rad-chunked` for `.rad` plus `.radc` chunks; load the `.rad` URL with `paged: true`.
- Tune global detail with `spark.lodSplatScale` first. Use `spark.lodSplatCount` only when platform defaults are unsuitable.
- Tune individual objects with `splatMesh.lodScale`.
- Use `extSplats: true` on `SplatMesh` for large coordinate precision in non-paged loads.
- Use `pagedExtSplats: true` on `SparkRenderer` for paged streaming precision. Do not set `extSplats` directly with `paged`; source warns to configure this on the renderer.
- `maxPagedSplats` must be a multiple of `65536`.

## Dyno Modifiers And Shader Effects

```js
import * as THREE from "three";
import { dyno } from "@sparkjsdev/spark";

const t = dyno.dynoFloat(0);
mesh.objectModifier = dyno.dynoBlock(
  { gsplat: dyno.Gsplat },
  { gsplat: dyno.Gsplat },
  ({ gsplat }) => {
    const { center } = dyno.splitGsplat(gsplat).outputs;
    const lift = dyno.mul(dyno.sin(t), dyno.dynoConst("float", 0.05));
    const up = dyno.dynoConst("vec3", new THREE.Vector3(0, 1, 0));
    const shifted = dyno.combineGsplat({
      gsplat,
      center: dyno.add(center, dyno.mul(up, lift)),
    });
    return { gsplat: shifted };
  },
);
mesh.updateGenerator();

renderer.setAnimationLoop((time) => {
  t.value = time / 1000;
  mesh.updateVersion();
  renderer.render(scene, camera);
});
```

- Inside Dyno graphs, use `dyno.add`, `dyno.mul`, `dyno.mix`, `dyno.sin`, `dyno.splitGsplat`, `dyno.combineGsplat`, etc. Do not use JavaScript arithmetic on `DynoVal`s.
- Use `dyno.dynoFloat`, `dyno.dynoVec3`, and other uniforms for values that change every frame.
- Call `mesh.updateVersion()` when uniform values or source data changed and the graph shape is the same.
- Call `mesh.updateGenerator()` when changing modifier structure, selected effect branch constants, `maxSh`, or modifier arrays.
- For custom GLSL, create `new dyno.Dyno({ inTypes, outTypes, globals, statements })` inside a `dynoBlock`; use `dyno.unindent` and `dyno.unindentLines`.

## Procedural Splats

```js
const mesh = new SplatMesh({
  constructSplats: (splats) => {
    const center = new THREE.Vector3();
    const scales = new THREE.Vector3(0.01, 0.01, 0.01);
    const quat = new THREE.Quaternion();
    const color = new THREE.Color();
    for (let i = 0; i < 10000; i++) {
      center.random().subScalar(0.5);
      color.setHSL(i / 10000, 0.8, 0.55);
      splats.pushSplat(center, scales, quat, 1, color);
    }
  },
});
scene.add(mesh);
```

- Reuse temporary `Vector3`, `Quaternion`, and `Color` objects in loops.
- Built-ins: `constructGrid`, `constructAxes`, `constructSpherePoints`, `textSplats`, `imageSplats`.
- Particle helpers: `generators.staticBox`, `generators.snowBox`, `DEFAULT_SNOW`, `DEFAULT_RAIN`.

## Splat Edits

```js
const edit = new SplatEdit({
  rgbaBlendMode: SplatEditRgbaBlendMode.ADD_RGBA,
  sdfSmooth: 0.05,
  softEdge: 0.25,
});
const sphere = new SplatEditSdf({
  type: SplatEditSdfType.SPHERE,
  radius: 0.5,
  color: new THREE.Color(1, 0.6, 0.2),
  opacity: 0,
});
edit.add(sphere);
scene.add(edit);
```

- Add a `SplatEdit` globally to affect editable meshes, or as a child/assigned edit to scope it.
- Current source enum values are `MULTIPLY`, `SET_RGB`, and `ADD_RGBA`; verify examples that mention other blend names.
- SDF types include `ALL`, `PLANE`, `SPHERE`, `BOX`, `ELLIPSOID`, `CYLINDER`, `CAPSULE`, and `INFINITE_CONE`.

## Raycasting And Interaction

```js
const raycaster = new THREE.Raycaster();
canvas.addEventListener("click", (event) => {
  const rect = canvas.getBoundingClientRect();
  const ndc = new THREE.Vector2(
    ((event.clientX - rect.left) / rect.width) * 2 - 1,
    -((event.clientY - rect.top) / rect.height) * 2 + 1,
  );
  raycaster.setFromCamera(ndc, camera);
  const hit = raycaster.intersectObjects(scene.children, true)
    .find((item) => item.object instanceof SplatMesh);
  if (hit) hit.object.recolor.set(1, 0.5, 0.5);
});
```

- Raycasting is synchronous and can be expensive for millions of splats. Use it for clicks/taps, not every frame.
- `SplatMesh` has `raycastable` and `minRaycastOpacity` options.

## Controls And XR

- Basic first-person controls: `const controls = new SparkControls({ canvas: renderer.domElement }); controls.update(camera);`.
- Separate controls: `FpsMovement` for keyboard/gamepad, `PointerControls` for pointer/touch.
- XR wrapper: `new SparkXr({ renderer, mode: "vr", enableHands: true, sessionInit })`.
- For XR, attach camera and SparkRenderer to a movable local frame when the app needs locomotion or reference-frame compensation.

## Cleanup

- Call `scene.remove(mesh)` and `mesh.dispose()` for removed splat meshes.
- Call `spark.dispose()` for secondary/offscreen SparkRenderers.
- Dispose Three.js geometries/materials/textures created outside Spark as usual.
