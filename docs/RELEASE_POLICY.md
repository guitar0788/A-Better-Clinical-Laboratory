# Release and Compatibility Policy

## Labels and acceptance

- **G0/G1 probe:** disposable-save investigation, never promoted to a general user release.
- **Alpha:** a complete, playable thin slice with real game evidence, explicit limitations, and a repeatable installation package.
- **Beta:** Alpha gate passed; primary work is defects, regression and compatibility.
- **Stable:** documented and reproducible release acceptance; not just successful automated CI.

An Alpha may ship with known Workshop incompatibilities. It may **not** ship with a known game-breaking failure in the vanilla base game, a nonfunctional advertised procedure, or a test-only patient-spawn feature active by default.

## Alpha 0.1 gate

A release candidate must demonstrate all of the following:

1. One ABCL toxicology lab can be built, staffed, and used in a new test save.
2. Three independent sampling/testing pairs complete and return diagnostic information; the three linked clinical cases can be treated to completion.
3. Two **original** medical devices pass four-direction visual and actual staff-interaction checks.
4. Baseline hematology, microbiology, histology and CBC still operate in supported configurations.
5. Save, quit, restart and load succeed in a new test save; document known limitations of existing saves and uninstallation.
6. Vanilla and every explicitly supported DLC combination are tested. Unsupported Workshop mods are disclosed; do not claim blanket Workshop compatibility.
7. The package contains only original/authorized assets, a supported build and complete English/Chinese localization.
8. Debug patient spawning and disposable G0/G1 overrides are excluded from production.
9. The test record identifies the game build, DLCs, exact package SHA256, steps and expected/actual outcomes.

The 60-day Alpha planning target does not waive any release gate. If a critical native integration gate fails, stop/re-scope instead of relabeling a broken build as Alpha.

## Database overrides and incompatibilities

Document each overridden vanilla ID, fields changed, original behavior preserved, dependencies and incompatibilities. Never edit files inside the user's original game installation. Prefer a removable addon. If two mods overwrite the same records, do not claim that load order makes the combination safe without actual testing.

A save containing ABCL room types or medical entries may retain references to those types. **Safe uninstallation is not presumed.** Back up saves; do not recommend opening an ABCL-dependent save after removing the mod unless a tested migration/removal procedure exists.

## Public release checklist

- Source commit and build job are linked.
- L1/L2, genuine L3 (if any compiled code is shipped), and L4 evidence are separately recorded.
- The exact artifact SHA256 is listed.
- Supported game/DLC versions, known conflicts and save caveats appear in release notes.
- No proprietary game DLLs/assemblies/assets, secrets, test spawn helpers or internal patient data in the package.
- No GitHub Action automatically publishes a public release.

Project licensing is undecided; do not infer a license or reuse policy from the public repository setting.
