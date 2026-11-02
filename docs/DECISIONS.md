# Decision Log

Decisions are append-only records. An amended decision must reference the previous ID and explain why; do not silently rewrite history.

| ID | Date | Status | Decision | Reason / consequence |
| --- | --- | --- | --- | --- |
| ABCL-D001 | 2026-11-01 | Approved | Keep ABCL wholly separate from the archived ProjectHospital-Pediatrics repository. | No cross-repository writes or shared milestones. |
| ABCL-D002 | 2026-11-01 | Approved | Alpha 0.1 targets one clinical toxicology lab, two original devices, three sampling/testing pairs, three clinical cases and EN/ZH. | Freeze the first playable slice; the two-month planning window begins at recorded kickoff. |
| ABCL-D003 | 2026-11-01 | Approved | Reuse native adult lab AI, procedures and save infrastructure; do not rebuild patient creation, rendering or clinical AI. | Avoid Pediatrics-class engine integration risk. |
| ABCL-D004 | 2026-11-01 | Approved | Intentional, documented overrides of vanilla medical XML (including DPT_LAB) are permitted. Workshop incompatibility may be declared. | Mod author must document exact overridden IDs, precedence and the resulting incompatibilities. Do not overwrite installed game files. |
| ABCL-D005 | 2026-11-01 | Approved | Keep original CBC and core laboratories operational. No promise that removing a mod from an affected save is safe. | Explicit baseline regression and save/load gates. |
| ABCL-D006 | 2026-11-01 | Approved | L1/L2, actual net35/game-reference L3, and real game L4 are distinct. Only L4 can establish gameplay. | No fake green CI or mock proof. |
| ABCL-D007 | 2026-11-01 | Approved | Public repository, English public development documentation, PR-based protected main, short-lived task branches, no auto-merge. | Game DLLs and copyrighted original assets cannot be committed or published. |
| ABCL-D008 | 2026-11-01 | Approved | G1 blood-lead exam and test patient panel are test-only until independently compiled and gameplay-verified. | Never ship patient-spawn debug controls enabled in Alpha. |
| ABCL-D009 | 2026-11-01 | Approved | Failed core integration gets at most one evidence-backed local repair before stop/re-scope decision. | Prevent endless research loops. |

| ABCL-D010 | 2026-11-02 | Owner-approved scope change | The project owner reports permission from the game author for compiling ABCL in the public GitHub repository. Use AES-256-GCM encrypted original-game DLL references, kept separate from the decryption key held in GitHub Actions Secrets. | This permits a public-repository build without publishing plaintext original binaries; public redistribution or relicensing of game DLLs is **not inferred**. Revises the private-only build assumption in D007; all game-DLL source and L3/L4 evidence rules remain. |

| ABCL-D011 | 2026-11-02 | Owner-approved, applies to all future laboratory expansions | All player-visible rooms, furniture, equipment, descriptions and menu labels are neutral vanilla-style terminology, with **no project branding**. Internal database IDs, functional tags and addon resource names remain ABCL-namespaced for vanilla/DLC/Workshop collision safety. Original-art instruments are scaled to authentic laboratory tabletops, use subdued in-game palettes and matching isometric lighting, and must pass four-direction continuity and in-game tabletop contact before approval. A dedicated private attachment parent may be used, but may not alter vanilla tables or impersonate native equipment/procedure tags. | Supersedes the visual/name choices of the first ART-001 prototype without rewriting its historical failure report. This is a project-wide design gate for ART-001 and every future laboratory object; source/CI passing cannot substitute for player-visible visual approval or L4. |

| ABCL-D012 | 2026-11-02 | Owner-approved ART-001 art-direction amendment; applies to all laboratory additions | Do **not** treat coarse procedural pixel-block silhouettes as acceptable Project Hospital-style equipment. Use the actual vanilla `objects_small_atlas.png` specimens at IDs 248–255 (hematology analyzer and RIA) and 472–475 (equipment workbench), plus original XML layout/attachment contracts, as **read-only references** for antialiasing, lighting, surface detail, four-direction continuity, native tabletop size and baseline. Create separate original, editable artwork (vector or high-resolution raster rendered smoothly to 128×128 cells) without copying/releasing game pixels. Suspend the earlier pixel-generator installation package until owner visual approval and revised ART-only L4. | Amends D011 by rejecting the literal old 65×51px silhouette cap as an unproven game-scale requirement: real game atlas silhouettes vary significantly, with shadows and orientation affecting alpha bounds. Exact in-game fit must be proven by an ART-only placement test. Current generated concept art is **not** a native game sprite and is not evidence of L4. Preserve original owner result 3 PASS / 2 FAIL / 3 BLOCKED. |

## Pending decisions

- Execute and verify the authorized public GitHub L3 build against genuine game assemblies, recording each DLL's hash and compiler result; no presumed permission to redistribute plaintext original DLLs.
- Actual kickoff date and Alpha 0.1 deadline.
- Specific vanilla/DLC/Workshop combinations claimed supported.
- Long-term release license (no license is presumed by this repository).
