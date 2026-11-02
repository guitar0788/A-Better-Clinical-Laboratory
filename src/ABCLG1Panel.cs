using System;
using UnityEngine;
using UnityEngine.SceneManagement;
using GLib;
using Lopital;

// Strictly test-only; not permitted in an Alpha or public release package.
public sealed class ModEntryPoint : HospitalMod
{
    private bool expanded;
    private Rect window = new Rect(40f, 100f, 405f, 220f);
    private string status = "Ready: one patient per click.";
    private float lastSpawn = -100f;

    private bool HospitalIsReady()
    {
        if (SceneManager.GetActiveScene().name != "main_scene_default")
            return false;
        if (!Database.Instance.Loaded)
            return false;
        if (Hospital.Instance == null || Hospital.Instance.GetGroundFloor() == null)
            return false;
        return MapScriptInterface.Instance != null;
    }

    private void OnGUI()
    {
        if (!HospitalIsReady()) return;

        float x = Mathf.Max(8f, Screen.width - 132f);
        if (GUI.Button(new Rect(x, 56f, 125f, 32f), expanded ? "ABCL G1 [Close]" : "ABCL G1 [Test]"))
            expanded = !expanded;

        if (expanded)
        {
            window.x = Mathf.Clamp(window.x, 4f, Mathf.Max(4f, Screen.width - window.width - 4f));
            window.y = Mathf.Clamp(window.y, 4f, Mathf.Max(4f, Screen.height - window.height - 4f));
            window = GUI.Window(681401, window, DrawWindow, "ABCL G1 | Test only");
        }
    }

    private void DrawWindow(int id)
    {
        GUILayout.Space(7f);
        GUILayout.Label("Spawn one immobile lead poisoning patient (TRM_LDP)");
        if (GUILayout.Button("SPAWN 1 LEAD POISONING PATIENT", GUILayout.Height(34f)))
            SpawnOne();
        GUILayout.Space(5f);
        GUILayout.Label(status);
        GUILayout.Label("Native ambulance admission required. Test save only.");
        GUI.DragWindow(new Rect(0f, 0f, 405f, 25f));
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
                status = "Hospital not ready.";
                return;
            }
            GameDBMedicalCondition lead = Database.Instance.GetEntry<GameDBMedicalCondition>("TRM_LDP");
            if (lead == null)
            {
                status = "TRM_LDP missing from the game database.";
                Debug.LogError("[ABCL G1] TRM_LDP medical condition not found.");
                return;
            }
            // TRM_LDP always has SYM_LEAD_LEVELS_HIGH, whose vanilla
            // PatientMobility is IMOBILE. A mobile walk-in bypasses the
            // native ambulance and insurer eligibility path and can
            // disappear on the following BehaviorPatient state update.
            if (!Hospital.Instance.HasAnyInpatientDepartment() ||
                Hospital.Instance.GetRandomDepartmentWithDiagnoses(PatientMobility.IMOBILE) == null)
            {
                status = "Need an operational inpatient department for immobile patients.";
                return;
            }
            if (AmbulanceManager.Instance.GetAmbulanceCount() < 1)
            {
                status = "Need at least one ambulance for an immobile lead patient.";
                return;
            }
            InsuranceCompany insurer = InsuranceManager.Instance.GetRandomImmobileCompany();
            if (insurer == null || !insurer.m_isContracted ||
                insurer.m_immobileSpawnedToday <= 0)
            {
                status = "No contracted insurer with an immobile patient slot. Check inpatient services / next day.";
                return;
            }
            Floor floor = Hospital.Instance.GetGroundFloor();
            Vector2i position = MapScriptInterface.Instance.GetRandomSpawnPosition();
            Entity patient = LopitalEntityFactory.CreateCharacterPatient(
                floor, position, lead, PatientMobility.IMOBILE,
                insurer.m_gameDBInsuranceCompany.Entry);
            if (patient == null)
            {
                status = "Native patient factory returned null.";
                Debug.LogError("[ABCL G1] CreateCharacterPatient returned null.");
                return;
            }
            patient.GetComponent<BehaviorPatient>().m_state.m_fVisitTime =
                DayTime.Instance.GetDayTimeHours();
            floor.AddCharacter(patient);
            status = "Lead patient queued for native ambulance arrival. Check vehicles.";
            Debug.Log("[ABCL G1] TRM_LDP patient queued via native immobile / ambulance pathway.");
        }
        catch (Exception error)
        {
            status = "Spawn failed. Check output_log.txt.";
            Debug.LogError("[ABCL G1] Spawn failed: " + error);
        }
    }
}
