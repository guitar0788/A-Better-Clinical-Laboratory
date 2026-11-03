# ART-001 — feasibility of floor-standing, integrated-base instruments

**Status (2026-11-03): source-supported GO for an independent floor-object *candidate*; placement/staff/diagnosis L4 not passed.** This research answers the owner's request to **prefer instruments with their own bases**, not forcing the full-cabinet FA concepts onto a separate equipment table.

## Current handoff and visual source

- FA branch `feature/art-001-two-devices` latest reviewed Git HEAD `0e8ff6720402961a102a7788dd6bbfe74e9e1d14`; Draft PR #14. FA separately reports two 1254×1254 RGBA, four-view original images, with large integrated cabinet/floor bases. These images are **not yet public-branch committed game-ready 128×128 sprites**; FA's own review flagged downsampled detail, alpha noise, pivots and direction correspondence. Do not claim an approved machine art set or redraw from screenshots.
- Existing FA GameDB explicitly marks both devices `AttachedToObject=true`, uses a private 0.9-height workbench and still references an older equipment atlas. This contradicts the visual concepts' integrated floor-standing cabinets.
- Historical ART owner L4 **3 PASS / 2 FAIL / 3 BLOCKED** remains the record. Changing the candidate installation model does not rewrite it.

## Actual vanilla engine evidence (read-only, owner-provided)

1. **`Lopital.Floor.CanPlaceObject`:** for `AttachedToObject=true`, the native engine requires a `m_centerObject` with an accepting `AttachmentSlot`; without it placement fails with `NOT_ALLOWED_ATTACHMENT_NO_PARENT` or `NOT_ALLOWED_ATTACHMENT_WRONG_PARENT`. The engine's tile has a single `m_attachmentObject` and rejects an occupied attachment slot.
2. **`AttachedToObject=false`** bypasses that parent requirement, becoming an ordinary tile-center object when `PlacedToEdge=false`, `AttachedToWall=false`, and room/footprint rules allow placement. Existing occupied tiles remain blocked, and indoor/roof rules still apply.
3. Native example **`OBJECT_ULTRACENTRIFUGE`** is a standalone indoor `SHAPE_1_X_1` lab instrument with four directional texture IDs, an `AccessPosition(-1,0)`, `UseOffsetXNW=-1.0` and working animation references. **`OBJECT_MECHANICAL_VENTILATOR`** is a second explicitly `AttachedToObject=false`, standalone indoor interactable one-tile machine, with an explicit access position and use animation. **`OBJECT_XRAY_CONTROL_PANEL`** uses the same center-object convention with four native views and staff-use animation.
4. The existing ABCL private atlas uses `LAYOUT_16_X_8`; original `ObjectRenderer.GetTextureCoords` supports this layout, while `LAYOUT_8_X_8` returns null. Original `SHAPE_1_X_1` is a valid center-object shape. Four-way **actual projected silhouette size, occlusion, foot contact and staff animation offsets remain L4 tasks**.
5. The **current** G1 room requires original lab fixtures `ui_hematoanalyzer`, `ui_ria`, `thermal_cycler` etc.; G1 blood-lead testing still references `stat_lab_exam` and `hematoanalyzer`. An independent new object must **not** impersonate these original tags or silently replace their clinical jobs. Room readiness and assay routing are distinct from build-menu/placement support.

All original game source and XML were inspected locally from user-supplied archives; **no copyrighted original pixels, serialized archives or DLLs are committed**.

## Noninstallable TS implementation

`tools/stage_art001_selfstanding_candidate.py` reads **exact immutable FA source commit** `0e8ff6720402961a102a7788dd6bbfe74e9e1d14`. It makes a **separate generated candidate**, leaves FA's attached variant untouched, and:
- removes the *provisional* private workbench object, its one-off icon and its two extra UI labels from the staged, isolated candidate;
- retains the two private original ART object IDs, all private functional tags, equipment atlas and exact NW/NE/SE/SW slots `0–7`;
- changes only the candidate objects to `AttachedToObject=false`, `Placement=INDOORS`, one tile and a **provisional** original-inspired one-side `AccessPositions[-1,0]`;
- keeps the source's existing staff-use animation references and NW use offsets **provisionally**, with neither correctness nor actual specialist interaction asserted;
- refuses original lab/CBC/RIA tags, illegal shared atlas references, unexpected object definitions or altered input source SHA.

The output is four GameDB XML proposals plus `SELFSTANDING_SOURCE_GATE.json`; **no art PNG, no G1 DLL, no standalone ModAddon or installer**. These candidates intentionally are **not to be copied directly into an installed game folder**. Using both old attachment-based and independent candidates together would duplicate the same private IDs; final integration must pick exactly one implementation.

## Pre-existing G1 room / original clinical ownership (independent new source audit)

The existing G1 room (frozen test addon `feature/g1-secure-build@851b3059bed871d38844cffff7310de995bb2019`) has `BuildingModeFilters/Tag=ui_lab_equipment` and still requires original `ui_hematoanalyzer`, `ui_ria` and `thermal_cycler` for room readiness. The *candidate* private objects retain `ui_lab_equipment`, so the native build filter can discover them as an **additional equipment type**. However, `ui_lab_equipment` is a **generic** menu category and does *not* prove the objects will appear *only* in Toxicology Laboratory; in-game visibility scope remains unverified. Their unique `abcl_art001_*` tags do **not** impersonate or satisfy `ui_hematoanalyzer` / `ui_ria`, so these additions do **not** secretly replace CBC equipment or remove existing room requirements.

`tools/audit_art001_selfstanding_room_boundaries.py` applies these restrictions to a **pinned G1 source file** and the generated independent-object candidate; synthetic negative tests reject loss of original room tags, original instrument requirements, newly mandatory unapproved private objects, generic build-category removal, and any private-to-vanilla tag collision. This is additive source-level evidence, not runtime clinical/lab acceptance.

## Feasibility / decision gate

- **Source-only candidate: GO.** The vanilla center-object mode is supported and is a better match for two full-cabinet visuals than tabletop attachment.
- **Real device implementation: CONDITIONAL.** Need FA-native-quality two actual 128px four-view assets with common scale, base-ground contact and consistent pivot; check a one-tile foot print against each image (if oversized, investigate native `SHAPE_1_X_2` / tall atlas independently rather than stretching).
- **Placement test:** two device instances can be positioned on independent empty indoor tiles, rotate NW/NE/SE/SW, and should be blocked on an occupied cell or invalid roof/outdoor placement; verify native menu presence and staff access at every orientation, room readiness and save/reload.
- **Functional test:** confirm animation feet/arms and use-offset for a staffed lab; only when device routing is proven should clinical G1 be connected to new tags. Original CBC/three labs must continue working. Keep enabled DLC/Workshop matrix explicitly scoped.
- **Decision conflict to resolve when promoting:** binding owner art-direction **ABCL-D011** currently describes tabletop proportions and allows a private attachment parent. Owner's newest instruction explicitly **prioritizes checking integrated-base independent devices**. This source-only feasibility gate does **not** silently rewrite D011; a documented, user-approved amendment is needed to freeze the standalone model for Alpha.
- **Stop if:** true source footprint needs geometry impossible within available atlas/shape conventions, staff cannot reach the equipment, or unchanged G1 lab predicates require overriding native tags. No speculative Harmony/vanilla registry patches.

**Do not merge main, publish equipment, change original files, revise TO-004 V3 or retest prior G1 R3 patient spawning.** Keep Issue #3 and FA #14 open/Draft.
