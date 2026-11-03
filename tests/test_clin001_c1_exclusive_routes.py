"""Synthetic C1 source-isolation contracts; no proprietary game XML."""
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1] / "tools"))
from audit_clin001_c1_exclusive_routes import audit_from_records

ROOM = b'<Database><GameDBRoomType ID="ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB"><Tags><Tag>stat_lab</Tag><Tag>lab_specialist_workspace</Tag><Tag>abcl_g1_toxicology_lab</Tag></Tags></GameDBRoomType></Database>'
OWN = b'<Database><GameDBExamination ID="EXM_ABCL_C1_SAMPLING"><LabTestingExaminationRef>EXM_ABCL_C1_TESTING</LabTestingExaminationRef></GameDBExamination><GameDBExamination ID="EXM_ABCL_C1_TESTING"><Procedure><RequiredRoomTags><Tag>abcl_g1_toxicology_lab</Tag></RequiredRoomTags></Procedure></GameDBExamination></Database>'

def source(tags, name="EXM_CBC_TESTING", direct=None):
    tags=''.join('<Tag>'+t+'</Tag>' for t in tags)
    types='<RequiredRoomTypeList><RequiredRoomTypeRef>'+direct+'</RequiredRoomTypeRef></RequiredRoomTypeList>' if direct else ''
    return ET.fromstring('<GameDBExamination ID="'+name+'"><Procedure><RequiredRoomTags>'+tags+'</RequiredRoomTags>'+types+'</Procedure></GameDBExamination>')

def sampling():
    return ET.fromstring('<GameDBExamination ID="EXM_CBC_SAMPLING"><LabTestingExaminationRef>EXM_CBC_TESTING</LabTestingExaminationRef></GameDBExamination>')

class NativeRoutes(unittest.TestCase):
    def test_native_cbc_separated_by_private_room_tag(self):
        report=audit_from_records([('base',sampling()),('base',source(['deprecated_lab','hematology_lab']))],ROOM,OWN)
        self.assertTrue(report['native_tag_isolation_l2_pass'])
        self.assertEqual(report['distinct_vanilla_test_ids'],1)
    def test_shared_stat_lab_tag_is_a_real_failure(self):
        report=audit_from_records([('base',sampling()),('base',source(['stat_lab']))],ROOM,OWN)
        self.assertFalse(report['native_tag_isolation_l2_pass'])
        self.assertEqual(report['vanilla_tests_with_matching_abcl_room'][0]['exam'],'EXM_CBC_TESTING')
    def test_undefined_native_room_tags_must_not_pass(self):
        report=audit_from_records([('base',sampling()),('base',source([]))],ROOM,OWN)
        self.assertFalse(report['native_tag_isolation_l2_pass'])
        self.assertTrue(report['vanilla_tests_unresolved_or_unscoped'])
    def test_direct_room_requirement_is_a_collision(self):
        report=audit_from_records([('base',sampling()),('base',source(['hematology_lab'],direct='ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB'))],ROOM,OWN)
        self.assertFalse(report['native_tag_isolation_l2_pass'])
    def test_missing_private_abcl_tag_blocks_c1(self):
        bad=OWN.replace(b'abcl_g1_toxicology_lab',b'hematology_lab')
        report=audit_from_records([('base',sampling()),('base',source(['hematology_lab']))],ROOM,bad)
        self.assertFalse(report['native_tag_isolation_l2_pass'])
    def test_missing_native_testing_target_blocks(self):
        with self.assertRaises(ValueError):audit_from_records([('base',sampling())],ROOM,OWN.replace(b'EXM_ABCL_C1_TESTING\"><Procedure',b'OTHER_TESTING\"><Procedure'))

if __name__=='__main__':unittest.main()
