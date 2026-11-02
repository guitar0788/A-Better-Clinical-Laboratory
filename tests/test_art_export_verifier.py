"""Security and correctness tests for the offline SVG export verifier."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "tools" / "verify_art_exports.py"
SPEC = importlib.util.spec_from_file_location("art_export_verifier", VERIFIER)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SvgExportVerifierTests(unittest.TestCase):
    def test_standard_svg_namespace_and_local_gradient_are_allowed(self):
        safe = '''<svg xmlns="http://www.w3.org/2000/svg"
          width="128" height="128" viewBox="0 0 128 128">
          <defs><linearGradient id="shell"><stop stop-color="#ffffff"/>
          <stop offset="1" stop-color="#aabbcc"/></linearGradient></defs>
          <path d="M 5 5 L 40 5 L 40 40 Z" fill="url(#shell)"
                stroke="#334455"/>
        </svg>'''
        root = MODULE.validate_svg_text(safe, "icp_ms_NW.svg")
        self.assertTrue(root.tag.endswith("svg"))

    def test_script_and_event_handlers_are_rejected(self):
        script = '''<svg xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 128 128"><script>alert(1)</script></svg>'''
        event = '''<svg xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 128 128" onload="alert(1)"><path d="M0 0"/></svg>'''
        with self.assertRaisesRegex(ValueError, "Unsupported/active"):
            MODULE.validate_svg_text(script, "icp_ms_NW.svg")
        with self.assertRaisesRegex(ValueError, "Event handler"):
            MODULE.validate_svg_text(event, "icp_ms_NW.svg")

    def test_external_images_and_paint_references_are_rejected(self):
        external_image = '''<svg xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 128 128"><image href="https://example.invalid/a.png"/></svg>'''
        external_paint = '''<svg xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 128 128"><path d="M0 0" fill="url(https://example.invalid/a.svg#x)"/></svg>'''
        data_uri = '''<svg xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 128 128"><path d="M0 0" fill="data:image/png;base64,AA=="/></svg>'''
        for candidate in (external_image, external_paint, data_uri):
            with self.subTest(candidate=candidate):
                with self.assertRaises(ValueError):
                    MODULE.validate_svg_text(candidate, "icp_ms_NW.svg")

    def test_doctype_and_entity_declarations_are_rejected(self):
        unsafe = '''<!DOCTYPE svg [<!ENTITY x SYSTEM "file:///etc/passwd">]>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
          <text>&x;</text></svg>'''
        with self.assertRaisesRegex(ValueError, "DTD/entities"):
            MODULE.validate_svg_text(unsafe, "icp_ms_NW.svg")


if __name__ == "__main__":
    unittest.main()
