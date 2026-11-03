using System;
using System.Reflection;
using UnityEngine;
using UnityEngine.SceneManagement;
using GLib;
using Lopital;

// R2: isolated development-only lab fixture. Never package in Alpha or release.
// A normal, mobile ER patient avoids R1's unrelated ambulance/inpatient gates.
public sealed class ModEntryPoint : HospitalMod
{
    private ABCLSuperGmTestPanel superGm = new ABCLSuperGmTestPanel();
    private bool expanded;
    private Rect window = new Rect(40f, 80f, 520f, 470f);
    private string status = "Ready: verify Emergency clinic and ABCL lab before spawning.";
    private float lastSpawn = -100f;
    private bool r3SpawnAttempted;

    // Optional TO-001 room-menu appearance only; the R2/R3 clinical path is unchanged.
    private G1ToxicologyRoomIconAdapter to001RoomIcon;

    private void LateUpdate()
    {
        if (to001RoomIcon == null)
            to001RoomIcon = new G1ToxicologyRoomIconAdapter();
        to001RoomIcon.LateTick();
    }

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
        superGm.Draw(); // test-only G1 DLL; original R2/R3 controls untouched
        float x = Mathf.Max(8f, Screen.width - 132f);
        if (GUI.Button(new Rect(x, 56f, 125f, 32f),
                       expanded ? "ABCL G1 [Close]" : "ABCL G1 [Test]"))
            expanded = !expanded;

        if (!expanded) return;
        window.width = IsNativeLeadMode() ? 520f : 430f;
        window.height = IsNativeLeadMode() ? 470f : 215f;
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
            GUILayout.Label("R3: TRM_LDP native IMOBILE case; Liver TY progression");
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
        GUI.DragWindow(new Rect(0f, 0f, window.width, 25f));
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

    // Liver TY is the vanilla Chinese-localized insurer IN_COM_CCC.
    // NameLocID is stable across the base/patch database entry ID suffix.
    private InsuranceCompany FindLiverTyInsurance()
    {
        if (InsuranceManager.Instance == null ||
            InsuranceManager.Instance.m_state == null ||
            InsuranceManager.Instance.m_state.m_insuranceCompanies == null)
            return null;

        InsuranceCompany fallback = null;
        foreach (InsuranceCompany company in
                 InsuranceManager.Instance.m_state.m_insuranceCompanies)
        {
            if (company == null || company.m_hidden ||
                !company.m_gameDBInsuranceCompany.IsValid ||
                company.m_gameDBInsuranceCompany.Entry == null ||
                company.m_gameDBInsuranceCompany.Entry.Deprecated ||
                company.m_gameDBInsuranceCompany.Entry.NameLocID != "IN_COM_CCC")
                continue;

            if (company.m_isContracted) return company;
            if (fallback == null) fallback = company;
        }
        return fallback;
    }

    private bool IsInsuranceObjectivePassed(InsuranceCompany company, int objectiveIndex)
    {
        return company != null && company.m_objectivesPassed != null &&
               company.m_objectivesPassed.Count > objectiveIndex &&
               company.m_objectivesPassed[objectiveIndex];
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

        // Show the vanilla Liver TY (IN_COM_CCC) progression that normally
        // unlocks ambulances and then its IMOBILE quota. Do not mutate it.
        InsuranceCompany liverTy = FindLiverTyInsurance();
        bool liverTyContracted = liverTy != null && liverTy.m_isContracted &&
                                 !liverTy.m_hidden;
        GameDBDepartment icuType = Database.Instance.GetEntry<GameDBDepartment>("DPT_ICU");
        Department icu = icuType == null ? null :
            MapScriptInterface.Instance.GetDepartmentOfType(icuType);
        // Mirrors WORKING_HOSPITALIZATION_AT_DEPARTMENT in the vanilla objective.
        bool icuHospitalization = icu != null && icu.AcceptsInpatients();
        bool liverTyIcuObjective = IsInsuranceObjectivePassed(liverTy, 3);
        bool liverTyAmbulanceObjective = IsInsuranceObjectivePassed(liverTy, 4);
        bool ambulancesUnlocked = InsuranceManager.Instance != null &&
            InsuranceManager.Instance.m_state != null &&
            InsuranceManager.Instance.m_state.m_ambulancesUnlocked;
        int ambulanceCount = AmbulanceManager.Instance == null ? 0 :
            AmbulanceManager.Instance.GetAmbulanceCount();

        // Preserve vanilla admission semantics: any contracted company with a
        // positive live IMOBILE quota is valid; Liver TY is the documented
        // normal unlock route, not a hard-coded restriction on other insurers.
        insurer = ChooseEligibleImmobileInsurer();
        int selectedQuota = insurer == null ? 0 : insurer.m_immobileSpawnedToday;
        string selectedInsurer = insurer == null ? "NONE" :
            insurer.m_gameDBInsuranceCompany.Entry.NameLocID;
        string liverTyQuota = liverTy == null ? "NOT FOUND" :
            liverTy.m_immobileSpawnedToday.ToString() + " today / target " +
            liverTy.m_currentImmobilePatients.ToString();
        bool freeAmbulance = AmbulanceManager.Instance != null &&
            AmbulanceManager.Instance.GetFreeAmbulance(false, false) != null;

        report = "Native TRM_LDP + ABCL exam: " + (caseLinked ? "OK" : "MISSING") +
                 "\nInternal Medicine outpatient: " + (clinic ? "OK" : "NOT READY") +
                 "\nInternal Medicine inpatient: " + (ward ? "OK" : "NOT READY") +
                 "\nNative immobile diagnosis pool: " + (originalPool ? "OK" : "EMPTY") +
                 "\nNative hospital intake gate: " + (hospitalGate ? "OK" : "NOT READY") +
                 "\nLiver TY (肝泰保险) contracted: " +
                    (liverTy == null ? "NOT FOUND" : (liverTyContracted ? "OK" : "NOT CONTRACTED")) +
                 "\nLiver TY ICU hospitalization objective (#4): " +
                    (liverTy == null ? "N/A" : (liverTyIcuObjective ? "DONE" : "PENDING")) +
                 "\nICU hospitalization operational: " + (icuHospitalization ? "OK" : "NOT READY") +
                 "\nAmbulances unlocked / owned: " + (ambulancesUnlocked ? "YES" : "NO") +
                    " / " + ambulanceCount.ToString() +
                 "\nLiver TY one-ambulance objective (#5): " +
                    (liverTy == null ? "N/A" : (liverTyAmbulanceObjective ? "DONE" : "PENDING")) +
                 "\nLiver TY IMOBILE quota: " + liverTyQuota +
                 "\nEligible IMOBILE insurer: " + selectedInsurer +
                    " (today " + selectedQuota.ToString() + ")" +
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

// TO-001: optional additive UI-only adapter. Original room/access-area rendering,
// core medical definitions, insurer state and all non-ABCL room rows stay untouched.
internal sealed class G1ToxicologyRoomIconAdapter
{
    internal const string RoomId = "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB";
    internal const string ActiveId = "ASSET_ABCL_TOXICOLOGY_ROOM_ICON";
    internal const string InactiveId = "ASSET_ABCL_TOXICOLOGY_ROOM_ICON_INACTIVE";

    // Original BuildingModeButtonController has no public item ID accessor.
    // Never guess by localized text or atlas icon 850 (shared with vanilla labs).
    private static readonly FieldInfo RoomButtonItemId =
        typeof(BuildingModeButtonController).GetField(
            "m_itemDatabaseID", BindingFlags.Instance | BindingFlags.NonPublic);
    private static readonly FieldInfo RoomButtonItemType =
        typeof(BuildingModeButtonController).GetField(
            "m_itemType", BindingFlags.Instance | BindingFlags.NonPublic);

    private DepartmentManagementLogisticsHybridController hybridPanel;
    private SegmentItemIconTextTextIconController targetSegment;
    private UnityEngine.Component cachedSegmentImage;
    private PropertyInfo cachedSpriteProperty;
    private RoomItemController targetRoomItem;
    private GameDBRoomType targetRoom;
    private float nextProbe;
    private bool faulted;
    private bool missingContractLogged;

    internal void LateTick()
    {
        if (faulted) return;
        try { Tick(); }
        catch (Exception ex)
        {
            // UI-only compatibility boundary: one bounded warning, then stop.
            faulted = true;
            Debug.LogWarning("[ABCL TO-001] Room-icon adapter disabled without altering native room data: " + ex);
        }
    }

    private void Tick()
    {
        if (SceneManager.GetActiveScene().name != "main_scene_default" ||
            Database.Instance == null || !Database.Instance.Loaded ||
            StreamingAssetManager.GetInstance() == null ||
            !StreamingAssetManager.GetInstance().IsReady() ||
            IconManager.Instance == null || !IconManager.Instance.m_initialized)
        {
            targetSegment = null;
            targetRoomItem = null;
            hybridPanel = null;
            targetRoom = null;
            return;
        }

        // Never call IconManager.GetIcon(string) for unregistered/unloaded assets;
        // its normal missing-icon fallback is not acceptable as an ABCL icon.
        if (Database.Instance.GetEntry<GameDBAsset>(ActiveId) == null ||
            Database.Instance.GetEntry<GameDBAsset>(InactiveId) == null ||
            StreamingAssetManager.GetInstance().GetTextureAsset(ActiveId) == null ||
            StreamingAssetManager.GetInstance().GetTextureAsset(InactiveId) == null)
        {
            if (!missingContractLogged)
            {
                Debug.LogWarning("[ABCL TO-001] Optional private room icons unavailable; preserving native IconIndex fallback.");
                missingContractLogged = true;
            }
            return;
        }
        if (targetRoom == null)
            targetRoom = Database.Instance.GetEntry<GameDBRoomType>(RoomId);
        if (targetRoom == null) return;

        // Original DepartmentManagementLogisticsHybridController.UpdateRoomButtons
        // writes the integer icon *every Update*. Apply at LateUpdate so the
        // icon is not immediately reset. Only one cached Image is changed.
        if (!targetSegment || !targetSegment.gameObject.activeInHierarchy)
        {
            targetSegment = null;
            cachedSegmentImage = null;
            cachedSpriteProperty = null;
        }
        if (!targetRoomItem || !targetRoomItem.gameObject.activeInHierarchy)
            targetRoomItem = null;
        if (Time.unscaledTime >= nextProbe)
        {
            nextProbe = Time.unscaledTime + 0.75f;
            if (!targetSegment) FindHybridRoomRow();
            if (!targetRoomItem) FindLegacyRoomRow();
        }

        bool locked = InsuranceManager.Instance != null &&
            InsuranceManager.Instance.IsRoomLocked(targetRoom);
        string assetId = locked ? InactiveId : ActiveId;
        Sprite sprite = IconManager.Instance.GetIcon(assetId);
        if (sprite == null) return;

        if (targetSegment && targetSegment.m_icon)
        {
            // The approved L3 refs intentionally omit UnityEngine.UI.dll.
            // Cache one native Image component/property for this exact ABCL
            // room row, instead of repeating GetProperty() every frame.
            if (!cachedSegmentImage ||
                cachedSegmentImage.gameObject != targetSegment.m_icon)
            {
                cachedSegmentImage = targetSegment.m_icon.GetComponent("Image");
                cachedSpriteProperty = cachedSegmentImage == null ? null :
                    cachedSegmentImage.GetType().GetProperty("sprite",
                        BindingFlags.Instance | BindingFlags.Public);
            }
            if (cachedSegmentImage && cachedSpriteProperty != null &&
                cachedSpriteProperty.CanRead && cachedSpriteProperty.CanWrite &&
                cachedSpriteProperty.PropertyType == typeof(Sprite) &&
                (cachedSpriteProperty.GetValue(cachedSegmentImage, null) as Sprite) != sprite)
            {
                // Never change native Image.color, room-area or access colors.
                cachedSpriteProperty.SetValue(cachedSegmentImage, sprite, null);
            }
        }
        if (targetRoomItem && targetRoomItem.m_icon)
        {
            IconController icon = targetRoomItem.m_icon.GetComponent<IconController>();
            if (icon != null && icon.m_customIconAssetID != assetId)
                icon.SetIcon(assetId);
        }
    }

    private void FindHybridRoomRow()
    {
        if (RoomButtonItemId == null || RoomButtonItemType == null) return;
        if (!hybridPanel)
            hybridPanel = UnityEngine.Object.FindObjectOfType<DepartmentManagementLogisticsHybridController>();
        if (!hybridPanel || !hybridPanel.gameObject.activeInHierarchy) return;
        GameObject[] panels = {
            hybridPanel.m_roomPanelClinic,
            hybridPanel.m_roomPanelClinicShared,
            hybridPanel.m_roomPanelHospitalization,
            hybridPanel.m_roomPanelHospitalizationShared
        };
        foreach (GameObject panel in panels)
        {
            if (!panel || !panel.activeInHierarchy) continue;
            SegmentItemIconTextTextIconController[] rows =
                panel.GetComponentsInChildren<SegmentItemIconTextTextIconController>();
            foreach (SegmentItemIconTextTextIconController row in rows)
            {
                BuildingModeButtonController button =
                    row.GetComponentInChildren<BuildingModeButtonController>();
                if (button == null) continue;
                string id = RoomButtonItemId.GetValue(button) as string;
                object kind = RoomButtonItemType.GetValue(button);
                if (id == RoomId && kind != null &&
                    (BuildingModeItemType)kind == BuildingModeItemType.ROOM)
                {
                    targetSegment = row;
                    return;
                }
            }
        }
    }

    private void FindLegacyRoomRow()
    {
        MapEditorUIController editor = MapEditorUIController.Instance;
        if (editor == null || editor.m_roomPanel == null ||
            !editor.m_roomPanel.activeInHierarchy)
            return;
        RoomItemController[] items =
            editor.m_roomPanel.GetComponentsInChildren<RoomItemController>();
        foreach (RoomItemController item in items)
        {
            if (item != null && item.m_roomDatabaseID == RoomId)
            {
                targetRoomItem = item;
                return;
            }
        }
    }
}



// DEVELOPMENT TEST PACKAGE ONLY: no Alpha/release or ordinary save use.
// The super-GM controls bypass *scenario policy* such as patient quota, not
// native entity/data invariants. Never call a forced spawn a clinical L4 pass.
internal sealed class ABCLSuperGmTestPanel
{
    private const string RoomId = "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB";
    private const string BloodLeadTestId = "EXM_ABCL_G1_BLOOD_LEAD_TESTING";
    private const string BloodLeadSamplingId = "EXM_ABCL_G1_BLOOD_LEAD_SAMPLING";
    private Rect window = new Rect(45f, 95f, 530f, 415f);
    private bool opened;
    private int forceAttempts;
    private bool factoryFailed;
    private float lastClick = -100f;
    private string caseId = "DIA_CLD";
    private string status = "请选择临时存档。本面板仅供开发测试，不属于正式医疗流程。";
    private string routing = "点击“核对路由标签”查看源码级隔离状态。";

    internal void Draw()
    {
        float x = Mathf.Max(6f, Screen.width - 280f);
        if (GUI.Button(new Rect(x, 56f, 140f, 32f),
                       opened ? "超级GM · 关闭" : "中文超级GM"))
            opened = !opened;
        if (!opened) return;

        window.width = Mathf.Min(530f, Mathf.Max(320f, Screen.width - 18f));
        window.height = Mathf.Min(415f, Mathf.Max(250f, Screen.height - 20f));
        window.x = Mathf.Clamp(window.x, 2f, Mathf.Max(2f, Screen.width - window.width - 2f));
        window.y = Mathf.Clamp(window.y, 2f, Mathf.Max(2f, Screen.height - window.height - 2f));
        window = GUI.Window(681415, window, DrawWindow, "ABCL · 中文超级GM（仅测试版）");
    }

    private void DrawWindow(int id)
    {
        GUILayout.Space(5f);
        GUILayout.Label("测试存档专用 | 强制操作不计入真实诊疗通过证据");
        GUILayout.Label("病例 ID（例如 DIA_CLD / 将来的 ABCL 私有病例）");
        caseId = GUILayout.TextField(caseId, 80);
        bool previous = GUI.enabled;
        GUI.enabled = previous && !factoryFailed && forceAttempts < 5;
        if (GUILayout.Button("强制生成门诊测试患者（跳过保险名额限制）", GUILayout.Height(35f)))
            ForceMobilePatient();
        GUI.enabled = previous;
        if (GUILayout.Button("核对路由标签：原版 CBC / ABCL 血铅（只读）", GUILayout.Height(29f)))
            ExamineRoutingTags();
        GUILayout.Label("患者请求次数：" + forceAttempts + "/5");
        GUILayout.Label("状态：" + status);
        GUILayout.Label("路由：" + routing);
        GUILayout.Label("注意：绕过门诊/保险配额 ≠ 绕过原版对象构造，\n不自动强制确诊、不替代检验人员、不会更改原版数据库。\n真实 L4 仍需观察病人抵达、检验与结果回传。");
        GUI.DragWindow(new Rect(0f, 0f, window.width, 27f));
    }

    private static bool HasTag(GameDBExamination exam, string tag)
    {
        if (exam == null || exam.Procedure == null ||
            exam.Procedure.RequiredRoomTags == null) return false;
        foreach (string item in exam.Procedure.RequiredRoomTags)
            if (item == tag) return true;
        return false;
    }

    private static bool CanUseRoom(GameDBExamination exam, GameDBRoomType room)
    {
        if (exam == null || room == null || exam.Procedure == null) return false;
        string[] tags = exam.Procedure.RequiredRoomTags;
        if (tags == null) return false;
        foreach (string tag in tags)
            if (room.HasTag(tag)) return true;
        return false;
    }

    private void ExamineRoutingTags()
    {
        try
        {
            GameDBRoomType room = Database.Instance.GetEntry<GameDBRoomType>(RoomId);
            GameDBExamination cbc = Database.Instance.GetEntry<GameDBExamination>("EXM_CBC_TESTING");
            GameDBExamination blood = Database.Instance.GetEntry<GameDBExamination>(BloodLeadTestId);
            if (room == null || cbc == null || blood == null)
            {
                routing = "缺失毒理房间、CBC 或 ABCL 血铅的数据库条目。";
                return;
            }
            bool cbcNoMatch = !CanUseRoom(cbc, room);
            bool bloodPrivate = room.HasTag("abcl_g1_toxicology_lab") &&
                                HasTag(blood, "abcl_g1_toxicology_lab");
            routing = "CBC 的毒理室标签：" + (cbcNoMatch ? "不匹配" : "警告：可能匹配") +
                      " | 血铅独占标签：" + (bloodPrivate ? "存在" : "缺失") +
                      " | 仅静态检查，不能证明实际工作队列";
            Debug.Log("[ABCL GM TEST ONLY] " + routing);
        }
        catch (Exception ex)
        {
            routing = "读取路由失败，请查日志。";
            Debug.LogWarning("[ABCL GM TEST ONLY] Route inspection failed: " + ex);
        }
    }

    private static InsuranceCompany ChooseAnyInsuranceForFixture()
    {
        if (InsuranceManager.Instance == null || InsuranceManager.Instance.m_state == null ||
            InsuranceManager.Instance.m_state.m_insuranceCompanies == null)
            return null;
        InsuranceCompany firstValid = null;
        foreach (InsuranceCompany insurer in InsuranceManager.Instance.m_state.m_insuranceCompanies)
        {
            if (insurer == null || insurer.m_hidden ||
                !insurer.m_gameDBInsuranceCompany.IsValid ||
                insurer.m_gameDBInsuranceCompany.Entry == null) continue;
            if (firstValid == null) firstValid = insurer;
            if (insurer.m_isContracted) return insurer;
        }
        return firstValid;
    }

    private void ForceMobilePatient()
    {
        if (factoryFailed || forceAttempts >= 5 ||
            Time.realtimeSinceStartup - lastClick < 1.5f) return;
        lastClick = Time.realtimeSinceStartup;
        // This GM command is not gated on insurer quotas, an ER clinic, or a ward.
        // The native factory, active hospital, insurer object and valid disease still
        // have to exist. Failure is reported rather than spoofed as success.
        if (Hospital.Instance == null || Database.Instance == null ||
            !Database.Instance.Loaded || MapScriptInterface.Instance == null ||
            Hospital.Instance.GetGroundFloor() == null)
        {
            status = "游戏地图/数据库未准备好，无法安全构造患者。";
            return;
        }
        string id = (caseId ?? string.Empty).Trim();
        if (id.Length == 0 || id.Length > 80)
        {
            status = "请输入有效病例 ID。";
            return;
        }
        try
        {
            GameDBMedicalCondition condition = Database.Instance.GetEntry<GameDBMedicalCondition>(id);
            InsuranceCompany insurer = ChooseAnyInsuranceForFixture();
            if (condition == null || insurer == null)
            {
                status = "病例或保险对象不存在。无法创建原生患者（未修改保险合同/任务）。";
                return;
            }
            // Source-backed guard: GameDBMedicalCondition.HasImmobileSymptom()
            // checks severe, bed-bound and intubated symptom classes. A MOBILE
            // fixture for these diagnoses can leave invalid native patient
            // states and must not be treated as a successful forced case.
            if (condition.HasImmobileSymptom())
            {
                status = "此病例含卧床/插管症状，不能通过门诊强制生成。请使用原生严重患者流程；未创建患者。";
                Debug.LogWarning("[ABCL GM TEST ONLY] Rejected mobile spawn for immobile condition: " + id);
                return;
            }
            forceAttempts++;
            Floor floor = Hospital.Instance.GetGroundFloor();
            Vector2i origin = MapScriptInterface.Instance.GetRandomSpawnPosition();
            Entity patient = LopitalEntityFactory.CreateCharacterPatient(
                floor, origin, condition, PatientMobility.MOBILE,
                insurer.m_gameDBInsuranceCompany.Entry);
            if (patient == null || patient.GetComponent<BehaviorPatient>() == null)
            {
                factoryFailed = true;
                status = "原生工厂返回无效实体；为防止副作用已锁定继续生成。";
                return;
            }
            floor.AddCharacter(patient);
            GameDBExamination sample = Database.Instance.GetEntry<GameDBExamination>(BloodLeadSamplingId);
            bool hasSample = false;
            if (sample != null && condition.Examinations != null)
                foreach (GameDBExamination ex in condition.Examinations)
                    if (ex == sample) { hasSample = true; break; }
            status = "已请求创建 " + id + "（门诊测试实体；保险配额未限制）。" +
                     (hasSample ? " 已关联血铅采样。" : " 此病例未关联血铅采样。");
            Debug.Log("[ABCL GM TEST ONLY] Forced native MOBILE patient: " + id +
                      "; linked sampling=" + hasSample + "; not a clinical L4 pass.");
        }
        catch (Exception ex)
        {
            factoryFailed = true; // fail closed after potentially partial native side effects
            status = "患者构造发生异常，已锁定本次会话重复尝试；查看日志。";
            Debug.LogError("[ABCL GM TEST ONLY] Native forced fixture failed: " + ex);
        }
    }
}
