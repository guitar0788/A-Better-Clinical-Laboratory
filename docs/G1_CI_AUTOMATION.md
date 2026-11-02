# Automated G1 game-reference compilation

**Status:** **ACTIVE on protected `main`** since owner-approved [PR #19](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/19) squash merge `82a23174c1ad0af23e75036f5112660560f07c42`. Its first actual [Windows run 41495833103](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41495833103) **PASSED L3** with an independently audited ABCL-only test artifact; see [exact binary / ZIP / reference hashes](G1_AUTO_BUILD_L3_EVIDENCE.md). This is **NOT** diagnostic-panel L4 or a release.

## Why the former builder was manual

The original `Build G1 approved candidate` job uses the repository Secret `ABCL_G1_AES256_KEY` to temporarily decrypt author-authorized original game references for a real Windows `net35` build. It was restricted to an owner-initiated `workflow_dispatch` on `main` so an unreviewed PR or a fork could not automatically execute arbitrary build code in the presence of proprietary references. A green `Verify` alone is not a security review of MSBuild targets, installers or other executable source.

## Active verified-source build path

`.github/workflows/auto-build-g1-verified.yml` is stored on **protected `main`** and uses `workflow_run` after `Verify`, not PR-supplied workflow code.

1. A commit is pushed to **the existing same-repository PR #7**, branch `feature/g1-secure-build`. GitHub runs ordinary read-only `Verify`.
2. If Verify succeeds, the protected-main automation checks the upstream workflow event, source repository, actor `guitar0788`, current owner-authored PR #7, and exact current head SHA. Forks, stale SHAs, other PRs and failed tests are rejected *before decrypting*.
3. The Windows checkout must match the independently authorized exact G1 SHA. Before reading the AES secret, the workflow verifies that the checkout contains all five required G1 laboratory XML files and three test-only installer/readme inputs; missing or mismatched files fail closed. Credentials are not persisted by checkout. Only a **pinned** `ABCL.G1.Panel.csproj` and `ABCLG1Panel.cs` are copied to a fresh `RUNNER_TEMP` build directory. Build configuration edits fail closed until explicitly reviewed in the protected-main workflow.
4. The pinned NuGet reference package is restored **before** decrypting any original game file. Immediately before decrypting, the Windows job independently checks that owner PR #7 remains open and that its exact head SHA still matches the approved checkout. Only authorized Windows `build` jobs enter a cancellation group, so forked, failed or otherwise rejected upstream Verify events cannot cancel an owner's active build. Superseded authorized G1 build jobs are cancelled; if the head changes, fail closed and do not use the AES key. The encrypted `ABCL_G1_refs.aes` must match its recorded SHA256. Authorized assemblies are decrypted only in the temporary Windows runner; their hashes are recorded.
5. The temporary isolated project is compiled for real `net35`/`CLR2`. Only ABCL-authored test DLL, XML, temporary-save installer and a hash manifest are packaged. The proprietary references, encryption key and encrypted input are excluded. Art and G1 gameplay assets are not modified.
6. Immediately before the test artifact is uploaded, the Windows job again requires PR #7's current head SHA to match the originally approved SHA. Superseded or closed PR candidates cannot upload stale artifacts. A successful build uploads the **test-only**, 7-day `ABCL-G1-AutoBuilt-TestOnly` artifact. This proves L3 only; it neither installs the Mod nor proves L4.

**One-time automatic bootstrap (COMPLETED):** PR #19's merge pushed the workflow to `main`; protected-main Verify run `41495795717` passed and triggered auto-build `41495833103` for the authorized current G1 PR #7 source. The bootstrap accepts the verified `main` push only when that trusted workflow file changed in the merge commit, preventing unrelated main pushes from rebuilding G1. The initial build has been executed and audited; do **not** create fake source commits or repeat this bootstrap.

**Minimum token permissions:** the upstream authorization job alone gets `pull-requests: read` and `checks: read`; the Windows build job inherits only `contents: read` from the protected workflow. No step is granted `contents: write`, and no PR-authored workflow executes with the AES key.

The previous owner-only manual workflow remains available as an emergency fallback, not the routine process. It is not a bypass for source review. A genuinely new G1 MSBuild project requires separate protected-main security review before the pin can change.

## Stages that cannot be auto-accepted

- `Verify` / CodeQL: source-level/static checks, not L3 or L4.
- Genuine Windows compile: L3 only, even when automatically triggered.
- Owner-facing diagnostic-panel display: focused L4, only when changed panel code has an exact-SHA L3 package. Do **not** repeat the already accepted R3 patient/ambulance/laboratory/CBC/save sequence solely for read-only diagnostics.
- New equipment placement, visual quality, staff interaction and DLC/Workshop/save compatibility: actual L4 still required.
- Pull request merge, Alpha/stable release, and test patient-spawner publication: **never automated**.

No additional GitHub account, credit card, manually copied build secret or extra local plugin is required. The existing repository Secret stays in GitHub Actions.
