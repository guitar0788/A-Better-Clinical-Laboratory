# G1 single-pass L4 protocol — research and hold gate

**Date:** 2026-11-02  
**Related:** Issue #2, draft PR #7, ABCL-D003/005/006/008/009/010.  
**Status:** **HOLD on further user gameplay retries of the current R1 spawn-panel path.** This is a research/test plan, not evidence of successful G1 gameplay and not approval to merge.

## Why the current R1 is blocked

On compiled R1 candidate `ea1a9ecb76484b9f86e5cc54dcf659f5548b3160` (genuine Windows/net35 build Actions `41369385877`, PASS), the owner observed:

- Game and G1 panel load; base CBC works (user-reported).
- Pressing the patient-spawn button displays `Need an operational inpatient department for immobile patients.`.
- **No factory call or ambulance reservation occurred** on that click, because the C# guard returns before checking the ambulance and insurer. Treat "no ambulance arrival" as **not reached**, not an ambulance AI failure.
- Blood-lead sample/test/result and save/reload remain **untested**.

The current guard is:
```csharp
!Hospital.Instance.HasAnyInpatientDepartment() ||
Hospital.Instance.GetRandomDepartmentWithDiagnoses(PatientMobility.IMOBILE) == null
```

Inspected original ILSpy `Lopital/Hospital.cs`, `Lopital/Department.cs`, `Lopital/InsuranceCompany.cs`, `Lopital/AmbulanceManager.cs`, `Lopital/BehaviorPatient.cs`, `GameDBDepartment.cs`, and supplied `StreamingAssets` XML. These are source-grounded observations, **not** a claim of verified L4 behavior:

1. `HasAnyInpatientDepartment` misleadingly requires a department with a nonempty immobile diagnosis pool **and valid outpatient intake**. `GetRandomDepartmentWithDiagnoses(IMOBILE)` separately requires an open, valid **inpatient** department with such a pool. Both expressions must pass, but the current panel combines them into one message.
2. Original base diagnosis counts: Emergency `DPT_EMERGENCY`: 30 conditions, **0 immobile**; Internal Medicine `DPT_INTERNAL_MEDICINE_DEPARTMENT`: 69 conditions, **15 immobile**. `TRM_LDP` belongs to Internal Medicine. An Emergency hospitalization alone cannot clear this guard for the supplied vanilla dataset.
3. `TRM_LDP` has `SYM_LEAD_LEVELS_HIGH` at 100% probability, `IMOBILE`, `Hazard=High`, collapse window **6–12 game hours**, and `TRT_HOSPITALIZATION_HIGH_PRIORITY`. The patient is therefore **not** a simple walk-in and must have clinical follow-through.
4. Internal Medicine must have both a functioning outpatient office/waiting room/day doctor and valid inpatient office/on-call room/nurses' station/inpatient ward/high-priority ward, with day/night inpatient doctor and nurse, and a stretcher. Actual room validity, staff home room, department open/closed state and possible DLC changes must be checked in game.
5. `AmbulanceManager.GetAmbulanceCount()` counts owned ambulances, while actual dispatch uses `GetFreeAmbulance()`: **PARKED**, not stopped, no patient assigned, below daily-call cap. Insurance's `m_immobileSpawnedToday` may be 0 while its daily counts await recalculation after clinical departments become eligible. These have not yet been reached in the owner's attempt.
6. **Additional static lab-availability risk requiring developer analysis before another L4 attempt:** `ProcedureComponent.UpdateAllExaminationsForMedicalCondition` uses `department.GetDepartmentType().CanHaveAnyRoom(item.LabTestingExaminationRef.Entry.Procedure.RequiredRoomTags)` for a linked sample/test. Internal Medicine's original allowed room types do **not** contain G1's `abcl_g1_toxicology_lab` tag, whereas that tag is present only on the optional room registered to `DPT_LAB`. The method can report `NOT_AVAILABLE_DEPARTMENT`. The vanilla CBC has related cross-department tags and the owner reports CBC PASS, so **do not assert the entire G1 path is impossible from this static check alone**; trace the remaining fallback/availability path with real game assets and tests before requiring a user to build an Internal Medicine wing.

## Decision: no more incremental room-guessing tests

**DO NOT** ask the owner to install another build, repeatedly click Spawn, build one room at a time, or unlock unrelated insurance/event content just to clear the next status. The historical XML-only forced-event test also depends on manual-event unlock and clinical department readiness; it is not a reliable escape.

**Preferred engineering re-scope for the test harness only (requires review, not implemented):** keep original `TRM_LDP` and all its vanilla severity/mobility intact; stage the independent laboratory sample/test first with an **ABCL-namespaced, benign, walk-in, test-only clinical fixture**, using vanilla patient/exam and lab AI, no Harmony/global random pool modification. Verify actual samples, labor, results and CBC before separately validating the original severe `TRM_LDP` admission scenario. Remove test-only fixture and spawn controls from Alpha. This changes the G1 *test mechanism*, not the frozen Alpha product boundary; record any implementation change and respect the ABCL-D009 stop/re-scope decision.

## One-pass user execution gate (only after offline review declares GO)

Before sending the owner to the game, the engineer must independently provide **one** immutable, genuinely compiled and inspected test candidate and one validated preflight:

- [ ] No unpublished original-game assets, decrypted DLLs, key or arbitrary tokens in source/artifact; loader/entry point and encrypted-reference build verified.
- [ ] Test fixture's clinical severity/department routing is deterministic and does **not** require the owner to unlock Internal Medicine hospitalization if only the laboratory chain is under test.
- [ ] The complete clinic-room and lab-room metadata, namespaced exam links, laboratory specialist selection, equipment tags, `CanHaveAnyRoom` and fallback routing are traced in original code. Cross-department G1 tag risk above is resolved or explicitly marked NO-GO.
- [ ] Build is L3 PASS for exact current source SHA; artifact package contents and `BUILD_INFO.txt` SHA match; source-only `Verify` is not accepted as L3.
- [ ] One-page requirements list is fixed **before** the user test: a disposable hospital, an operating original lab (waiting room + hematology + staff), an operating ABCL lab with its required equipment + staff, clinical receiving rooms/staff appropriate to the test fixture; no conflicting old G0/G1 probes or unnecessary Workshop mods.
- [ ] The one-click panel displays **separate**, read-only preflight reasons; it must not report `queued` unless creation actually passed. Capture screenshot/status and relevant logs from that one run.
- [ ] Test sequentially in the **same disposable session**, stopping immediately on the first failure: addon load, suitable patient appears, sample order offered, sample collected, ABCL lab analysis runs, result reaches physician, original CBC remains functional, save/quit/reload while addon stays installed.
- [ ] Record game build, enabled DLC/Workshop set, user-installed package SHA, patient status, screenshots/log lines and game-time elapsed; never mark a later step PASS because an earlier step compiled.

**If the owner already has a fully operational Internal Medicine and Emergency hospital, an as-is R1 diagnostic run is possible**, but still cannot be promised as a one-pass G1 clinical acceptance while the static cross-department lab tag issue and insurance timing remain unverified. It must not be presented as the preferred next step.

## Stop rule

Current R1: genuine **L3 PASS**, **L4 BLOCKED**. The ABCL-D009 one bounded patient-spawn correction was already tried. Do not make a second speculative repair under the same G1 route; document a deliberate test-harness re-scope / NO-GO decision before implementing any alternative. Keep PR #7 **Draft**, Issue #2 **Open**, no release or Alpha claim.
