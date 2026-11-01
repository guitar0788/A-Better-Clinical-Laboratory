# G1 — Verified Source Build Path (Test Only)

**Issue:** #2. This is an unproven test candidate, **not** an installable Alpha release.

## GitHub build prerequisites

The public GitHub repository stores only ABCL-authored source, XML and build scripts. The genuine Project Hospital DLLs needed for .NET Framework 3.5 compilation must **never** be committed to the public repository, included in build artifacts, or uploaded to public Releases.

The owner must privately provision two GitHub Actions secrets: `ABCL_G1_SOURCE_URL` (short-lived, access-controlled HTTPS URL to an archive of five DLLs from their legitimate game installation) and `ABCL_G1_SOURCE_SHA256` (full ZIP SHA256, uppercase/lowercase accepted). Do not post private links or bearer tokens in Issues/PRs. The archive must contain these files at its root:

```text
Assembly-CSharp.dll
Assembly-CSharp-firstpass.dll
UnityEngine.dll
UnityEngine.CoreModule.dll
UnityEngine.IMGUIModule.dll
```

After reviewing the exact G1 source commit (without merging the draft gameplay PR), open **Actions → Build G1 approved candidate** on protected `main`, select **Run workflow**, and enter the full 40-character **candidate_sha** from the approved draft PR. The builder requires a successful `Verify` result for that immutable SHA before it accesses any private game references. This workflow was introduced separately through infrastructure PR #8. Missing inputs, altered hashes or actual C# compilation errors fail the build. Green repository `Verify` is never used as a substitute for an L3 compile.

## Single-install test artifact

The compiler artifact will contain **ABCL G1 compiled install ZIP** (not an extra patient-spawn plugin) and a SHA256 build record. The ZIP has ABCL XML, panel DLL, a native code-mod loader marker, and an installer. The native loader ignores the empty `0Harmony.dll` marker; it is **not** Harmony patching.

The installer runs only on the owner's Windows game installation. It reads `DPT_LAB`, `TRM_LDP`, and `SYM_LEAD_LEVELS_HIGH` from the original database, copies these XML entries and appends the ABCL room/check references **inside the Mod addon folder**. It never edits original game files. This prevents posting copied vanilla XML definitions in a public repo or artifact.

The installer refuses to overwrite existing G1, refuses concurrent G0 probes and refuses unexpected missing/changed vanilla structures. Use only a disposable save and enable code mods; save compatibility and uninstall safety are **not** established.

## Status

- L2: standalone room/exam XML schema and historical G0 path provide a candidate. The local generator was separately tested against the user-supplied vanilla XML, with mandatory hematology preserved. The *PowerShell installer* and GitHub target have not been executed on Windows.
- L3: **NOT RUN**, requires genuine private game references on a GitHub runner.
- L4: **NOT RUN**, blood-lead sampling, new room dispatch, result return and save/load remain unverified.

Stop on real compilation failure; do not label the next artifact playable until in-game G1 validation is recorded.
