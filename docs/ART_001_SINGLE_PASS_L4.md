# ART-001 art-only placement L4 — single-pass owner checklist

**Gate:** original-device PNG/XML/native-loader source review and exact-SHA
art-only package audit PASS. *Runtime placement, staff route and animation
remain NOT TESTED.* This checklist does not claim clinical laboratory or
case testing.

## Immutable test package

- Source candidate: `1fa723d336f95b27762a202a34aab9c64d003504`.
- [ART-001 placement package run](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41408148144),
  artifact `13124027790`, name `ABCL-ART001-PLACEMENT-TESTONLY`.
- The outer Actions artifact ZIP contains one inner file:
  `ABCL-ART001-Placement-TestOnly.zip` (13,517 bytes).
- Outer artifact SHA256:
  `c634eac32d86ca6023af26197ba57e019e927b46ce911f6482b05b5e17980cbf`.
- Inner install ZIP SHA256:
  `f39086a685c2ca557cec32e1538d874b4661792a5f68d3f7f8af7ee887b0196a`.
- The package contains exactly 12 explicitly allowlisted ABCL source and
  installer files: one additive ModABCLArt001Test directory holding four
  original-art XML resources + ModAddon.xml + 3 original PNGs; installer PS1,
  CMD, README and BUILD_INFO. No game/DLC DLL, AES key, Harmony, original
  sprites, G1 procedure code or debug patient-spawn panel.
- The BUILD_INFO file confirms the source SHA and atlas SHA256
  `fa0b2e0bea72ab71b94d2752599bfc66fb642c0a64b748ca358ba9a2479e9249`.

## Preparation

- [ ] Completely quit Project Hospital; keep the verified R3 test build,
      original lab and any historical R3 saves unchanged.
- [ ] Use a **new disposable save**; do not open existing hospitals with the
      experimental objects installed or later remove it from a save that uses them.
- [ ] Confirm `StreamingAssets/Addons/ModABCLArt001Test` does **not** already
      exist. The installer will refuse to overwrite.
- [ ] Extract the **inner** exact test ZIP. Run `INSTALL_ART001.cmd`; enter
      the actual game root containing `ProjectHospital_Data`. This installs
      only `ModABCLArt001Test`, separate from `ModABCLG1LeadTest`.

## One game session — stop on first failure

- [ ] Project Hospital opens normally and the game reaches the main menu.
- [ ] New disposable hospital opens; ABCL G1 R3 and vanilla labs remain
      unaffected (do not regenerate any lead patient).
- [ ] In the lab build menu, find **ABCL Mass Spectrometer** and
      **ABCL Sample Digestion Station** using `ui_lab_equipment`.
- [ ] Both EN/ZH names appear correctly where that language is selected.
- [ ] Place one native equipment table and then both ART-001 devices
      in the ABCL lab without relocating existing original analyzers.
- [ ] Preview each of the two objects in NW/NE/SE/SW orientations, noting
      clipping, transparency, visible face, proportions and desk attachment.
- [ ] Objects can be selected/moved through the vanilla object controls.
- [ ] Nearby lab staff can walk around these placed objects. **This is not**
      evidence that a worker can execute a procedure on the new objects.
- [ ] Vanilla hematology analyzer and CBC are still available. The G1
      patient/ambulance/blood-lead sequence is **already accepted**, do not
      repeat it for art-only placement.

If a step fails, stop and preserve one screen/photo of the failure,
the exact on-screen error, and a matching game log. Do not install multiple
replacement packages in the same session.

## Explicitly outside this test

These objects are not yet connected to `EXM_ABCL_G1_BLOOD_LEAD_TESTING`.
Therefore the following are **NOT TESTED**: lab specialists using either
ABCL object for a procedure; every animation/contact frame; clinical
result production on original equipment; DLC or third-party Workshop
coexistence; long-term save/uninstall migration. No automatic release,
merging or game-internal manipulation is authorized by a green CI result.

Keep Issue #3 open, PR #14 Draft. The next gate is native procedure routing
with **isolated equipment tags**, followed by a bounded staff interaction
L4 session. Avoid retesting R3 patient generation and chelation solely to
exercise new art.
