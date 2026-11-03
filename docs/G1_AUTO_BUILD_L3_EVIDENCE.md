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

**Historical package selection:** the second artifact `13168800066` was the preferred package for source `ecd6cc66868fa0ef31320b79eebb0040b8f3f3e8` when that commit was current. It is now superseded by later exact-source builds. For the current TO-001 room-icon acceptance, use only the independently audited combined icon test package for `851b3059bed871d38844cffff7310de995bb2019` (fourth L3 run and packaging details below), **not** this historical artifact or third-source localization package. Neither build establishes gameplay L4, global DLC/Workshop compatibility, safe uninstall, or release readiness. **Do not spawn patients again solely to test read-only diagnostics.**

## Scope, later source and remaining test gate

- R3's earlier owner-reported real-game L4 (source `1a13e8d9ccc41fbf2a86f9c36dcb07b75b477d2b`) remains historical and separate from this **new L3**. The newer read-only Liver TY/ICU/ambulance/IMOBILE diagnostic panel has **not** been tested in the game.
- A subsequent PR #7 revision `4e7c65a12977eccbc88676b19f15f66ff62e0ea7` edited only `tools/G1_TEST_README.txt`; after protected-main sync the newer exact-source `ecd6cc66868fa0ef31320b79eebb0040b8f3f3e8` passed the **second actual Windows L3 build**, with unchanged DLL bytes and a newly packaged README. Prefer the second audited package `13168800066` / `BUILD_INFO.txt` for focused panel-only L4.
- **Focused L4 only:** open the panel in a disposable installation, compare its Liver TY contract/ICU objective, ambulance, configured and live IMOBILE states to vanilla, and record a screenshot plus logs on failure. Do **not** spawn another lead patient or repeat the accepted R3 admission/lab/CBC/save-load scenarios solely for read-only status changes.
- Four-DLC/Workshop combinations, art placement/interaction, uninstall safety, legacy saves and Alpha release remain **NOT ACCEPTED**. G1 debug spawning is test-only and cannot ship enabled in Alpha.

The source and test artifacts contain no game assemblies as publishable binaries, and the workflow keeps the original author's protected game references in its temporary build environment.
## Third exact-head automatic build — professional medical display text, no clinical code change (2026-11-03 UTC+8)

User-facing G1 titles/descriptions were changed in the existing ABCL-owned English and Simplified Chinese string tables to remove test/brand language and describe actual medical functions. Visible room name: **Toxicology Laboratory / 临床毒理实验室**; sample: **Blood sample collection / 血液标本采集**; linked analysis: **Blood lead level / 血铅测定**. Internal IDs, `RoomType`, examination/procedure tags and player/spawner C# were not changed. Three new bilingual source tests enforce six matching LocIDs, neutral clinical terms, and unchanged native room/examination description references.

The revised Draft PR #7 exact SHA `63aa4c5ea067e58e2b79e2d1d1a233791224dbd8` passed Verify, CodeQL and Python tests and an automated genuinely compiled [Windows net35/CLR2 run 41548682348](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41548682348) with **0 errors and 0 warnings**. The independently downloaded and inspected ZIP shows:

| Field | Value |
| --- | --- |
| Candidate in `BUILD_INFO.txt` | `63aa4c5ea067e58e2b79e2d1d1a233791224dbd8` |
| GitHub test-only artifact | `13190690403` / `ABCL-G1-AutoBuilt-TestOnly` |
| Outer artifact ZIP SHA256 | `f780e9b03c8682ac9c2720c55e0989e45da58c8dd0777789617245bfd4aec716` |
| Inner install ZIP SHA256 | `8240bc06cc933025baff3e06e9cd12f010090dca589dfd586e88469958095578` |
| ABCL managed DLL SHA256 / bytes | `39db73bd3707700c7aa2adda6004b67408dcea98b271ebf1af241f4288ed8500` / 14,848 — **identical to prior two genuine L3 builds** |
| XML localization files | `ModStringTableEnABCL.xml`, `ModStringTableZhHansABCL.xml` — six matching original LocIDs in each, revised medical display text present |
| Archive contents | Same 10 expected entries; no original-game DLLs, reference ciphertext or AES key files; zero-byte Harmony placeholder unchanged |

Two earlier interim auto-builder runs were **fail-closed** as the feature HEAD advanced: one was rejected at upstream authorization, and one at the stale-SHA pre-decryption gate; these are **not** a clinical build failure and did not publish an obsolete package. Only the third exact-head run described in that historical checkpoint was accepted; a newer verified TO-001 source and fourth real Windows build are recorded next.

**L3 and bilingual package audit PASS; gameplay L4 still NOT RUN.** Install only a matching disposable-save test package for the *single read-only panel* verification; neither R3 clinical/Lab/CBC retesting nor any Alpha/release is authorized by this stage.


## Fourth exact-head real Windows L3 — TO-001 native room icon UI (2026-11-03 UTC+8)

- Exact Draft PR #7 head **`851b3059bed871d38844cffff7310de995bb2019`**: additive 64×64 original FA red/gray sprites and separate namespaced `TEXTURE_CUSTOM_SPRITE` XML, plus a fail-closed **exact-room-only, Harmony-free** UI adapter for the original `DepartmentManagementLogisticsHybridController` and `RoomItemController` native room-menu paths. No original database/atlas overwrite, room-area/access coloring modifications, or medical procedure changes.
- FA corrected original art source `5c739b4e1cba7eb8d8e81b5d0f823de2f2077973`; original Git blob IDs `8b06b857603c72a73765c61ae13f4b987805cc33` and `98724f23bea8807c1c2e2c002db34da8c944dcd2`, SHA256 `26b537e5b549a82c85f53e2491114d63dcc0df0bd146b40a12db26e3f9c6510f` and `2f3b4dc43ec0d4bbee96cf7baf695efa79db036b9816fa95e911a35e24b971ea`. Original native laboratory active/inactive panel colors `#C93F3D` and `#999999`; glyph white `#F2F2F2`.
- [Genuine Windows Actions net35/CLR2 run **41566322905**](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41566322905) **SUCCESS: 0 warnings, 0 errors**; exact current G1 SHA verified twice around the secret/decrypt/upload boundary. ABCL-authored DLL 19,456 bytes, SHA256 **`7b13e698024c660f40257b713535b9b2b23354289301e3b1d1bbf41476112f2e`**. GitHub base artifact ID `13199007269`, outer SHA256 `998bf7f0ce9f0f0a6e5c504eda2e4bcbdf4de30519c890be9d76f0625d0a7a99`. GitHub base artifact deliberately follows protected workflow's five-XML whitelist and **does not** include the optional TO-001 icon.
- The owner-facing **complete** test-only package was separately assembled with reproducible `tools/assemble_to001_test_only.py` source contract, using that genuinely compiled G1 DLL, the original 10 base-package entries, the extra namespaced icon `ModAssetListsTO001.xml`, both original FA PNGs and a focused TO-001 test-only README: **14 inner ZIP entries**. Inner ZIP SHA256 `73b54157b948345d354def7c8497394b08d178fc869eb53c97f834eb2e8001b1`, outer delivery ZIP SHA256 `a30e9f3f6854ee502dd5aea3028ed95dde5e553df4ad6ebf2e0fe0e3f64f81eb`. Independent extraction compared each file, original FA PNG SHA, exact current compiled DLL hash, original XML and no third-party/original-game DLL, AES archive or secret files; the zero-byte Harmony placeholder remains inert. The outer delivery file is provided to the owner in the TS ChatGPT conversation, **not uploaded to GitHub or published as a release**.
- **Gate disposition: source/L2, real net35 L3 and packaging audit PASS; native room-menu L4 NOT RUN.** Owner must check exact red icon and gray unavailable state, hover/close/reopen, unchanged hematology/microbiology/histology/DLC icons, world zoning colors and save/reload in a disposable save. Existing R3 clinical/CBC pathway must **not** be retested solely for the icon. There is no claim of owner visual acceptance, full DLC/Workshop interoperability or Alpha readiness.
