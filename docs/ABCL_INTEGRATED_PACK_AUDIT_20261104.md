# ABCL integrated G1 + ART001 + TO004 local test candidate — 2026-11-04

**Authority:** `docs/MASTER_PLAN.md`, binding decisions `ABCL-D002..D014`. This is an evidence-only record in Draft PR #33, not Alpha or a public GitHub release.

## Exact package provenance and checks

- **Chat-delivered test-only ZIP:** `ABCL_G1_ART_TO004_TEST_20261104_G1-22db2f.zip`; size **273,325 bytes**; SHA256 **`e4c2fbc77af26aeee71736062ced7fc4e5198b7e1184c79fe2e3b6b53ad2e7ca`**.
- **G1 current PR #7:** exact SHA `22db2f50b95b6c7af6dc548cac3b9cb954a1faf8`, real Windows net35 / CLR2 [Actions #41658767363](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41658767363), artifact **13240663594**, compiled ABCL-only DLL SHA256 **`9a338528ce40da8e1e7c153428d12fbf8e34e0a1251ed42529b62d1a667b729f`**.
- **Owner-approved TO004 original V3:** source `a7d399d429b64ad0f41d16c002a18889ae7b00e8`, source artifact **13229169917**, two 104x104 room preview PNGs, two native prefabs, original owner-reported **6/6 V3 game L4**. That earlier test does NOT prove the present combination.
- **FA standalone machines:** approved-source-submission SHA `cb3a7ab5d03e8677dcb84f486a04bf0ea5f8f622`, source/artifact **13244905333**; exactly two additive 1x1 stand-alone GameDB machines, 2048x1024 private atlas, menu icons and bilingual descriptions. Independent visual game L4 **NOT RUN**.
- The separate TO001 floor source artifact **13235300478** is bundled as **quarantined source only**, not installed; exact private renderer C# is absent from the compiled G1 DLL.
- G2 V3 Cd/Hg medical source artifact **13251869955** (preceding the 2026-11-04 disabled-fixture correction) is bundled as **quarantined source only**. The quarantine copy explicitly applies `<Disabled>true</Disabled>` to both private experimental diagnoses and is **not installed**. Current separate G2 GM C# PR #45 has L2 PASS but **NO genuine game-compatible L3**. G2 normal C2 diagnostic exclusivity is **not proved**, so this ZIP is **not a playable three-metal-assay test**.
- TO002 relationship-diagram node/edges remain unimplemented. TO003 full bilingual/visual L4 remains pending. Four-DLC/Workshop noninterference is not proven.

## Offline archive / compatibility audit results

Local Python checks against the **owner-provided original** read-only `StreamingAssets.zip` and `dll_ilspy.zip`:

| Gate | Observed | Result |
| --- | --- | --- |
| ZIP CRC, no duplicate/traversal paths, SHA256 for every manifest entry | 63 ZIP entries; 62 SHA-pinned entries | **L2 PASS** |
| Active addon file inventory | 22 owned runtime files; 13 GameDB XML documents | **L2 PASS** |
| Non-overlapping GameDB records | 21 namespaced DB entries; no duplicate IDs | **L2 PASS** |
| Bilingual names/description pairs | 14 English and 14 zh-Hans keys, exact-key parity | **L2 PASS** |
| Private standalone equipment/preview images | Private atlas 2048x1024; two prefab previews 104x104 | **L2 PASS** |
| Native game-defined baseline | DPT_LAB and TRM_LDP original entry/expectations found; vanilla EXM_CBC_TESTING not overridden | **L2 PASS** |
| Game binary safety | Original Unity/Assembly-CSharp references, decrypted files and key absent from ZIP | **L2 PASS** |
| Native code-mod loading sentinel | Empty 0Harmony.dll exists and is deliberately skipped by `TitleScreenController.cs` | **Source PASS** |
| Genuine G1 C# compile | Exact G1 head and DLL hash verified against successful Windows Actions output | **G1-only L3 PASS** |
| Combined G1+FA+TO004 native game installation/interaction/save | No Windows installation or Project Hospital game run in this environment | **L4 NOT RUN** |
| New G2 GM C#/clinical gating | Source-only, non-installed | **L3/L4 BLOCKED** |

**Important sentinel correction:** Original `TitleScreenController.cs` explicitly checks that `0Harmony.dll` exists alongside code DLLs before scanning, then skips that exact filename in `Assembly.LoadFrom`. A **0-byte file is the intended sentinel for the vanilla loader**, not a Harmony dependency or broken executable DLL. Previous attempts to *remove* this marker as a blanket fix risked preventing the actual ABCL DLL from being loaded. See owner-source correction comments on archived #34 and active #7/#42.

## Test-only installer and safe rollback

The chat-delivered ZIP includes `INSTALL_INTEGRATED_TEST.cmd` / `Install-ABCL-Integrated.ps1` and `RESTORE_PREVIOUS_ABCL.cmd` / `Restore-ABCL-Previous.ps1`:

- Installer validates source files against the manifest and checks original game database paths. It only installs `StreamingAssets/Addons/ModABCLG1LeadTest`, using the original G1 installer to derive additive-local `DPT_LAB` and `TRM_LDP` XML copies. It does **not** replace game XML or any third-party addon.
- A recognized old ABCL G1 addon is moved into `ABCL_Test_Backups` **outside** the Addons tree before replacement, to avoid the game scanning an extra addon copy. Install failures attempt rollback; current and previous saves must not be interchanged.
- Restore validates all managed-file hashes and native generated override hashes, retires the current ABCL folder, and optionally restores the earlier owned ABCL test folder. Unsupported/modified files fail closed.
- The Windows PowerShell scripts themselves **were not executed** here: no Windows/game runtime exists in this environment. Do not represent the offline checks as Windows install smoke or actual mod/game compatibility.

## Next gate: focused one-session L4 (no redundant lead-case replay)

Test on a fresh disposable save: native game launch, G1 test panel display (do not spawn severe lead patient), Toxicology Laboratory menu, two standalone equipment menus/placement/four views/footprints/staff access, original V3 small/large native prefabs and previews, original CBC, save/quit/reload, and safe restore. Record game version and actual DLC/Workshop set. Stop on first failure and preserve log/screenshot. The interactive PASS/FAIL/BLOCKED checklist is provided **inside the ChatGPT conversation**, not as PDF.

**No Alpha release, no merged core/CI/art PRs, no universal DLC compatibility claim.**
