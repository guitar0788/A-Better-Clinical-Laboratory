"""Reject old glossy diagnosis icons, miscategorized equipment and poisoning fallback."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location(
    "g2_v2",ROOT/"tools/build_g2_clinical_overlay.py")
g2=importlib.util.module_from_spec(spec)
spec.loader.exec_module(g2)
from test_g2_clinical_native_contract import fixtures


class CorrectedMedicalIconContract(unittest.TestCase):
    def test_only_two_new_disease_symbol_pairs(self):
        self.assertEqual(set(g2.ICON_NAMES),{"cadmium","mercury"})
        self.assertEqual(set(g2.ICON_SOURCE_SHA),
            {"cadmium_64.png","cadmium_32.png","mercury_64.png","mercury_32.png"})
        script=(ROOT/"tools/build_g2_clinical_overlay.py").read_text()
        self.assertNotIn("ASSET_ABCL_G2_METALS_EXAM_",script)
        self.assertNotIn('("cadmium","mercury","metals_exam","digestion")',script)

    def test_native_exam_glyphs_and_non_poisoning_fallback(self):
        with tempfile.TemporaryDirectory() as temp:
            src=fixtures(Path(temp)/"G1")
            out=Path(temp)/"G2"
            g2.generate(src,out)
            atlas=ET.parse(out/"ModAssetListsG2.xml").getroot()
            self.assertEqual(len(atlas.findall("GameDBAsset")),4)
            for file in ("ModDiagnosesG2.xml","ModSymptomsG2.xml"):
                root=ET.parse(out/file).getroot()
                for item in root:
                    self.assertEqual(item.findtext("IconIndex"),"1169")
                    for kind in ("CustomIconBigAssetRef","CustomIconSmallAssetRef"):
                        self.assertIn(item.findtext(kind),{
                            a.get("ID") for a in atlas})
            for file in ("ModExaminationsG2.xml","ModExaminations.xml"):
                for exam in ET.parse(out/file).getroot():
                    self.assertIsNone(exam.find("CustomIconBigAssetRef"))
                    self.assertIsNone(exam.find("CustomIconSmallAssetRef"))

    def test_source_svg_is_original_flat_white_only(self):
        for element in ("cadmium","mercury"):
            text=(ROOT/f"assets/g2/disease_icons_v2/{element}.svg").read_text()
            root=ET.fromstring(text)
            self.assertEqual(root.attrib.get("viewBox"),"0 0 64 64")
            self.assertIn("#FFFFFF",text)
            for forbidden in ("linearGradient","radialGradient","<image",
                              "filter","shadow","base64,","<text"):
                self.assertNotIn(forbidden,text)

if __name__=="__main__":
    unittest.main()
