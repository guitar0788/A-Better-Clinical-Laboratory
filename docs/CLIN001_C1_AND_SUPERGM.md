# CLIN-001 C1 / Super-GM — RETIRED 2026-11-04

**Status: RETIRED / DO NOT INSTALL / DO NOT REOPEN AS A TEST ROUTE.**

The owner L4 report found that a Super-GM-created patient had no usable final
diagnosis or treatment and that other patients appeared affected. The source
audit found the C1 fixture used four original symptoms, all with
`IsMainSymptom=false`. The fixture therefore lacked the native main symptom
required by diagnosis/treatment UI paths.

The panel also called the original patient factory, which registers the new
patient with the insurer. It was not a side-effect-free preview.

The Super-GM runtime class, C1 fixture injection, C1 localization entries and
R2 generic `DIA_CLD` override have been removed from the current G1 candidate.
The installer now supports only the original native `TRM_LDP` R3 route.
Do not install an earlier artifact containing `中文超级GM` or
`DIA_ABCL_C1_GM_MILD_LEAD_EXPOSURE`.

This document and the historical commits remain for audit only. A future
test harness requires a separately reviewed private main symptom, proper
diagnosis/treatment chain, and proof that it cannot mutate other patients,
insurance quotas, or native diagnosis pools before it can be reconsidered.

No diagnosis, treatment, patient-routing or gameplay L4 pass is claimed by
this retired fixture.
