# Canonical Development Plan

**Project:** A Better Clinical Laboratory (ABCL)  
**State:** pre-alpha technical integration; Alpha 0.1 not yet released  
**Target:** first playable Alpha within two calendar months *after an explicit kickoff is recorded*. The clock has not started. This is a planning ceiling, not a guarantee.  
**Authority:** this file records the current task state. `docs/DECISIONS.md` records binding decisions; `docs/TEST_EVIDENCE.md` records verified evidence. Do not remove historical decisions or overstate completion.

## Frozen Alpha 0.1 product boundary

- One optional clinical toxicology laboratory integrated into the existing laboratory department.
- Two original, interactable lab devices.
- Three independent sampling/testing pairs and three linked clinical cases.
- English and Simplified Chinese localization.
- Reuse original adult characters, laboratory staff and work queues; no new patient/rendering/clinical AI, standalone stock ledger, or numeric laboratory-result engine.
- Vanilla laboratory basics must remain usable. Unsupported Workshop combinations may be documented (including HAO).
- No proprietary game DLLs/assets in the public repository or release.

## Active task register

| ID | Work item | Status | Completion / blocker |
| --- | --- | --- | --- |
| GOV-001 | Establish governance, `Verify`, branch protection | Done | Governance PR #5 merged; GitHub Actions Verify passed; active main ruleset #26316259 requires PR and Verify, blocks deletion and force pushes; extra CodeQL gate removed |
| G0-001 | Fourth-room disposable-save CBC preflight | Evidence recorded (user report) | User reported room placement and successful lab processing; no preserved game logs/version or complete save/load evidence; not a production test |
| G1-001 | Independent blood-lead sample/test and isolated patient-spawn test panel | In Progress (L3/L4 blocked) | G1 XML/source candidate exists from prior chat; original-game DLL compilation and L4 blood-lead examination not verified |
| ART-001 | Original toxicology analyzer assets and interaction validation | In Progress / NEEDS_FIX (first owner ART-001 L4: 3 PASS, 2 FAIL, 3 BLOCKED; corrected attachment-parent candidate pending exact-source CI, package audit and L4) | Owner tested artifact `13124027790` from Actions `41408148144`, source `1fa723d336f95b27762a202a34aab9c64d003504`: game launch/menu/labels PASS; placement of two ART-001 instruments on vanilla lab equipment table FAIL; in-game four-direction rotation FAIL; scale/occlusion, staff walking, original equipment noninterference BLOCKED. No screenshot/log, game build, DLC list or precise placement status supplied. Original `Lopital.Floor.CanPlaceObject` and `GameDBObject.AcceptsAttachment` require `AttachedToObject` children to match the parent's `AttachmentSlot.AllowedTags`; original `OBJECT_TABLE_EQUIPMENT` and `OBJECT_TABLE_SQUERE` do not accept private ABCL instrument tags. Vanilla table `ForcesAttachmentOrientation=true` may additionally constrain rotation (independent cause not confirmed). To avoid poisoning vanilla `hematoanalyzer`/`lab_eq_small` tags, Draft PR #14 now stages a separate ABCL-owned `OBJECT_ABCL_ART001_WORKBENCH` using an existing installed vanilla desk texture REF, only the two ART private attachment tags, and `ForcesAttachmentOrientation=false`, leaving all original XML unchanged. Source regression tests added; this corrected version is NOT yet proven in game. Preserve initial L4 failure exactly and block staff/procedure/occlusion/compatibility claims. After CI/artifact audit, only a separate art placement/rotation test is needed; G1 R3 clinical PASS remains historical and must NOT be rerun. Keep Issue #3 open, PR #14 Draft, no merge/release. |
| ALPHA-001 | Integrated Alpha 0.1 case content and gameplay acceptance | Backlog | Depends on G1 + art; test original labs, save/load and claimed DLC support |

A G0 result is not G1 completion. A pass on XML, source scaffolding, mock tests or the CI `Verify` job is not proof of gameplay.

## Stage gates and stop rules

1. **G1 core clinical gate:** an ABCL-namespaced sampling/testing pair is offered to an eligible patient, dispatched to the new laboratory, processed by a staffed interactable instrument, exposes a diagnostic result and permits treatment. Existing CBC must still work. If no reliable native path exists after one scoped, evidence-backed correction, stop this implementation.
2. **Art gate:** original 4-direction equipment displays correctly and a lab specialist can actually operate it.
3. **Regression gate:** base game, baseline laboratories, saves/loads, and every DLC configuration explicitly declared supported are exercised. Unsupported mods and save migration modes are documented.
4. **Release gate:** an actual packaged Alpha was installed and tested. No automatic release based on green CI.

## Dependency order

GOV-001 → G1-001 → ART-001 → ALPHA-001. Research results do not silently unlock a dependent task. Maintain one active engineering bottleneck, not many parallel Issues waiting for each other.

## Update rules

Update status only when a dated evidence record supports the change; preserve why an item became Blocked, Done, or Cancelled. Any new feature must cite a recorded decision and account for the frozen Alpha scope.
