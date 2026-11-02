# G1 — genuine game-build test candidate

**Issue #2; draft feature PR #7.** The **original** candidate `a8e4dadd146ba925ec7b25641eddc43f25171eb1` passed genuine game-DLL compilation on 2026-11-02 (UTC+8), Actions run [41331315755](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41331315755). A first user L4 attempt showed the UI and native patient creation request, but not arrival. The single corrective immobile/ambulance routing change is not yet compiled and remains NOT RUN at new-source L3/L4; this is not a release.

GitHub Actions compiles from protected `main` using a reviewed, immutable SHA from this feature branch. The authorized game references are stored as the encrypted file `ABCL_G1_refs.aes` in this branch; **only** the separately stored GitHub Actions secret `ABCL_G1_AES256_KEY` can decrypt them during a manual owner-triggered build.

See [the public-repository build procedure](G1_GITHUB_BUILD.md) on `main` (introduced through the infrastructure-only PR) for encryption format, expected ciphertext SHA256 and steps. Plaintext game DLLs and the decryption key must never be committed or included in artifacts.

## Package behavior

On a successful genuine `net35` L3 build, the workflow creates one test-only archive containing the ABCL G1 addon XML and C# test panel DLL plus a Windows installer. The installer derives three necessary database overrides (`DPT_LAB`, `TRM_LDP`, `SYM_LEAD_LEVELS_HIGH`) from the user's local game files. It never edits original game files and refuses to overwrite an existing G1 probe.

The native addon loader uses a zero-byte `0Harmony.dll` marker; the actual assembly is not linked and this candidate installs no Harmony patches. Only disposable test saves are permitted.

## Evidence and stop rule

- L1/L2: G1 source-contract tests and XML syntax checks executed in GitHub `Verify`.
- L3: **PASS only for original candidate** `a8e4dad`: genuine `net35` compilation, 0 warnings/errors, CLR2 metadata and downloaded artifact contents verified. **PENDING for the corrected immobile ambulance-route source**; rerun on the reviewed latest candidate SHA. See `TEST_EVIDENCE.md` for exact hashes and environment.
- L4: **PARTIAL / BLOCKED for the original package**: game, new room and panel visible, patient object created but admission unobserved. **NOT RUN for corrected source**. Blood-lead sample handling, vanilla CBC and save/reload still unverified.

Do not merge draft PR #7 or label the test package an Alpha until the actual gate and regressions pass.
