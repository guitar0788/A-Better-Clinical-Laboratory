# Owner-approved integrated-package gate — code only, 2026-11-04

This branch adds a **fail-closed** offline verifier for an ABCL test-only ZIP; it does **not** produce an installable package or modify owner-approved assets.

## Mandatory upstream inputs
- The owner's exact five PNGs from the November 4 `Assets.rar`, each SHA-256 pinned and immutable.
- The approved two 1254px machine design sources and exact 8-sprite atlas (SHA256 `b412b384...`), integrated via the **standalone** TS PR #42 XML transformation: two GameDB objects with `AttachedToObject=false` and NO workbench.
- Exact uploaded November 4 prefab 8×6/12×6 XML byte hashes, accepted two 104px preview images, and TO-001 floor private tile-376 atlas.
- A *newly* compiled G1 DLL from the exact PR #49 C# source SHA, independently verified by the Windows net35/CLR2 L3 Actions job; manifest must state `compiled_g1_source_sha`, `dll_sha256` and L4 NOT_RUN.
- All these inputs must be the same VERSION. Never mix a previous compiled G1 binary and later C# source.

## One complete failure must stop publication
This script rejects legacy R1/R2/R3 ZIPs: old attached/table-top `ModObjectsABCL.xml`, workbench icons/color definitions, wrong equipment atlas SHA, wrong/unknown prefab source, miswired icon file IDs and mismatched DLL/source proof. A ZIP file opening successfully is not proof that the game will display its contents.

Unit tests verify positive freestanding XML and rejected workbench/attachment/native-tag cases. L2 only; no Unity/game test, no original files embedded. Do not auto-merge; integrate the fail-closed gate into the *future* controlled single-build workflow only when G1 exact-source L3 exists.
