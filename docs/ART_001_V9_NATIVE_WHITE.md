# FA ART-001 V9 — actual original-game white palette study

Status: **SOURCE-ONLY / owner visual review required / NOT INSTALLABLE**. Supersedes V8 as the **experimental design study**, not the V7 live atlas/edited GameDB. Existing PR #14 stays Draft and existing G1 code, XML registration, attachment and gameplay interfaces remain unchanged.

## Objective colour evidence

Using the owner's previously supplied `StreamingAssets.zip` **read-only**, FA sampled opaque, nearly neutral shell pixels in installed original-game `objects_small_atlas.png` (native HEM analyzer frames **248–251**; RIA frames **252–255**), with 128px cell width. The most frequent reference colours are:

| Original-game neutral shell | RGB | Role in V9 |
| --- | --- | --- |
| Highlight | **#F2F2F2** (242,242,242) | Main illuminated housing |
| Body | **#E6E6E6** (230,230,230) | Main white shell |
| Secondary shade | **#CCCCCC** (204,204,204) | Lower/right shell shade |
| Deeper shade | **#B3B3B3** (179,179,179) | Shadow/depth boundary |

The HEM four-view shell counts for these colors were 3611, 3001, 598 and 1757 fully opaque or nearly opaque pixels respectively. RIA also prominently uses #E6E6E6, #F2F2F2, plus shell #DBDBDB. **These are shared neutral RGB colour values, not copied pixels/geometry.** The prior green/blue-tinted pseudo-white (#FAFBF7, #E8EEEB etc.) is rejected for the shell. Do not apply arbitrary pure #FFFFFF fills as the primary body tone.

## V9 authoring changes

- New editable `tools/art001_v9_study.py`: preserve and clearly separate V8 history; build original mass-spectrometer and digestion-workstation turnaround artwork from coherent geometric components, not mirrored output.
- All four primary shell material gradients are restricted to sampled vanilla neutral-white ladder. The warm white is gone; localized blue status screens remain accents.
- Darker outlines, realistic metal/plastic separation and non-trivial side/rear service features; digestion protective top uses darker curved lid material like native low-height instruments. Added physical screws, seams and access panel details.
- Generates **eight** editable SVGs and native 128px RGBA previews, a mobile source-only visual sheet with four swatches, and SHA256 manifest. There is **no GameDB export or installer**, and no native game art or DLL inside.
- V8 remains on branch for a reversible comparison. V7 production resources and existing `verify_art_exports.py` are unchanged. The V9 study must not be represented as a visually accepted texture or L4 result.

## FA / TS gate

FA verifies exact-SHA GitHub Actions, inspects actual V9 rendering and presents original art for owner visual approval. If still schematic next fix must be truly authored layered mechanical surfaces rather than small colour-only iteration. TS retains placement, attachment, staff access, native game/API changes and L4 responsibility; this source study does not request clinical G1 retesting.

Historical art L4 remains **3 PASS / 2 FAIL / 3 BLOCKED**. No merge, release, install package, proprietary asset upload, or DLC/Workshop compatibility claim.
