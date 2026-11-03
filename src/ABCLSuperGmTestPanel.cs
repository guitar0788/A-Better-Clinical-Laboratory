using System;
using UnityEngine;
using GLib;
using Lopital;

// DEVELOPMENT TEST PACKAGE ONLY: no Alpha/release or ordinary save use.
// The super-GM controls bypass *scenario policy* such as patient quota, not
// native entity/data invariants. Never call a forced spawn a clinical L4 pass.
#if ABCL_GM_TEST_ONLY
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
#endif
