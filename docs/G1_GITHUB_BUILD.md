# G1: GitHub public-repository compilation with encrypted game references

> **2026-11-02 current update:** This page preserves the original owner-only manual bootstrap procedure as history/fallback. G1 R3 has since passed genuine Windows net35/CLR2 L3 and its core clinical L4 was owner-reported PASS; the newer diagnostic-panel candidate still needs its **own** exact-SHA L3. See [automated verified G1 build](G1_CI_AUTOMATION.md) for the proposed no-manual-dispatch path. That new workflow only becomes active after protected-main review and merge; it cannot establish gameplay L4.
>
> **Historical status at original writing:** Build infrastructure only; genuine G1 L3 and L4 had not yet passed.

The owner reports authorization from the game's author to perform compilation in the public ABCL GitHub repository. This is recorded as authorization for **compilation**; it is not assumed to authorize publication or redistribution of the original proprietary game DLLs. Accordingly the repository stores **encrypted build inputs**, not plaintext binaries. ABCL-authored test artifacts exclude game assemblies.

## Historical one-time setup / manual fallback (no payment card, no second repository)

1. Download the encrypted reference asset **ABCL_G1_refs.aes** supplied in the ABCL development chat. This file is ciphertext; **do not upload** the unencrypted original ZIP `ABCL_G1_Private_Game_References_DoNotPublish.zip`.
2. On the existing `feature/g1-secure-build` branch of this repository, upload that exact `ABCL_G1_refs.aes` at the **repository root**. Do not add it to protected `main` directly. The workflow authenticates the SHA256 of this ciphertext: `918A1E3FC74AD530AF070C012BB8075DBC3874438FE5BA3C96A8D8AD39A3FCE2`.
3. In **Settings → Secrets and variables → Actions → New repository secret**, create `ABCL_G1_AES256_KEY` and paste only the 64-character hexadecimal key from the separately supplied private key file. **Never upload that key file**, post the key in an Issue/PR, or commit it. The encrypted reference object alone does not give anyone the plaintext DLLs.
4. After the feature branch upload, wait until its *new exact head SHA* passes the existing `Verify` job, then have the repository owner manually run **Actions → Build G1 approved candidate → Run workflow** on `main`, entering that full 40-character SHA as `candidate_sha`.

The Actions job requires owner-triggered execution on protected `main`, verifies the specified commit's successful GitHub Actions `Verify` run, checks the ciphertext SHA256, decrypts in the temporary Windows runner, checks the five real original game assemblies, and attempts a true `net35` compilation. Any missing input, altered file, failed compile or missing output must fail the job.

**Security boundary:** candidate source and build scripts MUST be reviewed before dispatch. A green source-only `Verify` check is not a substitute for reviewing code which executes while original game DLLs are temporarily available. The game author's permission is reported by the project owner; ABCL does not claim that the original binaries have become open-source or distributable.

## G1 output

Only if real L3 compilation succeeds, Actions uploads `ABCL-G1-Compiled-TestOnly`, which contains **one** test-only installer package, ABCL-authored XML and DLL, and a SHA256 record. It does not upload original game DLLs, the decryption key or the decrypted input archive. This is not a release or proof of in-game L4.

The G1 installer locally assembles original-record overlays from the user's own installed game. It does not overwrite the original installation. Do not use a normal save.

## Evidence — current checkpoint (2026-11-02)

- **R3 genuine build (L3, historical tested source):** commit `1a13e8d9ccc41fbf2a86f9c36dcb07b75b477d2b`, [Windows Actions 41391983195](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41391983195), test-only Actions artifact ID `13117942292`. Genuine `net35`/CLR2 compilation and package audit were reported successful. **Artifact ZIP or DLL SHA256 is not reproduced here because the exact value is not present in the checked evidence record; do not invent a hash.**
- **R3 gameplay (owner-reported L4, not an independent environment audit):** the owner reported native lead patient creation/ambulance, inpatient admission, blood-lead sampling and staffed laboratory analysis, result delivery, chelation, original CBC and save/quit/reload PASS in a disposable save. See [G1 PR #7](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/7), [Issue #2](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/2), and the dated [cross-workstream evidence update proposed in PR #18](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/18). The exact game build, DLC list and independent raw game logs were not supplied. This does **not** prove all-DLC/Workshop/uninstall compatibility or a releasable Alpha.
- **Updated read-only diagnostic panel (newer candidate):** source `7faf31c6bba34ab58a9e288217d0359956bd2af2` passed static `Verify`, CodeQL and Python contract tests. Its **own exact-SHA genuine L3/package audit remains pending**. After that, request a focused panel-only L4 check, not another complete R3 gameplay loop.
- **Source-only `Verify` remains L1/L2** and never substitutes for genuine L3 or in-game L4.
- **Historical setup status below:** the owner-only workflow setup steps and statements about not-yet-running L3/L4 describe the original initial bootstrap stage in 2026-11-01, **not** the later R3 candidate. Retained for traceability and manual fallback.
