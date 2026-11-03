"""G2 heavy-metal toxicology native-source and no-vanilla-overwrite contracts."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

SCRIPT=Path(__file__).resolve().parents[1]/"tools/build_g2_clinical_overlay.py"
spec=importlib.util.spec_from_file_location("g2_native_records",SCRIPT)
g2=importlib.util.module_from_spec(spec);spec.loader.exec_module(g2)


def child(parent,name,text):
    e=ET.SubElement(parent,name);e.text=str(text);return e


def fixtures(path):
    source=Path(path);source.mkdir(parents=True,exist_ok=True)
    root=ET.Element("Database")
    for id in ("EXM_ABCL_G1_BLOOD_LEAD_SAMPLING","EXM_ABCL_G1_BLOOD_LEAD_TESTING"):
        e=ET.SubElement(root,"GameDBExamination",ID=id)
        child(e,"AbbreviationLocID",id+"_DESCRIPTION")
        child(e,"DiscomfortLevel","None")
        p=ET.SubElement(e,"Procedure")
        equipment=ET.SubElement(p,"RequiredEquipmentList")
        for tag in ("stat_lab_exam","hematoanalyzer","biohazard_trash","clean_hands"):
            row=ET.SubElement(equipment,"RequiredEquipment");child(row,"Tag",tag)
            child(row,"DurationHours",0.1);child(row,"BlocksSpecialist","true")
        room=ET.SubElement(p,"RequiredRoomTags");child(room,"Tag","abcl_g1_toxicology_lab")
        child(e,"IconIndex",1641);child(e,"DurationHours",2)
        if id.endswith("SAMPLING"):
            child(e,"LabTestingExaminationRef","EXM_ABCL_G1_BLOOD_LEAD_TESTING")
    ET.ElementTree(root).write(source/"ModExaminations.xml",encoding="utf-8")
    rooms=ET.Element("Database")
    r=ET.SubElement(rooms,"GameDBRoomType",ID="ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB")
    required=ET.SubElement(r,"RequiredEquipment")
    for tag in ("ui_hematoanalyzer","ui_ria","thermal_cycler"):
        row=ET.SubElement(required,"GameDBRequiredEquipment")
        child(row,"Tag",tag);child(row,"MinCount",1)
    ET.ElementTree(rooms).write(source/"ModRoomTypes.xml",encoding="utf-8")
    return source


class G2NativeClinicalSafety(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.src=fixtures(Path(self.temp.name)/"g1")
        self.out=Path(self.temp.name)/"out"
    def tearDown(self):self.temp.cleanup()
    def generated(self):
        meta=g2.generate(self.src,self.out)
        root=lambda x:ET.parse(self.out/x).getroot()
        return meta,root

    def test_three_pairs_and_exact_private_equipment_steps(self):
        meta,root=self.generated()
        self.assertEqual(set(meta["three_native_assays"]),{"LEAD","CADMIUM","MERCURY"})
        self.assertEqual(meta["new_disease_exclusive_C2"],"NOT_PROVEN")
        self.assertEqual(meta["native_L4"],"NOT_RUN")
        o=root("ModExaminations.xml")
        lead=[x for x in o if x.get("ID")=="EXM_ABCL_G1_BLOOD_LEAD_TESTING"][0]
        self.assertEqual([x.text for x in lead.findall("Procedure/RequiredEquipmentList/RequiredEquipment/Tag")],
                         list(g2.PROCEDURE_STEPS["LEAD"]))
        self.assertEqual(len(o.findall("GameDBExamination")),2)
        g=root("ModExaminationsG2.xml")
        for key,meta in g2.TESTS.items():
            items={x.get("ID"):x for x in g.findall("GameDBExamination")}
            self.assertEqual(items[meta["sampling"]].findtext("LabTestingExaminationRef"),
                             meta["testing"])
            test=items[meta["testing"]]
            self.assertEqual([x.text for x in test.findall("Procedure/RequiredEquipmentList/RequiredEquipment/Tag")],
                             list(g2.PROCEDURE_STEPS[key]))
            self.assertEqual(test.findtext("Procedure/RequiredRoomTags/Tag"),"abcl_g1_toxicology_lab")
        self.assertEqual(g.find("./GameDBExamination[@ID='EXM_ABCL_G2_URINE_MERCURY_SAMPLING']").findtext("Procedure/ProcedureScript"),"ProcedureScriptExaminationUrineAnalysis")

    def test_two_exposure_assessments_with_icons_and_no_claim_of_exclusive_diagnosis(self):
        _,root=self.generated()
        d=root("ModDiagnosesG2.xml").findall("GameDBMedicalCondition")
        s=root("ModSymptomsG2.xml").findall("GameDBSymptom")
        assets={e.get("ID"):e for e in root("ModAssetListsG2.xml")}
        self.assertEqual(len(d),len(s))
        self.assertEqual(len(d),2)
        self.assertEqual(len(assets),8)
        for condition in d:
            self.assertEqual(condition.findtext("OccurrenceRef"),"OCCURRENCE_RARE")
            self.assertEqual(condition.findtext("DepartmentRef"),"DPT_INTERNAL_MEDICINE_DEPARTMENT")
            self.assertIn("clinic",[x.text for x in condition.findall("Tags/Tag")])
            for icon in ("CustomIconBigAssetRef","CustomIconSmallAssetRef"):
                self.assertIn(condition.findtext(icon),assets)
            linked={x.get("ID"):x for x in s}
            refs=[x.findtext("GameDBSymptomRef") for x in condition.findall("Symptoms/GameDBSymptomRules")]
            main=[ref for ref in refs if ref in linked]
            self.assertEqual(len(main),1)
            self.assertEqual(linked[main[0]].findtext("IsMainSymptom"),"true")
            self.assertEqual(linked[main[0]].findtext("PatientMobility"),"MOBILE")

    def test_original_G1_room_mandatory_CBC_and_RIA_unchanged(self):
        _,root=self.generated()
        r=root("ModRoomTypes.xml")
        required={x.findtext("Tag"):x.findtext("MinCount")
                  for x in r.findall(".//RequiredEquipment/GameDBRequiredEquipment")}
        self.assertEqual(required["ui_hematoanalyzer"],"1")
        self.assertEqual(required["ui_ria"],"1")
        self.assertEqual(required["thermal_cycler"],"1")
        self.assertEqual(required["abcl_art001_icp_ms"],"0")
        self.assertEqual(required["abcl_art001_digestion"],"0")

    def test_localized_elements_match_eight_original_private_ids(self):
        _,root=self.generated()
        ids=[x.findtext("LocID") for x in root("ModStringTableEnG2.xml").findall(".//GameDBLocalizedString")]
        zh=[x.findtext("LocID") for x in root("ModStringTableZhHansG2.xml").findall(".//GameDBLocalizedString")]
        self.assertEqual(set(ids),set(zh))
        self.assertEqual(len(ids),16)
        self.assertNotIn("ABCL Test",str(ids))

    def test_wrong_G1_hematoanalyzer_baseline_rejected(self):
        ex=ET.parse(self.src/"ModExaminations.xml")
        ex.find(".//GameDBExamination[@ID='EXM_ABCL_G1_BLOOD_LEAD_TESTING']/Procedure/RequiredEquipmentList/RequiredEquipment/Tag[2]").text="some-other-device"
        ex.write(self.src/"ModExaminations.xml")
        with self.assertRaisesRegex(ValueError,"hematoanalyzer|original"):
            g2.generate(self.src,self.out)

    def test_missing_vanilla_RIA_requirement_rejected(self):
        rooms=ET.parse(self.src/"ModRoomTypes.xml")
        req=rooms.find(".//RequiredEquipment")
        for r in list(req):
            if r.findtext("Tag")=="ui_ria":req.remove(r)
        rooms.write(self.src/"ModRoomTypes.xml")
        with self.assertRaisesRegex(ValueError,"requirements changed"):
            g2.generate(self.src,self.out)

    def test_no_second_generation_overwrites_existing_output(self):
        self.generated()
        with self.assertRaisesRegex(FileExistsError,"overwrite"):
            g2.generate(self.src,self.out)

    def test_reject_writing_into_installed_game_streaming_assets(self):
        with self.assertRaisesRegex(ValueError,"installed game"):
            g2.generate(self.src,Path(self.temp.name)/"ProjectHospital_Data/StreamingAssets/Addons/G2")

    def test_fake_or_tampered_medical_icons_rejected(self):
        fake=Path(self.temp.name)/"icons";fake.mkdir()
        for name in g2.ICON_SOURCE_SHA:(fake/name).write_bytes(b"NOT A PNG")
        with self.assertRaisesRegex(ValueError,"Icon source changed"):
            g2.generate(self.src,self.out,icons=fake)

if __name__=="__main__":unittest.main()
