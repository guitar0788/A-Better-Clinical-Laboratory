# TO-004 — One-session focused room-prefab L4 checklist (test only)

This guide is for the two owner-authored Toxicology Laboratory room prefabs, **not** the G1 patient spawner or ART-001 new instruments. Existing G1 R3 clinical/CBC evidence is not repeated.

## Exact package identity

1. On Draft PR #31, find the passing **TO-004 prefab source-only candidate** workflow at the specific reviewed head SHA. Download its `ABCL-TO004-Prefab-Overlay-TestOnly` artifact and check `TO004_BUILD_INFO.json` matches that SHA; preserve the displayed ZIP SHA256.
2. Existing **G1 test-only addon must be installed first**. Close the game and run `tools/INSTALL_TO004_TEST_ONLY.cmd` inside the extracted overlay. Enter the root folder containing `ProjectHospital_Data` when prompted. Do not copy into the original game's `Database` folder. This installer refuses to replace existing TO-004 files or work without the G1 toxicology room.
3. Use a new disposable hospital test save with baseline Laboratory enabled and a valid, already-operational Toxicology Laboratory. Do **not** use a normal long-term save or untested Workshop stack.

## Focused game L4 — single session

| # | Action | Expected |
| - | - | - |
| 1 | Launch game / open building menu > laboratory prefabs | No new startup error; both variants listed |
| 2 | Compare small/large entries | Distinct readable 104×104 art; localized names and correct 8×6 / 12×6 dimensions; prices are provisional 25,000 / 30,000 |
| 3 | Place 8×6 layout on open foundation | No missing object ID, missing texture, malformed walls/doors, or forced overriding an existing room |
| 4 | Rotate small layout through four available directions | Preview and placed walls/doors/objects rotate sensibly; no clipping or impossible placement |
| 5 | Place 12×6 layout; inspect four directions | All required original equipment is present and room remains Toxicology Laboratory, not hematology |
| 6 | Inspect room requirements and staff routes | Game recognizes required equipment; laboratory specialist has a traversable route and can enter; no unintended occupation/zone colors |
| 7 | Check vanilla hematology, microbiology, histology prefab menus | Icons/prefabs/prices are unchanged and still usable; no duplicated/replaced entries |
| 8 | Save, quit, reload disposable save with same addon installed | Both rooms, equipment and type remain intact; no new XML/prefab errors |

If any step fails, stop and record the **first failing step**, screenshot, game version, enabled official DLCs/Workshop mods, and matching `output_log.txt` / `Player.log`. Do not repeat G1 patient-generation tests just to investigate room-art failures.

## Uninstall / rollback

Stop the game, retire the disposable test save, and run `tools/UNINSTALL_TO004_TEST_ONLY.cmd` **from the same extracted package**; it removes exactly eight TO-004 files only if their SHA256 still matches the package. Keep the G1 addon and all original game files untouched. Do not open the disposable save after TO-004 is removed.

No claims of Alpha, general Workshop interoperability or long-term save/uninstall safety are made by this test.