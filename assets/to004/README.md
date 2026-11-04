# TO-004 — Toxicology Laboratory prefab room candidates

**DRAFT / L2 SOURCE-ONLY PASS / OWNER L4 NOT RUN.** See [Issue #30](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/30) and [Draft PR #31](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/31). This branch is separate from TS G1 and FA ART-001.

## Owner-supplied original room files

| Variant | Saved original | Indoor size | Saved outer m_size | Original SHA256 |
| --- | --- | --- | --- | --- |
| Small | `Toxicology Laboratory Map8x6.xml` | 8×6 | 10×7 | `1477eb5580e1002c33384f84aaa708dfbe2fb19b09ea01dcd330309295d61457` |
| Large | `Toxicology Laboratory Map12x6.xml` | 12×6 | 13×7 | `4454abe727234fd8f8e6a70bcfff2f58860f05dbf3f8351b99951d7725bbad8d` |

The original owner-authored XML files are preserved **byte-for-byte** in `Prefabs/`. They reference `ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB` from the G1 development addon, and use only native lab instruments (the new ART-001 instruments are **not** embedded). Do not normalize `m_size` or overwrite vanilla prefabs.

## Included native-prefab registration

- `Database/`: additive `PREFAB` and `TEXTURE_CUSTOM_PREFAB_SPRITE` assets, two `GameDBPrefabObject` records, EN / Simplified Chinese strings.
- `Prefabs/`: original small and large room XML.
- `Assets/ABCL/Prefabs/`: **both final 104×104 RGBA PNG icon assets committed**.
- `art_sources/`: **both self-contained screenshot-backed SVG sources with editable vector crop masks** and `manifest.json` containing the exact source/PNG/SVG SHA256 hashes.
- `tools/render_to004_prefabs.py`: rebuilds PNGs from the captured game screenshot layers embedded in the editable SVGs (no generated equipment) (requires Pillow and CairoSVG for developers only).
- `tests/test_to004_prefabs.py`: six offline structural and resource tests.

The earlier illustrated previews were rejected in L4. V3 thumbnails are manually masked from **owner-supplied in-game screenshots** `37.png` (8×6) and `38.png` (12×6), NOT AI-generated illustrations. The SVGs embed the photographed room as a single movable layer and editable polygon clipping mask; individual screenshot fixtures are not editable vector objects. No original game atlas sprites or DLLs are included. Native prefab entries use the existing `ui_prefab_lab` category and provisional small/large costs of 25,000 / 30,000 matching hematology price brackets, subject to owner testing.

## Reproduce and verify

From this directory, with Python, Pillow and CairoSVG installed:

```sh
python -m unittest discover -s tests -v
python tools/render_to004_prefabs.py
python -m unittest discover -s tests -v
```

The screenshot-backed SVGs embed the exact native PNG bytes in non-rendered metadata for hash-verified integration. The 104×104 outputs reproduce from the sources in the authoring environment; CI validates PNG SHA256 and owner-room XML byte preservation. Owner visual and actual game L4 remain pending. GitHub CI, actual game loader behavior and in-game artwork acceptance remain separate gates.

## G1 packaging dependency

`assets/to004/` is the *addon-root overlay*, not a standalone installable Mod. To package a new G1 test candidate, copy only its **`Database/`, `Prefabs/`, and `Assets/` contents** into the **existing** G1 addon staging root, while retaining the original G1 toxicology room definition. Do not copy `art_sources/`, `tests/` or `tools/` into a release. Do not replace original `StreamingAssets/Database/` entries or disturb the TS/FA feature branches.

A green static test does not prove runtime. With an explicitly SHA-matched disposable test package, focus L4 on room menu, two distinct thumbnails, small/large placement, rotation, doors/walls, room readiness, worker access, original lab regression, save/reload and each declared DLC/Workshop combination. No repeat of the accepted full G1 patient workflow solely for prefab artwork.

**Do not merge or release this PR until its current exact-head CI and owner in-game L4/visual approval are available.** No original game DLLs, pixels, encryption references or secrets are included.

## Vanilla-consistent prefab display names (owner instruction)
Original vanilla English strings in `StringTableEnPatch_1_1.xml` use `Hematology Lab - 8 x 6` and `Hematology Lab - 12 x 6`. Therefore player-facing names are `Toxicology Lab - 8 x 6` and `Toxicology Lab - 12 x 6`, with Chinese `临床毒理实验室 - 8 x 6` / `临床毒理实验室 - 12 x 6`. No `(small)`, `(large)`, `（小型）` or `（大型）` is appended. Internal namespaced SMALL/LARGE IDs are unchanged.

## Screenshot provenance and distribution
The source SVGs embed a JPEG-sampled owner-provided game screenshot and an editable cutout polygon, plus an exact PNG data block for verified binary reconstruction. `37.png` source SHA256 `531b9b65e6e40e34ac2696bf0154e3c33d76dc8620c4ae0d31578370cb998912`; `38.png` source SHA256 `51815e0af3c52980e5a5cf6f637029c7e2f022e95ac29081853c3b3872c791bd`. The original full screenshots and private vanilla-reference comparison are not committed. The only runtime artwork added is two 104×104 PNG thumbnails. No room layout, furniture, doors, G1 logic, game database or other-mod entries changed.
