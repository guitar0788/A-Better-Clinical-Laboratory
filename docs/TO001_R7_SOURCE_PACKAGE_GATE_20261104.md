# ABCL R7 provenance gate — no legacy R6 binaries

**Status (2026-11-04): source L2 and real Windows net35/CLR2 L3 confirmed, native game L4 NOT_RUN.**

### New exact source and DLL

- G1 source SHA: `a0e5330d7317acb522ed76086817171edcaf5912`, as built from the feature/g1-secure-build branch.
- Genuine GitHub Windows Actions compiler: [#41817061156](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41817061156).
- Compiled `ModABCLG1LeadTest.dll` SHA-256: `605b27bfb2ed5865217c97bb5d083a6e062a8d8d37f157e119418ac4519c5e73`.
- DO NOT repackage R6's source `aada123989f835feb38d8a7d38b1b338e14cc75f` / compiled DLL `72cf86abb5bbb539a5b364aaf314b8f36a4746ca2caab955b191de754ff602c7`. Both package builder and independent audit now reject these historical pinned values.
- Original pardeike Harmony 1.2.0.1 net35 loader: original SHA and MIT license pinned in PR #52.
- Only code changed; exact five owner-approved room/floor/prefab images, two free-standing instruments and both owner-uploaded 8×6/12×6 XML are frozen, untouched (D016).

### Observed failure and correction

The user's read-only R6 report proves the G1 DLL **loaded** and Code Mods are enabled, but the old TO-001 adapter rejected the private room icon cache before binding. R7's exact-head G1 source checks only the requested active/disabled asset, verifies the native custom icon dictionary (because `GetIcon(string)` returns a vanilla nonnull fallback on a missing key), and falls back only to a SHA-256 verified private PNG from its own G1 folder via the original Unity module. Native floor icon applies to ABCL only and produces explicit logs for early-return gates; foreign material overrides stop without globally replacing original game assets. Never edit approved art to mask this.

### Gates

This record documents genuine L3, not game appearance. R5 and R6 retain L4 FAIL. R7 requires a single focused L4 with exact package source match; report room list red, floor isometric preview, G1 code loading and the `[ABCL TO-001]` logs. If failure persists, do not make blind speculative art edits or require multiple repeated tests. The package and code should remain Draft/test-only, no auto release, no modifications to other mods, DLC or existing saves.
