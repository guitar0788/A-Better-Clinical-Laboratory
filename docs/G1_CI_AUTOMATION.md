# Automated G1 game-reference compilation

**Status:** Proposed in the accompanying CI PR. This automatic workflow is not active until it is reviewed and merged into protected `main`.

## Why the former builder was manual

The original `Build G1 approved candidate` job uses the repository Secret `ABCL_G1_AES256_KEY` to temporarily decrypt author-authorized original game references for a real Windows `net35` build. It was restricted to an owner-initiated `workflow_dispatch` on `main` so an unreviewed PR or a fork could not automatically execute arbitrary build code in the presence of proprietary references. A green `Verify` alone is not a security review of MSBuild targets, installers or other executable source.

## Normal automated path after merge

`.github/workflows/auto-build-g1-verified.yml` is stored on **protected `main`** and uses `workflow_run` after `Verify`, not PR-supplied workflow code.

1. A commit is pushed to **the existing same-repository PR #7**, branch `feature/g1-secure-build`. GitHub runs ordinary read-only `Verify`.
2. If Verify succeeds, the protected-main automation checks the upstream workflow event, source repository, actor `guitar0788`, current owner-authored PR #7, and exact current head SHA. Forks, stale SHAs, other PRs and failed tests are rejected *before decrypting*.
3. The checked-out commit is immutable and credentials are not persisted. Only a **pinned** `ABCL.G1.Panel.csproj` and `ABCLG1Panel.cs` are copied to a fresh `RUNNER_TEMP` build directory. Build configuration edits fail closed until explicitly reviewed in the protected-main workflow.
4. The pinned NuGet reference package is restored **before** decrypting any original game file. The encrypted `ABCL_G1_refs.aes` must match its recorded SHA256. Authorized assemblies are decrypted only in the temporary Windows runner; their hashes are recorded.
5. The temporary isolated project is compiled for real `net35`/`CLR2`. Only ABCL-authored test DLL, XML, temporary-save installer and a hash manifest are packaged. The proprietary references, encryption key and encrypted input are excluded. Art and G1 gameplay assets are not modified.
6. A successful build uploads the **test-only**, 7-day `ABCL-G1-AutoBuilt-TestOnly` artifact. This proves L3 only; it neither installs the Mod nor proves L4.

**One-time automatic bootstrap:** After this workflow itself is merged, the resulting `main` push runs `Verify`. The protected-main workflow accepts that specific verified main commit **only if the workflow file was changed in that commit**, then validates the latest current PR #7 SHA and its own passing Verify. This avoids having to make a fake G1 source change or manually enter a 40-character SHA to start the first build.

The previous owner-only manual workflow remains available as an emergency fallback, not the routine process. It is not a bypass for source review. A genuinely new G1 MSBuild project requires separate protected-main security review before the pin can change.

## Stages that cannot be auto-accepted

- `Verify` / CodeQL: source-level/static checks, not L3 or L4.
- Genuine Windows compile: L3 only, even when automatically triggered.
- Owner-facing diagnostic-panel display: focused L4, only when changed panel code has an exact-SHA L3 package. Do **not** repeat the already accepted R3 patient/ambulance/laboratory/CBC/save sequence solely for read-only diagnostics.
- New equipment placement, visual quality, staff interaction and DLC/Workshop/save compatibility: actual L4 still required.
- Pull request merge, Alpha/stable release, and test patient-spawner publication: **never automated**.

No additional GitHub account, credit card, manually copied build secret or extra local plugin is required. The existing repository Secret stays in GitHub Actions.
