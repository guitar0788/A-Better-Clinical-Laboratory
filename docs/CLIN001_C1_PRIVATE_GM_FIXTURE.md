# CLIN-001 C1 private GM fixture — RETIRED

This candidate is withdrawn following the owner's 2026-11-04 L4 failure.

The four original symptoms used by the fixture all have `IsMainSymptom=false`,
so the fixture had no main symptom. The original game diagnosis and treatment
UI expects a main symptom. The owner also reported that using the Super-GM
affected other patients. The factory call was not side-effect-free: it
registered the created patient with the selected insurer.

Do not install, merge or use the C1 disabled diagnosis or Super-GM controls.
The current G1 installer no longer injects C1 and no longer modifies the
generic `DIA_CLD` outpatient diagnosis. It supports only the original
`TRM_LDP` native R3 route.

The original branch, commits and failed test evidence are retained. This
file is a historical audit note, not an active implementation guide.
