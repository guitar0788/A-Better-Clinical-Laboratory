ABCL ART-001 EQUIPMENT PLACEMENT TEST — NO CLINICAL WORKFLOW
==============================================================

STATUS: test-only addon candidate. Not Alpha. Do not install until its
exact-source GitHub Actions artifact has passed source/package audit.
This addon is independent of the R3 patient test; it does not install any
patient spawner, procedure, treatment, insurance logic, or game DLL.

CONTENT
- Two ORIGINAL equipment objects, ABCL ICP-MS and sample digestion station.
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
6. In a fresh laboratory scene, place a standard vanilla lab equipment table.
7. In build mode, inspect the two new ABCL devices in lab equipment; check
   EN and ZH labels when available. Do not move original analyzers.
8. Place both objects on tables; rotate each through NW/NE/SE/SW.
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
