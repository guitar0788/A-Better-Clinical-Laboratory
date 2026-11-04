# G1 — native lead workflow and test-build status

**Current implementation branch:** `feature/g1-secure-build`  
**Parent work:** Issue #2 / Draft PR #7  
**Current test mode:** R3 native `TRM_LDP` only. No R2 outpatient fixture and no Super-GM.

## Owner L4 report — 2026-11-04

The owner tested the G1 + standalone equipment + TO-004 V3 package:

- Install and G1 panel: PASS.
- Toxicology Laboratory selectable: PASS.
- Two standalone devices visible and placeable: PASS.
- Both devices' NW/NE/SE/SW views and size/perspective/ground contact: PASS.
- TO-004 8×6 and 12×6 prefabs: placement, rotation and access PASS; displayed labels FAIL because the localized names already included dimensions and vanilla UI appended dimensions again.
- TO-001 room-list and floor icons: not present in that package.
- Super-GM generated patient: FAIL; patient had no usable final diagnosis/treatment, and owner reported effects on other patients.
- Staff operation, original CBC, save/reload and rollback: NOT TESTED.

The combined candidate is **not L4 accepted**. The four untested gates remain open.

## Super-GM / C1 fixture retired

The previous C1 private fixture selected four vanilla symptoms whose original GameDB records all have `IsMainSymptom=false`. The resulting medical condition had no native main symptom, which is required by diagnosis/treatment UI paths. Its disabled-diagnosis behavior also makes it a poor proxy for normal diagnostic candidate selection.

The Super-GM called the original `LopitalEntityFactory.CreateCharacterPatient`, which performs native insurance-patient registration. It was therefore not a side-effect-free preview. The owner reported broader patient-state impact in L4. The runtime Super-GM class and C1 fixture have been removed. Historical source and failure evidence remain in Git history and the retired CLIN-001 documents.

The generic R2 path that locally overrode `DIA_CLD` is also retired. The installer now fails closed unless `-NativeLeadTest` is explicitly supplied and writes only an addon-local `TRM_LDP` override adding the ABCL sampling exam. No generic outpatient diagnosis is changed. The native severe symptom, mobility, hospitalization and chelation treatment remain original.

## G1 native R3 route

- The panel checks original department, insurance, ICU progression, ambulance and live IMOBILE quota gates before one native request.
- The request uses the original native IMOBILE patient factory and one-attempt latch.
- A successful factory return does not prove ambulance reservation, arrival, admission, sample collection, analysis, result return or treatment.
- Use only a fresh disposable save. Do not repeat the owner's historical full R3 clinical test solely for unrelated UI changes.

## TO-001 visual integration

The approved FA room-list sprites and direct isometric floor projection are now staged as additive assets. The room-menu sprites use separate `TEXTURE_CUSTOM_SPRITE` IDs. The floor renderer uses a private 2048×2048 atlas containing only tile 376; it never replaces the vanilla floor texture or writes shared renderer materials. Exact source/atlas hashes and the owner-approved FA commit are checked by the package builder.

Source/asset Verify is not native game L4. Confirm menu state, disabled state, hover, floor rendering, area colors, other room icons and save/reload in the refreshed package.

## TO-004 prefab display names

Vanilla `MapEditorUIController.CreatePrefabButton` appends ` - DisplayedSizeX x DisplayedSizeY` after the localized prefab name. Therefore the two localized strings must be `Toxicology Laboratory` / `临床毒理实验室`, without dimensions. The prefab geometry, IDs, room sizes and approved thumbnails remain unchanged.

## Genuine build and release boundary

Only an exact-head Windows net35/CLR2 build against owner-authorized original references establishes L3. Verify/CodeQL and offline XML/asset tests do not establish L3 or L4.

No Alpha release, all-DLC claim, Workshop compatibility claim or ordinary-save safety claim is made. Keep PR #7 Draft until the current integrated candidate passes its focused owner L4 gates.
