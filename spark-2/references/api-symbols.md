# Spark 2.0 Public API Map

Source of truth: `src/index.ts`. Re-check that file when a symbol fails to import.

## Rendering

| Symbol | Use |
| --- | --- |
| `SparkRenderer`, `SparkRendererOptions` | Required scene-level splat renderer; also handles LoD, sorting, offscreen targets, env maps, and paged splat pools. |
| `OldSparkRenderer`, `OldSparkViewpoint` | Temporary fallback for old/deprecated rendering paths such as stochastic and splat texture examples. |
| `SplatAccumulator` | Internal-style aggregation target used by `SparkRenderer`; inspect when changing renderer data flow. |
| `Readback` | GPU compute/readback helper used for sort metrics and custom data extraction. |
| `RgbaArray`, `readRgbaArray` | Per-splat RGBA extraction/painting/baking workflows. |

## Splat Loading And Storage

| Symbol | Use |
| --- | --- |
| `SplatMesh`, `SplatMeshOptions` | Main display/manipulation object for splat files, procedural splats, LoD, modifiers, edits, and raycasting. |
| `PackedSplats`, `PackedSplatsOptions` | Compact 16-byte/splat storage; fastest/default path for most scenes. |
| `ExtSplats`, `ExtSplatsOptions` | Extended 32-byte/splat storage for large-coordinate precision. |
| `SplatLoader` | Three Loader-style loading with progress/callbacks. |
| `unpackSplats`, `getSplatFileType`, `isPcSogs` | Format helpers and lower-level loading utilities. |
| `PagedSplats`, `SplatPager` | Paged/streamed `.rad` infrastructure exported through `SplatPager.ts`. |
| `PlyReader`, `SpzReader`, `SpzWriter`, `transcodeSpz` | Direct format read/write/transcode workflows. |
| `SplatFileType` | Explicit file type for extension-less or non-auto-detectable inputs, especially `.splat` and `.ksplat`. |

## Procedural And Dyno

| Symbol | Use |
| --- | --- |
| `dyno` | Shader graph namespace. Use for `DynoVal`, `dynoBlock`, uniforms, GLSL helpers, math/logic, and splat read/modify helpers. |
| `SplatGenerator`, `SplatModifier`, `SplatTransformer` | Lower-level programmable splat generation and modifier pipeline. |
| `constructGrid`, `constructAxes`, `constructSpherePoints` | CPU-side procedural constructors for common scene helpers. |
| `textSplats`, `imageSplats` | Convert browser text/image pixels into SplatMesh instances. |
| `generators` | Namespaced particle/procedural helpers such as `staticBox`, `snowBox`, `DEFAULT_SNOW`, `DEFAULT_RAIN`. |
| `modifiers` | Namespaced built-in modifiers such as depth/normal coloring. |

## Editing, Animation, And Interaction

| Symbol | Use |
| --- | --- |
| `SplatEdit`, `SplatEdits` | SDF-based RGBA/displacement edit layers applied globally or per mesh. |
| `SplatEditSdf`, `SplatEditSdfType` | SDF shapes for edit volumes. |
| `SplatEditRgbaBlendMode` | Current blend modes: `MULTIPLY`, `SET_RGB`, `ADD_RGBA`. |
| `SplatSkinning`, `SplatSkinningMode` | Skeletal/skinned splat animation. |
| `SparkControls` | Convenience wrapper for camera movement and pointer controls. |
| `FpsMovement`, `PointerControls` | Separate movement/control primitives. |

## XR, Hands, And Portals

| Symbol | Use |
| --- | --- |
| `SparkXr` | WebXR wrapper for VR/AR sessions, buttons, controllers, and hands. |
| `JointEnum`, `JOINT_IDS`, `JOINT_TIPS`, `FINGER_TIPS`, `Hand`, `HANDS`, `XrHands`, `HandMovement` | Hand tracking helpers exported from `SparkXr`/`hands`. |
| `SparkPortals`, `SparkPortalsOptions`, `PortalPair`, `DISK_PORTAL_FRAGMENT_SHADER` | Experimental portal rendering utilities. |

## Utilities And Constants

| Symbol | Use |
| --- | --- |
| `utils` | Namespace for low-level packing, half-float, pixel, and device helpers. |
| `isMobile`, `isAndroid`, `isOculus`, `isQuest2`, `isIos`, `isVisionPro` | Platform tuning, especially LoD and pixel-ratio decisions. |
| `flipPixels`, `pixelsToPngUrl` | Pixel buffer conversion helpers. |
| `toHalf`, `fromHalf`, `floatToUint8`, `floatToSint8`, `Uint8ToFloat`, `Sint8ToFloat` | Encoding helpers. |
| `setPackedSplat`, `unpackSplat` | Packed splat read/write helpers. |
| `LN_SCALE_MIN`, `LN_SCALE_MAX`, `defines` | Encoding constants and definitions. |

## Selection Rules

- Use `SplatMesh` unless the task specifically needs shared storage (`PackedSplats`/`ExtSplats`), low-level format conversion, or a custom generator.
- Use `PackedSplats` by default; switch to `ExtSplats` for visible precision artifacts from large coordinates.
- Use `.rad` + `paged: true` for huge worlds and streaming. Configure paged precision on `SparkRenderer`.
- Use `OldSparkRenderer` only when intentionally working on deprecated examples.
