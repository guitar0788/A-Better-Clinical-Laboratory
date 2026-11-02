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

## G1 genuine L3 build — 2026-11-02 (UTC+8)

- Candidate: `a8e4dadd146ba925ec7b25641eddc43f25171eb1`; protected-main builder: `4eacfef6be50298d5930a6e0b40e6cbfec54528e`.
- [Actions run 41331315755](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41331315755), job `124921843743`: PASS.
- Windows Server 2022; .NET SDK 8.0.427 installed by setup-dotnet; target `net35`, C# 3. Compiler: 0 warnings, 0 errors.
- Owner-authorized AES-256-GCM references decrypted successfully in temporary runner storage; key held only in Actions Secret.
- Produced `ModABCLG1LeadTest.dll`: 7,168 bytes; CLR metadata `v2.0.50727`; SHA256 `9443fa71f3c989aaf865beaba7e240e055e0b2a9c8a4a55dc16b3f7d8015ecaa`.
- Test install package SHA256: `036e7cc1f8c149a562e5cbfbc13b1731da3043bbe5b85c2d02e69fc160c135dc`.
- Actions artifact `ABCL-G1-Compiled-TestOnly`, ID `13092844976`, 9,073 bytes; outer artifact SHA256 `572053f852cef9f5ddf59074110fefe644a58e9334bc5e4ec3e1e18ce9520f0c`; retention ends 2026-11-09 01:25 UTC+8.
- Downloaded artifact inspected: five ABCL XML files, ABCL panel DLL, zero-byte loader marker, installer and test instructions. No original game DLLs or decryption key included. DLL hash matches BUILD_INFO.
- L4 remains NOT RUN: native patient spawning, independent blood-lead workflow, original CBC and save/load require in-game testing. This is not an Alpha release. PR #7 remains draft.

### Genuine reference SHA256 recorded by the build

| Assembly | SHA256 |
| --- | --- |
| Assembly-CSharp.dll | `1120D899FB74D16F31115C5C27325EDBD1154B68E9419E6B7EA03CC3D43B6F24` |
| Assembly-CSharp-firstpass.dll | `63294CC19E24ECBE76F17F0776C9ABF6BF84358C4EF0B55967F141871308360F` |
| UnityEngine.dll | `0613DEFCBE1E30BFBA003D1A18E06000D6606FE14958E89752BA4C74CC7DD673` |
| UnityEngine.CoreModule.dll | `F65BEC39F0D3E75BAC559130775FC7C965BCB3AF03E1B44BC59C004F72F8645F` |
| UnityEngine.IMGUIModule.dll | `3B8E0A9655BAF1EDBA10D68464D03280F9B00D88BDAB0E5CFB1E7B409652C400` |

Game marketing version, DLC/Workshop combinations and gameplay behavior have not been verified by this compile.

## G1 first user L4 attempt — 2026-11-02 (UTC+8), reported

- Source: owner direct in-game test report, with screenshot of an exclamation indicator in the department UI. The screenshot does **not** include the complete G1 spawn-panel status text or a runtime exception log.
- Compiled G1 candidate identified in this PR: `a8e4dadd146ba925ec7b25641eddc43f25171eb1`, Actions `41331315755`; **the owner has not independently supplied the installed package hash**.
- Game started: **reported PASS**.
- New ABCL toxicology laboratory present / inspected: **reported PASS for visibility**, not evidence that the lab is fully operational; the department's warning indicator is unresolved.
- G1 test-panel present: **reported PASS for visibility**.
- Spawn one lead-poisoning patient: **reported PROBLEM / BLOCKED**, exact outcome and exception are unknown. Do not assert a confirmed runtime exception or a confirmed C# defect without the panel status and a log.
- Independent blood-lead sampling, laboratory result, vanilla CBC and save/reload: **NOT RUN**.
- Game version, active DLCs, Workshop mods, game-time state, normal intake/insurance state and screenshot of the spawn-panel status: **not supplied**.

### Focused source diagnosis (not yet a repair)

The ABCL panel calls the same `LopitalEntityFactory.CreateCharacterPatient` overload and schedules `m_fVisitTime` in the same pattern as the original `EventScriptTest.Activate`. Vanilla `BehaviorPatient.UpdateStateSpawned` waits for simulation time and validates insurance before un-hiding the patient. The original blood-lead main symptom `SYM_LEAD_LEVELS_HIGH` is marked `PatientMobility=IMOBILE`, so subsequent patient flow must be checked in actual gameplay. An exclamation icon in the screenshot alone cannot identify a failing room or missing staff.

**Next minimal evidence:** Screenshot immediately after clicking the G1 spawn button, showing its status line; if it reads `Spawn failed. Check output_log.txt.`, supply the error beginning with `[ABCL G1] Spawn failed:` from the game's runtime log. If it instead says `Requested one lead poisoning patient`, record whether simulation time is unpaused and a normal clinic can admit patients. Do not press the spawn button repeatedly or change a real save.

**Gate:** L4 remains **BLOCKED**, Issue #2 open, PR #7 draft. No Alpha claim, no source repair applied before the failure mode is known.

### Focused L4 patient-spawn diagnosis and one bounded repair — 2026-11-02

Owner's second screenshot shows the exact G1 panel message `Requested one lead poisoning patient. Check arrival.` after the click. From the old `SpawnOne()` source, this establishes `TRM_LDP` lookup, non-null native factory result, and `floor.AddCharacter(patient)` returning without exception; **not** visible admission. No `Spawn failed` exception is reported.

Source-backed mechanism (original game XML + ILSpy):
- Original `TRM_LDP` includes `SYM_LEAD_LEVELS_HIGH` with `ProbabilityPercent=100`.
- That symptom has `PatientMobility=IMOBILE`.
- The old test panel forced `PatientMobility.MOBILE`, unlike the disease's mobility. Vanilla `BehaviorPatient.UpdateStateSpawned` subsequently checks whether the insurance company is contracted and whether the immobile patient quota is positive; the patient may transition to `SpawnedFromDisabledInsurance` or `ReservingAmbulance`, instead of being admitted as a normal walk-in.
- Vanilla `LopitalEntityFactory.DebugAddPatients` also requires an inpatient department and at least one ambulance for immobile patients. This is distinct from the ABCL room's own equipment/technologist requirements.

**One D009-bounded correction was committed to PR #7** (new source changes after the successful original L3 build): preflight an inpatient department, an ambulance, a valid contracted insurer with an immobile slot; create `TRM_LDP` with `PatientMobility.IMOBILE` and that insurer; report "queued for native ambulance arrival" rather than suggesting the patient should walk in. Added static source assertions for the expected route.

**Gate reset for corrected source:** the earlier successful L3 build `41331315755` belongs only to old source SHA `a8e4dadd146ba925ec7b25641eddc43f25171eb1`. The corrected C# source is **L3 NOT YET RUN** until it is compiled with original-game DLLs on the trusted runner; corrected L4 **NOT RUN**. The user's previous three UI observations remain true for the original package but do not validate the corrected package.

Next validation in a disposable hospital: ensure operational inpatient care, ambulance, suitable insurance quota, advance game time, verify an actual ambulance arrival, then follow the lab sample/result and vanilla CBC. If the single corrected route still fails, record exact evidence and apply the project stop/re-scope gate rather than making repeated speculative changes.

## R1 corrected build and second owner L4 attempt — 2026-11-02 (UTC+8)

- Owner report explicitly identified source SHA `ea1a9ecb76484b9f86e5cc54dcf659f5548b3160`.
- **L3 PASS — verified independently:** Actions `41369385877`, genuine net35/CLR2 Windows runner job `125036379770`. Logs confirm `Verified SHA ea1a9ecb76484b9f86e5cc54dcf659f5548b3160`, checkout of that exact commit, decrypted original-game references, `Build succeeded`, **0 Warning(s), 0 Error(s)**, packaged and uploaded artifact `ABCL-G1-Compiled-TestOnly` ID `13109130314` (9,502 bytes). Actions' outer artifact SHA256: `6b800f65e56991eb52904294890ae9fe2de7f0db651075144c9eb6db9f9f1bd4`. This proves compilation and artifact creation, **not** which binary hash the owner installed.
- **L4 FAIL/BLOCKED at step 3:** owner reports (1) R1 real compile pass, (2) previous G1 removed/new version installed, (3) combined 'game load and G1 interface' item **failed**. It is **not yet known** whether the game failed to open, game opened but the G1 test button was absent, or another failure. No screenshot, installation transcript, `output_log.txt`, `Player.log`, game version or DLC/Workshop list supplied.
- (4) native department prerequisites, (5) clicking spawn, (6) observed patient admission, (7-8) blood-lead sample/result, (9) original CBC, and (10) save/reload: **NOT TESTED**.
- Source delta from original working G1 GUI to R1: `HospitalIsReady()` and initial GUI button creation are unchanged; changes involve panel window size/text and the `SpawnOne()` immobile-patient method. The installer and original G1 XML have not changed. Therefore a missing GUI before clicking Spawn is **not proof** that immobile insurance preconditions were the cause. Runtime type loading, addon-file placement, hospital readiness or Unity log errors remain unproven hypotheses.

**Required first discriminator:** does the game reach an in-hospital scene but the `ABCL G1 [Test]` button not appear, or does game/start/save loading itself fail? For the former, inspect the current Addons/ModABCLG1LeadTest location and whether code mods are enabled, then the log for `ModABCLG1LeadTest`, `ModEntryPoint`, `TypeLoadException`, `MissingMethodException` and `[ABCL G1]`. For the latter, stop further gameplay testing, close the game and isolate only the new addon after preserving logs. Do not delete original game XML or modify long-term saves.

**Gate:** R1 L3 PASS; R1 L4 FAIL/BLOCKED, Issue #2 remains open and PR #7 Draft. No second speculative code change; one bounded D009 source correction has already been made and needs an evidence-based failure classification before stop/re-scope.
