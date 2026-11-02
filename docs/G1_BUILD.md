# G1 — genuine game-build test candidates

# G1 — genuine game-build test candidates

**Current R3 status (2026-11-02):** the exact C# candidate `b0a66222f483319baf8750f23c7d064021781a23` passed genuine Windows/net35/CLR2 L3 in Actions [41389454623](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41389454623): 0 warnings, 0 errors. Artifact `13116563798` was independently inspected; it contains only ABCL-owned files and no original game DLLs or key. Its installer still carried an offline-review-only warning and the generic CMD defaulted to R2, so **do not install that first artifact**. A refreshed R3-specific installer and one-session checklist are being prepared. R3 L4 remains NOT RUN. PR #7 stays Draft.

See [G1 R3 single-pass L4 protocol](G1_R3_SINGLE_PASS_L4.md).

**Related:** Issue #2; draft PR #7. **No G1 Alpha release or verified ABCL blood-lead L4.**

## R2 candidate — lab-only mobile fixture (CURRENT; L3 NOT RUN)

The source branch now stages the **R2 disposable-save-only fixture** under
engineering test re-scope `ABCL-D013`:

- `src/ABCLG1Panel.cs` requests **one native mobile outpatient** with the
  original, Emergency clinic-only `DIA_CLD` medical condition.
- The test-only installer derives `DIA_CLD` from the local original
  `Diagnoses/DiagnosesER.xml` and appends the independent ABCL sampling
  examination only in the addon, without touching the original game files.
- `TRM_LDP` and `SYM_LEAD_LEVELS_HIGH` are **not overridden by R2**.
  The original severe case is preserved as a separate future integration gate.
- Native Emergency outpatient readiness and a contracted insurer with positive
  walk-in quota are checked before any patient factory call.
- The independent ABCL sampling/testing XML and optional DPT_LAB toxicology room
  are unchanged; fallback remains `DPT_LAB`. No Harmony or global patient-pool
  modification has been added.
- The fixture may produce a completed **negative** blood-lead test: it is
  intended to check dispatch and result completion, not positive lead toxicity
  or treatment. R2 must NEVER ship in Alpha or Stable.

**HOLD:** R2 has **not yet passed genuine L3 compilation, package auditing, or
L4**. Do not run its new source on the owner's hospital until the exact candidate
SHA passes the owner-only game-reference Windows build and the full single-pass
review gate. No source-only green check can replace L3.

## Source-level diagnostic and vanilla CBC control

`tools/audit_g1_native_route.py --game-db <local StreamingAssets/Database>`
compares ABCL room tags and examination links to the original game (locally,
without uploading assets). `tests/test_g1_native_route_audit.py` uses only
synthetic XML in public CI. In the inspected original-game dataset, the
`CanHaveAnyRoom` linked-test check flags both ABCL G1 **and vanilla CBC** from
Emergency / Internal Medicine, despite the owner's existing successful CBC
report. This is a source-path warning, **not** established inability to route
a laboratory sample. Native `ProcedureSceneFactory` and
`BehaviorPatient.FindLabSpecialist` have explicit DPT_LAB fallback logic.

See `G1_SINGLE_PASS_L4_PROTOCOL.md` for one-session preflight requirements,
audit limitations and stop rules. No further incremental user retries of R1.

## Previously compiled candidates (historical; not an R2 build)

| Source SHA | Genuine L3 action | Result | L4 result |
| --- | --- | --- | --- |
| `a8e4dadd146ba925ec7b25641eddc43f25171eb1` | [41331315755](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41331315755) | PASS, net35/CLR2, zero compiler warnings/errors | G1 panel appeared; lead patient did not arrive |
| `ea1a9ecb76484b9f86e5cc54dcf659f5548b3160` | [41369385877](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41369385877) | PASS, net35/CLR2, zero compiler warnings/errors | **Preflight stopped**: `Need an operational inpatient department`; no patient generated; vanilla CBC reported PASS |

GitHub's protected-main owner-only Windows workflow `Build G1 approved candidate`
checks a manually approved immutable Verify-passed source SHA, decrypts the
owner-authorized references using AES-256-GCM plus a **GitHub Actions Secret**,
and emits ABCL-only test artifacts. Never commit plaintext game assemblies,
private key or inherited proprietary assets. A real build does not establish
in-game gameplay or compatibility.

## Release constraints

No test patient-spawn controls or local vanilla disease override in release.
Original CBC and installed vanilla files must remain intact. No safe uninstall
claim for saves that have already loaded the test addon. Keep PR #7 **Draft**
until real G1 sample, specialist processing, physician result, and save/load
are evidenced in-game.
