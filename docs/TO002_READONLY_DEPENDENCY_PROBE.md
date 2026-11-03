# TO-002 — native Dependency tree read-only L4 probe (test-only)

**Status:** Source-only TS draft. Not a rendered Toxicology Laboratory node. No L3 or L4.

## Why this exists
Original game's `DependencyTreePanelController` exposes only a close button; it does not construct graph nodes through a normal GameDB room-type registry. The on-screen diagram is most likely part of a serialized Unity UI hierarchy. An additive ABCL room entry **does not** automatically inject into that graph. Current source lacks evidence for a safe external node-registration API.

## Bounded, nonintrusive inspection
`ABCLTO002ReadOnlyTreeProbe` runs only in the main hospital scene. Every 2 seconds until the native `DependencyTreePanelController` is actually visible, it does one read-only lookup. At first visible opening in a session it records **at most 180 transforms / 24,000 characters** (names, relative UI positions, bounds, optional local text and Sprite names) in one ordinary game log message starting `[ABCL TO-002 TREE STRUCTURE — READ ONLY / TEST ONLY]`. It then never scans again in that session. No Unity inspector or new player-installed plugin is required; it piggybacks on the existing G1 development panel test DLL. No writes, allocations of game objects, global patches, patient data, graph edits, or game/save changes.

**This does not require a separate immediate owner gameplay test.** Batch it with the next properly packaged, SHA-audited L4 round after TO-001 has its art ready, so the owner opens the relationship graph once during the same test session and can provide `output_log.txt` along with TO-001 screenshots. Do not ask the owner to repeat an entire L4 session only for this diagnostic.

## Stage gate
1. Source-only L2 guard validates one-shot bounded read-only behavior.
2. Genuine net35/CLR2 L3 against owner-authorized encrypted original DLLs; no source-only mock may be counted.
3. Package this test-only probe only in a disposable-save installation; DO NOT ship in public Alpha.
4. Inspect real logged hierarchy before proposing any node/edge. If Unity UI graph is static or an add-on registration cannot be isolated from the original tree, record a precise compatibility NO-GO; do not overwrite original serialized assets or draw fake clinical edges.
5. Only a later owner-accepted L4 could establish a genuine native graph modification.

Separate issues: #24 for room and on-floor icons; #26 for terminology. Preserve G1 clinical routes and all original/DLC/Workshop UI and saves.
