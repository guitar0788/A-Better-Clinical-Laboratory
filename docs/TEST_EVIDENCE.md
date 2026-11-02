# Test Evidence and Claims

Never convert source-level plausibility, a green workflow or third-party examples into an assertion of working gameplay. Each result must identify the tested SHA/package, game build, DLC/Workshop set, environment, steps, expected/actual result, and raw logs/screenshots when available.

## Current evidence baseline (2026-11-01)

| Test | Source and type | Result | Limitation |
| --- | --- | --- | --- |
| G0 disposable CBC in a fourth lab | User's direct in-game report in the predecessor conversation | Reported PASS: fourth room appeared and CBC workflow returned a result | No saved raw output log, game version or reproducible save/load report available here; does not validate G1 |
| G1 independent blood-lead examination | G1 test package/source candidate in predecessor conversation | NOT TESTED / BLOCKED | New test IDs and lead-case flow not demonstrated in actual game |
| G1 patient-spawn panel compilation | Previous Windows installer error screenshot | FAILED / NOT COMPILED | Required legacy C# compiler not found. No genuine game-DLL L3 success recorded |
| G1 GItHub Actions build | Proposed only | NOT RUN | Public repository CI must not assume access to proprietary game references |
| Original-device art acceptance | Not delivered | NOT TESTED | No original interactive equipment approved |
| Four DLC / Workshop / save-load regression | No ABCL L4 matrix | NOT TESTED | Do not claim compatibility or safe uninstall |

## Four evidence levels

- **L1 — unit/logic:** test command, negative cases, results, tested SHA.
- **L2 — data/source/assets:** XML parser, all referenced IDs resolved, room/equipment/medical linkage, atlas/pivots/directions and test failures.
- **L3 — game-compatible build:** real game assembly hashes, compiler/target metadata, exact successful build job and artifact hash. No public upload of game binaries.
- **L4 — gameplay:** human-run test or recorded game run, settings, exact actions, diagnosis/treatment outcome, save/load, baseline regressions, screenshots and output log.

`Verify` initially validates policy files, absence of proprietary compiled artifacts, and any future tracked XML syntax. It **does not** compile a game DLL or run in-game tests.

## L4 case template

```text
Date:
Commit/package SHA256:
Project Hospital build:
DLCs enabled:
Other mods enabled:
Save type (new/existing/disposable):
Scenario and prerequisites:
Steps performed:
Expected:
Actual:
Result (PASS/FAIL/BLOCKED):
Raw log / screenshot references:
Known limitations:
```

## Required G1 gameplay cases

1. New ABCL blood-lead sampling appears for a valid lead-poisoning patient.
2. Sample reaches a staffed ABCL toxicology lab; specialist interacts with an actual required instrument.
3. Lab result returns to the physician and contributes to the diagnostic path.
4. Original CBC still processes at the original hematology lab.
5. Save, close, reopen and reload preserve functioning laboratory tasks and rooms.
6. Test-only spawn controls are off or absent in release configuration.


## ART-001 first owner L4 placement report — 2026-11-02

**Exact tested artifact, as reported by owner**
- Actions artifact ID: `13124027790` (`ABCL-ART001-PLACEMENT-TESTONLY`), Actions run [41408148144](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41408148144).
- Source SHA embedded in the tested package: `1fa723d336f95b27762a202a34aab9c64d003504`.
- This is the original art-only test package, not any later Draft PR #14 commit. The package lacks the later issue-fix changes; do not assign this report to a future candidate.
- Owner supplied a checklist result in chat with no screenshot, matching game log, placement-validation error string, game build, DLC list or additional fault description. **Do not invent those details.**

| # | Owner test item | Actual reported status |
|---|---|---|
| 1 | Game started and entered disposable hospital | **PASS** |
| 2 | Build menu showed both ABCL objects | **PASS** |
| 3 | Equipment names/descriptions displayed normally | **PASS** |
| 4 | Both objects could be placed on a laboratory workbench | **FAIL** |
| 5 | Both objects rendered correctly in all four game rotations | **FAIL** |
| 6 | Scale/occlusion/character-table contact | **BLOCKED** |
| 7 | Nearby staff could still walk normally | **BLOCKED** |
| 8 | Original hematology analyzer and other original equipment unaffected | **BLOCKED** |

**Aggregate:** 3 PASS, 2 FAIL, 3 BLOCKED. **ART-001 L4 placement acceptance = FAIL / NEEDS_FIX.** No staff execution or native procedure routing was attempted. The three blocked items are *not* PASS, and G1 R3's separately accepted patient/CBC test is not substitute evidence for ART-001 item #8 in this run.

**Source-grounded diagnosis after report**
- The staged ART-001 objects declare `AttachedToObject=true` and only `abcl_art001_icp_ms`, `abcl_art001_digestion` (plus generic `ui_*` and `equipment`) tags.
- Vanilla `Lopital.Floor.CanPlaceObject` returns `NOT_ALLOWED_ATTACHMENT_NO_PARENT` without a center/parent table object, and `NOT_ALLOWED_ATTACHMENT_WRONG_PARENT` if that parent has no `AttachmentSlot` or its `AllowedTags` do not match the object tags.
- Vanilla `GameDBObject.AcceptsAttachment` checks for **at least one exact string match** between the parent's `AttachmentSlot.AllowedTags` and the child object's tags.
- The original `OBJECT_TABLE_EQUIPMENT` and `OBJECT_TABLE_SQUERE` tables allow known vanilla tags such as `hematoanalyzer`, `RIA`, `lab_eq_small`, etc. They do **not** list either ART-001 namespaced functional tag, and the object definitions contain none of those allowed tags. Therefore placement onto those unmodified tables will be rejected by original `CanPlaceObject`. This is a verified *contract defect*, not an art-asset loading defect.
- The original equipment-table parent has `ForcesAttachmentOrientation=true`. The source of `Floor.CanPlaceObject` may override the child's direction to match that parent. The owner's four-direction FAIL is retained exactly, but without a screenshot of the rotation UI or a successfully placed object the precise independent rotation behavior is not established.
- Avoid adding general vanilla tags such as `hematoanalyzer`, `RIA` or `lab_eq_small` just to get through `AllowedTags`: this risks altering vanilla procedure equipment resolution, particularly CBC or unrelated Workshop labs. Prefer a dedicated **ABCL-only attachment parent** accepting only the two new tags and not re-registering any vanilla object; verify the changed result in a *new* exact-source candidate before further game testing.

**Next gate:** prepare an additive isolated attachment-parent fix in the ART-001 Draft branch, add static tests that independently model the original AllowedTags/AcceptsAttachment rule and forced-orientation flag, then rebuild and audit one new art-only package. No further owner L4 test is requested at this stage; the already passed R3 clinical patient/ambulance/sampling/chelation sequence is not repeated. Keep Issue #3 open and PR #14 Draft; no merge, release or blanket compatibility claim.


## ART-001 private attachment workbench correction — source/package gate PASS, L4 NOT RUN (2026-11-02)

- Fixed candidate source: `b4c94125cfbba03c0b473de9678560ddf8356843` on `feature/art-001-two-devices`, **not** the historical owner-tested source `1fa723d336f95b27762a202a34aab9c64d003504`.
- Original `Lopital.Floor.CanPlaceObject` and `GameDBObject.AcceptsAttachment` directly support the private-parent contract: parent must expose `AttachmentSlot`, accept the child tag, and may use `ForcesAttachmentOrientation=false` to avoid overriding independent object orientation. No change was made to any vanilla table's ID, tags or XML.
- Updated `assets/art001/Database/ModObjectsABCL.xml` adds `OBJECT_ABCL_ART001_WORKBENCH` based on the original game's installed equipment-table texture (`ASSET_TEX_OBJECTS_SMALL`, `LAYOUT_16_X_64`, texture slots 472–475, referenced rather than bundled). Private attachment allowlist contains **only** `abcl_art001_icp_ms` and `abcl_art001_digestion`; `ForcesAttachmentOrientation=false`.
- Both device definitions retain private functional tags and do not impersonate original `hematoanalyzer`, `RIA`, `lab_eq_small`, `lab_analyzer`, `stat_lab_exam` tags. Added EN/ZH workbench localization and regression tests for parent/child tag matching and static orientation flag. Original G1 R3 source and patient flow remain untouched.
- `Verify`, `CodeQL`, `Analyze Python`, ART-001 preview and ART-001 placement package workflows all concluded **success** for source `b4c94125cfbba03c0b473de9678560ddf8356843`.
- Corrected test package: [Actions run 41410173007](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41410173007), artifact `13125296497` (`ABCL-ART001-PLACEMENT-TESTONLY`), tied to the exact source above.
- Independent downloaded archive audit: outer ZIP 13,339 bytes SHA256 `f8e9b8d36de8d2fbb419b1db3dae4dde7f1cb08e788e7787d9a9036b47697797`. Inner `ABCL-ART001-Placement-TestOnly.zip` 14,419 bytes SHA256 `1ab3b3ceba2ce8fcdbd34778af9d0710d717e95bf1a1c23e062d08f0429d9770`.
- The 12 allowlisted inner files contain one original-art atlas, two original icon PNGs, the additive three-object XML, bilingual strings, installer, README and `BUILD_INFO.txt`. BUILD_INFO source SHA equals `b4c94125...` and atlas SHA256 equals `fa0b2e0bea72ab71b94d2752599bfc66fb642c0a64b748ca358ba9a2479e9249`. No game DLL, Harmony binary, original XML override, AES key or R3 patient-spawn files are present.
- **Disposition:** source-based correction and exact-source static/package audits PASS; **ART-001 in-game placement and rotation on this new package are NOT TESTED**. The historical first-owner result remains **3 PASS / 2 FAIL / 3 BLOCKED** for artifact `13124027790`. In particular, this new green Actions run does **not** change any of those historical statuses to PASS.
- Next permitted ART-only step: one disposable-save placement and rotation check **using the dedicated ABCL Instrument Workbench**, with the same first-failure stop rule. Do not repeat G1 R3 patient generation/CBC, and do not claim staff procedure routing, DLC/Workshop, normal-save or uninstall compatibility. Keep Issue #3 open, PR #14 Draft.


## ART-001 revised native-style sprite candidate — offline review only (2026-11-02)

- The user rejected the first in-game oversized/blocky red-looking equipment and required original-style presentation and no player-facing ABCL branding. Decision `ABCL-D011` applies to ART-001 and future laboratory content.
- An initial reduction/desaturation candidate at `d05648633befe3ae9e85792e4080ed879fdc7e8a` was generated and inspected but **not accepted**: shapes became too small and still looked like generic boxes.
- The generator was then rewritten with independently authored medical-equipment geometry: the mass spectrometer has an identifiable upright analysis column, ventilation, capped sample tray and panel; the digestion workstation is lower/flatter with a safety hood, reactor window, sample wells and rear service grilles. All four orientations now distinguish front control surfaces from rear ventilation without replacing the machine identity.
- Exact **source/art/test candidate**: `82182ceb7ad99d1ac59289ec7d5b78305e7a76da` on Draft PR #14. The generated atlas is 2048×1024 with 128px cells and eight private original-art frames. Relative occupied silhouette target is <=65px wide and <=51px high, sharing a y≈108 baseline. This is a pixel-space review constraint, **not a measured in-game physical height**.
- Real GitHub Actions: `41423765997` Verify **17 tests / 1 existing skip** (PASS), `41423765967` CodeQL PASS, `41423757029` original-art preview PASS, and `41423757150` placement-test-only package PASS. Four-view source contract requires each directional pair to differ by at least 100 visibly changed pixels, rather than merely one status light.
- The original preview output from `af82f65eae54cae02bb1e8e1adf077620ec581a8` was independently extracted and viewed; the later `82182...` change adds tests only, no sprite geometry changes. A separate readable review-sheet PNG was created from actual generated original-art frames (not native screenshots) and a **schematic** tabletop outline, explicitly labeled as not representing actual game placement.
- Downloaded Actions artifact `13130498961` for exact candidate `82182...` and audited both archives: outer artifact SHA256 `76e7ed0442988def630e0a7cfc81e82b67498c241fabd60a3e3c4f598d2f72f2`; inner test ZIP SHA256 `2494c318a0427fb88691e1e2d2369b772419588d003afb4b1a083f3ddced1a83`. Inner BUILD_INFO source SHA matches `82182...`; atlas SHA256 `1173a464058da589b7af8f3d1c95a5f218f1f697ee27c5b039101c961e49a9b9`. All 12 allowlisted files are ABCL-owned; none is an original game DLL, Harmony, AES key, native medical XML override, patient-spawn code or a release binary.
- User-facing EN/ZH strings inside the actual package read `Mass Spectrometer` / `质谱分析仪`, `Sample Digestion Workstation` / `样本消解工作站`, and `Instrument Workbench` / `仪器工作台`, with no ABCL project branding. Internal IDs/tags remain ABCL-namespaced.
- **Disposition:** exact-source CI and package audit PASS; preliminary **offline** sprite source review improved compared with rejected box models; **owner visual approval pending**; corrected in-game placement, four-direction rendering, tabletop contact, occlusion, staff walking and original equipment coexistence are **NOT RETESTED**. Preserve historical ART-001 L4 result **3 PASS / 2 FAIL / 3 BLOCKED** on artifact `13124027790` without converting any of those statuses to PASS. Keep PR #14 Draft and Issue #3 open; no new user game test requested yet. The independently accepted G1 R3 clinical L4 is unchanged.


## ART-001 authentic vanilla-style nonpixel art investigation — 2026-11-02

**Owner visual requirement:** reject coarse block/pixelated equipment; require smooth original-like 2D isometric sprites and correct scale on a lab equipment tabletop for ART-001 and all later laboratories. Player-facing equipment/room names must remain unbranded; internal resource IDs remain collision-safe.

**Source-backed game art references from the owner-provided StreamingAssets archive (read-only):**
- `StreamingAssets/Textures/objects_small_atlas.png`: 2048×8192 RGBA, 16×64 original atlas, one sprite per 128×128 cell.
- `ObjectsAttachments.xml` `OBJECT_HEMATOLOGY_ANALYZER` occupies original sprite IDs 248–251, and `OBJECT_RIA` IDs 252–255.
- `Objects.xml` `OBJECT_TABLE_EQUIPMENT` occupies IDs 472–475 and uses an original private attachment-slot rule.
- At natural atlas resolution the original equipment has variable antialiased alpha pixels: e.g. HEM NW alpha bounds (7,20,126,128) and RIA NW bounds (8,43,108,127). These include the original shadows, so bounds are **not a direct game-space collision or scale measurement**.
- No original game image was copied into the new generator or committed.

**Source implementation on PR #14:**
- `tools/generate_art_001_svg.py`: editable original SVG plus CairoSVG 4× rendering and Pillow Lanczos 128×128 output; 8 directional frames in a 16×8 atlas, original icons and preview. A small local vector sample was generated and inspected; it is an early technical proof rather than finished artistic acceptance.
- `tests/test_art_001_svg.py`: original source isolation, eight distinct sprites, antialiased partial-alpha coverage, atlas layout/dimensions. A preview-only GitHub workflow installs offline rendering dependencies; regular lightweight Verify treats absent optional rendering deps as skipped without allowing a fake L4 PASS.
- `.github/workflows/art-001-placement-test.yml` no longer auto-produces installation packages from the visually rejected pixel-art source, and the old placement artifact is historical evidence only.
- Separate high-resolution generated art **concept** images were created to illustrate direction; they are **not exact asset sources, not real game screenshots, and not a claim the equipment now fits on a workbench**. Concepts illustrating floor-cabinet-sized designs were rejected at preliminary review.

**Gate:** first ART owner L4 remains **3 PASS / 2 FAIL / 3 BLOCKED**. Smooth source/CI may pass, but user visual approval, final four-frame art polish, actual game attachment/rotation/occlusion/staff access and original CBC non-interference remain **NOT TESTED**. Keep Draft PR #14 and Issue #3 open; do not repeat G1 R3 clinical L4.


## ART-001 smooth vector exact artifact review — run 41429598675 (2026-11-02)

- Source/branch head tested: `158c06ed484e6ba6d1de0c90785f3dd1ca5ee11f` on Draft PR #14. [Preview Actions run 41429598675](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41429598675) completed successfully. Verify also passed on the same SHA.
- Artifact `13134075987`, `ABCL-ART001-ANTIALIASED-REVIEW-NOT-INSTALLABLE`: downloaded and independently examined. Outer ZIP SHA256 `4aa302a03c34f1d80c7278d62fc8821918598e349c05870692695c43a7ecb419`. Exactly **13 files**: two icon PNGs, one original-art shared atlas, one preview PNG, eight editable SVG sources, and `art_manifest.json`.
- Manifest schema `ABCL-ART-001-v2-antialias-review-only`, generated atlas 2048×1024, 16×8 cells, 128px sprites; SHA256 of the actual atlas agrees with its manifest. **Zero** installer, GameDB addon XML, original game bitmap, game DLL, encrypted secret or patient-spawn debug binary. The preview is a genuine CI-produced source proof, not an L4 or a release build.
- The actual SVG source proof is antialiased, but preliminary local visual inspection still considers the geometry simplified compared with the vanilla RIA/hematology analyzer reference. Owner aesthetic acceptance **NOT YET OBTAINED**; do not install as a game asset merely because it has antialiased edges.
- The separate high-detail visual concept generated for owner review is a non-game-rendered image. It is not a machine-readable four-view source, is not the exact CI-rendered SVG, and must not be falsely cited as a game art test.
- Historical first ART-001 L4 remains exactly **3 PASS / 2 FAIL / 3 BLOCKED** on original artifact `13124027790`. The updated style, new private workbench, actual in-game object placement, four-direction rendering, scale/occlusion and staff use remain NOT TESTED. Old pixel-art placement-package CI remains on HOLD; no new user test requested.


## ART-001 v4 integrated-device silhouettes — original-art offline gate (2026-11-02)

- Exact source commit: `5b5f103cb9407edf14bb826d96151455de0b2547` on Draft PR #14, with no corresponding owner game L4 test. Four-view source uses an original smooth antialiased SVG pipeline; the giant empty tabletop and tiny extra box of v3 were replaced by an integrated instrument enclosure, with actual body/front-panel shape differences, a mass-spectrometer ion-source housing plus vial carousel, and a distinct lower sealed sample-digestion hood/front glass/rear service panels.
- **Source-only CI:** Verify PASS ([run 41434695557](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41434695557)); CodeQL and Analyze Python PASS; antialiased preview PASS ([run 41434687791](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41434687791)).
- Exact-source preview artifact ID `13136265935` (13 file *non-installable* archive) was retrieved and extracted. Downloaded outer ZIP SHA256: `6d458a1f5bad6b09435e2e548a41379068ddda808a2a06791fa15b7720e81ec5`; original source-generated atlas SHA256 `ae7d6017f62ffe70d0455b06e5f9b47acfea372a3dbbbacbac1e85197028861f`. Manifest schema `ABCL-ART-001-v4-native-body-review-only`, eight editable SVGs, transparent 2048×1024 atlas, icons and preview. No installation script, executable game DLL, original-game bitmap or AES secrets are in this preview ZIP.
- **Read-only local visual comparison, not uploaded to public GitHub:** owner-supplied original atlas cropped at IDs HEM 248–251 and RIA 252–255 and the eight actual v4 SVG-generated frames were placed side by side at the same 128px cell resolution, enlarged uniformly for inspection. V4 is still simplified compared with the original HEM/RIA (control surfaces and material detail), and front/back visibility remains insufficient to claim that the owner will accept the aesthetic. It is a new source concept, **not final accepted artwork**.
- Distinction: actual GitHub Actions preview is the authored SVG-generated artwork. Any high-resolution concept render shown separately is *not* the authored machine-readable source. No original game pixels have been committed or redistributed.
- Historic first-game L4 on artifact `13124027790` is still **3 PASS / 2 FAIL / 3 BLOCKED**. The v4 artifact does **not** include the private workbench installer, and no v4 in-game placement, four-view game renderer, lab worker pathfinding, save or original CBC regression has been run. Old pixel-art placement CI stays suspended, PR #14 stays Draft, Issue #3 stays open. Previously accepted G1 R3 clinical flow does not need to be repeated.


## ART-001 v6 curved-hood review artifact — exact source verified (2026-11-02)

- **Exact source**: `f98a841484f6e834676b3b5fb3facc5d45ea3b50`, Draft PR #14 on `feature/art-001-two-devices`.
- Implemented original SVG source revisions in `tools/generate_art_001_svg.py`: added molded-shell seams, discrete LCD/power status and service vents, common baseline alignment with reduced vertical bulk, capped vials and carousel contact on the ICP-MS, curved protective sample-digestion hood with separate front-glass / rear-service surfaces, and a clearly labeled 2× mobile review sheet. Player-facing names remain neutral; technical IDs remain namespaced.
- **All source checks PASS on the exact SHA**: Verify [41437792048](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41437792048), CodeQL [41437792129](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41437792129), Analyze Python PASS, and the [smooth preview build 41437783510](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41437783510).
- Review artifact: `13136802898`, `ABCL-ART001-ANTIALIASED-REVIEW-NOT-INSTALLABLE`. It was downloaded and extracted. Outer ZIP SHA256 `98cccbb700455e37cae2e060a1a052a85e50a281bfeeab7d513154c7fd9cb57a`; actual atlas SHA256 `7b17bef0ad4dc768c9008fba280ebe2e0fc0b630ba6a0b0abc7105074a0464a4`; manifest schema `ABCL-ART-001-v6-hood-review-only`.
- Exactly 14 allowlisted preview files: eight editable SVG sources, one antialiased 2048×1024 original-art atlas, original UI icons (two), native 1024×256 preview, enlarged mobile review PNG, and manifest JSON. No install script or game DLL, no game-owned original bitmap, no Harmony/AES key, and no native G1 patient-spawn files.
- A local owner-reference comparison image was generated using the owner's original-game HEM and RIA sprite crops and exact v6 native 128×128 sprites. It is **not committed to public GitHub** and not an in-game render or proof of scale/contact. A separate mobile sheet made from exact v6 source is available for viewing.
- **Visual judgment**: smoother curves and clearer physical instrument details than v4, but still simplified compared with the game's detailed original sprites; formal owner visual acceptance **NOT YET GIVEN**. In particular, the original first ART-001 L4 remains **3 PASS, 2 FAIL, 3 BLOCKED** on separate artifact `13124027790` (bench placement and rotation FAIL, three further checks BLOCKED). No v6 runtime L4 was run. Do not infer tabletop contact, pathfinding, vanilla CBC/Workshop compatibility or clinical procedure use from source/preview PASS.
- The old pixel-art installation-package CI remains on HOLD. Keep Issue #3 OPEN and PR #14 DRAFT. Do not repeat the already accepted G1 R3 clinical L4.

## V7 edge-safe preview checkpoint (2026-11-02)

- Source: `45d84ac7f6dcb10a18327810089acb752af42e53`, Draft PR #14. The current original SVG generator remains the only production candidate; the rejected pixel generator is deprecated.
- Eight 128x128 isometric frames; ICP-MS alpha bounds 107x106px, digestion alpha bounds 99x85px; all reach cell y=128. Three original 64x64 icons meet the inner 60x60 safe-area rule. These dimensions are image-space measurements, not collision/placement evidence.
- Transparent-edge filter correction: the exporter uses a two-pixel nearest-colour RGB bleed under zero-alpha pixels, applied separately to each sprite and icon, preserving every alpha value.
- Native source supports `LAYOUT_16_X_8` coordinates and PNG loading, but actual in-game texture loading, rotations and bench contact are NOT YET L4 verified. Do not switch to the original 16x64 atlas without runtime evidence.
- Exact run links: [preview 41444867554](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41444867554), [Verify 41444867580](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41444867580), [CodeQL 41444867525](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41444867525) all PASSED.
- Downloaded cloud artifact `13140934442` has 16 original source/preview files. Outer SHA256 `cfbfcff2854817fe5a4dd4c2238f2060780011553a4816505c72bac8b63f1b28`; atlas SHA256 `a5bad4aae0c41b5775586bba358f1c3a5c42cc099a8e28b41c1e174e485559c3`. Full manifest matches.
- Phone review: open the preview Actions run, download `ABCL-ART001-V7-ANTIALIASED-REVIEW-NOT-INSTALLABLE`, then view `Previews/ABCL/review_mobile.png`; the PNG depicts generated sprites, NOT a game screenshot.
- Historical owner L4 still reads **3 PASS / 2 FAIL / 3 BLOCKED**. Owner visual approval, private-bench placement, independent rotation, occlusion, staff access and vanilla object coexistence are pending. No game installation/release artifact; G1 R3 accepted clinical test must not be repeated for an art-only change.
