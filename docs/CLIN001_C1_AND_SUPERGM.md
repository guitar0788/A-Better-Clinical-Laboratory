# CLIN-001 C1 and Chinese Super-GM — test-only implementation candidate

**Branch:** `feature/clin001-c1-gm-test-harness` (forked from the currently accepted G1 draft). This is **not** a release and not an L3/L4 pass.

## Owner requirement

Every **subsequent ABCL test-only** game candidate should include a single built-in **Simplified Chinese Super-GM** panel; no additional third-party plugin or separate installation. The panel is permanently **excluded from Alpha/Stable**. It is a test accelerator, **not a gameplay proof**.

## Integrated C1 operations in this candidate

- `tools/audit_clin001_c1_exclusive_routes.py`: read-only native/DLC examination routing matrix; reports native testing IDs, their room tags, ABCL room tag overlaps, and private ABCL test pair. Accepts the user's **local** `StreamingAssets.zip`, never uploads or commits it.
- `tests/test_clin001_c1_exclusive_routes.py`: eight synthetic negative/regression cases, including shared `stat_lab` collision, missing tags, explicit ABCL room-type collision, lost private ABCL tag and unresolved testing ID. All tests require a result of `False` in failed isolation scenarios.
- `src/ABCLG1Panel.cs`: Chinese IMGUI launcher and GM class embedded in the **existing test-only G1 source file**, preserving the exact pinned `src/ABCL.G1.Panel.csproj` Git blob SHA `71daed7c3aa9e62edf9eea207fd77b2041be52ed` required by the trusted Windows builder. Uses the native `LopitalEntityFactory.CreateCharacterPatient` with `PatientMobility.MOBILE` and **an existing in-memory insurer entity**, and rejects diagnoses containing original immobilizing/intubation symptoms via `GameDBMedicalCondition.HasImmobileSymptom()` before touching the native factory; it **does not gate on** insurer day quota, contracted inpatient ward, ambulance acquisition or available Emergency clinic. This is a deliberately unnatural **disposable-save fixture**. It cannot and must not claim that it naturally reproduces a real severe diagnosis or laboratory completion. The screen reports requested cases, whether the blood-lead sampling exam is linked, and a **read-only** CBC/ABCL room-tag comparison.
- The original `src/ABCL.G1.Panel.csproj` is **byte-for-byte unchanged**. The built-in GM class is in the G1 *test-only* entry file; the Alpha/release project must not reuse `ModABCLG1LeadTest.dll` or this debug entry file. The existing R2/R3 patient buttons and read-only panel code are otherwise unchanged.

## Hard boundaries

- **No claims of invincible forced execution.** Even GM cannot safely create a character without a live scene, loaded game database, valid original medical condition, an existing insurance object or a working native entity factory. This panel reports the actual failure. Repeated attempts are throttled to protect incomplete factory side effects (max five requests per session; a factory exception locks the panel until reload). It does *not* set insurer objectives, ICU, ambulances, quotas, force medical examination completion, move lab tasks, or write original XML.
- Severe/immobile diagnoses are **rejected for the MOBILE-only GM path**; use the original R3 severe-case route instead. The generated non-severe test patient may be **created but not admitted/arrived**. Manual observation and L4 are still necessary; this is not a "one click everything passed" tool.
- Read-only C1 room-tag test is source/data evidence, NOT patient workflow proof. The limited game-original + four-DLC zip scan produces **88 original/DLC examination records (80 distinct IDs) with 0 room-tag matches, including 16 native sampling links to 14 distinct lab testing IDs**. The real-game negative/positive routing gate remains outstanding.
- **Chinese glyphs need actual in-game verification** (Unity IMGUI font fallback is not proven) and an exact-SHA, genuine game-reference .NET 3.5/CLR2 build before distribution.
- The existing G1 R3 native lead patient workflow is preserved. A forced *MOBILE* TRM_LDP patient is not medically equivalent to native immobile/ambulance progression. Use the unchanged R3 mode for authentic severe tests.
- The G1 test-only DLL must not be merged into ordinary Alpha and must not be bundled in a standalone TO-004 art-only overlay. A future full ABCL test package should incorporate the GM test-only binary through its existing native G1 test build, not as a new plugin dependency.

## Built test-DLL and release no-debug gate

`tools/audit_clin001_gm_binary.py` implements an **opt-in post-build** binary marker check:
- After an authorized, exact-SHA genuine `net35/CLR2` G1 test build, execute `python tools/audit_clin001_gm_binary.py --dll PATH_TO_ABCL_TEST_DLL --mode test`. It fails if the output managed DLL does not embed the Chinese Super-GM UI text and its specific debug log marker.
- For any future Alpha/stable candidate, run `python tools/audit_clin001_gm_binary.py --dll PATH_TO_RELEASE_DLL --mode release`. It rejects Chinese GM strings **and legacy G1 debug UI/patient-spawn text**.
- This scanner requires an actual `MZ` PE file containing `BSJB` CLI metadata and tests the expected compiler-emitted UTF-16 literal strings. It does **not** compile a DLL, validate its dependencies, prove exact game ABI or certify the absence of every possible debug control.
- Six synthetic Python negative/positive tests cover the scanner, with **no game-owned binaries embedded**. The protected-main encrypted reference compiler workflow is **not modified** or automatically authorized for PR #38 by this addition.

## Evidence and next step

- Local Python unit tests: **18/18 PASS** (8 native-route tests + 4 GM source/packaging guards + 6 synthetic compiled-marker tests).
- Local original/DLC XML read-only C1 scan: 88 original/DLC records / 80 unique exam IDs, 16 sampling links / 14 unique testing IDs, zero ABCL room-tag overlaps, one private ABCL sampling/testing pair; **source-only candidate PASS**.
- GitHub Actions Verify/CodeQL and exact-SHA genuine net35/CLR2 L3 build: **separate gates; current source does not yet carry a compiled success claim.** The protected-main auto-build authorizer accepts only PR #7 current `feature/g1-secure-build` head, not this child draft branch; do not bypass its safeguards.
- Chinese UI, forced native entity creation, original exam isolation and save/reload: **not yet game-tested**.

**No main merge, no automatic release, no modification to previous user-approved prefab XML or art.**
