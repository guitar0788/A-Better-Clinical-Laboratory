# CLIN-001 C1 and Chinese Super-GM — test-only implementation candidate

**Branch:** `feature/clin001-c1-gm-test-harness` (forked from the currently accepted G1 draft). This is **not** a release and not an L3/L4 pass.

## Owner requirement

Every **subsequent ABCL test-only** game candidate should include a single built-in **Simplified Chinese Super-GM** panel; no additional third-party plugin or separate installation. The panel is permanently **excluded from Alpha/Stable**. It is a test accelerator, **not a gameplay proof**.

## Integrated C1 operations in this candidate

- `tools/audit_clin001_c1_exclusive_routes.py`: read-only native/DLC examination routing matrix; reports native testing IDs, their room tags, ABCL room tag overlaps, and private ABCL test pair. Accepts the user's **local** `StreamingAssets.zip`, never uploads or commits it.
- `tests/test_clin001_c1_exclusive_routes.py`: six synthetic negative/regression cases, including shared `stat_lab` collision, missing tags, explicit ABCL room-type collision, lost private ABCL tag and unresolved testing ID. All tests require a result of `False` in failed isolation scenarios.
- `src/ABCLSuperGmTestPanel.cs` / `src/ABCLG1Panel.cs`: Chinese IMGUI launcher inside the **same G1 DLL**. Uses the native `LopitalEntityFactory.CreateCharacterPatient` with `PatientMobility.MOBILE` and **any existing in-memory insurer entity**; it **does not gate on** insurer day quota, contracted inpatient ward, ambulance acquisition or available Emergency clinic. This is a deliberately unnatural **disposable-save fixture**. It cannot and must not claim that it naturally reproduces a real severe diagnosis or laboratory completion. The screen reports requested cases, whether the blood-lead sampling exam is linked, and a **read-only** CBC/ABCL room-tag comparison.
- `src/ABCL.G1.Panel.csproj`: enables `ABCL_GM_TEST_ONLY` compilation symbol for this **test-only** assembly; GM class intentionally does not exist in an Alpha build without this symbol or source entry. The existing patient-generation and read-only panel code is not otherwise changed.

## Hard boundaries

- **No claims of invincible forced execution.** Even GM cannot safely create a character without a live scene, loaded game database, valid original medical condition, an existing insurance object or a working native entity factory. This panel reports the actual failure. Repeated attempts are throttled to protect incomplete factory side effects (max five requests per session; a factory exception locks the panel until reload). It does *not* set insurer objectives, ICU, ambulances, quotas, force medical examination completion, move lab tasks, or write original XML.
- The generated test patient may be **created but not admitted/arrived**. Manual observation and L4 are still necessary; this is not a "one click everything passed" tool.
- Read-only C1 room-tag test is source/data evidence, NOT patient workflow proof. The limited game-original + four-DLC zip scan produces **16 native sampling links to 14 different lab testing IDs, with 0 matching the ABCL room tags**. The real-game negative/positive routing gate remains outstanding.
- **Chinese glyphs need actual in-game verification** (Unity IMGUI font fallback is not proven) and an exact-SHA, genuine game-reference .NET 3.5/CLR2 build before distribution.
- The existing G1 R3 native lead patient workflow is preserved. A forced *MOBILE* TRM_LDP patient is not medically equivalent to native immobile/ambulance progression. Use the unchanged R3 mode for authentic severe tests.
- The test-only DLL must not be merged into ordinary Alpha and must not be bundled in a standalone TO-004 art-only overlay. A future full ABCL test package should incorporate the GM test-only binary through its existing native G1 test build, not as a new plugin dependency.

## Evidence and next step

- Local Python unit tests: **6/6 PASS**.
- Local original/DLC XML read-only C1 scan: 16 sampling links, 14 unique native lab testing IDs, 0 tag overlap, 1 private ABCL sampling/testing pair; **source-only candidate PASS**.
- GitHub Actions Verify and exact-SHA genuine net35/CLR2 L3 build: **pending** at the time of drafting.
- Chinese UI, forced native entity creation, original exam isolation and save/reload: **not yet game-tested**.

**No main merge, no automatic release, no modification to previous user-approved prefab XML or art.**
