using System;
using UnityEngine;
using UnityEngine.SceneManagement;
using GLib;
using Lopital;

// R2: isolated development-only lab fixture. Never package in Alpha or release.
// A normal, mobile ER patient avoids R1's unrelated ambulance/inpatient gates.
public sealed class ModEntryPoint : HospitalMod
{
    private bool expanded;
    private Rect window = new Rect(40f, 100f, 430f, 215f);
    private string status = "Ready: verify Emergency clinic and ABCL lab before spawning.";
    private float lastSpawn = -100f;
    private bool r3SpawnAttempted;

    private bool HospitalIsReady()
    {
        return SceneManager.GetActiveScene().name == "main_scene_default"
            && Database.Instance.Loaded
            && Hospital.Instance != null
            && Hospital.Instance.GetGroundFloor() != null
            && MapScriptInterface.Instance != null;
    }

    private void OnGUI()
    {
        if (!HospitalIsReady()) return;
        float x = Mathf.Max(8f, Screen.width - 132f);
        if (GUI.Button(new Rect(x, 56f, 125f, 32f),
                       expanded ? "ABCL G1 [Close]" : "ABCL G1 [Test]"))
            expanded = !expanded;

        if (!expanded) return;
        window.height = IsNativeLeadMode() ? 350f : 215f;
        window.x = Mathf.Clamp(window.x, 4f,
                               Mathf.Max(4f, Screen.width - window.width - 4f));
        window.y = Mathf.Clamp(window.y, 4f,
                               Mathf.Max(4f, Screen.height - window.height - 4f));
        window = GUI.Window(681401, window, DrawWindow,
            IsNativeLeadMode() ? "ABCL G1 | R3 Native Lead TEST" : "ABCL G1 | R2 Lab Test ONLY");
    }

    private void DrawWindow(int id)
    {
        GUILayout.Space(7f);
        if (IsNativeLeadMode())
        {
            GUILayout.Label("R3: genuine IMOBILE lead-poisoning case TRM_LDP");
            GameDBMedicalCondition lead;
            InsuranceCompany insurer;
            string readiness;
            bool ready = CheckNativeLeadPreflight(out lead, out insurer, out readiness);
            GUILayout.Label(readiness);
            bool previousEnabled = GUI.enabled;
            GUI.enabled = previousEnabled && ready && !r3SpawnAttempted;
            if (GUILayout.Button("REQUEST ONE NATIVE LEAD PATIENT", GUILayout.Height(34f)))
                SpawnNativeLead(lead, insurer);
            GUI.enabled = previousEnabled;
            GUILayout.Label(status);
            GUILayout.Label("One attempt/session. Native ambulance arrival is NOT guaranteed.");
            GUILayout.Label("Disposable save ONLY; not for Alpha or existing saves.");
        }
        else
        {
            GUILayout.Label("Fixture: mobile Emergency clinic case DIA_CLD (not lead poisoning)");
            if (GUILayout.Button("SPAWN ONE MOBILE LAB TEST PATIENT", GUILayout.Height(34f)))
                SpawnOne();
            GUILayout.Space(5f);
            GUILayout.Label(status);
            GUILayout.Label("Disposable save ONLY. ABCL blood-lead assay is test-attached.");
        }
        GUI.DragWindow(new Rect(0f, 0f, 430f, 25f));
    }

    private bool HasAbclSampling(GameDBMedicalCondition condition)
    {
        if (condition == null || condition.Examinations == null)
            return false;
        GameDBExamination exam = Database.Instance.GetEntry<GameDBExamination>(
            "EXM_ABCL_G1_BLOOD_LEAD_SAMPLING");
        if (exam == null)
            return false;
        foreach (GameDBExamination available in condition.Examinations)
            if (available == exam) return true;
        return false;
    }

    private bool IsNativeLeadMode()
    {
        if (!HospitalIsReady()) return false;
        return HasAbclSampling(Database.Instance.GetEntry<GameDBMedicalCondition>("TRM_LDP"));
    }

    private InsuranceCompany ChooseEligibleImmobileInsurer()
    {
        if (InsuranceManager.Instance == null ||
            InsuranceManager.Instance.m_state == null ||
            InsuranceManager.Instance.m_state.m_insuranceCompanies == null)
            return null;
        foreach (InsuranceCompany company in
                 InsuranceManager.Instance.m_state.m_insuranceCompanies)
        {
            if (company != null && company.m_isContracted && !company.m_hidden &&
                company.m_immobileSpawnedToday > 0 &&
                company.m_gameDBInsuranceCompany.IsValid &&
                company.m_gameDBInsuranceCompany.Entry != null)
                return company;
        }
        return null;
    }

    // Preflight reports all blocking conditions at once. It never changes the
    // department, insurer, game database, ambulance, or any vanilla patient.
    private bool CheckNativeLeadPreflight(out GameDBMedicalCondition lead,
                                          out InsuranceCompany insurer,
                                          out string report)
    {
        lead = null;
        insurer = null;
        report = "Hospital scene or database is not ready.";
        if (!HospitalIsReady()) return false;

        lead = Database.Instance.GetEntry<GameDBMedicalCondition>("TRM_LDP");
        bool caseLinked = HasAbclSampling(lead);
        GameDBDepartment type = Database.Instance.GetEntry<GameDBDepartment>(
            "DPT_INTERNAL_MEDICINE_DEPARTMENT");
        Department department = type == null ? null :
            MapScriptInterface.Instance.GetDepartmentOfType(type);
        bool clinic = department != null && !department.IsClosed() &&
                      department.AcceptsOutpatients();
        bool ward = department != null && !department.IsClosed() &&
                    department.AcceptsInpatients();
        bool originalPool = type != null && type.DiagnosisRandomizerImmobile.Count > 0;
        bool hospitalGate = Hospital.Instance.HasAnyInpatientDepartment();
        insurer = ChooseEligibleImmobileInsurer();
        bool freeAmbulance = AmbulanceManager.Instance != null &&
            AmbulanceManager.Instance.GetFreeAmbulance(false, false) != null;

        report = "Native TRM_LDP + ABCL exam: " + (caseLinked ? "OK" : "MISSING") +
                 "\nInternal Medicine outpatient: " + (clinic ? "OK" : "NOT READY") +
                 "\nInternal Medicine inpatient: " + (ward ? "OK" : "NOT READY") +
                 "\nNative immobile diagnosis pool: " + (originalPool ? "OK" : "EMPTY") +
                 "\nNative hospital intake gate: " + (hospitalGate ? "OK" : "NOT READY") +
                 "\nContracted immobile insurer quota: " + (insurer != null ? "OK" : "ZERO") +
                 "\nParked free ambulance: " + (freeAmbulance ? "OK" : "NONE");
        return caseLinked && clinic && ward && originalPool && hospitalGate &&
               insurer != null && freeAmbulance;
    }

    private void SpawnNativeLead(GameDBMedicalCondition lead, InsuranceCompany insurer)
    {
        if (r3SpawnAttempted) return;
        // Recheck at the moment of creation; preflight GUI may be stale.
        GameDBMedicalCondition currentLead;
        InsuranceCompany currentInsurer;
        string readiness;
        if (!CheckNativeLeadPreflight(out currentLead, out currentInsurer, out readiness))
        {
            status = "R3 preflight changed; no patient created. See checks above.";
            return;
        }
        if (currentLead != lead || currentInsurer != insurer)
        {
            status = "R3 case or insurer changed; no patient created.";
            return;
        }

        r3SpawnAttempted = true; // no retry after partial native factory side effects
        try
        {
            Floor floor = Hospital.Instance.GetGroundFloor();
            Vector2i position = MapScriptInterface.Instance.GetRandomSpawnPosition();
            Entity patient = LopitalEntityFactory.CreateCharacterPatient(
                floor, position, lead, PatientMobility.IMOBILE,
                insurer.m_gameDBInsuranceCompany.Entry);
            if (patient == null)
            {
                status = "R3 native factory returned null. Do not retry in this save.";
                return;
            }
            BehaviorPatient behavior = patient.GetComponent<BehaviorPatient>();
            if (behavior == null || behavior.m_state.m_medicalCondition == null)
            {
                status = "R3 native medical condition missing. Do not retry.";
                Debug.LogError("[ABCL G1 R3] Native factory did not supply a condition.");
                return;
            }
            floor.AddCharacter(patient);
            status = "R3 patient CREATED, pending native ambulance reservation/arrival.";
            Debug.Log("[ABCL G1 R3] Created one original TRM_LDP IMOBILE patient; arrival not confirmed.");
        }
        catch (Exception error)
        {
            status = "R3 native creation failed; do not retry. Check game log.";
            Debug.LogError("[ABCL G1 R3] Native lead creation failed: " + error);
        }
    }

    private InsuranceCompany ChooseEligibleOutpatientInsurer()
    {
        if (InsuranceManager.Instance == null ||
            InsuranceManager.Instance.m_state == null ||
            InsuranceManager.Instance.m_state.m_insuranceCompanies == null)
            return null;

        foreach (InsuranceCompany company in
                 InsuranceManager.Instance.m_state.m_insuranceCompanies)
        {
            if (company != null && company.m_isContracted && !company.m_hidden &&
                company.m_patientsSpawnedToday > 0 &&
                company.m_gameDBInsuranceCompany.IsValid &&
                company.m_gameDBInsuranceCompany.Entry != null)
                return company;
        }
        return null;
    }

    private void SpawnOne()
    {
        if (Time.realtimeSinceStartup - lastSpawn < 2f)
        {
            status = "Please wait before spawning another patient.";
            return;
        }
        lastSpawn = Time.realtimeSinceStartup;
        try
        {
            if (!HospitalIsReady())
            {
                status = "Hospital scene/database not ready.";
                return;
            }

            GameDBDepartment emergencyType =
                Database.Instance.GetEntry<GameDBDepartment>("DPT_EMERGENCY");
            Department emergency = (emergencyType == null) ? null :
                MapScriptInterface.Instance.GetDepartmentOfType(emergencyType);
            if (emergency == null || emergency.IsClosed() ||
                !emergency.AcceptsOutpatients())
            {
                status = "Need a working Emergency OUTPATIENT clinic, not hospitalization.";
                return;
            }

            GameDBMedicalCondition fixture =
                Database.Instance.GetEntry<GameDBMedicalCondition>("DIA_CLD");
            GameDBExamination abclSampling =
                Database.Instance.GetEntry<GameDBExamination>(
                    "EXM_ABCL_G1_BLOOD_LEAD_SAMPLING");
            if (fixture == null || abclSampling == null)
            {
                status = "Missing vanilla fixture diagnosis or ABCL sampling exam.";
                return;
            }

            // Local test-only DIA_CLD override must contain the ABCL exam.
            // This protects against accidentally running an incomplete package.
            bool linked = false;
            if (fixture.Examinations != null)
            {
                foreach (GameDBExamination exam in fixture.Examinations)
                {
                    if (exam == abclSampling) { linked = true; break; }
                }
            }
            if (!linked)
            {
                status = "R2 DIA_CLD test override absent. Reinstall complete R2 test package.";
                return;
            }

            InsuranceCompany insurer = ChooseEligibleOutpatientInsurer();
            if (insurer == null)
            {
                status = "Need contracted insurer with a positive WALK-IN patient quota.";
                return;
            }

            Floor floor = Hospital.Instance.GetGroundFloor();
            Vector2i position = MapScriptInterface.Instance.GetRandomSpawnPosition();
            Entity patient = LopitalEntityFactory.CreateCharacterPatient(
                floor, position, fixture, PatientMobility.MOBILE,
                insurer.m_gameDBInsuranceCompany.Entry);
            if (patient == null)
            {
                status = "Native fixture patient factory returned null.";
                return;
            }
            patient.GetComponent<BehaviorPatient>().m_state.m_fVisitTime =
                DayTime.Instance.GetDayTimeHours();
            floor.AddCharacter(patient);
            status = "One mobile test patient scheduled; observe outpatient ARRIVAL.";
            Debug.Log("[ABCL G1 R2] Scheduled one DIA_CLD walk-in fixture; no lead severity/ambulance changes.");
        }
        catch (Exception error)
        {
            status = "R2 spawn failed; inspect the game's runtime log.";
            Debug.LogError("[ABCL G1 R2] Spawn failed: " + error);
        }
    }
}
