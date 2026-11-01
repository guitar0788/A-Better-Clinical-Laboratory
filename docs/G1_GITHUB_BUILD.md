# G1 owner-approved GitHub build

The G1 code is still in draft PR #7. GitHub only exposes a new manual `workflow_dispatch` action once that workflow exists on the default branch. This infrastructure-only workflow is therefore reviewed and merged separately, **without merging G1 test code**.

Run **Actions → Build G1 approved candidate → Run workflow** on `main` using the full 40-character SHA of a reviewed and `Verify`-passed G1 commit. Only `guitar0788` can run the build job. This gate does not replace a human review. **Do not run it on a fork or a candidate containing unreviewed scripts, project files or build targets**: compiling untrusted code with access to proprietary game references is unsafe.

GitHub cannot conjure the Project Hospital DLLs. The owner must supply an access-controlled, short-lived HTTPS URL privately, using GitHub Actions repository secrets `ABCL_G1_SOURCE_URL` and `ABCL_G1_SOURCE_SHA256`. The ZIP must contain at its root, from the owner's legitimate game installation:

```text
Assembly-CSharp.dll
Assembly-CSharp-firstpass.dll
UnityEngine.dll
UnityEngine.CoreModule.dll
UnityEngine.IMGUIModule.dll
```

The SHA256 must be the digest of the **complete private ZIP**, not of a single DLL. The runner checks its digest and the five files before compiling; it copies **only ABCL-authored** XML and the new ABCL DLL into the downloadable test artifact. Never place the private URL, archive, game DLLs or full installer debug logs in GitHub Issues, commits, public Releases or artifacts.

The artifact is **G1 test-only**, not Alpha. A successful build is L3, and patient generation, blood-lead test routing, CBC regression and save/load still require L4 in-game evidence.

On unconfigured secrets this workflow fails closed, rather than reporting a green fake build. No extra GitHub secrets are used for routine `Verify` or pull requests.
