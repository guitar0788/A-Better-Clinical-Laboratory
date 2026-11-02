# FA ART-001 V10 — correct object-space occlusion study

Status: **SOURCE-ONLY, review required; not a GameDB sprite, installable package or accepted in-game art.**

## What failed in V9

The owner identified genuine perspective/visibility errors. The prior generator appended each SVG polygon in creation order, even if physically behind a cabinet; `vent` and `status` only culled their base rectangle but leaked rear grid lines and status dots onto opposite views. The digestion hood was a disconnected open roof with no arch-front or side enclosure. Neutral vanilla white did not fix these construction defects.

## Repair in V10

- Editable 3D-origin polygons now carry an isometric camera depth key; polygons, edge lines and LEDs are ordered from far to near in SVG rather than appended by code-construction order. Four views use independent 90° rotations of one object-space design, not SVG mirroring.
- `vent` and `status` return immediately when their underlying physical face faces away. Front-only control dots are also culled. An offline self-test verifies hidden-face non-emission and front/back draw ordering.
- Digestion workstation gains closed curved enclosure: opaque rear arch face, physical side caps, front arch with inset tinted window and a continuous top arch. The interior heating rack is physically underneath the roof rather than independently placed on top of a flat plane.
- Retains owner-approved read-only vanilla HEM/RIA shell palette **#F2F2F2, #E6E6E6, #CCCCCC, #B3B3B3**. Original game geometry/pixels/DLLs are never imported.
- Generates 8 original editable SVG studies, 8 native 128×128 previews, mobile contact sheet and hash manifest. Previous V7/V8/V9 are preserved, not overwritten. This remains a separate experimental study; no G1, tag, XML, rotation/placement, staff AI, save or private workbench changes.
- Rendering uses a planar painter's algorithm, not a full mesh z-buffer. It substantially limits mistaken see-through but **visual inspection at each orientation and owner acceptance are still required**. Renderer source is not an L4 runtime proof.

No automatic merge or installable artifact. Historical ART L4 stays 3 PASS / 2 FAIL / 3 BLOCKED. Native game placement, attachment, employee contact and formal L4 belong to TS.
