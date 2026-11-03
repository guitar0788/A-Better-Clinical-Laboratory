# TO + FA — one-session integrated L4 candidate

**Status:** Draft, TEST-ONLY. Preserve every original/third-party Mod and all clinical evidence. No public Alpha or merge into main.

## Why combine
Owner requested **one unified test session**, instead of separate installation rounds for TO and FA:
- TO-owned **TO-004 #30 / Draft PR #31**: two owner-authored Toxicology Laboratory prefabs (8x6 / 12x6), unchanged original XML hashes and independent 104px previews.
- FA-owned **ART-001 #3 / Draft PR #14**: two original tabletop devices and a private compatible workbench. These remain separate from TO prefab floor plans and original equipment.
- FA/TS **TO-001 #24 / Draft PR #29**: corrected native-sized room-list white glyph and its *visually matching* private floor atlas tile 376. No original atlas overwrite or zone-color tint override.
- TS **TO-002 #25 / Draft PR #32**: strictly read-only native Dependency tree hierarchy probe, not an added graph node.
- G1 source clinical path continues unchanged. Test artifact contains no proprietary original game DLLs, secrets or user saves.

## Exact-source pins
- Original G1 + TS floor bridge base: feature/ts-to001-private-floor-renderer@49475e91cabb2fa361c85e28d2f29ee0b7510c17.
- FA room/floor shared SVG + ART assets: feature/art-001-two-devices@cafcc32d9eb21b1f7e5df39a7f7f443d3ebf1da7.
- TO-004 prefab/layout/preview source: feature/to004-toxicology-prefabs@eac88c04f6d585e987b921938b76e3a3a4d4d1b0.
- TS TO002 probe implementation: feature/ts-to002-readonly-tree-probe@109e3f06c94b86e223d06c6126d328e874709e22.
- This branch has its own exact HEAD SHA in the packaged BUILD_INFO.json.

## Build and supply-chain policy
\`.github/workflows/build-tofa-unified-l4.yml\` checks out immutable FA and TO commits, generates original art on Ubuntu, then authenticates the **exact integration commit's GitHub Actions Verify PASS** before decrypting references on an ephemeral Windows runner and compiling genuine net35/CLR2. The only uploaded deliverable is **one** combined test-only ZIP with **two ABCL-owned addon directories** (G1/TO and ART), a SHA manifest, a single guarded installer and a restore launcher. Both native source test-only placeholders and the private floor tile are included. No auto-deploy, no PR merge, no Alpha release.

## One-time user installation and L4
Extract the single ZIP **outside the game directory**, close Project Hospital, run \`INSTALL_TOFA_UNIFIED.cmd\` and provide the Steam game root. The installer handles existing ABCL G1/ART test folders by **backing up only those known addon folders** outside the game, with hashes and safe failure rollback. It refuses unknown/third-party folder ownership. Run exactly one disposable-save session using \`TOFA_L4_CHECKLIST.txt\`, with no repeat of previously accepted blood-lead/ambulance/CBC treatment workflow.

After L4, close game, retire the disposable save, run \`RESTORE_TOFA_PREVIOUS.cmd\` from the **same extracted directory** to restore any previous ABCL test setup. Do not delete the extracted directory/backup until restoration succeeds.

## Acceptance gates (still open)
- [ ] Integration exact-head Verify + CodeQL PASS.
- [ ] Genuine Windows net35/CLR2 L3 + compiled ABCL DLL, only original-art TO+FA assets and compatible XML.
- [ ] Independent manifest/hash package audit, no game DLL/key/vanilla file.
- [ ] User L4 screenshot/first failure & log for TO004 two rooms, FA devices, TO001 both icon surfaces and TO002 read-only hierarchy.
- [ ] Vanilla hematology/microbiology/histology, original CBC, installed DLCs and declared Workshop coexistence.
- [ ] Owner visual approval before resolving issues or merging.

The source-only FA sprite L2 is not an actual in-game aesthetic pass. The Dependency tree probe does not implement a node. Keep original Draft PRs and Issues open until evidence is accepted.
