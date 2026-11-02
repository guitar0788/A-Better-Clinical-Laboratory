# Laboratory visual and player-facing naming standard

**Scope:** ART-001 and every subsequent ABCL laboratory room, piece of
furniture, device, examination-facing label and description.
**Owner-approved:** 2026-11-02. See decision ABCL-D011.

## Non-negotiable design rules

1. **No player-visible branding.** Object names, menu labels, room labels,
   descriptions and tooltips must not expose the internal project prefix
   `ABCL`. English: `Mass Spectrometer`, `Sample Digestion Workstation`,
   `Instrument Workbench`. Chinese: `质谱分析仪`, `样本消解工作站`, `仪器工作台`.
2. **Keep internal namespaces.** Internal `OBJECT_ABCL_*`,
   `ASSET_ABCL_*`, `abcl_art001_*` identifiers must remain distinct.
   Never overwrite vanilla IDs or impersonate vanilla `hematoanalyzer`,
   `RIA`, `stat_lab_exam` or `lab_eq_small` procedure tags.
3. **Use the user's real game screenshots as visual baseline.** Subdued,
   mostly neutral/cool lab surfaces; small amounts of functional accent,
   not red/pink neon boxes; harmonized isometric illumination and modest
   contrast. Screenshots are references, not texture assets to redistribute.
4. **Tabletop proportions first.** Use the original 128×128 atlas cell and
   actual vanilla equipment-scale references, including sprite IDs 248–255 in
   `objects_small_atlas.png`. Do not use an arbitrary 65×51px limit as a
   substitute for visual measurement: original silhouettes, orientation,
   shadow and origin offsets vary. Align device baselines across NW/NE/SE/SW;
   bench top height, actual attachment elevation and collision are L4 gates.
5. **One machine, four coherent directions.** NW/NE/SE/SW must preserve the
   same parts, panel placement logic and coherent proportions while showing
   legitimate different orientations. No independent arbitrary redesign
   of each direction.
6. **Separate private attachment parent.** The `Instrument Workbench`
   uses an ABCL-only GameDBObject and attachment allowlist, references an
   existing installed game texture by ID and does not replace original lab
   equipment tables. Never introduce broad vanilla functional tags to
   artificially make it placeable.
7. **No false verification.** Source tests, generated PNG previews, and
   green GitHub Actions can prove file and atlas contracts, but cannot
   prove in-game tabletop proportions, native rotation, staff access or
   professional art-quality acceptance. ART-001's first owner L4 remains
   3 PASS / 2 FAIL / 3 BLOCKED, until a newly built source candidate
   has been tested.
8. **One focused test at a time.** Review generated preview and native
   references before one disposable-save art-only placement test. Never
   repeat the previously accepted R3 patient/ambulance/blood-lead/chelation
   test solely because a device's appearance or text changed.

## Reference-backed smooth rendering amendment — D012

The original game source materials supplied by the owner were examined
read-only. Relevant originals:

| Game resource | Atlas IDs | Purpose |
| --- | --- | --- |
| `OBJECT_HEMATOLOGY_ANALYZER` | 248–251 | Smooth-edged laboratory device with detailed front/rear housing |
| `OBJECT_RIA` | 252–255 | Lower, console-shaped benchtop machine with consistent four views |
| `OBJECT_TABLE_EQUIPMENT` | 472–475 | Native tabletop/attachment parent and visual proportions |

All rows use the original game's `StreamingAssets/Textures/objects_small_atlas.png`
with a `LAYOUT_16_X_64` 2048×8192 texture atlas and 128×128 cells.
Original game graphics are **references only** and MUST NOT be bundled in the
public repository, install packages or original-art outputs.

The former direct per-pixel block generator is **rejected** for final ART-001
artwork. The new editable SVG pipeline `tools/generate_art_001_svg.py`
rasterizes at 4× target size and downsamples with Lanczos antialiasing
to transparent 128×128 original-art sprites. The workflow is preview-only,
not an installation package. Package CI for the obsolete pixel source is
paused while ART-001 remains under visual review.

**Do not confuse three different materials:** (1) original copyrighted game
references, (2) AI-rendered concept layouts shown privately to the owner,
and (3) editable, hand-authored SVG artwork intended to become exportable
game sprites. (2) is not a reliable source for (3), and none of these proves
native placement, contact, employee interaction, or save compatibility.

## Review gates

- [ ] EN/ZH player-visible labels free of brand names.
- [ ] Eight independent sprite outputs with neutral palette, compact
      occupied-pixel bounds and stable tabletop baseline.
- [ ] Visual review against the actual user's laboratory screenshots,
      including native worktop scale and believable materials.
- [ ] Exact candidate source + artifact hashes audited, no copyrighted
      original sprites/DLLs/secrets in package.
- [ ] One L4 showing correct private-bench placement, four directions,
      proportions, occlusion and staff walkability.
- [ ] Independent proof of task routing/animation contact before claiming
      the devices perform lab procedures.

**Current disposition:** ART-001 visual/code correction in progress; do
not merge PR #14 or publish as Alpha before owner-visible L4 and subsequent
native equipment interaction tests.
