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
- `art_sources/`: **both editable SVG illustrations** and `manifest.json` containing the exact source/PNG/SVG SHA256 hashes.
- `tools/render_to004_prefabs.py`: reproducibly renders the SVGs and thumbnail PNGs from the owner room XML (requires Pillow and CairoSVG for developers only).
- `tests/test_to004_prefabs.py`: six offline structural and resource tests.

These custom previews are original **isometric room illustrations**, NOT native in-game screenshots or copied vanilla art. Native prefab entries use the existing `ui_prefab_lab` category and provisional small/large costs of 25,000 / 30,000 matching hematology price brackets, subject to owner testing.

## Reproduce and verify

From this directory, with Python, Pillow and CairoSVG installed:

```sh
python -m unittest discover -s tests -v
python tools/render_to004_prefabs.py
python -m unittest discover -s tests -v
```

The generator was verified offline against the committed candidate: the two PNGs and two SVGs reproduce exactly; all six static checks pass. GitHub CI, actual game loader behavior and in-game artwork acceptance remain separate gates.

## G1 packaging dependency

`assets/to004/` is the *addon-root overlay*, not a standalone installable Mod. To package a new G1 test candidate, copy only its **`Database/`, `Prefabs/`, and `Assets/` contents** into the **existing** G1 addon staging root, while retaining the original G1 toxicology room definition. Do not copy `art_sources/`, `tests/` or `tools/` into a release. Do not replace original `StreamingAssets/Database/` entries or disturb the TS/FA feature branches.

A green static test does not prove runtime. With an explicitly SHA-matched disposable test package, focus L4 on room menu, two distinct thumbnails, small/large placement, rotation, doors/walls, room readiness, worker access, original lab regression, save/reload and each declared DLC/Workshop combination. No repeat of the accepted full G1 patient workflow solely for prefab artwork.

**Do not merge or release this PR until its current exact-head CI and owner in-game L4/visual approval are available.** No original game DLLs, pixels, encryption references or secrets are included.
