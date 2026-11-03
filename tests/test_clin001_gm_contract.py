"""Enforce G1 Chinese GM build scope: included in test DLL only."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'

class GMContract(unittest.TestCase):
    def test_gm_component_is_compiled_into_test_dll(self):
        project = ET.parse(SRC / 'ABCL.G1.Panel.csproj').getroot()
        include={e.get('Include') for e in project.findall('.//Compile')}
        self.assertIn('ABCLG1Panel.cs',include)
        self.assertIn('ABCLSuperGmTestPanel.cs',include)
        defs=[(e.text or '') for e in project.findall('.//DefineConstants')]
        self.assertTrue(any('ABCL_GM_TEST_ONLY' in d for d in defs))
    def test_gm_compiled_conditionally_without_original_control_regression(self):
        text=(SRC / 'ABCLSuperGmTestPanel.cs').read_text(encoding='utf-8')
        panel=(SRC / 'ABCLG1Panel.cs').read_text(encoding='utf-8')
        self.assertTrue(text.startswith('using System;'))
        self.assertIn('#if ABCL_GM_TEST_ONLY',text)
        self.assertIn('#if ABCL_GM_TEST_ONLY',panel)
        self.assertIn('superGm.Draw();',panel)
        self.assertIn('SpawnNativeLead(lead, insurer)',panel)
        self.assertIn('SpawnOne()',panel)
        self.assertIn('中文超级GM',text)
    def test_quota_override_is_separate_from_native_scene_safety(self):
        text=(SRC / 'ABCLSuperGmTestPanel.cs').read_text(encoding='utf-8')
        self.assertIn('forceAttempts < 5',text)
        self.assertIn('PatientMobility.MOBILE',text)
        self.assertIn('CreateCharacterPatient(',text)
        self.assertIn('Hospital.Instance.GetGroundFloor()',text)
        self.assertIn('!Database.Instance.Loaded',text)
        self.assertNotIn('m_immobileSpawnedToday =',text)
        self.assertNotIn('m_patientsSpawnedToday =',text)
        self.assertNotIn('ForceDiagnosis(',text)
        self.assertNotIn('SwitchLabProceduresToDeliveredToStatLab()',text)
    def test_no_extra_third_party_dependency(self):
        project=(SRC / 'ABCL.G1.Panel.csproj').read_text(encoding='utf-8')
        self.assertNotIn('Harmony',project)
        self.assertNotIn('BepInEx',project)
        self.assertIn('<TargetFramework>net35</TargetFramework>',project)

if __name__ == '__main__': unittest.main()
