"""TO-002 one-shot native hierarchy probe: source-only safety checks.

No Unity editor, game DLL compile, or actual dependency-graph extension claimed.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROBE = (ROOT / "src" / "ABCLTO002ReadOnlyTreeProbe.cs").read_text("utf-8")
CORE = (ROOT / "src" / "ABCLG1Panel.cs").read_text("utf-8")
PROJECT = (ROOT / "src" / "ABCL.G1.Panel.csproj").read_text("utf-8")


class TO002NativeTreeProbeContract(unittest.TestCase):
    def test_compile_path_and_one_shot_bounded_trigger(self):
        self.assertIn('<Compile Include="ABCLTO002ReadOnlyTreeProbe.cs" />', PROJECT)
        self.assertIn("to002TreeProbe.ScanIfVisible();", CORE)
        for t in (
            "DependencyTreePanelController",
            "gameObject.activeInHierarchy",
            "FindObjectsOfType<DependencyTreePanelController>()",
            "Time.unscaledTime + 2f",
            "private const int MaxNodes = 180",
            "private const int MaxOutputChars = 24000",
            "root.GetComponentsInChildren<Transform>(true)",
            "captured = true",
            "RectTransform",
            "SafeText(img, \"sprite\")",
            "SafeText(text, \"text\")",
        ):
            self.assertIn(t, PROBE, t)

    def test_exact_serialized_static_sprite_anchor_is_read_only_and_scaled(self):
        # Vanilla resources.assets contains a Texture2D and Sprite named
        # dep_tree (1400 x 620). The code must *observe* the actual native
        # RectTransform/canvas, never guess positions from a screenshot.
        for token in (
            'sprite.name == "dep_tree"',
            "TryReadSprite(img)",
            "sourceRect.width",
            "sourceRect.height",
            "sprite.texture.width",
            "sprite.texture.height",
            "rect.GetWorldCorners(corners)",
            "displayedRect=",
            "Screen.width",
            "Screen.height",
            "GetComponent(\"Canvas\")",
            "GetComponent(\"CanvasScaler\")",
            "dep_tree_sprite_matches=",
            "DO NOT infer an overlay anchor",
        ):
            self.assertIn(token, PROBE, token)
        self.assertNotIn("GetPixels", PROBE)
        self.assertNotIn("Texture2D.LoadImage", PROBE)

    def test_no_scene_mutations_or_extra_binaries(self):
        forbidden = (
            "SetActive(", "Instantiate(", "Destroy(", "SetParent(",
            ".anchoredPosition =", ".sizeDelta =", "GetComponent<Renderer>().material",
            ".sprite =", "Patch(", "Save(", "File.Write", "Directory.Create",
            "PlayerPrefs.", "Harmony",
        )
        for item in forbidden:
            self.assertNotIn(item, PROBE, item)
        self.assertNotIn("DllImport", PROBE)
        self.assertNotIn("UnityEngine.UI", PROJECT)


if __name__ == "__main__":
    unittest.main()
