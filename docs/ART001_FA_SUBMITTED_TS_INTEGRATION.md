# ART-001 — TS intake of FA's submitted four-direction instrument artwork

**Source-integration status (2026-11-03): L2 candidate only; owner submission permission ≠ game art approval.**  
**FA immutable commit:** `cb3a7ab5d03e8677dcb84f486a04bf0ea5f8f622`.  
**TS working design:** independent, built-in-base floor devices. The attached tabletop design in FA Draft PR #14 and the alternative in TS Draft PR #39 remain historical drafts, not simultaneous installable definitions.

## Sources accepted for intake, without changing originals

FA has now genuinely committed **two original 1254×1254 RGBA four-view sheets**, **eight 128×128 RGBA native-direction frames**, one diagnostic 2048×1024 atlas with exactly the eight 128×128 cells at slots 0–7, and `assets/art001/review_20261103/manifest.json`. FA source approval is authorization to retain these exact bytes and hand them to TS; **it is not owner acceptance of native visual quality, coherent mechanical four-way rotation, 1×1 footprint, actor occlusion or staff contact**.

The TS assembler `tools/stage_art001_fa_submitted_standalone.py` refuses a moving FA branch, validates all **11 file hashes and Git blobs**, original source dimensions and private atlas layout, and byte-compares the atlas with the eight registered frames. It copies the original atlas **byte-for-byte**, with SHA256 `b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651`, to an *offline* `Assets/ABCL/equipment_atlas.png`. **There is no repaint, crop, transparency cleanup, shape modification or Blender rerender of any submitted frame.** The source artwork is unchanged.

Because the FA GameDB expects two separate custom item icons but no owner-approved menu icons were supplied for these two new cabinet bodies, this source-only stage computes two **provisional** 64×64 UI thumbnails by fixed 2:1 Lanczos resize of the exact FA NW sprites. They are entirely new derived UI assets, explicitly *NOT OWNER VISUALLY APPROVED* and not a reason to create a public game release. These generated thumbnails must not be confused with the frozen TO-001 toxicology room/floor icons.

## Native GameDB integration contract

Reuse the already source-tested [TS Draft PR #40](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/40) `transform` operation, but consume the now-submitted FA source for GameDB. The output is exactly four isolated GameDB XML proposals with **the two independent, namespaced, center-tile devices only**:

- `OBJECT_ABCL_ART001_ICP_MS`: `AttachedToObject=false`, `Placement=INDOORS`, `SHAPE_1_X_1`, atlas NW/NE/SE/SW slots **0/1/2/3**, access position `(-1,0)`.
- `OBJECT_ABCL_ART001_DIGESTION`: same independent layout, atlas NW/NE/SE/SW slots **4/5/6/7**.
- Private atlas asset `ASSET_TEX_ABCL_ART001_EQUIPMENT` `TEXTURE_OBJECTS` and derived NW-build-menu icon assets `ASSET_ABCL_ART001_ICON_ICPMS` / `ASSET_ABCL_ART001_ICON_DIGESTION`.
- The **additional** `OBJECT_ABCL_ART001_WORKBENCH`, its texture reference, custom icon, color set and localization are **absent** from this candidate, not overwritten in the FA historical branch.

Generated asset paths follow the earlier, loader-tested original ART contract (in an isolated output directory): `Database/ModObjectsABCL.xml`, `Database/ModAssetListsABCL.xml`, English and Simplified Chinese ModStringTable XML, and three `Assets/ABCL/` images. There is no `ModAddon.xml`, clinical DLL, managed assembly, vanilla atlas, G1 diagnosis/examination change or installation script in this source-only stage. **Do not install the candidate alongside the previous attached ART addon: duplicate object IDs could corrupt the load.**

## Clinical/compatibility and visual hold

The original G1 Toxicology Lab required-equipment list remains unchanged, including `ui_hematoanalyzer`, `ui_ria` and `thermal_cycler`. These two private cabinet devices carry neither those original tag names nor any permission to reroute CBC or blood-lead assays. The generic `ui_lab_equipment` build tag may expose the equipment in other departments; Toxicology-only UI visibility is not a proven feature.

FA source pictures contain previously observed low-alpha fringe and very small details, and 1254px image quadrants cannot independently prove the physical reverse-side component arrangement. The report records each actual 128px frame's alpha bbox and 1–7 alpha fringe count without changing the artwork. **Stop if any model's feet/base, staff use positions or 1×1 footprint do not match native game scale**, rather than hide a defect by stretching or redrawing already supplied images.

## Targeted L4 installer delivered after independent Windows gate

New test-only scripts `tools/Install-ART001-Standalone-Into-G1.ps1`, `tools/Uninstall-ART001-Standalone-From-G1.ps1` and deterministic `tools/package_art001_standalone_test_only.py` assemble a **separate, reversible, thirteen-entry ART001 overlay ZIP**, for an owner-authorized disposable-save test only. It contains exactly **seven ART001 resources** (four private GameDB XML files, the exact FA image atlas and two derived provisional menu icons), the source manifest, two defensive PowerShell scripts, two one-click CMD wrappers and a README. It contains **no G1 DLL, original game/Workshop assets, private keys or Harmony**.

- Frozen user-submitted FA art commit `cb3a7ab5d03e8677dcb84f486a04bf0ea5f8f622`.
- Source/display original 2048×1024 equipment atlas SHA256 `b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651`.
- Exact-head Windows mock and source gate [Actions #41664545949](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41664545949) **PASS**; CodeQL [#41664546154](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41664546154) **PASS**.
- GitHub artifact `ABCL-ART001-FA-Standalone-L4-TestOnly`, ID `13244905333` (outer Actions artifact digest `sha256:4873e892ed890a57965948633e049d7af2e01919c3845e40654f209aa3d5b56c`).
- Actual inner 13-file test ZIP independently re-downloaded and audited: **168,620 bytes; SHA256 `b5abf3b261afc90bb5c913c9a713995c2aef0eb1539304187596a3b6f6a1074c`**; 7/7 exact source file hashes, 13/13 unique entries, no original game DLL/keys.
- On Windows fixture: verified G1 ownership, seven exactly additive files, duplicate-install refusal, changed-file uninstall refusal, exact matching-file rollback, preserved mock G1 DLL, unmodified TO-004 V3 marker and unrelated Workshop marker, **PASS**. This is a test harness, *not actual game L4*.
- Tested error gate: Installer stops on missing compiled G1, existing ART001 files, changed source SHA or any third-party-owned target; it never deletes unknown files. Users with a previous rejected ART test should **not manually delete/copy** unknown resources. The installer may refuse until a known owned previous version is safely retired.
- This stage's prior notes saying the **source-only staging directory** is not installable remain correct; the **separate** test-only packaging step is an explicit, still-unreleased L4 experiment. No published Alpha is implied.

## Gates, in order

1. TS exact-head GitHub source L2: 11/11 frozen FA files and derived atlas 8/8 cells; negative case tests; original G1 room/CBC and directional offset audits, hashed staging folder.
2. Owner evaluates native 128px full-cabinet eight-view appearance and the two *derived* NW custom menu icons. A file-submission approval alone cannot turn this gate green.
3. If art/runtime candidate approved, build **one** G1-compatible ART-only, SHA-pinned test package, with additive-only install/rollback and no overwrite of accepted TO-004 V3 files. For XML-only resources, no fictitious C# L3 claim; any genuine changed DLL must undergo net35/CLR2 L3 separately.
4. Real disposable-save L4: both build-menu entries, individual placement without a table, four directions, accessible worker animation, actual required-equipment status, original three labs/CBC, save/quit/reload, and declared DLC/Workshop compatibility combinations. Do not re-run already accepted lead-patient workflow merely because new art is being tested.
5. For production, user-approved decision amendment to tabletop-oriented ABCL-D011 is required; preserve original historical decision and test failures as records.

**No PR merge, release or Alpha publication is authorized by this staging.**
