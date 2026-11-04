#!/usr/bin/env python3
"""Generate additive ABCL G2 test-only medical XML from pinned G1 source.

Never reads/writes original game's installed Database. Source-only output is
not a playable/tested add-on without two exact FA instruments, optional
icons, a G1 compiled DLL, and genuine game L4 acceptance.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

TESTS = {
    # Preserve the private G2 *_EXPOSURE database IDs: independent GM/asset
    # branches still reference them. Names and medical content describe actual
    # clinical conditions; internal legacy IDs do not become player-facing.
    # Probabilities are simplified game presentation, not epidemiology.
    "CADMIUM": dict(sampling="EXM_ABCL_G2_BLOOD_CADMIUM_SAMPLING",
                    testing="EXM_ABCL_G2_BLOOD_CADMIUM_TESTING",
                    diagnosis="DIA_ABCL_G2_CADMIUM_EXPOSURE",
                    symptom="SYM_ABCL_G2_CADMIUM_ELEVATED",
                    shared=("SYM_ABDOMINAL_CRAMPS","SYM_NAUSEA",
                            "SYM_VOMITING","SYM_DIARRHEA","SYM_DEHYDRATION"),
                    probabilities=(95,85,75,65,30),
                    exams=("EXM_ABDOMINAL_PALPATION",),
                    treatments=("TRT_REHYDRATION","TRT_STOMACHICS",
                                "TRT_HOSPITALIZATION_OBSERVATION"),
                    duration=2,icon="cadmium",digestion=True,payment=550),
    "MERCURY": dict(sampling="EXM_ABCL_G2_URINE_MERCURY_SAMPLING",
                    testing="EXM_ABCL_G2_URINE_MERCURY_TESTING",
                    diagnosis="DIA_ABCL_G2_MERCURY_EXPOSURE",
                    symptom="SYM_ABCL_G2_MERCURY_ELEVATED",
                    shared=("SYM_TREMOR","SYM_IRRITABILITY","SYM_HEADACHE",
                            "SYM_FATIGUE","SYM_PROTEINURIA"),
                    probabilities=(95,85,65,60,30),
                    # Urinalysis stays in the ORIGINAL histology lab; it is
                    # supportive renal evaluation, not an ABCL toxicology test.
                    exams=("EXM_URINE_SAMPLE_ANALYSIS_SAMPLING",),
                    treatments=("TRT_REST","TRT_HOSPITALIZATION_OBSERVATION",
                                "TRT_CHELATION_THERAPY"),
                    duration=14,icon="mercury",digestion=False,payment=600),
}
STRINGS = {
 "en":{
  "EXM_ABCL_G2_BLOOD_CADMIUM_SAMPLING":("Blood cadmium sample","Collect whole blood to assess recent cadmium exposure."),
  "EXM_ABCL_G2_BLOOD_CADMIUM_TESTING":("Blood cadmium level","Prepare and analyze a blood sample for cadmium by ICP-MS."),
  "EXM_ABCL_G2_URINE_MERCURY_SAMPLING":("Urine mercury sample","Collect urine for assessment of mercury exposure."),
  "EXM_ABCL_G2_URINE_MERCURY_TESTING":("Urine mercury level","Measure urinary mercury concentration by ICP-MS."),
  "DIA_ABCL_G2_CADMIUM_EXPOSURE":("Acute cadmium poisoning","Acute gastrointestinal toxicity after ingestion of cadmium salts."),
  "DIA_ABCL_G2_MERCURY_EXPOSURE":("Chronic elemental mercury poisoning","Chronic toxicity from mercury vapor with neurologic and possible renal symptoms."),
  "SYM_ABCL_G2_CADMIUM_ELEVATED":("Elevated blood cadmium","Indicates recent cadmium exposure; correlate with acute gastrointestinal illness."),
  "SYM_ABCL_G2_MERCURY_ELEVATED":("Elevated urinary mercury","Supports elemental/inorganic mercury exposure; alone does not prove poisoning.")},
 "zh-Hans":{
  "EXM_ABCL_G2_BLOOD_CADMIUM_SAMPLING":("血镉采样","采集全血标本，评估近期镉暴露。"),
  "EXM_ABCL_G2_BLOOD_CADMIUM_TESTING":("血镉测定","经样本前处理后，使用质谱分析血镉浓度。"),
  "EXM_ABCL_G2_URINE_MERCURY_SAMPLING":("尿汞采样","采集尿液标本，辅助评估汞暴露。"),
  "EXM_ABCL_G2_URINE_MERCURY_TESTING":("尿汞测定","使用质谱分析尿汞浓度。"),
  "DIA_ABCL_G2_CADMIUM_EXPOSURE":("急性镉中毒","摄入镉盐后出现急性胃肠道损伤，需结合病史和血镉结果判断。"),
  "DIA_ABCL_G2_MERCURY_EXPOSURE":("慢性元素汞中毒","长期吸入汞蒸气所致，可出现震颤、行为改变和肾脏损害。"),
  "SYM_ABCL_G2_CADMIUM_ELEVATED":("血镉升高","提示近期接触镉，需结合急性胃肠道症状判断，不能单凭数值确诊。"),
  "SYM_ABCL_G2_MERCURY_ELEVATED":("尿汞升高","提示元素汞或无机汞暴露，需结合临床表现，不能单凭数值确诊。")}
}
PROCEDURE_STEPS={
 "LEAD":("stat_lab_exam","abcl_art001_icp_ms","biohazard_trash","clean_hands"),
 "CADMIUM":("stat_lab_exam","abcl_art001_digestion","abcl_art001_icp_ms","biohazard_trash","clean_hands"),
 "MERCURY":("stat_lab_exam","abcl_art001_icp_ms","biohazard_trash","clean_hands")
}
ICON_NAMES=("cadmium","mercury")  # only new DIAGNOSIS+MAIN SYMPTOM icons
# V2 owner-review assets: pure-white vanilla-size flat sprites; not yet game L4.
ICON_SOURCE_SHA={
 "cadmium_64.png":"b93bc9e188146aa392e48585eeb2c162efa167ab836f0b2532b0feedc94c3a48",
 "cadmium_32.png":"81561399b2a88921a01741dae978c7f223f24ba03e82d1d8c516ddb19bc9d774",
 "mercury_64.png":"bd5d12d9edc5f1fce126687cdbcedd54ad81e4802c913e8d7104d03a8b7e3afc",
 "mercury_32.png":"8613ea09713ea577feb6d9bb507dc0ebfd05dd0727f43b21cdb35896db93201d",
}

def sub(p,k,value):
    e=ET.SubElement(p,k);e.text=str(value);return e

def findentry(root,kind,id):
    matches=[x for x in root.findall(kind) if x.get("ID")==id]
    if len(matches)!=1:raise ValueError("Expected one additive G1 source "+id)
    return matches[0]

def dump(root,out,name):
    out.mkdir(parents=True,exist_ok=True)
    data=ET.tostring(root,encoding="utf-8",xml_declaration=True)
    (out/name).write_bytes(data)

def generate(g1:Path,out:Path,icons:Path|None=None):
    g1=Path(g1);out=Path(out)
    if out.exists():raise FileExistsError("Refuse to overwrite another test snapshot")
    if any(s.lower() in {"streamingassets","addons","projecthospital_data"} for s in out.parts):
        raise ValueError("Never generate content inside installed game")
    ex=ET.parse(g1/"ModExaminations.xml").getroot()
    lead=findentry(ex,"GameDBExamination","EXM_ABCL_G1_BLOOD_LEAD_TESTING")
    tags=[x for x in lead.findall("Procedure/RequiredEquipmentList/RequiredEquipment/Tag") if x.text=="hematoanalyzer"]
    if len(tags)!=1:raise ValueError("G1 blood-lead source is no longer the tested original route")
    tags[0].text="abcl_art001_icp_ms"
    original_sampling=findentry(ex,"GameDBExamination","EXM_ABCL_G1_BLOOD_LEAD_SAMPLING")
    room=ET.parse(g1/"ModRoomTypes.xml").getroot()
    lab=findentry(room,"GameDBRoomType","ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB")
    req=lab.find("RequiredEquipment")
    if req is None:raise ValueError("G1 room no longer has original equipment list")
    orig_req={e.findtext("Tag"):e.findtext("MinCount") for e in req.findall("GameDBRequiredEquipment")}
    if any(orig_req.get(tag)!="1" for tag in ("ui_hematoanalyzer","ui_ria","thermal_cycler")):
        raise ValueError("Original G1/RIA/CBC room requirements changed")
    for tag in ("abcl_art001_icp_ms","abcl_art001_digestion"):
        if tag in orig_req:raise ValueError("Private G2 equipment already present; refuse duplicate")
        e=ET.SubElement(req,"GameDBRequiredEquipment");sub(e,"Tag",tag);sub(e,"MinCount",0)
    fresh=ET.Element("Database")
    for key,meta in TESTS.items():
        if key=="CADMIUM":
            sampling=copy.deepcopy(original_sampling)
            sampling.set("ID",meta["sampling"])
            sampling.find("AbbreviationLocID").text=meta["sampling"]+"_DESCRIPTION"
        else:
            sampling=ET.Element("GameDBExamination",ID=meta["sampling"])
            sub(sampling,"AbbreviationLocID",meta["sampling"]+"_DESCRIPTION")
            sub(sampling,"DiscomfortLevel","Low")
            p=ET.SubElement(sampling,"Procedure")
            sub(p,"StaffSelectionRules","REQUIRED_ROOM_OR_DEFAULT_ROOM")
            q=ET.SubElement(p,"RequiredDoctorQualificationList")
            sub(q,"SkillRef","SKILL_DOC_QUALIF_GENERAL_MEDICINE")
            r=ET.SubElement(p,"RequiredEquipmentList")
            for tag in ("sit_exam","doc_equipment","clean_hands"):
                z=ET.SubElement(r,"RequiredEquipment");sub(z,"Tag",tag)
            t=ET.SubElement(p,"RequiredRoomTags")
            for roomtag in ("examinations_basic_equipment","emergency_doctors_office","internal_medicine_office"):
                sub(t,"Tag",roomtag)
            sub(p,"ProcedureScript","ProcedureScriptExaminationUrineAnalysis")
            lie=ET.SubElement(p,"AnimationSetupLying")
            for tag,val in [("AnimationNameIn","stand_examination_in"),("AnimationNameIdle","stand_examination_idle"),("AnimationNameOut","stand_examination_out")]:
                sub(lie,tag,val)
            sitting=ET.SubElement(p,"AnimationSetupSitting")
            sub(sitting,"AnimationNameOut","stand_urine_sampling")
            sub(p,"DressLevel","FULL");sub(p,"Biohazard","true");sub(p,"Priority",21)
            sub(sampling,"Cost",50);sub(sampling,"IconIndex",1691);sub(sampling,"DurationHours",0)
        link=sampling.find("LabTestingExaminationRef")
        if link is None:link=ET.SubElement(sampling,"LabTestingExaminationRef")
        link.text=meta["testing"]
        # Examination UI uses original medical atlas icons (blood/urine);
        # never register a disease icon or a glossy equipment illustration.
        for field in ("CustomIconBigAssetRef","CustomIconSmallAssetRef"):
            existing=sampling.find(field)
            if existing is not None:sampling.remove(existing)
        fresh.append(sampling)
        testing=copy.deepcopy(lead);testing.set("ID",meta["testing"])
        testing.find("AbbreviationLocID").text=meta["testing"]+"_DESCRIPTION"
        testing.find("IconIndex").text="1641" if key=="CADMIUM" else "1691"
        r=testing.find("Procedure/RequiredEquipmentList")
        for existing in list(r):r.remove(existing)
        for tag in PROCEDURE_STEPS[key]:
            node=ET.SubElement(r,"RequiredEquipment")
            sub(node,"Tag",tag)
            sub(node,"DurationHours","0.15" if tag.startswith("abcl_art001_") else "0.1")
            sub(node,"BlocksSpecialist","false" if tag=="abcl_art001_icp_ms" else "true")
        for field in ("CustomIconBigAssetRef","CustomIconSmallAssetRef"):
            existing=testing.find(field)
            if existing is not None:testing.remove(existing)
        fresh.append(testing)
    symptomdb=ET.Element("Database")
    diseasedb=ET.Element("Database")
    for meta in TESTS.values():
        main=ET.SubElement(symptomdb,"GameDBSymptom",ID=meta["symptom"])
        for k,v in [("DescriptionLocID",meta["symptom"]+"_DESCRIPTION"),("DiscomfortLevel","None"),
                    ("PatientComplains","false"),("Hazard","Low"),("PatientMobility","MOBILE")]:
            sub(main,k,v)
        exs=ET.SubElement(main,"Examinations");sub(exs,"ExaminationRef",meta["testing"])
        tr=ET.SubElement(main,"Treatments");sub(tr,"TreatmentRef","TRT_REST")
        sub(main,"IsMainSymptom","true");sub(main,"ShameLevel",0);sub(main,"IconIndex",1169)
        illness=ET.SubElement(diseasedb,"GameDBMedicalCondition",ID=meta["diagnosis"])
        sub(illness,"AbbreviationLocID",meta["diagnosis"]+"_DESCRIPTION")
        sub(illness,"Duration",meta["duration"]);sub(illness,"OccurrenceRef","OCCURRENCE_RARE")
        # Experimental G2 diseases must remain explicit-GM-only until C2 and L4.
        # GameDBMedicalCondition.Disabled excludes them from vanilla random pools.
        sub(illness,"Disabled","true")
        illnesses=ET.SubElement(illness,"Symptoms")
        for ref,prob in [(meta["symptom"],100)]+list(zip(meta["shared"],meta["probabilities"])):
            rr=ET.SubElement(illnesses,"GameDBSymptomRules")
            sub(rr,"DayOfFirstOccurence",0);sub(rr,"ProbabilityPercent",prob);sub(rr,"GameDBSymptomRef",ref)
        exams=ET.SubElement(illness,"Examinations")
        for ref in ("EXM_INTERVIEW","EXM_PHYSICAL_AND_VISUAL_EXAMINATION",*meta["exams"],meta["sampling"]):
            sub(exams,"ExaminationRef",ref)
        tr=ET.SubElement(illness,"Treatments")
        for ref in meta["treatments"]:sub(tr,"TreatmentRef",ref)
        sub(illness,"IconIndex",1169)  # neutral vanilla droplet, not poisoning skull 1203
        sub(illness,"DepartmentRef","DPT_INTERNAL_MEDICINE_DEPARTMENT")
        sub(illness,"InsurancePayment",meta["payment"])
        categories=ET.SubElement(illness,"Tags")
        sub(categories,"Tag","disease");sub(categories,"Tag","clinic")
        for target in (main,illness):
            for size,field in [(64,"CustomIconBigAssetRef"),(32,"CustomIconSmallAssetRef")]:
                sub(target,field,"ASSET_ABCL_G2_"+meta["icon"].upper()+"_"+str(size))
    images=ET.Element("Database")
    for kind in ICON_NAMES:
        for size in (64,32):
            item=ET.SubElement(images,"GameDBAsset",ID=f"ASSET_ABCL_G2_{kind.upper()}_{size}")
            sub(item,"Type","TEXTURE_CUSTOM_SPRITE")
            sub(item,"File",f"MOD_ROOT/Assets/ABCL/MedicalIcons/{kind}_{size}.png")
    out.mkdir(parents=True)
    for filename,tree in [
        ("ModExaminations.xml",ex),("ModRoomTypes.xml",room),
        ("ModExaminationsG2.xml",fresh),("ModSymptomsG2.xml",symptomdb),
        ("ModDiagnosesG2.xml",diseasedb),("ModAssetListsG2.xml",images),
    ]:dump(tree,out,filename)
    for lang,values in STRINGS.items():
        db=ET.Element("Database")
        table=ET.SubElement(db,"GameDBStringTable",
                            ID="LOC_"+("EN" if lang=="en" else "ZHHANS")+"_ABCL_G2")
        sub(table,"LanguageCode",lang)
        sub(table,"LanguageNameLocalized","English" if lang=="en" else "简体中文")
        contributors=ET.SubElement(table,"Contributors");sub(contributors,"Name","ABCL medical design")
        strs=ET.SubElement(table,"LocalizedStrings")
        for id,(name,desc) in values.items():
            for suffix,val in (("",name),("_DESCRIPTION",desc)):
                row=ET.SubElement(strs,"GameDBLocalizedString")
                sub(row,"LocID",id+suffix);sub(row,"Text",val)
        dump(db,out,"ModStringTableEnG2.xml" if lang=="en" else "ModStringTableZhHansG2.xml")
    icon_report={}
    if icons:
        for name in ICON_SOURCE_SHA:
            src=Path(icons)/name
            if not src.is_file():raise ValueError("Missing exact original icon "+name)
            sha=hashlib.sha256(src.read_bytes()).hexdigest()
            if sha!=ICON_SOURCE_SHA[name]:raise ValueError("Icon source changed: "+name)
            from PIL import Image
            with Image.open(src) as im:
                if im.mode!="RGBA" or im.size!=(64 if name.endswith("_64.png") else 32,)*2:
                    raise ValueError("Incorrect medical icon size/mode")
            icon_report[name]=sha
    return {"new_conditions":[x["diagnosis"] for x in TESTS.values()],
            "three_native_assays":list(PROCEDURE_STEPS),"sha256":{
                p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(out.glob("*.xml"))},
            "icons":icon_report,"new_disease_exclusive_C2":"NOT_PROVEN",
            "native_L4":"NOT_RUN","g1_dll_rebuilt":False,
            "medical_review":"SOURCE_ONLY: CLINICAL SYNDROME PLUS ASSAY REQUIRED",
            "internal_diagnosis_ids_kept_stable":True}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--g1",type=Path,required=True,help="Pinned ABCL G1 addon source Database dir")
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--icons",type=Path,help="Exact original big/small clinical artwork (optional in CI)")
    a=p.parse_args()
    print(json.dumps(generate(a.g1,a.output,a.icons),indent=2,ensure_ascii=False))
