# TO-001 — owner-approved native room-list icon revision (2026-11-04)

**Status:** Owner APPROVED both actual 64x64 PNGs after visual review. This
supersedes the previously frozen **room-list active and inactive source PNGs
only** under ABCL-D016; it does NOT amend the approved floor atlas, the
approved prefab preview images, the standalone equipment or the room XMLs.

| Item | New original PNG SHA-256 | Appearance |
| --- | --- | --- |
| `toxicology_room_icon.png` | `c2c6c83cb0f8c2ca49dce7184bdd4f71df1c71a20ecf0c38e05337df6a48f62b` | vanilla red RGB (201,63,61), opaque icon face |
| `toxicology_room_icon_inactive.png` | `eb37ce261299f7df2ac87c61272168f71b5faca5de1578b71a172a8d75e861eb` | vanilla gray RGB (153,153,153), opaque icon face |

These exact images were reviewed as **actual usable PNGs**, not a rendered
mockup. They preserve the existing flask shape, slightly thicken its strokes,
and add a soft antialiased shadow to the right and lower sides. The 42x45
colored central face is alpha 255; soft shadow pixels outside it legitimately
carry partial alpha. Do **not** mistakenly force outer shadow alpha=255.

The earlier D016 room-icon hashes remain historical provenance only:
active `225b2918c448b5d36d1d8582389e8952f2baf1574d0d72935017c81eab7d8199`;
inactive `50c17ea8ba8b42b28295564f594713069a31c9e48fa05f3a6b623a36851b6490`.
They must not be repackaged as the latest accepted room art.

## Exact native integration

- Package the **original PNG bytes unchanged** in G1 `Assets/ABCL/`.
- `G1ApprovedPrivateTexture` continues source SHA checking but creates the
  native Sprite directly from the full 64x64 PNG, with no RGB recoloring,
  flask extraction, artificial shadow, or source recompression.
- ABCL-only UI image rectangle cap 30 units: the 45px-high colored face at
  1.1x native hover occupies ~23.2 units, inside the original 26-unit row
  pitch. The outer shadow is semitransparent by design.
- Preserve native room filters, third-party icon override protections, and
  **ALL** existing private floor renderer code. Owner R9 floor icon L4 PASS
  remains a regression constraint and is not reworked here.
- No original icons or game DLLs are committed. No Harmony patch; no
  original/DLC/Workshop asset or save changes.

**Proof level:** source art SHA and PNG properties can be verified offline.
An exact-head Windows net35/CLR2 L3 build and separate full-package L2 audit
are still needed before a focused L4 image acceptance. This art approval
does not independently grant a merge to main or an Alpha release.
