ABCL ART-001 EQUIPMENT PLACEMENT TEST — NO CLINICAL WORKFLOW
==============================================================

STATUS: first test artifact 13124027790 FAILED in-game placement/rotation
(3 PASS, 2 FAIL, 3 BLOCKED). Keep it as historical evidence. This source
now includes a dedicated ABCL-owned instrument workbench, but the corrected
source has NOT passed a new exact-SHA build/package audit or any updated L4.
Do NOT install or test a newly built version until it has been audited.
Not Alpha.
This addon is independent of the R3 patient test; it does not install any
patient spawner, procedure, treatment, insurance logic, or game DLL.

CONTENT
- Two ORIGINAL equipment objects, ABCL ICP-MS and sample digestion station.
- One private ABCL Instrument Workbench using the installed original game's
  desk texture reference (no copy of vanilla pixels) and allowing ONLY
  abcl_art001_icp_ms / abcl_art001_digestion attachment tags. It never
  overrides original equipment tables or registers original analyzer tags.
- One 16x8 original RGBA atlas, two small icons, EN/ZH strings.
- No base-game/DLC content or copyrighted game textures.
- New ABCL-only functional tags; do not replace the original hematoanalyzer
  or use the original stat_lab_exam procedure tag.

ONE DISPOSABLE-SAVE PLACEMENT TEST — only after artifact approval
1. Completely quit Project Hospital.
2. Use a NEW, disposable save; keep previously accepted G1 R3 saves separate.
3. Extract the exact approved ART-001 placement-test ZIP.
4. Run INSTALL_ART001.cmd and select the directory containing ProjectHospital_Data.
5. Installer refuses an existing ModABCLArt001Test folder; never overwrite it.
6. In a fresh laboratory scene, place the new ABCL Instrument Workbench.
   Native vanilla equipment tables reject our private attachment tags; this
   first test failed there. Do not patch or move any vanilla equipment table.
7. In build mode, inspect the two new ABCL devices in lab equipment; check
   EN and ZH labels when available. Do not move original analyzers.
8. Place the two devices on separate ABCL workbenches; rotate through NW/NE/SE/SW.
9. Check draw order and clipping at table/character edges, device proportions,
   basic click/placement behavior and nearby staff walking paths.
10. Do NOT claim lab specialist interaction just because the object is placed.
    The current G1 exam intentionally uses the vanilla original equipment.
11. If an object does not load, renders blank, is unplaceable or obstructs
    walking, stop at the first failure, preserve screenshot and output_log.
12. Do NOT save a long-term game with these experimental objects. Do not remove
    this addon from a save that has already referenced its objects.

R3 CLINICAL TEST: already owner-reported L4 PASS on a separately compiled
artifact. Never repeat the R3 ambulance/patient/lab/chelation path for this
standalone artwork placement check. No Workshop or all-DLC claim.
