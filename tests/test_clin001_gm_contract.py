"""C1 game-fixture GM contract: must use existing trusted G1 test source/project."""
from pathlib import Path
import hashlib
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
TRUSTED_PROJECT_GIT_BLOB = '71daed7c3aa9e62edf9eea207fd77b2041be52ed'

class GMContract(unittest.TestCase):
    def test_pinned_project_hash_not_modified(self):
        raw = (SRC/'ABCL.G1.Panel.csproj').read_bytes()
        blob = ('blob %d\0' % len(raw)).encode('ascii') + raw
        self.assertEqual(hashlib.sha1(blob).hexdigest(),TRUSTED_PROJECT_GIT_BLOB,
                         'Protected-main G1 compiler rejects changed project')
        project = ET.fromstring(raw)
        include = {x.get('Include') for x in project.findall('.//Compile')}
        self.assertEqual(include,{'ABCLG1Panel.cs'})
        self.assertFalse((SRC/'ABCLSuperGmTestPanel.cs').exists())

    def test_chinese_gm_embedded_in_testonly_g1_panel(self):
        text=(SRC/'ABCLG1Panel.cs').read_text(encoding='utf-8')
        self.assertIn('internal sealed class ABCLSuperGmTestPanel',text)
        self.assertIn('private ABCLSuperGmTestPanel superGm',text)
        self.assertIn('superGm.Draw();',text)
        self.assertIn('中文超级GM',text)
        self.assertIn('仅测试版',text)
        self.assertIn('SpawnNativeLead(lead, insurer)',text)
        self.assertIn('SpawnOne()',text)

    def test_native_factory_safeguards(self):
        text=(SRC/'ABCLG1Panel.cs').read_text(encoding='utf-8')
        self.assertIn('forceAttempts < 5',text)
        self.assertIn('PatientMobility.MOBILE',text)
        self.assertIn('condition.HasImmobileSymptom()',text)
        # Prevent severe/immobile diagnoses from being spawned through
        # the MOBILE-only GM fixture before the native entity factory runs.
        fn=text[text.index('private void ForceMobilePatient()'):]
        self.assertLess(fn.index('if (condition.HasImmobileSymptom())'),
                        fn.index('forceAttempts++'))
        self.assertLess(fn.index('if (condition.HasImmobileSymptom())'),
                        fn.index('LopitalEntityFactory.CreateCharacterPatient('))
        self.assertIn('CreateCharacterPatient(',text)
        self.assertIn('Hospital.Instance.GetGroundFloor()',text)
        self.assertIn('!Database.Instance.Loaded',text)
        self.assertNotIn('m_immobileSpawnedToday =',text)
        self.assertNotIn('m_patientsSpawnedToday =',text)
        self.assertNotIn('ForceDiagnosis(',text)
        self.assertNotIn('SwitchLabProceduresToDeliveredToStatLab()',text)

    def test_no_extra_plugin(self):
        text=(SRC/'ABCL.G1.Panel.csproj').read_text(encoding='utf-8')
        self.assertNotIn('Harmony',text)
        self.assertNotIn('BepInEx',text)
        self.assertIn('<TargetFramework>net35</TargetFramework>',text)

if __name__=='__main__': unittest.main(verbosity=2)
