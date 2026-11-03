using System;
using System.Reflection;
using System.Text;
using UnityEngine;
using UnityEngine.SceneManagement;

// TO-002 isolated TEST-ONLY diagnostic. Read original Dependency tree hierarchy
// after the player opens it. Never creates, moves, enables or repaints UI nodes.
// An exact game L3/L4 is still required; source-only checks cannot prove layout.
internal sealed class ABCLTO002ReadOnlyTreeProbe
{
    private const int MaxNodes = 180;
    private const int MaxOutputChars = 24000;
    private float nextProbe;
    private bool captured;
    private bool faulted;

    internal void ScanIfVisible()
    {
        if (captured || faulted ||
            SceneManager.GetActiveScene().name != "main_scene_default" ||
            Time.unscaledTime < nextProbe)
            return;

        nextProbe = Time.unscaledTime + 2f;
        try
        {
            DependencyTreePanelController[] panels =
                UnityEngine.Object.FindObjectsOfType<DependencyTreePanelController>();
            if (panels == null) return;
            foreach (DependencyTreePanelController panel in panels)
            {
                if (panel != null && panel.gameObject.activeInHierarchy)
                {
                    Capture(panel.transform);
                    captured = true;
                    return;
                }
            }
        }
        catch (Exception ex)
        {
            faulted = true;
            Debug.LogWarning("[ABCL TO-002] Read-only relationship-tree probe stopped: " +
                ex.GetType().FullName);
        }
    }

    private static string SafeText(Component control, string property)
    {
        if (control == null) return "";
        try
        {
            PropertyInfo p = control.GetType().GetProperty(property,
                BindingFlags.Instance | BindingFlags.Public);
            if (p == null || !p.CanRead) return "";
            object value = p.GetValue(control, null);
            if (value == null) return "";
            if (value is Sprite) return ((Sprite)value).name;
            string s = value.ToString();
            s = s.Replace('\n', ' ').Replace('\r', ' ');
            if (s.Length > 90) s = s.Substring(0, 90);
            return s;
        }
        catch (Exception)
        {
            return "<unavailable>";
        }
    }

    private static string PathFromRoot(Transform root, Transform element)
    {
        StringBuilder path = new StringBuilder();
        Transform item = element;
        for (int i = 0; item != null && i < 24; i++)
        {
            if (path.Length > 0) path.Insert(0, "/");
            path.Insert(0, item.name);
            if (item == root) break;
            item = item.parent;
        }
        return path.ToString();
    }

    private void Capture(Transform root)
    {
        Transform[] all = root.GetComponentsInChildren<Transform>(true);
        StringBuilder report = new StringBuilder();
        report.AppendLine("[ABCL TO-002 TREE STRUCTURE — READ ONLY / TEST ONLY]");
        report.AppendLine("scene=" + SceneManager.GetActiveScene().name +
            " root=" + root.name + " total_child_transforms=" + all.Length);
        report.AppendLine("No graph nodes were added, moved or edited.");
        int count = Math.Min(MaxNodes, all.Length);
        for (int i = 0; i < count; i++)
        {
            Transform t = all[i];
            if (t == null) continue;
            RectTransform rect = t as RectTransform;
            report.Append(i).Append(" ").Append(PathFromRoot(root, t));
            report.Append(" active=").Append(t.gameObject.activeSelf);
            if (rect != null)
            {
                report.Append(" xy=(").Append(rect.anchoredPosition.x.ToString("F1"))
                      .Append(",").Append(rect.anchoredPosition.y.ToString("F1"))
                      .Append(") size=(").Append(rect.sizeDelta.x.ToString("F1"))
                      .Append(",").Append(rect.sizeDelta.y.ToString("F1")).Append(")");
            }
            Component img = t.gameObject.GetComponent("Image");
            if (img != null)
            {
                report.Append(" image=").Append(SafeText(img, "sprite"));
            }
            Component text = t.gameObject.GetComponent("Text");
            if (text != null)
            {
                report.Append(" text=").Append(SafeText(text, "text"));
            }
            report.AppendLine();
            if (report.Length > MaxOutputChars)
            {
                report.AppendLine("[ABCL TO-002] output capped by safety budget");
                break;
            }
        }
        if (count < all.Length) report.AppendLine("[ABCL TO-002] hierarchy truncated at 180 nodes");
        Debug.Log(report.ToString());
    }
}
