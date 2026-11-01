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
