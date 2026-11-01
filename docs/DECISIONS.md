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

## Pending decisions

- Exact legal and private L3 build runner/reference provisioning, including original assembly version and SHA.
- Actual kickoff date and Alpha 0.1 deadline.
- Specific vanilla/DLC/Workshop combinations claimed supported.
- Long-term release license (no license is presumed by this repository).
