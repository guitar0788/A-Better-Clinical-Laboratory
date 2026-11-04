using System;
using System.Collections.Generic;
using System.IO;
using System.Security.Cryptography;
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

    private void OnEnable()
    {
        // Rebind the exact ABCL room glyph before main-camera rendering.
        // Native RoomRenderer creates it with the original tile-376 atlas.
        Camera.onPreCull -= BeforeMainCameraCull;
        Camera.onPreCull += BeforeMainCameraCull;
    }

    private void OnDisable()
    {
        Camera.onPreCull -= BeforeMainCameraCull;
        if (to001FloorIcon != null) to001FloorIcon.ReleaseOwned();
    }

    private void OnDestroy()
    {
        Camera.onPreCull -= BeforeMainCameraCull;
    }

    private void BeforeMainCameraCull(Camera camera)
    {
        if (!isActiveAndEnabled || camera == null || camera != Camera.main ||
            to001FloorIcon == null)
            return;
        to001FloorIcon.LateTick();
    }

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


/* TO-001: approved local-original image fallback, used only if the native
 * StreamingAssetManager did not expose a specific private ABCL asset.
 * Images are read from the current addon folder and verified by SHA-256.
 * No shared GameDB, atlas or other Mod asset is mutated. This code runs only
 * on Unity's main thread (ModEntryPoint.LateUpdate).
 */
internal sealed class G1ApprovedPrivateTexture
{
    private readonly string fileName;
    private readonly string expectedSha256;
    private readonly int expectedWidth;
    private readonly int expectedHeight;
    // UnityEngine.WWW is forwarded to a module not present in our protected
    // net35 compile references. Resolve the original Unity type at runtime.
    private object request;
    private Type requestType;
    private Texture2D ownedTexture;
    private Sprite ownedSprite;
    private bool unavailable;
    private bool warned;
    private bool loggedLoaded;

    internal G1ApprovedPrivateTexture(string name, string sha, int width, int height)
    {
        fileName = name;
        expectedSha256 = sha;
        expectedWidth = width;
        expectedHeight = height;
    }

    internal Texture2D GetTexture()
    {
        if (ownedTexture != null) return ownedTexture;
        if (unavailable) return null;
        try
        {
            if (request == null)
            {
                // The original title-screen loader uses Assembly.LoadFrom.
                // Resolve next to THIS DLL, not a guessed Steam installation.
                string root = Path.GetDirectoryName(typeof(ModEntryPoint).Assembly.Location);
                string path = Path.Combine(root, "Assets/ABCL/" + fileName);
                if (!File.Exists(path))
                {
                    Fail("approved source file absent: " + fileName);
                    return null;
                }
                byte[] original = File.ReadAllBytes(path);
                using (SHA256 sha = SHA256.Create())
                {
                    byte[] digest = sha.ComputeHash(original);
                    string actual = BitConverter.ToString(digest).Replace("-", "").ToLowerInvariant();
                    if (actual != expectedSha256)
                    {
                        Fail("approved source SHA-256 mismatch: " + fileName);
                        return null;
                    }
                }
                // Call native UnityEngine.WWW by reflection. This is the same
                // file:// loader used by StreamingAssetManager; no extra
                // third-party library or protected game reference is added.
                requestType = FindNativeWwwType();
                if (requestType == null)
                {
                    Fail("original Unity WWW file loader module unavailable");
                    return null;
                }
                string localUrl = "file:///" + Uri.EscapeUriString(path.Replace('\\', '/'));
                request = Activator.CreateInstance(requestType, new object[] { localUrl });
            }
            PropertyInfo isDoneProperty = requestType.GetProperty("isDone");
            PropertyInfo errorProperty = requestType.GetProperty("error");
            MethodInfo loadImage = requestType.GetMethod("LoadImageIntoTexture",
                new Type[] { typeof(Texture2D) });
            if (isDoneProperty == null || errorProperty == null || loadImage == null)
            {
                Fail("original Unity WWW image-loader ABI unavailable");
                return null;
            }
            if (!(bool)isDoneProperty.GetValue(request, null)) return null;
            string loadError = errorProperty.GetValue(request, null) as string;
            if (!string.IsNullOrEmpty(loadError))
            {
                Fail("local source decoding failed: " + fileName);
                return null;
            }
            Texture2D local = new Texture2D(16, 16, TextureFormat.ARGB32, true);
            loadImage.Invoke(request, new object[] { local });
            if (local.width != expectedWidth || local.height != expectedHeight)
            {
                UnityEngine.Object.Destroy(local);
                Fail("approved source dimensions changed: " + fileName);
                return null;
            }
            local.filterMode = FilterMode.Trilinear;
            local.wrapMode = TextureWrapMode.Clamp;
            local.Apply(false, true);
            ownedTexture = local;
            DisposeRequest();
            if (!loggedLoaded)
            {
                loggedLoaded = true;
                Debug.Log("[ABCL TO-001] Verified private source loaded: " + fileName);
            }
            return ownedTexture;
        }
        catch (Exception ex)
        {
            Fail("private source read/decode error: " + fileName + " (" + ex.GetType().Name + ")");
            return null;
        }
    }

    private static Type FindNativeWwwType()
    {
        foreach (Assembly loaded in AppDomain.CurrentDomain.GetAssemblies())
        {
            Type found = loaded.GetType("UnityEngine.WWW", false);
            if (found != null) return found;
        }
        try
        {
            Assembly module = Assembly.Load("UnityEngine.UnityWebRequestWWWModule");
            return module.GetType("UnityEngine.WWW", false);
        }
        catch { return null; }
    }

    private void DisposeRequest()
    {
        if (request == null) return;
        IDisposable disposable = request as IDisposable;
        if (disposable != null) disposable.Dispose();
        request = null;
    }

    internal Sprite GetRoomSprite()
    {
        if (ownedSprite != null) return ownedSprite;
        Texture2D texture = GetTexture();
        if (texture == null) return null;
        ownedSprite = Sprite.Create(texture, new Rect(2f, 2f, 60f, 60f),
            new Vector2(0f, 0f), 32f, 0u, SpriteMeshType.FullRect);
        return ownedSprite;
    }

    private void Fail(string reason)
    {
        unavailable = true;
        DisposeRequest();
        if (!warned)
        {
            warned = true;
            Debug.LogWarning("[ABCL TO-001] PRIVATE ASSET ERROR: " + reason);
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
    // Native IconManager.GetIcon(string) silently supplies a different atlas
    // sprite on a missing private key. Inspect its actual cache first so
    // "non-null fallback" is NEVER mistaken for the approved red/gray icon.
    private static readonly FieldInfo NativeCustomSpriteCache =
        typeof(IconManager).GetField("m_customIconSprites",
            BindingFlags.Instance | BindingFlags.NonPublic);

    private static readonly FieldInfo RoomButtonItemId =
        typeof(BuildingModeButtonController).GetField(
            "m_itemDatabaseID", BindingFlags.Instance | BindingFlags.NonPublic);
    private static readonly FieldInfo RoomButtonItemType =
        typeof(BuildingModeButtonController).GetField(
            "m_itemType", BindingFlags.Instance | BindingFlags.NonPublic);

    // The vanilla CreateRoomButton() adds BuildingModeButtonController to
    // the Button child of a root m_roomButtons item; the icon segment may
    // be a sibling, not an ancestor of that Button. Walk the native root
    // lists and resolve both components from the SAME root.
    private static readonly FieldInfo[] NativeRoomButtonLists = {
        typeof(DepartmentManagementLogisticsHybridController).GetField(
            "m_roomButtons", BindingFlags.Instance | BindingFlags.NonPublic),
        typeof(DepartmentManagementLogisticsHybridController).GetField(
            "m_roomButtonsShared", BindingFlags.Instance | BindingFlags.NonPublic),
        typeof(DepartmentManagementLogisticsHybridController).GetField(
            "m_roomButtonsHospitalization", BindingFlags.Instance | BindingFlags.NonPublic),
        typeof(DepartmentManagementLogisticsHybridController).GetField(
            "m_roomButtonsHospitalizationShared", BindingFlags.Instance | BindingFlags.NonPublic)
    };

    private DepartmentManagementLogisticsHybridController hybridPanel;
    private GameObject targetButtonRoot;
    private SegmentItemIconTextTextIconController targetSegment;
    // Exact native UnityEngine.UI.Image located via UnityEngine.Component.
    // No UnityEngine.UI.dll compile dependency or change to sealed L3 refs.
    private UnityEngine.Component cachedSegmentImage;
    private PropertyInfo cachedSpriteProperty;
    private PropertyInfo cachedColorProperty;
    private PropertyInfo cachedOverrideProperty;
    private bool loggedHybridBind;
    private bool loggedHybridConflict;
    private RoomItemController targetRoomItem;
    private GameDBRoomType targetRoom;
    private float nextProbe;
    private bool faulted;
    private bool missingContractLogged;
    private bool noRoomRowLogged;
    private bool loggedLegacyBind;
    private bool loggedLegacyConflict;
    private GameObject cachedLegacyIconRoot;
    private UnityEngine.Component cachedLegacyImage;
    private PropertyInfo cachedLegacySpriteProperty;
    private PropertyInfo cachedLegacyColorProperty;
    private PropertyInfo cachedLegacyOverrideProperty;
    private readonly G1ApprovedPrivateTexture approvedActive =
        new G1ApprovedPrivateTexture("toxicology_room_icon.png",
            "225b2918c448b5d36d1d8582389e8952f2baf1574d0d72935017c81eab7d8199", 64, 64);
    private readonly G1ApprovedPrivateTexture approvedInactive =
        new G1ApprovedPrivateTexture("toxicology_room_icon_inactive.png",
            "50c17ea8ba8b42b28295564f594713069a31c9e48fa05f3a6b623a36851b6490", 64, 64);

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

    // Native CreateRoomButton places rows 26 UI units apart. This caps
    // only the exact ABCL UI Image, never the owner-approved PNG.
    private static void FitRoomListIconToNativeRow(GameObject imageObject)
    {
        if (!imageObject) return;
        RectTransform rect = imageObject.GetComponent<RectTransform>();
        if (!rect) return;
        const float MaxNativeRoomIconSide = 22f; // hover 1.1x -> 24.2 < 26 row pitch
        if (rect.rect.width > MaxNativeRoomIconSide)
            rect.SetSizeWithCurrentAnchors(RectTransform.Axis.Horizontal,
                MaxNativeRoomIconSide);
        if (rect.rect.height > MaxNativeRoomIconSide)
            rect.SetSizeWithCurrentAnchors(RectTransform.Axis.Vertical,
                MaxNativeRoomIconSide);
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
            targetButtonRoot = null;
            targetRoomItem = null;
            hybridPanel = null;
            targetRoom = null;
            return;
        }

        // Evaluate only the asset needed for the current state. Do not
        // block the active red icon merely because the gray asset is missing.
        // If the game's asset manager dropped this private asset, a SHA-pinned
        // private copy is loaded beside the G1 DLL (no global registration).
        if (targetRoom == null)
            targetRoom = Database.Instance.GetEntry<GameDBRoomType>(RoomId);
        if (targetRoom == null) return;

        // Original DepartmentManagementLogisticsHybridController.UpdateRoomButtons
        // writes the integer icon *every Update*. Apply at LateUpdate so the
        // icon is not immediately reset. Only one cached Image is changed.
        if (!targetSegment || !targetSegment.gameObject.activeInHierarchy ||
            !IsExactNativeRoomButton(targetButtonRoot))
        {
            targetSegment = null;
            targetButtonRoot = null;
            cachedSegmentImage = null;
            cachedSpriteProperty = null;
            cachedColorProperty = null;
            cachedOverrideProperty = null;
        }
        if (!targetRoomItem || !targetRoomItem.gameObject.activeInHierarchy)
            targetRoomItem = null;
        if (Time.unscaledTime >= nextProbe)
        {
            nextProbe = Time.unscaledTime + 0.75f;
            if (!targetSegment) FindHybridRoomRow();
            if (!targetRoomItem) FindLegacyRoomRow();
            if (!targetSegment && !targetRoomItem && !noRoomRowLogged)
            {
                noRoomRowLogged = true;
                Debug.LogWarning("[ABCL TO-001] Exact toxicology room row not found in native " +
                    "hybrid/legacy lists; no icon or other department row modified.");
            }
        }

        bool locked = InsuranceManager.Instance != null &&
            InsuranceManager.Instance.IsRoomLocked(targetRoom);
        // IconController's custom-asset path ignores its m_inactive sprite index;
        // provide a distinct transparent disabled-state glyph without tinting
        // the native Image, room-area background or access colors.
        string assetId = locked ? InactiveId : ActiveId;
        bool hasDbEntry = Database.Instance.GetEntry<GameDBAsset>(assetId) != null;
        bool hasNativeTexture = StreamingAssetManager.GetInstance().GetTextureAsset(assetId) != null;
        Dictionary<string, Sprite> nativeCache = NativeCustomSpriteCache == null ? null :
            NativeCustomSpriteCache.GetValue(IconManager.Instance) as Dictionary<string, Sprite>;
        Sprite sprite = null;
        bool iconRegistered = nativeCache != null && nativeCache.TryGetValue(assetId, out sprite);
        if (!hasDbEntry || !hasNativeTexture || !iconRegistered) sprite = null;
        if (sprite == null)
        {
            if (!missingContractLogged)
            {
                missingContractLogged = true;
                Debug.LogWarning("[ABCL TO-001] Native custom icon missing: " +
                    assetId + " GameDB=" + hasDbEntry +
                    " TextureLoaded=" + hasNativeTexture +
                    " IconRegistered=" + iconRegistered +
                    "; attempting SHA-pinned approved source fallback.");
            }
            sprite = (locked ? approvedInactive : approvedActive).GetRoomSprite();
        }
        if (sprite == null) return;

        if (targetSegment && targetSegment.m_icon &&
            IsExactNativeRoomButton(targetButtonRoot))
        {
            // Vanilla UpdateRoomButtons overwrites only this Image.sprite on
            // every Update (native SegmentItemIconTextTextIconController).
            // Bind after native Update; never edit shared icons, atlas, room
            // types or neighboring department rows.
            if (!cachedSegmentImage ||
                cachedSegmentImage.gameObject != targetSegment.m_icon)
            {
                cachedSegmentImage = null;
                cachedSpriteProperty = null;
                cachedColorProperty = null;
                cachedOverrideProperty = null;
                foreach (UnityEngine.Component candidate in targetSegment.m_icon.GetComponents<UnityEngine.Component>())
                {
                    if (!candidate || candidate.GetType().FullName != "UnityEngine.UI.Image")
                        continue;
                    cachedSegmentImage = candidate;
                    Type t = candidate.GetType();
                    cachedSpriteProperty = t.GetProperty("sprite", BindingFlags.Instance | BindingFlags.Public);
                    cachedColorProperty = t.GetProperty("color", BindingFlags.Instance | BindingFlags.Public);
                    cachedOverrideProperty = t.GetProperty("overrideSprite", BindingFlags.Instance | BindingFlags.Public);
                    break;
                }
            }
            if (cachedSegmentImage != null && cachedSpriteProperty != null &&
                cachedColorProperty != null && cachedOverrideProperty != null &&
                cachedSpriteProperty.CanRead && cachedSpriteProperty.CanWrite &&
                cachedColorProperty.CanRead && cachedColorProperty.CanWrite &&
                cachedOverrideProperty.CanRead &&
                cachedSpriteProperty.PropertyType == typeof(Sprite) &&
                cachedOverrideProperty.PropertyType == typeof(Sprite) &&
                cachedColorProperty.PropertyType == typeof(Color))
            {
                Sprite current = cachedSpriteProperty.GetValue(cachedSegmentImage, null) as Sprite;
                Sprite candidateOverride =
                    cachedOverrideProperty.GetValue(cachedSegmentImage, null) as Sprite;
                // Unity may return null OR the current sprite for an unset
                // overrideSprite. Never replace a distinct foreign override.
                if (candidateOverride == null ||
                    candidateOverride == current ||
                    candidateOverride == sprite)
                {
                    // The approved 64px PNG already contains red/gray backing.
                    // Only this exact ABCL row gets an opaque white UI tint.
                    Color tint = (Color)cachedColorProperty.GetValue(cachedSegmentImage, null);
                    if (tint != Color.white)
                        cachedColorProperty.SetValue(cachedSegmentImage, Color.white, null);
                    if (current != sprite)
                        cachedSpriteProperty.SetValue(cachedSegmentImage, sprite, null);
                    FitRoomListIconToNativeRow(targetSegment.m_icon);
                    if (!loggedHybridBind)
                    {
                        loggedHybridBind = true;
                        Debug.Log("[ABCL TO-001] Exact native toxicology room icon bound: "
                            + assetId + "; owner PNG unchanged.");
                    }
                }
                else if (!loggedHybridConflict)
                {
                    loggedHybridConflict = true;
                    Debug.LogWarning("[ABCL TO-001] Foreign room Image.overrideSprite detected; "
                        + "ABCL does not override another mod.");
                }
            }
            else if (!loggedHybridConflict)
            {
                loggedHybridConflict = true;
                Debug.LogWarning("[ABCL TO-001] Exact native UI.Image or its sprite/color "
                    + "properties unavailable; preserve native icon.");
            }
        }
        if (targetRoomItem && targetRoomItem.m_icon &&
            targetRoomItem.m_roomDatabaseID == RoomId)
        {
            // Original RoomItemController has an IconController and a child
            // UnityEngine.UI.Image. IconController.SetIcon(string) calls
            // IconManager.GetIcon(), whose missing-ID fallback is a vanilla
            // sprite, not the approved red/gray icon. Reuse the exact SHA-
            // verified Sprite from the SAME current-state resolver above.
            // Only the ABCL RoomItemController row is ever modified.
            IconController icon = targetRoomItem.m_icon.GetComponent<IconController>();
            if (icon != null &&
                !string.IsNullOrEmpty(icon.m_customIconAssetID) &&
                icon.m_customIconAssetID != ActiveId &&
                icon.m_customIconAssetID != InactiveId)
            {
                if (!loggedLegacyConflict)
                {
                    loggedLegacyConflict = true;
                    Debug.LogWarning("[ABCL TO-001] Another mod owns the legacy ABCL room icon; "
                        + "foreign custom sprite preserved.");
                }
                return;
            }
            if (cachedLegacyIconRoot != targetRoomItem.m_icon || !cachedLegacyImage)
            {
                cachedLegacyIconRoot = targetRoomItem.m_icon;
                cachedLegacyImage = null;
                cachedLegacySpriteProperty = null;
                cachedLegacyColorProperty = null;
                cachedLegacyOverrideProperty = null;
                foreach (UnityEngine.Component component in
                    targetRoomItem.m_icon.GetComponentsInChildren<UnityEngine.Component>(true))
                {
                    if (!component || component.GetType().FullName != "UnityEngine.UI.Image")
                        continue;
                    cachedLegacyImage = component;
                    Type imageType = component.GetType();
                    cachedLegacySpriteProperty = imageType.GetProperty("sprite",
                        BindingFlags.Public | BindingFlags.Instance);
                    cachedLegacyColorProperty = imageType.GetProperty("color",
                        BindingFlags.Public | BindingFlags.Instance);
                    cachedLegacyOverrideProperty = imageType.GetProperty("overrideSprite",
                        BindingFlags.Public | BindingFlags.Instance);
                    break;
                }
            }
            if (cachedLegacyImage && cachedLegacySpriteProperty != null &&
                cachedLegacyColorProperty != null && cachedLegacyOverrideProperty != null &&
                cachedLegacySpriteProperty.CanRead && cachedLegacySpriteProperty.CanWrite &&
                cachedLegacyColorProperty.CanRead && cachedLegacyColorProperty.CanWrite &&
                cachedLegacyOverrideProperty.CanRead &&
                cachedLegacySpriteProperty.PropertyType == typeof(Sprite) &&
                cachedLegacyColorProperty.PropertyType == typeof(Color) &&
                cachedLegacyOverrideProperty.PropertyType == typeof(Sprite))
            {
                Sprite current = cachedLegacySpriteProperty.GetValue(cachedLegacyImage, null) as Sprite;
                Sprite thirdPartyOverride =
                    cachedLegacyOverrideProperty.GetValue(cachedLegacyImage, null) as Sprite;
                if (thirdPartyOverride == null || thirdPartyOverride == current ||
                    thirdPartyOverride == sprite)
                {
                    if ((Color)cachedLegacyColorProperty.GetValue(cachedLegacyImage, null) != Color.white)
                        cachedLegacyColorProperty.SetValue(cachedLegacyImage, Color.white, null);
                    if (current != sprite)
                        cachedLegacySpriteProperty.SetValue(cachedLegacyImage, sprite, null);
                    FitRoomListIconToNativeRow(cachedLegacyImage.gameObject);
                    if (!loggedLegacyBind)
                    {
                        loggedLegacyBind = true;
                        Debug.Log("[ABCL TO-001] Exact legacy toxicology room icon bound: "
                            + assetId + "; original owner art unchanged.");
                    }
                }
                else if (!loggedLegacyConflict)
                {
                    loggedLegacyConflict = true;
                    Debug.LogWarning("[ABCL TO-001] A foreign Image.overrideSprite owns "
                        + "the legacy ABCL room icon; no change made.");
                }
            }
            else if (!loggedLegacyConflict)
            {
                loggedLegacyConflict = true;
                Debug.LogWarning("[ABCL TO-001] Original legacy room Image missing; "
                    + "preserving vanilla fallback.");
            }
        }
    }

    private static bool IsExactNativeRoomButton(GameObject root)
    {
        if (!root || !root.activeInHierarchy ||
            RoomButtonItemId == null || RoomButtonItemType == null)
            return false;

        // Vanilla creates the button on the ROOT prefab's Button child,
        // while its SegmentItemIconTextTextIconController is independently
        // resolved by UpdateRoomButton(root, ...). Never assume the button
        // is a child of the SegmentItem component itself.
        BuildingModeButtonController button =
            root.GetComponentInChildren<BuildingModeButtonController>();
        if (!button) return false;
        string id = RoomButtonItemId.GetValue(button) as string;
        object kind = RoomButtonItemType.GetValue(button);
        return id == RoomId && kind != null &&
            (BuildingModeItemType)kind == BuildingModeItemType.ROOM;
    }

    private void FindHybridRoomRow()
    {
        if (RoomButtonItemId == null || RoomButtonItemType == null) return;
        if (!hybridPanel)
            hybridPanel = UnityEngine.Object.FindObjectOfType<DepartmentManagementLogisticsHybridController>();
        if (!hybridPanel || !hybridPanel.gameObject.activeInHierarchy) return;

        // Native CreateRoomButtons()/UpdateRoomButtons() operate on four
        // private lists of root GameObjects. Checking the exact ID on each
        // root works for both mandatory and optional room entries, without
        // localized-text guessing or changing vanilla IconIndex values.
        foreach (FieldInfo field in NativeRoomButtonLists)
        {
            if (field == null) continue; // Fail closed on a changed game ABI.
            List<GameObject> buttons = field.GetValue(hybridPanel) as List<GameObject>;
            if (buttons == null) continue;
            foreach (GameObject root in buttons)
            {
                if (!IsExactNativeRoomButton(root)) continue;
                SegmentItemIconTextTextIconController row =
                    root.GetComponentInChildren<SegmentItemIconTextTextIconController>();
                if (!row || !row.m_icon) continue;
                targetButtonRoot = root;
                targetSegment = row;
                return;
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
    private bool faulted;
    private string lastFloorGate;
    private readonly G1ApprovedPrivateTexture approvedFloor =
        new G1ApprovedPrivateTexture("toxicology_floor_atlas_private_376.png",
            "00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd",
            2048, 2048);

    private void FloorGate(string reason)
    {
        if (lastFloorGate == reason) return;
        lastFloorGate = reason;
        Debug.Log("[ABCL TO-001 FLOOR] " + reason);
    }


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
            Hospital.Instance == null ||
            MapEditorController.sm_instance == null ||
            MapEditorController.sm_instance.FloorCount == 0)
        {
            RestoreOwned();
            return;
        }

        // Vanilla RoomRenderer.RenderRooms draws actual room glyphs in
        // BUILDING, BUILDING_FLOORS and LOGISTICS. Previously we handled only
        // LOGISTICS, so the approved tile-376 glyph could NEVER appear while
        // the owner was painting or inspecting a room in building mode.
        // Preserve the native floor marker/room highlight colors: swap only
        // the exact ABCL room icon renderer's per-instance mainTexture.
        ViewModes roomView = ViewModeController.Instance.m_currentMode;
        if (roomView != ViewModes.BUILDING &&
            roomView != ViewModes.BUILDING_FLOORS &&
            roomView != ViewModes.LOGISTICS)
        {
            FloorGate("native view mode " + roomView +
                " does not display room glyphs; retaining original atlas");
            RestoreOwned();
            return;
        }
        // Scan immediately: never expose a new room's vanilla hematology
        // glyph for the previous 750ms waiting period.

        if (MapRoomRendererField == null || RoomDataField == null)
        {
            FloorGate("native room renderer fields unavailable, version-sensitive ABI");
            RestoreOwned();
            return;
        }
        bool floorEntry = Database.Instance.GetEntry<GameDBAsset>(PrivateFloorAtlasId) != null;
        Texture atlas = StreamingAssetManager.GetInstance().GetTextureAsset(PrivateFloorAtlasId);
        if (atlas == null)
        {
            FloorGate("private texture absent from game asset manager; GameDB=" + floorEntry +
                "; loading pinned ABCL source");
            atlas = approvedFloor.GetTexture();
        }
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
            FloorGate("texture preflight rejected: privateReady=" + (atlas != null) +
                " privateSize=" + (atlas == null ? "NA" : atlas.width + "x" + atlas.height) +
                " baselineReady=" + (baseline != null) +
                " textureDistinct=" + (atlas != baseline));
            RestoreOwned();
            return;
        }

        MapRenderer map = MapEditorController.sm_instance.CurrentFloorRenderer;
        if (map == null)
        {
            FloorGate("CurrentFloorRenderer missing");
            RestoreOwned();
            return;
        }
        RoomRenderer nativeRooms = MapRoomRendererField.GetValue(map) as RoomRenderer;
        Dictionary<Room, RoomData> rooms = nativeRooms == null ? null :
            RoomDataField.GetValue(nativeRooms) as Dictionary<Room, RoomData>;
        if (rooms == null)
        {
            FloorGate("native RoomRenderer room dictionary unavailable");
            RestoreOwned();
            return;
        }

        HashSet<Renderer> present = new HashSet<Renderer>();
        int exactRooms = 0;
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

            exactRooms++;
            Renderer glyph = pair.Value.m_roomIcon.m_gameObject.GetComponent<Renderer>();
            if (glyph == null) { FloorGate("exact ABCL room icon renderer component missing"); continue; }
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
                    FloorGate("exact room glyph uses foreign or unexpected native material texture");
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
            if (material.mainTexture != atlas)
            {
                material.mainTexture = atlas;
                FloorGate("approved isometric private atlas bound to exact ABCL room");
            }
        }
        if (exactRooms == 0)
            FloorGate("no matching ABCL floor icon in current native RoomRenderer");
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

    internal void ReleaseOwned()
    {
        RestoreOwned();
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
