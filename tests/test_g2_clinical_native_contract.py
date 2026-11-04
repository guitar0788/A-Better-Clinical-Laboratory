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
        # Mirror the actual G1 distinction: the physician's blood draw
        # happens in an original office, while ABCL metal analysis has its
        # own private laboratory route. Never put hematoanalyzer on sampling.
        tags=(("sit_exam","doc_equipment","clean_hands") if id.endswith("SAMPLING")
              else ("stat_lab_exam","hematoanalyzer","biohazard_trash","clean_hands"))
        for tag in tags:
            row=ET.SubElement(equipment,"RequiredEquipment");child(row,"Tag",tag)
            child(row,"DurationHours",0.1);child(row,"BlocksSpecialist","true")
        room=ET.SubElement(p,"RequiredRoomTags")
        child(room,"Tag","examinations_basic_equipment" if id.endswith("SAMPLING")
              else "abcl_g1_toxicology_lab")
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
        self.assertEqual(meta["g1_lab_mode_preserved"],"legacy_test")
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
            for exam in (items[meta["sampling"]],test):
                self.assertIsNone(exam.find("CustomIconBigAssetRef"))
                self.assertIsNone(exam.find("CustomIconSmallAssetRef"))
            self.assertEqual(test.findtext("IconIndex"),
                             "1641" if key=="CADMIUM" else "1691")
            self.assertEqual([x.text for x in test.findall("Procedure/RequiredEquipmentList/RequiredEquipment/Tag")],
                             list(g2.PROCEDURE_STEPS[key]))
            self.assertEqual(test.findtext("Procedure/RequiredRoomTags/Tag"),"abcl_g1_toxicology_lab")
        self.assertEqual(g.find("./GameDBExamination[@ID='EXM_ABCL_G2_URINE_MERCURY_SAMPLING']").findtext("Procedure/ProcedureScript"),"ProcedureScriptExaminationUrineAnalysis")

    def test_two_named_poisoning_syndromes_with_unchanged_icons_and_no_C2_claim(self):
        _,root=self.generated()
        d=root("ModDiagnosesG2.xml").findall("GameDBMedicalCondition")
        s=root("ModSymptomsG2.xml").findall("GameDBSymptom")
        assets={e.get("ID"):e for e in root("ModAssetListsG2.xml")}
        self.assertEqual(len(d),len(s))
        self.assertEqual(len(d),2)
        self.assertEqual(len(assets),4)
        self.assertTrue(all("METALS_EXAM" not in key and "DIGESTION" not in key
                            for key in assets))
        self.assertEqual({x.findtext("File") for x in assets.values()},{
            "MOD_ROOT/Assets/ABCL/MedicalIcons/cadmium_64.png",
            "MOD_ROOT/Assets/ABCL/MedicalIcons/cadmium_32.png",
            "MOD_ROOT/Assets/ABCL/MedicalIcons/mercury_64.png",
            "MOD_ROOT/Assets/ABCL/MedicalIcons/mercury_32.png",
        })
        for condition in d:
            self.assertEqual(condition.findtext("IconIndex"),"1169")
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

    def test_specific_native_clinical_syndromes_and_probabilities(self):
        _, root = self.generated()
        conditions={x.get("ID"):x for x in root("ModDiagnosesG2.xml")}
        expected={
          "CADMIUM":("SYM_ABDOMINAL_CRAMPS","SYM_NAUSEA","SYM_VOMITING",
                     "SYM_DIARRHEA","SYM_DEHYDRATION"),
          "MERCURY":("SYM_TREMOR","SYM_IRRITABILITY","SYM_HEADACHE",
                     "SYM_FATIGUE","SYM_PROTEINURIA")
        }
        for key,meta in g2.TESTS.items():
            with self.subTest(syndrome=key):
                self.assertEqual(meta["shared"],expected[key])
                rows=conditions[meta["diagnosis"]].findall("./Symptoms/GameDBSymptomRules")
                self.assertEqual([r.findtext("GameDBSymptomRef") for r in rows],
                                 [meta["symptom"],*expected[key]])
                self.assertEqual([int(r.findtext("ProbabilityPercent")) for r in rows],
                                 [100,*meta["probabilities"]])
                self.assertEqual(conditions[meta["diagnosis"]].findtext("Duration"),
                                 str(meta["duration"]))
                self.assertEqual(conditions[meta["diagnosis"]].findtext("Disabled"),"true")
                self.assertEqual(conditions[meta["diagnosis"]].findtext("DepartmentRef"),
                                 "DPT_INTERNAL_MEDICINE_DEPARTMENT")

    def test_native_supporting_exams_stay_in_original_labs(self):
        _, root=self.generated()
        illnesses={x.get("ID"):x for x in root("ModDiagnosesG2.xml")}
        for key,meta in g2.TESTS.items():
            ids=[x.text for x in illnesses[meta["diagnosis"]].findall("./Examinations/ExaminationRef")]
            self.assertEqual(ids,["EXM_INTERVIEW","EXM_PHYSICAL_AND_VISUAL_EXAMINATION",
                                   *meta["exams"],meta["sampling"]])
            self.assertEqual(ids.count(meta["sampling"]),1)
            self.assertNotIn(meta["testing"],ids)
            self.assertNotIn("EXM_CBC_TESTING",ids)
        self.assertEqual(g2.TESTS["CADMIUM"]["exams"],("EXM_ABDOMINAL_PALPATION",))
        # Proteinuria must be tested in the *vanilla histology* lab;
        # this does not permit any vanilla test to execute in ABCL.
        self.assertEqual(g2.TESTS["MERCURY"]["exams"],
                         ("EXM_URINE_SAMPLE_ANALYSIS_SAMPLING",))
        g2_exams={e.get("ID") for e in root("ModExaminationsG2.xml")}
        self.assertNotIn("EXM_URINE_SAMPLE_ANALYSIS_SAMPLING",g2_exams)
        self.assertNotIn("EXM_URINE_SAMPLE_ANALYSIS_TESTING",g2_exams)

    def test_cadmium_no_chelation_mercury_only_conditional_treatment(self):
        _, root=self.generated()
        illnesses={x.get("ID"):x for x in root("ModDiagnosesG2.xml")}
        for key,meta in g2.TESTS.items():
            actual=tuple(x.text for x in illnesses[meta["diagnosis"]].findall("./Treatments/TreatmentRef"))
            self.assertEqual(actual,meta["treatments"])
            self.assertIn("TRT_HOSPITALIZATION_NORMAL",actual)
            self.assertEqual(actual[0],"TRT_HOSPITALIZATION_NORMAL")
            self.assertNotIn("TRT_HOSPITALIZATION_OBSERVATION",actual)
        self.assertNotIn("TRT_CHELATION_THERAPY",g2.TESTS["CADMIUM"]["treatments"])
        self.assertIn("TRT_REHYDRATION",g2.TESTS["CADMIUM"]["treatments"])
        self.assertIn("TRT_STOMACHICS",g2.TESTS["CADMIUM"]["treatments"])
        self.assertNotIn("TRT_REHYDRATION",g2.TESTS["MERCURY"]["treatments"])
        self.assertIn("TRT_CHELATION_THERAPY",g2.TESTS["MERCURY"]["treatments"])

    def test_disease_names_are_diagnoses_not_assessments_and_lab_findings_are_distinct(self):
        _, root=self.generated()
        def language(file):
            return {x.findtext("LocID"):x.findtext("Text")
                    for x in root(file).findall(".//GameDBLocalizedString")}
        en=language("ModStringTableEnG2.xml")
        zh=language("ModStringTableZhHansG2.xml")
        for key,m in g2.TESTS.items():
            self.assertIn("poisoning",en[m["diagnosis"]].lower())
            self.assertIn("中毒",zh[m["diagnosis"]])
            self.assertNotIn("exposure assessment",en[m["diagnosis"]].lower())
            self.assertNotIn("暴露评估",zh[m["diagnosis"]])
            self.assertIn("升高",zh[m["symptom"]])
            self.assertNotIn("中毒",zh[m["symptom"]])
            self.assertNotEqual(zh[m["testing"]],zh[m["diagnosis"]])
        self.assertIn("Acute cadmium poisoning",en.values())
        self.assertIn("Chronic elemental mercury poisoning",en.values())
        self.assertIn("急性镉中毒",zh.values())
        self.assertIn("慢性元素汞中毒",zh.values())
        # Preserve stable private IDs for G2 instrumentation and dispatch.
        self.assertTrue(all(m["diagnosis"].endswith("_EXPOSURE") for m in g2.TESTS.values()))

    def test_no_false_claim_of_lab_only_diagnosis_or_patient_L4(self):
        meta, root=self.generated()
        self.assertEqual(meta["new_disease_exclusive_C2"],"NOT_PROVEN")
        self.assertEqual(meta["native_L4"],"NOT_RUN")
        self.assertFalse(meta["g1_dll_rebuilt"])
        self.assertEqual(meta["medical_review"],"SOURCE_ONLY: CLINICAL SYNDROME PLUS ASSAY REQUIRED")
        for entry in root("ModDiagnosesG2.xml"):
            self.assertEqual(entry.findtext("Disabled"),"true")

    def test_g2_experimental_diseases_are_explicit_gm_only(self):
        # GameDBMedicalCondition.Disabled is the native random-generation gate.
        # The older C1 development fixture follows this same model.
        _, root = self.generated()
        conditions = root("ModDiagnosesG2.xml").findall("GameDBMedicalCondition")
        self.assertEqual({e.get("ID") for e in conditions},
                         {m["diagnosis"] for m in g2.TESTS.values()})
        self.assertTrue(all(e.findtext("Disabled") == "true"
                            for e in conditions))
        self.assertEqual({e.findtext("OccurrenceRef") for e in conditions},
                         {"OCCURRENCE_RARE"})
        # No vanilla patient cases or the original lead disease are overridden.
        self.assertEqual(len(conditions), 2)
        self.assertFalse(any(e.get("ID") == "TRM_LDP" for e in conditions))

    def test_generation_does_not_mutate_pinned_g1_source(self):
        from hashlib import sha256
        files = [self.src / "ModExaminations.xml",
                 self.src / "ModRoomTypes.xml"]
        before = {str(p): sha256(p.read_bytes()).hexdigest() for p in files}
        self.generated()
        self.assertEqual(before,
                         {str(p): sha256(p.read_bytes()).hexdigest()
                          for p in files})

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
        ex.find(".//GameDBExamination[@ID='EXM_ABCL_G1_BLOOD_LEAD_TESTING']").findall("Procedure/RequiredEquipmentList/RequiredEquipment/Tag")[1].text="some-other-device"
        ex.write(self.src/"ModExaminations.xml")
        with self.assertRaisesRegex(ValueError,"Unknown G1|hematoanalyzer|original"):
            g2.generate(self.src,self.out)

    def test_missing_vanilla_RIA_requirement_rejected(self):
        rooms=ET.parse(self.src/"ModRoomTypes.xml")
        req=rooms.find(".//RequiredEquipment")
        for r in list(req):
            if r.findtext("Tag")=="ui_ria":req.remove(r)
        rooms.write(self.src/"ModRoomTypes.xml")
        with self.assertRaisesRegex(ValueError,"requirements changed"):
            g2.generate(self.src,self.out)

    def test_current_standalone_g1_lead_is_never_downgraded(self):
        # Simulate the exact G1 private standalone device contract at the
        # 2026-11-04 tested feature head, without bundling game-owned files.
        ex=ET.parse(self.src/"ModExaminations.xml")
        lead=ex.find(".//GameDBExamination[@ID='EXM_ABCL_G1_BLOOD_LEAD_TESTING']")
        eq=lead.find("Procedure/RequiredEquipmentList")
        old=[x for x in eq.findall("RequiredEquipment") if x.findtext("Tag")=="hematoanalyzer"]
        self.assertEqual(len(old),1)
        before=old[0]
        index=list(eq).index(before);eq.remove(before)
        for tag in ("abcl_art001_digestion","abcl_art001_icp_ms"):
            node=ET.Element("RequiredEquipment")
            child(node,"Tag",tag)
            child(node,"DurationHours",0.1)
            child(node,"BlocksSpecialist","false")
            eq.insert(index,node);index+=1
        ex.write(self.src/"ModExaminations.xml")
        room=ET.parse(self.src/"ModRoomTypes.xml")
        required=room.find(".//RequiredEquipment")
        for row in list(required):
            if row.findtext("Tag") in ("ui_hematoanalyzer","ui_ria","thermal_cycler"):
                required.remove(row)
        for tag in ("abcl_art001_digestion","abcl_art001_icp_ms"):
            row=ET.SubElement(required,"GameDBRequiredEquipment")
            child(row,"Tag",tag);child(row,"MinCount",1)
        room.write(self.src/"ModRoomTypes.xml")
        meta,root=self.generated()
        self.assertEqual(meta["g1_lab_mode_preserved"],"standalone_g1")
        lead_out=root("ModExaminations.xml").find(
            "./GameDBExamination[@ID='EXM_ABCL_G1_BLOOD_LEAD_TESTING']")
        self.assertEqual([x.text for x in lead_out.findall(
            "./Procedure/RequiredEquipmentList/RequiredEquipment/Tag")],
            ["stat_lab_exam","abcl_art001_digestion","abcl_art001_icp_ms",
             "biohazard_trash","clean_hands"])
        room_out=root("ModRoomTypes.xml")
        actual={x.findtext("Tag"):x.findtext("MinCount")
                for x in room_out.findall(".//RequiredEquipment/GameDBRequiredEquipment")}
        self.assertEqual(actual["abcl_art001_digestion"],"1")
        self.assertEqual(actual["abcl_art001_icp_ms"],"1")
        for old in ("ui_hematoanalyzer","ui_ria","thermal_cycler"):
            self.assertNotIn(old,actual)
        self.assertEqual(len(actual),2)
        # The new private G2 assays never include the vanilla analyzer.
        g2_assays=root("ModExaminationsG2.xml")
        self.assertFalse(any(x.text=="hematoanalyzer" for x in
            g2_assays.findall(".//RequiredEquipment/Tag")))

    def test_current_standalone_baseline_does_not_allow_hybrid_devices(self):
        ex=ET.parse(self.src/"ModExaminations.xml")
        lead=ex.find(".//GameDBExamination[@ID='EXM_ABCL_G1_BLOOD_LEAD_TESTING']")
        lead.findall("Procedure/RequiredEquipmentList/RequiredEquipment/Tag")[1].text="abcl_art001_digestion"
        ex.write(self.src/"ModExaminations.xml")
        with self.assertRaisesRegex(ValueError,"Unknown G1"):
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
