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

    // Avoid a compile-time UnityEngine.UI assembly dependency in net35.
    // Return only existing native sprite metadata; never read pixels or create nodes.
    private static Sprite TryReadSprite(Component image)
    {
        if (image == null) return null;
        try
        {
            PropertyInfo property = image.GetType().GetProperty("sprite",
                BindingFlags.Instance | BindingFlags.Public);
            if (property == null || !property.CanRead) return null;
            return property.GetValue(image, null) as Sprite;
        }
        catch (Exception) { return null; }
    }

    // Some Unity UI scene variants display a full background texture with
    // RawImage rather than a Sprite Image. Reflection avoids an extra UI ABI
    // dependency. This is read-only: no rendering or texture mutation occurs.
    private static Texture TryReadRawTexture(Component rawImage)
    {
        if (rawImage == null) return null;
        try
        {
            PropertyInfo property = rawImage.GetType().GetProperty("texture",
                BindingFlags.Instance | BindingFlags.Public);
            if (property == null || !property.CanRead) return null;
            return property.GetValue(rawImage, null) as Texture;
        }
        catch (Exception) { return null; }
    }

    private static bool IsExactNativeGraphGraphic(GameObject obj)
    {
        if (obj == null || !obj.activeInHierarchy) return false;
        Sprite sprite = TryReadSprite(obj.GetComponent("Image"));
        if (sprite != null && sprite.name == "dep_tree") return true;
        Texture texture = TryReadRawTexture(obj.GetComponent("RawImage"));
        return texture != null && texture.name == "dep_tree";
    }

    private static void AppendCanvasContext(Transform root, StringBuilder report)
    {
        for (Transform ancestor = root; ancestor != null; ancestor = ancestor.parent)
        {
            Component canvas = ancestor.gameObject.GetComponent("Canvas");
            if (canvas == null) continue;
            report.Append("canvas=").Append(ancestor.name)
                  .Append(" renderMode=").Append(SafeText(canvas, "renderMode"))
                  .Append(" scaleFactor=").Append(SafeText(canvas, "scaleFactor"));
            Component scaler = ancestor.gameObject.GetComponent("CanvasScaler");
            if (scaler != null)
                report.Append(" referenceResolution=")
                      .Append(SafeText(scaler, "referenceResolution"));
            report.AppendLine();
            break;
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
        report.Append("screen=").Append(Screen.width).Append("x")
              .Append(Screen.height).AppendLine();
        AppendCanvasContext(root, report);
        int matchedDepTreeSprites = 0;
        RectTransform exactGraphRect = null;
        // Find an unambiguous graph-image anchor BEFORE dumping the bounded UI
        // tree so each visible label/icon can be expressed in relative graph UV.
        for (int k = 0; k < all.Length; k++)
        {
            Transform item = all[k];
            if (item == null || !item.gameObject.activeInHierarchy) continue;
            if (!IsExactNativeGraphGraphic(item.gameObject)) continue;
            matchedDepTreeSprites++;
            exactGraphRect = item as RectTransform;
        }
        if (matchedDepTreeSprites != 1 || exactGraphRect == null)
        {
            report.AppendLine("[ABCL TO-002] Exact native graph Sprite is missing or ambiguous. No overlay anchor.");
            exactGraphRect = null;
        }
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
            if (exactGraphRect != null && rect != null &&
                rect != exactGraphRect && rect.gameObject.activeInHierarchy)
            {
                // InverseTransformPoint handles actual Canvas scale, anchors,
                // aspect-ratio adaptation, pivot and parent translation.
                Rect nativeFrame = exactGraphRect.rect;
                if (nativeFrame.width > 0f && nativeFrame.height > 0f)
                {
                    Vector3 relative = exactGraphRect.InverseTransformPoint(rect.position);
                    float u = (relative.x - nativeFrame.xMin) / nativeFrame.width;
                    float v = (relative.y - nativeFrame.yMin) / nativeFrame.height;
                    if (u >= 0f && u <= 1f && v >= 0f && v <= 1f)
                        report.Append(" graphUV=(").Append(u.ToString("F3"))
                              .Append(",").Append(v.ToString("F3")).Append(")");
                }
            }
            Component img = t.gameObject.GetComponent("Image");
            if (img != null)
            {
                report.Append(" image=").Append(SafeText(img, "sprite"));
                Sprite sprite = TryReadSprite(img);
                if (sprite != null && sprite.name == "dep_tree")
                {
                    Rect sourceRect = sprite.rect;
                    report.Append(" [NATIVE_STATIC_GRAPH_SPRITE]")
                          .Append(" nativeRect=")
                          .Append(sourceRect.width.ToString("F1"))
                          .Append("x").Append(sourceRect.height.ToString("F1"));
                    if (sprite.texture != null)
                        report.Append(" backingTexture=")
                              .Append(sprite.texture.width).Append("x")
                              .Append(sprite.texture.height);
                    if (rect != null)
                    {
                        Rect displayed = rect.rect;
                        report.Append(" displayedRect=")
                              .Append(displayed.width.ToString("F1")).Append("x")
                              .Append(displayed.height.ToString("F1"))
                              .Append(" localScale=").Append(rect.localScale);
                        Vector3[] corners = new Vector3[4];
                        rect.GetWorldCorners(corners);
                        report.Append(" worldBL=").Append(corners[0])
                              .Append(" worldTR=").Append(corners[2]);
                    }
                }
            }
            Component rawImage = t.gameObject.GetComponent("RawImage");
            if (rawImage != null)
            {
                report.Append(" rawTexture=").Append(SafeText(rawImage, "texture"));
                Texture texture = TryReadRawTexture(rawImage);
                if (texture != null && texture.name == "dep_tree")
                    report.Append(" [NATIVE_STATIC_GRAPH_RAW_TEXTURE]")
                          .Append(" backingTexture=").Append(texture.width)
                          .Append("x").Append(texture.height);
            }
            Component text = t.gameObject.GetComponent("Text");
            if (text != null)
                report.Append(" text=").Append(SafeText(text, "text"));
            else
            {
                // Some game versions render labels using TextMeshPro. Reflection
                // keeps this diagnostic independent of optional TMP assemblies.
                Component tmp = t.gameObject.GetComponent("TextMeshProUGUI");
                if (tmp != null)
                    report.Append(" tmpText=").Append(SafeText(tmp, "text"));
            }
            report.AppendLine();
            if (report.Length > MaxOutputChars)
            {
                report.AppendLine("[ABCL TO-002] output capped by safety budget");
                break;
            }
        }
        if (count < all.Length) report.AppendLine("[ABCL TO-002] hierarchy truncated at 180 nodes");
        report.Append("dep_tree_sprite_matches=").Append(matchedDepTreeSprites).AppendLine();
        if (matchedDepTreeSprites != 1)
            report.AppendLine("[ABCL TO-002] No unambiguous dep_tree sprite anchor; DO NOT infer overlay placement.");
        else
            report.AppendLine("[ABCL TO-002] graphUV values are read-only relative positions, NOT approved node/edge locations.");
        Debug.Log(report.ToString());
    }
}
