# G1 — First verified automatic Windows net35/CLR2 L3 package audit

**Evidence timestamp:** 2026-11-02 UTC  
**Gate:** L3 genuine original-game-reference compilation **PASS** for the exact immutable candidate below. This is **not** a gameplay L4 or Alpha release.

## Provenance and authorization

| Field | Exact evidence |
| --- | --- |
| Trusted protected-main workflow | PR #19 squash merge `82a23174c1ad0af23e75036f5112660560f07c42` |
| Protected-main Verify | [run 41495795717](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41495795717) — SUCCESS |
| Automatic protected-main G1 build | [run 41495833103](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41495833103) — SUCCESS |
| Owner-controlled source | Draft PR #7 `feature/g1-secure-build`, exact SHA `aa3e7b163b05f78b24ca5fdfeba4baba07953012` |
| Pinned original-isolated project Git blob | `71daed7c3aa9e62edf9eea207fd77b2041be52ed` |
| GitHub Actions test artifact | `ABCL-G1-AutoBuilt-TestOnly`, ID `13165179364`; 7-day retention |
| Outer Actions artifact ZIP SHA256 | `3669cc2584890e8839d7b34d230e140716a18d07fcb6b81b2fc0542ca9ca2190` |
| Inner test-only installation ZIP SHA256 | `89b8b2467795e6baf5aac65ac14f5cc280decad2f093d51d467de1e414118f77` |
| ABCL-authored DLL SHA256 | `39db73bd3707700c7aa2adda6004b67408dcea98b271ebf1af241f4288ed8500` |
| DLL size | 14,848 bytes |
| Metadata / binary type | Managed PE32, CLI header runtime 2.5, CLR metadata `v2.0.50727`, `net35` build target |

This workflow executed on Windows Server 2022, restored its isolated pinned project **before** AES access, checked all eight packaging inputs, authenticated the encrypted reference asset, and decrypted original-game references only in temporary runner storage. GitHub's build log reports **Build succeeded, 0 Warning(s), 0 Error(s)**. It re-queried PR #7's exact head before decryption and before uploading the artifact.

## Genuine original-game-reference hashes, from Windows Actions logs

Hash values are audit identifiers only; **the actual proprietary game DLLs were not uploaded**.

| Reference | SHA256 |
| --- | --- |
| Assembly-CSharp.dll | `1120d899fb74d16f31115c5c27325edbd1154b68e9419e6b7ea03cc3d43b6f24` |
| Assembly-CSharp-firstpass.dll | `63294cc19e24ecbe76f17f0776c9abf6bf84358c4ef0b55967f141871308360f` |
| UnityEngine.dll | `0613defcbe1e30bfba003d1a18e06000d6606fe14958e89752ba4c74cc7dd673` |
| UnityEngine.CoreModule.dll | `f65bec39f0d3e75bac559130775fc7c965bc3af03e1b44bc59c004f72f8645f` |
| UnityEngine.IMGUIModule.dll | `3b8e0a9655baf1edba10d68464d03280f9b00d88bdab0e5cfb1e7b409652c400` |

## Independently downloaded archive inspection

The Actions artifact was downloaded through GitHub. Both nested ZIP layers and the ABCL DLL were independently read and hashed; `BUILD_INFO.txt` matched the current compiled source SHA and DLL digest. Exactly **ten** expected installer entries were present:

- `ModABCLG1LeadTest/ModABCLG1LeadTest.dll` (ABCL-authored managed DLL).
- `ModABCLG1LeadTest/Database/` — `ModAddon.xml`, `ModExaminations.xml`, `ModRoomTypes.xml`, `ModStringTableEnABCL.xml` and `ModStringTableZhHansABCL.xml`.
- `Install-ABCL-G1.ps1`, `INSTALL_G1_R3.cmd` and `G1_TEST_README.txt`.
- `ModABCLG1LeadTest/0Harmony.dll` — **zero-byte packaging placeholder**, not a third-party Harmony runtime.

No unexpected ZIP entries, parent-directory traversal, plaintext original-game DLL, encrypted reference archive or AES key files were present **by file/package inspection**. The claimed absence is a file-level artifact audit, not a proof of any game's runtime behavior or of undisclosed binary semantics.

## Repeatability check after conflict-free canonical main sync (2026-11-02 UTC)

The Draft G1 feature branch was previously **unmergeable** against current `main`, which prevented a new `pull_request` Verify and therefore the trusted `workflow_run` build. The only overlapping changes were the three canonical `docs/DECISIONS.md`, `docs/MASTER_PLAN.md`, and `docs/TEST_EVIDENCE.md` files. TS made a **two-parent, non-force merge commit** `ecd6cc66868fa0ef31320b79eebb0040b8f3f3e8` with parents `4e7c65a12977eccbc88676b19f15f66ff62e0ea7` and `82a23174c1ad0af23e75036f5112660560f07c42`; it preserved all 23 G1-only files at their original blob SHAs, retained main's current authoritative docs/workflows, and archived the feature's detailed 345-line prior TEST_EVIDENCE record in `docs/history/G1_PR7_TEST_EVIDENCE_PRE_MAIN_SYNC_20261102.md`. No game C# or net35 project blob changed.

This restored **real Verify**, **CodeQL** and Python checks for the feature branch. Trusted auto build [Actions 41499553588](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41499553588) independently authorized that new PR #7 head and completed the genuine Windows net35/CLR2 build **0 warnings, 0 errors**. The ZIP was downloaded and independently checked:

| Exact evidence | Second build |
| --- | --- |
| G1 source `BUILD_INFO.txt` SHA | `ecd6cc66868fa0ef31320b79eebb0040b8f3f3e8` |
| Run / artifact | `41499553588` SUCCESS / `13168800066` `ABCL-G1-AutoBuilt-TestOnly` |
| Outer Actions artifact ZIP SHA256 | `08fa312951028ddff4997f2991b75bcced426befd6b88f5567dff5592bedceb7` |
| Inner installer ZIP SHA256 | `1543b1f03fcd9512ddf9f6f3363f2936c71eafede25bf8d5163bc4e3fc72fec6` |
| `ModABCLG1LeadTest.dll` SHA256 / size | `39db73bd3707700c7aa2adda6004b67408dcea98b271ebf1af241f4288ed8500` / 14,848 bytes |
| CLR metadata | Managed PE32, `v2.0.50727`; same DLL bytes as first run |
| XML / installer entries | All five ABCL XML, both installer scripts and correct new test README; 10 total inner ZIP entries |
| Proprietary references / key | **Not present in inspected ZIP entries**; `0Harmony.dll` remains a zero-byte placeholder |

This new artifact is the **preferred test package** for the *current* draft PR #7 SHA; it contains updated focused panel-only L4 instructions instead of the first package's obsolete manual directions. Neither Windows build establishes gameplay L4, global DLC/Workshop interoperability, safe uninstall, or release readiness. **Do not spawn patients again solely to test read-only diagnostics.**

## Scope, later source and remaining test gate

- R3's earlier owner-reported real-game L4 (source `1a13e8d9ccc41fbf2a86f9c36dcb07b75b477d2b`) remains historical and separate from this **new L3**. The newer read-only Liver TY/ICU/ambulance/IMOBILE diagnostic panel has **not** been tested in the game.
- A subsequent PR #7 revision `4e7c65a12977eccbc88676b19f15f66ff62e0ea7` edited only `tools/G1_TEST_README.txt`; after protected-main sync the newer exact-source `ecd6cc66868fa0ef31320b79eebb0040b8f3f3e8` passed the **second actual Windows L3 build**, with unchanged DLL bytes and a newly packaged README. Prefer the second audited package `13168800066` / `BUILD_INFO.txt` for focused panel-only L4.
- **Focused L4 only:** open the panel in a disposable installation, compare its Liver TY contract/ICU objective, ambulance, configured and live IMOBILE states to vanilla, and record a screenshot plus logs on failure. Do **not** spawn another lead patient or repeat the accepted R3 admission/lab/CBC/save-load scenarios solely for read-only status changes.
- Four-DLC/Workshop combinations, art placement/interaction, uninstall safety, legacy saves and Alpha release remain **NOT ACCEPTED**. G1 debug spawning is test-only and cannot ship enabled in Alpha.

The source and test artifacts contain no game assemblies as publishable binaries, and the workflow keeps the original author's protected game references in its temporary build environment.