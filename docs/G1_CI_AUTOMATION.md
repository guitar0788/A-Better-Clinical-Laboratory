# Automated G1 game-reference compilation

**Status:** The protected-main automatic G1 compiler is active (merged PR #19). Its exact-L3 provenance reporter and >100-comment pagination were owner-approved and merged in PR #64. The additional reporting of *authorized Windows build failures* is proposed in a separate Draft PR; it is not active until reviewed and merged.

## Why the former builder was manual

The original `Build G1 approved candidate` job uses the repository Secret `ABCL_G1_AES256_KEY` to temporarily decrypt author-authorized original game references for a real Windows `net35` build. It was restricted to an owner-initiated `workflow_dispatch` on `main` so an unreviewed PR or a fork could not automatically execute arbitrary build code in the presence of proprietary references. A green `Verify` alone is not a security review of MSBuild targets, installers or other executable source.

## Normal automated path after merge

`.github/workflows/auto-build-g1-verified.yml` is stored on **protected `main`** and uses `workflow_run` after `Verify`, not PR-supplied workflow code.

1. A commit is pushed to **the existing same-repository PR #7**, branch `feature/g1-secure-build`. GitHub runs ordinary read-only `Verify`.
2. If Verify succeeds, the protected-main automation checks the upstream workflow event, source repository, actor `guitar0788`, current owner-authored PR #7, and exact current head SHA. Forks, stale SHAs, other PRs and failed tests are rejected *before decrypting*.
3. The Windows checkout must match the independently authorized exact G1 SHA. Before reading the AES secret, the workflow verifies that the checkout contains all five required G1 laboratory XML files and three test-only installer/readme inputs; missing or mismatched files fail closed. Credentials are not persisted by checkout. Only a **pinned** `ABCL.G1.Panel.csproj` and `ABCLG1Panel.cs` are copied to a fresh `RUNNER_TEMP` build directory. Build configuration edits fail closed until explicitly reviewed in the protected-main workflow.
4. The pinned NuGet reference package is restored **before** decrypting any original game file. Immediately before decrypting, the Windows job independently checks that owner PR #7 remains open and that its exact head SHA still matches the approved checkout. Only authorized Windows `build` jobs enter a cancellation group, so forked, failed or otherwise rejected upstream Verify events cannot cancel an owner's active build. Superseded authorized G1 build jobs are cancelled; if the head changes, fail closed and do not use the AES key. The encrypted `ABCL_G1_refs.aes` must match its recorded SHA256. Authorized assemblies are decrypted only in the temporary Windows runner; their hashes are recorded.
5. The temporary isolated project is compiled for real `net35`/`CLR2`. Only ABCL-authored test DLL, XML, temporary-save installer and a hash manifest are packaged. The proprietary references, encryption key and encrypted input are excluded. Art and G1 gameplay assets are not modified.
6. Immediately before the test artifact is uploaded, the Windows job again requires PR #7's current head SHA to match the originally approved SHA. Superseded or closed PR candidates cannot upload stale artifacts. A successful build uploads the **test-only**, 7-day `ABCL-G1-AutoBuilt-TestOnly` artifact. This proves L3 only; it neither installs the Mod nor proves L4.

**One-time automatic bootstrap:** After this workflow itself is merged, the resulting `main` push runs `Verify`. The protected-main workflow accepts that specific verified main commit **only if the workflow file was changed in that commit**, then validates the latest current PR #7 SHA and its own passing Verify. This avoids having to make a fake G1 source change or manually enter a 40-character SHA to start the first build.

**Minimum token permissions:** the upstream authorization job alone gets `pull-requests: read` and `checks: read`; the Windows build job inherits only `contents: read` from the protected workflow. No step is granted `contents: write`, and no PR-authored workflow executes with the AES key.

The previous owner-only manual workflow remains available as an emergency fallback, not the routine process. It is not a bypass for source review. A genuinely new G1 MSBuild project requires separate protected-main security review before the pin can change.

## Stages that cannot be auto-accepted

- `Verify` / CodeQL: source-level/static checks, not L3 or L4.
- Genuine Windows compile: L3 only, even when automatically triggered.
- Owner-facing diagnostic-panel display: focused L4, only when changed panel code has an exact-SHA L3 package. Do **not** repeat the already accepted R3 patient/ambulance/laboratory/CBC/save sequence solely for read-only diagnostics.
- New equipment placement, visual quality, staff interaction and DLC/Workshop/save compatibility: actual L4 still required.
- Pull request merge, Alpha/stable release, and test patient-spawner publication: **never automated**.

No additional GitHub account, credit card, manually copied build secret or extra local plugin is required. The existing repository Secret stays in GitHub Actions.


## Active exact-source L3 success reporter (merged PR #64)

After a genuine Windows net35/CLR2 compiler job succeeds **and its test-only artifact is uploaded**, a protected-main reporting job can update a single marker-based comment on G1 PR #7 with the exact source commit, independently calculated compiled DLL SHA-256 and the Actions run link. The reporter has only `issues:write`, `pull-requests:read` and `contents:read` permissions; the secret-using Windows compilation job retains its previous read-only token. No encrypted game references or original DLLs are copied into the comment.

The reporter re-checks the currently open same-repository owner-authored PR #7 and exact head SHA before writing. A moved or replaced PR cannot publish stale evidence. Replacing the previous GitHub Actions bot marker avoids one new comment per compiled commit. A successful report establishes **L3 compilation only**, not the separately audited complete 34-file installable bundle or gameplay L4. Existing trusted build authorization and upload gates remain unchanged; a report failure does not invalidate an independently successful compiled artifact.

The successful-build reporting path was merged into protected main in PR #64. Source checks and a passing compiler must still be distinguished from owner game L4. An absence of a PR comment never proves the workflow failed to trigger: the reporter may have been skipped, failed, or the Windows compiler may have failed.

### Proposed failure-stage reporter extension (Draft only)

For authorized owner PR #7 builds whose real Windows job *fails*, the same marker comment can be updated with the exact G1 SHA, the trusted Actions run URL and the failed job step name read from the GitHub Actions jobs API. It must never assert an L3 success, invent a DLL SHA, include raw logs, or disclose original game references or Secrets. The reporter will skip rejected runs, cancelled/stale jobs, and unrelated PRs. The reporter's GitHub token gains only `actions: read` for step status lookup. Compile/secret jobs keep their existing access and behavior.

This extension is **not** a proof or fix of a triggering problem. It is only a safe error-reporting path, and a privileged main-workflow change requires separate owner authorization.
