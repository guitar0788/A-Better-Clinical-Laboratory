# G1: GitHub public-repository compilation with encrypted game references

> **2026-11-02 current update:** This page preserves the original owner-only manual bootstrap procedure as history/fallback. G1 R3 has since passed genuine Windows net35/CLR2 L3 and its core clinical L4 was owner-reported PASS; the newer diagnostic-panel candidate still needs its **own** exact-SHA L3. See [automated verified G1 build](G1_CI_AUTOMATION.md) for the proposed no-manual-dispatch path. That new workflow only becomes active after protected-main review and merge; it cannot establish gameplay L4.
>
> **Historical status at original writing:** Build infrastructure only; genuine G1 L3 and L4 had not yet passed.

The owner reports authorization from the game's author to perform compilation in the public ABCL GitHub repository. This is recorded as authorization for **compilation**; it is not assumed to authorize publication or redistribution of the original proprietary game DLLs. Accordingly the repository stores **encrypted build inputs**, not plaintext binaries. ABCL-authored test artifacts exclude game assemblies.

## One-time setup (no payment card, no second repository)

1. Download the encrypted reference asset **ABCL_G1_refs.aes** supplied in the ABCL development chat. This file is ciphertext; **do not upload** the unencrypted original ZIP `ABCL_G1_Private_Game_References_DoNotPublish.zip`.
2. On the existing `feature/g1-secure-build` branch of this repository, upload that exact `ABCL_G1_refs.aes` at the **repository root**. Do not add it to protected `main` directly. The workflow authenticates the SHA256 of this ciphertext: `918A1E3FC74AD530AF070C012BB8075DBC3874438FE5BA3C96A8D8AD39A3FCE2`.
3. In **Settings → Secrets and variables → Actions → New repository secret**, create `ABCL_G1_AES256_KEY` and paste only the 64-character hexadecimal key from the separately supplied private key file. **Never upload that key file**, post the key in an Issue/PR, or commit it. The encrypted reference object alone does not give anyone the plaintext DLLs.
4. After the feature branch upload, wait until its *new exact head SHA* passes the existing `Verify` job, then have the repository owner manually run **Actions → Build G1 approved candidate → Run workflow** on `main`, entering that full 40-character SHA as `candidate_sha`.

The Actions job requires owner-triggered execution on protected `main`, verifies the specified commit's successful GitHub Actions `Verify` run, checks the ciphertext SHA256, decrypts in the temporary Windows runner, checks the five real original game assemblies, and attempts a true `net35` compilation. Any missing input, altered file, failed compile or missing output must fail the job.

**Security boundary:** candidate source and build scripts MUST be reviewed before dispatch. A green source-only `Verify` check is not a substitute for reviewing code which executes while original game DLLs are temporarily available. The game author's permission is reported by the project owner; ABCL does not claim that the original binaries have become open-source or distributable.

## G1 output

Only if real L3 compilation succeeds, Actions uploads `ABCL-G1-Compiled-TestOnly`, which contains **one** test-only installer package, ABCL-authored XML and DLL, and a SHA256 record. It does not upload original game DLLs, the decryption key or the decrypted input archive. This is not a release or proof of in-game L4.

The G1 installer locally assembles original-record overlays from the user's own installed game. It does not overwrite the original installation. Do not use a normal save.

## Evidence

- GitHub source `Verify`: L1/L2 only.
- GitHub genuine `net35` build: L3 only, pending actual workflow execution.
- G1 blood-lead test, original CBC, save/load and player-spawn behavior: L4 **NOT RUN**.
