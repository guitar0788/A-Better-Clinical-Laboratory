"""ART-001 antialiased SVG candidate tests. NOT a gameplay/L4 assertion."""
import importlib.util
import hashlib
import tempfile
import unittest
from pathlib import Path
try:
    from PIL import Image
    import cairosvg  # noqa: F401
    VECTOR_DEPS_AVAILABLE = True
except ImportError:
    Image = None
    VECTOR_DEPS_AVAILABLE = False

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools" / "generate_art_001_svg.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("art001_svg", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Art001SmoothStyleTests(unittest.TestCase):
    @unittest.skipUnless(VECTOR_DEPS_AVAILABLE, "Offline vector renderer dependencies are not installed")
    def test_original_editable_svg_and_four_distinct_directions(self):
        generator = load_generator()
        for device in generator.DEVICES:
            svg_list = [generator.make_svg(device, d) for d in generator.DIRECTIONS]
            self.assertEqual(len(set(svg_list)), 4)
            for item in svg_list:
                self.assertIn("viewBox=\"0 0 128 128\"", item)
                self.assertNotIn("StreamingAssets/", item)
                self.assertNotIn("ABCL Mass Spectrometer", item)

    @unittest.skipUnless(VECTOR_DEPS_AVAILABLE, "Offline vector renderer dependencies are not installed")
    def test_smooth_antialias_native_atlas_manifest(self):
        generator = load_generator()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifest = generator.generate(root)
            self.assertEqual(manifest["atlas_layout"], "LAYOUT_16_X_8")
            self.assertEqual(manifest["schema"], "ABCL-ART-001-v3-detail-review-only")
            atlas_file = root / "Assets" / "ABCL" / "equipment_atlas.png"
            atlas = Image.open(atlas_file).convert("RGBA")
            self.assertEqual(atlas.size, (2048, 1024))
            self.assertEqual(hashlib.sha256(atlas_file.read_bytes()).hexdigest(),
                             manifest["sha256"]["equipment_atlas.png"])
            frames = []
            for i in range(8):
                tile = atlas.crop((i*128, 0, (i+1)*128, 128))
                alpha = tile.getchannel("A")
                bbox = alpha.getbbox()
                self.assertIsNotNone(bbox)
                self.assertGreaterEqual(bbox[2] - bbox[0], 65)
                self.assertLessEqual(bbox[2] - bbox[0], 108)
                self.assertGreaterEqual(bbox[3] - bbox[1], 48)
                self.assertLessEqual(bbox[3] - bbox[1], 95)
                # Proves real 4x vector rasterization, not solid chunky pixels.
                self.assertGreater(sum(0 < v < 255 for v in alpha.getdata()), 100)
                frames.append(tile.tobytes())
            self.assertEqual(len(set(frames)), 8)
            self.assertEqual(
                Image.open(root / "Previews" / "ABCL" /
                           "direction_preview.png").size, (1024, 256))
            self.assertEqual(len(list((root / "Sources" / "ABCL").glob("*.svg"))), 8)

    def test_does_not_include_vanilla_original_sprites(self):
        src = GENERATOR.read_text(encoding="utf-8")
        self.assertNotIn("objects_small_atlas.png", src)
        self.assertNotIn("OBJECT_HEMATOLOGY_ANALYZER", src)
        self.assertNotIn("OBJECT_RIA", src)


if __name__ == "__main__":
    unittest.main()
