# G2 private exposure-case dispatch gate — TS / source-only

**Status:** G2 test fixture source candidate, not a gameplay PASS, not Alpha, not a release.
**Parent baseline:** G1 Draft PR #7 (`feature/g1-secure-build`).
**Independent clinical XML:** G2 Draft PR #43, medical-icon V3 child Draft PR #44.
**Owner test scope:** disposable hospital save only; compiled test DLL is not yet available from this branch.

## Source-backed defect and repair

1. G2's two new experimental exposure conditions must declare
   `<Disabled>true</Disabled>` until the clinical exclusive-diagnosis C2 and
   game L4 gates pass. Original `GameDBMedicalCondition.Disabled` excludes
   these from the ordinary random diagnosis pool.
2. G1's current test-only super-GM panel **rejects every disabled diagnosis
   except its exact C1 fixture**. Simply disabling G2 cases would make
   both G2 in-game tests unreachable.
3. This child branch permits only these exact IDs in the test-only GM:
   - `DIA_ABCL_G2_CADMIUM_EXPOSURE` must have
     `EXM_ABCL_G2_BLOOD_CADMIUM_SAMPLING` and 100% main symptom
     `SYM_ABCL_G2_CADMIUM_ELEVATED`.
   - `DIA_ABCL_G2_MERCURY_EXPOSURE` must have
     `EXM_ABCL_G2_URINE_MERCURY_SAMPLING` and 100% main symptom
     `SYM_ABCL_G2_MERCURY_ELEVATED`.
4. Both conditions must be disabled in the loaded GameDB, have all
   referenced symptoms resolved, and contain no immobile/intubated
   symptom before a single native MOBILE patient is requested.
   This explicit check matters because native `HasImmobileSymptom()`
   returns false for disabled diagnoses.
5. Any other disabled diagnosis is still refused. The original C1
   allowlist and G1 R3 ambulance/lead/CBC paths remain unchanged.
   The report now identifies the actually selected sampling exam.

## Why this is not an L4 success

- The C# source was not recompiled against actual net35 original game
  references on this G2 child branch. Source-only Verify cannot establish
  the native ABI, game load or patient placement.
- The two G2 conditions' main biomarkers, device routing and native
  icon rendering have **not** been proven in game.
- A GM-created fixture is not proof that native diagnosis requires
  the assay; the **C2 direct/manual diagnosis bypass remains a HARD STOP**.
- The artwork of standalone ICP-MS and digestion equipment remains under
  FA/TS visual and interaction L4. Do not alter the FA asset SHA.
- Never ship an enabled GM panel or experimental disabled diagnoses in Alpha.

## Required gates before installation or merge

1. Exact-head source Verify and C1/R3 noninterference checks PASS.
2. Independent source review of the new G2 ID allowlist, strict
   test-only isolation, failure ordering, and disabled-symptom handling.
3. Owner-authorized **genuine Windows net35/CLR2 build against licensed
   Project Hospital assemblies**, using the trusted protected-main
   encrypted reference pipeline (never copy secrets into this branch).
4. Combine only pinned G1 + G2 clinical/icon V3 + approved FA
   independent instruments and frozen TO-004 V3 room preset;
   reject mismatched hashes and earlier withdrawn G2 ZIP.
5. One disposable-save L4: check 2 explicit G2 GM IDs, disease icons,
   true sample acquisition, staff usage of digestion/ICP-MS in correct
   order, diagnostic-result return, premature manual-diagnosis bypass,
   original blood lead/CBC, native labs and save/reload.
6. Record actual game version, enabled DLCs/Workshop, package/hash,
   screenshots and raw logs on failure.

**No owner action required merely to review this Draft PR.**
No automatic core merge, main update, public DLL or release.


## Original game ABI checks (2026-11-04)

Read-only verification against the owner's ILSpy export (`dll_ilspy.zip`):
- `DatabaseEntry.DatabaseID` is the original `ID` class, not `string`.
  The original `ID` has `ToString()`, but no implicit `ID == string` operator.
  Earlier candidate PR #45 used `symptom.DatabaseID == expectedMain`;
  this was a C# compile blocker even though Verify/L2 initially passed.
  Corrected with null-check plus `symptom.DatabaseID.ToString() == expectedMain`,
  and a dedicated negative regression assertion in
  `tests/test_g2_private_gm_dispatch.py`.
- `GameDBMedicalCondition.Symptoms` is `GameDBSymptomRules[]`,
  `GameDBSymptomRules.GameDBSymptomRef.Entry` resolves a `GameDBSymptom`,
  and the enum has `MOBILE`, `IMOBILE`, and `INTUBATED`.
  Explicit fail-closed checks cover null symptom rules and unresolved refs.
- **Critical gameplay caveat**: original `GameDBMedicalCondition.HasImmobileSymptom()`
  skips disabled diagnoses; the local explicit mobility validation is necessary.
  Original `MedicalCondition.UpdatePossibleDiagnoses()` also returns the
  disabled diagnosis as the sole candidate. Therefore a disabled G2 GM fixture
  is a **controlled technical test case**, not evidence of a normal
  diagnostic pathway, doctor decision-making or assay-exclusive confirmation.

These findings are ABI/source observations, not an executed .NET build.
Genuine L3 is gated by the protected-main CI proposal in
[Draft PR #46](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/46).
It cannot run with secrets merely because PR #45's Verify is green.
