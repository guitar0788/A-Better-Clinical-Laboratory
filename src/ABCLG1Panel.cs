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
        window.x = Mathf.Clamp(window.x, 4f,
                               Mathf.Max(4f, Screen.width - window.width - 4f));
        window.y = Mathf.Clamp(window.y, 4f,
                               Mathf.Max(4f, Screen.height - window.height - 4f));
        window = GUI.Window(681401, window, DrawWindow, "ABCL G1 | R2 Lab Test ONLY");
    }

    private void DrawWindow(int id)
    {
        GUILayout.Space(7f);
        GUILayout.Label("Fixture: mobile Emergency clinic case DIA_CLD (not lead poisoning)");
        if (GUILayout.Button("SPAWN ONE MOBILE LAB TEST PATIENT",
                             GUILayout.Height(34f)))
            SpawnOne();
        GUILayout.Space(5f);
        GUILayout.Label(status);
        GUILayout.Label("Disposable save ONLY. ABCL blood-lead assay is test-attached.");
        GUI.DragWindow(new Rect(0f, 0f, 430f, 25f));
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
