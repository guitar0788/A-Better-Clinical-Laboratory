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

| ABCL-D011 | 2026-11-02 | Test-only engineering re-scope; NOT an Alpha approval | Under D009, retire R1's severe TRM_LDP/ambulance patient generator as the primary G1 laboratory test harness. Draft an isolated R2 walk-in test fixture based on original Emergency clinic-only `DIA_CLD`, with the G1 sampling exam attached in a locally derived, disposable-save-only override. Preserve vanilla disease definitions on disk and all original CBC routing. The real TRM_LDP severity/hospitalization remains untouched and a separate future L4 gate. | Decouple lab workflow acceptance from Internal Medicine inpatient/ambulance/insurance immobile quotas. This changes test delivery only, does NOT prove the independent lab result, does NOT authorize release or promise unsupported Workshop combinations. No owner gameplay test until the full fixture, routing, L3 compilation and package audit are ready. |

## Pending decisions

- Exact legal and private L3 build runner/reference provisioning, including original assembly version and SHA.
- Actual kickoff date and Alpha 0.1 deadline.
- Specific vanilla/DLC/Workshop combinations claimed supported.
- Long-term release license (no license is presumed by this repository).
