# FA ART-001 NW V4: actual manually art-directed 2D illustration

**Status: source-only, NOT visually approved; remain in Draft PR #14.**

Previously rejected V7/V8/V9/V10, Blender V1 and V2/V3 drafts proved that generating models and adding more filters cannot establish Project Hospital's native visual standard. The latest V3 actual original render has a coherent functional screen and sample tray but continues to look overly photorealistic, uniform and box-shaped. The owner specifically rejects pixel art and blurry 3D stand-ins.

This new experiment uses **actual editable 2D illustration**, not another source of SVG boxes:

- Input is the *original ABCL* V3 1024x1024 transparent source generated from its independently editable Blender file. The 3D model is **unchanged** in this pass.
- Tool `tools/art001_nw_illustrated_finish.py` contains deliberately hand-positioned high-resolution art strokes aligned to the real NW view: shell/ionizer edge highlights, service-door seams, independent specimen rack glints, a functional spectrum trace on the analyzer and monitor, vent strip highlights and fine keyboard cap linework. No copied game art, copyright-protected sprites or unlicensed image assets.
- A continuous neutral-white tonal pass lightly corrects the source machine's surfaces. It does not quantize colors into four bands. A separate soft dark outer contour draws the screen-space edge at native-scale thickness. Art is blended on 1024px RGBA, then smoothly Lanczos-resized to real 128x128 RGBA. **No nearest-neighbor pixels.**
- The output includes three editable OpenRaster (ORA) layers and separate original high-resolution layers, a before/after phone sheet displaying actual native sprites at 1x and smooth zoom, plus an exact SHA256 manifest. It is an **offline aesthetic review**, not a game-registered texture.
- All original-game HEM/RIA references are **private read-only** and not included in the public GitHub artifact. No copied native sprites or original DLLs. Existing namespace/Workshop/DLC isolation boundaries are maintained.

**Not a final design:** The silhouette is still derived from V3, and 2D painting alone does not yet solve the broader proportion and hand-authored machine construction. The image must be judged against the owner's detailed concept and vanilla references. A CI PASS cannot override a visual FAIL, and no other direction or the second device should be exported before approval. If still below the original, alter the underlying mechanical silhouette instead of piling on more versions of filters.

Only FA source and an isolated review workflow changed. TS retains native placement, rotation, collisions, clinical G1 integration and L4 testing. PR #14 stays Draft, no merge/release, and the past ART L4 3 PASS/2 FAIL/3 BLOCKED remains unchanged.
