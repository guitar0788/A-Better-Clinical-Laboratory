using System;
using System.Collections.Generic;
using System.Reflection;
using UnityEngine;
using UnityEngine.SceneManagement;
using GLib;
using Lopital;

// R3: one native TRM_LDP IMOBILE test request. No generic outpatient fixture or Super-GM.
public sealed class ModEntryPoint : HospitalMod
{
    private bool expanded;
    private Rect window = new Rect(40f, 80f, 520f, 470f);
    private string status = "Ready: verify Emergency clinic and ABCL lab before spawning.";
    private bool r3SpawnAttempted;

    // Optional TO-001 room-menu appearance only; the R2/R3 clinical path is unchanged.
    private G1ToxicologyRoomIconAdapter to001RoomIcon;
    private G1ToxicologyPrivateFloorIconAdapter to001FloorIcon;

    private void LateUpdate()
    {
        if (to001RoomIcon == null)
            to001RoomIcon = new G1ToxicologyRoomIconAdapter();
        to001RoomIcon.LateTick();
        if (to001FloorIcon == null)
            to001FloorIcon = new G1ToxicologyPrivateFloorIconAdapter();
        to001FloorIcon.LateTick();
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
        if (!HospitalIsReady() || !IsNativeLeadMode()) return;
        float x = Mathf.Max(8f, Screen.width - 132f);
        if (GUI.Button(new Rect(x, 56f, 125f, 32f),
                       expanded ? "ABCL G1 [Close]" : "ABCL G1 [Test]"))
            expanded = !expanded;
        if (!expanded) return;
        window.width = 520f;
        window.height = 470f;
        window.x = Mathf.Clamp(window.x, 4f,
                               Mathf.Max(4f, Screen.width - window.width - 4f));
        window.y = Mathf.Clamp(window.y, 4f,
                               Mathf.Max(4f, Screen.height - window.height - 4f));
        window = GUI.Window(681401, window, DrawWindow, "ABCL G1 | R3 Native Lead TEST");
    }

    private void DrawWindow(int id)
    {
        GUILayout.Space(7f);
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

internal sealed class G1ToxicologyPrivateFloorIconAdapter
{
    internal const string RoomId = "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB";
    internal const string PrivateFloorAtlasId = "ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS";

    // A source-confirmed, version-sensitive original ABI. Missing fields fail
    // closed; no Harmony/global patches or speculative reflected writes.
    private static readonly FieldInfo MapRoomRendererField =
        typeof(MapRenderer).GetField("m_roomRenderer",
            BindingFlags.Instance | BindingFlags.NonPublic);
    private static readonly FieldInfo RoomDataField =
        typeof(RoomRenderer).GetField("m_roomData",
            BindingFlags.Instance | BindingFlags.NonPublic);

    private readonly Dictionary<Renderer, Texture> owned =
        new Dictionary<Renderer, Texture>();
    private readonly HashSet<Renderer> conflicts = new HashSet<Renderer>();
    private Texture privateAtlas;
    private float nextScan;
    private bool faulted;

    internal void LateTick()
    {
        if (faulted) return;
        try { Tick(); }
        catch (Exception ex)
        {
            // Undo only our own texture swaps; leave any foreign modification.
            try { RestoreOwned(); }
            catch (Exception rollbackEx)
            {
                // Never propagate a secondary rollback error through Unity LateUpdate.
                Debug.LogWarning("[ABCL TO-001] Floor-icon rollback skipped: " + rollbackEx);
            }
            faulted = true;
            Debug.LogWarning("[ABCL TO-001] Optional private floor icon disabled: " + ex);
        }
    }

    private void Tick()
    {
        if (SceneManager.GetActiveScene().name != "main_scene_default" ||
            Database.Instance == null || !Database.Instance.Loaded ||
            StreamingAssetManager.GetInstance() == null ||
            !StreamingAssetManager.GetInstance().IsReady() ||
            ViewModeController.Instance == null ||
            ViewModeController.Instance.m_currentMode != ViewModes.LOGISTICS ||
            Hospital.Instance == null ||
            MapEditorController.sm_instance == null ||
            MapEditorController.sm_instance.FloorCount == 0)
        {
            RestoreOwned();
            return;
        }

        if (Time.unscaledTime < nextScan) return;
        nextScan = Time.unscaledTime + 0.75f;

        if (MapRoomRendererField == null || RoomDataField == null ||
            Database.Instance.GetEntry<GameDBAsset>(PrivateFloorAtlasId) == null)
        {
            RestoreOwned();
            return;
        }
        Texture atlas = StreamingAssetManager.GetInstance().GetTextureAsset(PrivateFloorAtlasId);
        GameDBTweakableString floorAsset =
            Database.Instance.GetEntry<GameDBTweakableString>("TEXTURE_ASSET_FLOOR");
        Texture baseline = floorAsset == null ? null :
            StreamingAssetManager.GetInstance().GetTextureAsset(floorAsset.Value);
        // Native floor UVs are a 16 x 32 grid. The private 2048 square
        // image contains 128 x 64 cells, preserving the 2:1 native tile ratio.
        // Never bind the ordinary 64 x 64 room-menu PNG as a floor atlas.
        if (atlas == null || atlas.width != 2048 || atlas.height != 2048 ||
            baseline == null || atlas == baseline)
        {
            RestoreOwned();
            return;
        }

        MapRenderer map = MapEditorController.sm_instance.CurrentFloorRenderer;
        if (map == null)
        {
            RestoreOwned();
            return;
        }
        RoomRenderer nativeRooms = MapRoomRendererField.GetValue(map) as RoomRenderer;
        Dictionary<Room, RoomData> rooms = nativeRooms == null ? null :
            RoomDataField.GetValue(nativeRooms) as Dictionary<Room, RoomData>;
        if (rooms == null)
        {
            RestoreOwned();
            return;
        }

        HashSet<Renderer> present = new HashSet<Renderer>();
        foreach (KeyValuePair<Room, RoomData> pair in rooms)
        {
            Room room = pair.Key;
            if (room == null || room.m_roomPersistentData == null ||
                !room.m_roomPersistentData.m_roomType.IsValid ||
                room.m_roomPersistentData.m_roomType.Entry == null ||
                room.m_roomPersistentData.m_roomType.Entry.DatabaseID.ToString() != RoomId ||
                pair.Value == null || pair.Value.m_roomIcon == null ||
                pair.Value.m_roomIcon.m_gameObject == null)
                continue;

            Renderer glyph = pair.Value.m_roomIcon.m_gameObject.GetComponent<Renderer>();
            if (glyph == null) continue;
            present.Add(glyph);
            if (conflicts.Contains(glyph)) continue;

            // Renderer.material is per-renderer in native RendererObject's ctor.
            // Never change sharedMaterial or anything on another room.
            Material material = glyph.material;
            if (material == null) continue;
            Texture original;
            if (!owned.TryGetValue(glyph, out original))
            {
                if (material.mainTexture != baseline)
                {
                    conflicts.Add(glyph); // another Mod may already own it
                    continue;
                }
                owned.Add(glyph, baseline);
            }
            else if (material.mainTexture != privateAtlas &&
                     material.mainTexture != original)
            {
                owned.Remove(glyph);
                conflicts.Add(glyph); // do not fight external mutations
                continue;
            }
            material.mainTexture = atlas;
        }
        // Capture previous ownership before tracking the new asset instance.
        Texture previouslyOwnedAtlas = privateAtlas;
        privateAtlas = atlas;
        List<Renderer> stale = new List<Renderer>();
        foreach (KeyValuePair<Renderer, Texture> entry in owned)
        {
            if (entry.Key == null || !present.Contains(entry.Key))
            {
                if (entry.Key != null && entry.Key.material != null &&
                    (entry.Key.material.mainTexture == privateAtlas ||
                     entry.Key.material.mainTexture == previouslyOwnedAtlas))
                    entry.Key.material.mainTexture = entry.Value;
                stale.Add(entry.Key);
            }
        }
        foreach (Renderer glyph in stale) owned.Remove(glyph);
        conflicts.RemoveWhere(delegate(Renderer r) { return r == null; });
    }

    private void RestoreOwned()
    {
        foreach (KeyValuePair<Renderer, Texture> entry in owned)
        {
            if (entry.Key != null && entry.Key.material != null &&
                entry.Key.material.mainTexture == privateAtlas)
                entry.Key.material.mainTexture = entry.Value;
        }
        owned.Clear();
        privateAtlas = null;
        conflicts.Clear();
    }
}
