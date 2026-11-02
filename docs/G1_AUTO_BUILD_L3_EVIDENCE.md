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

## Scope, later source and remaining test gate

- R3's earlier owner-reported real-game L4 (source `1a13e8d9ccc41fbf2a86f9c36dcb07b75b477d2b`) remains historical and separate from this **new L3**. The newer read-only Liver TY/ICU/ambulance/IMOBILE diagnostic panel has **not** been tested in the game.
- A subsequent PR #7 revision `4e7c65a12977eccbc88676b19f15f66ff62e0ea7` edited only `tools/G1_TEST_README.txt` to correct outdated build instructions and provide a focused panel-only L4 checklist. **This audit artifact still belongs to `aa3e7b16…`**. A new package bearing the later SHA requires its own exact-SHA compilation, or keep using the audited original package and its matching `BUILD_INFO.txt`.
- **Focused L4 only:** open the panel in a disposable installation, compare its Liver TY contract/ICU objective, ambulance, configured and live IMOBILE states to vanilla, and record a screenshot plus logs on failure. Do **not** spawn another lead patient or repeat the accepted R3 admission/lab/CBC/save-load scenarios solely for read-only status changes.
- Four-DLC/Workshop combinations, art placement/interaction, uninstall safety, legacy saves and Alpha release remain **NOT ACCEPTED**. G1 debug spawning is test-only and cannot ship enabled in Alpha.

The source and test artifacts contain no game assemblies as publishable binaries, and the workflow keeps the original author's protected game references in its temporary build environment.