#!/usr/bin/env python3
"""Generate a review-only native TRM_LDP override outside original game files."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

DIAGNOSIS_ID = "TRM_LDP"
EXAM_ID = "EXM_ABCL_G1_BLOOD_LEAD_SAMPLING"
REQUIRED_SYMPTOM = "SYM_LEAD_LEVELS_HIGH"
REQUIRED_TREATMENTS = {"TRT_CHELATION_THERAPY", "TRT_HOSPITALIZATION_HIGH_PRIORITY"}
DEPARTMENT_ID = "DPT_INTERNAL_MEDICINE_DEPARTMENT"


def prepare(source: Path, destination: Path) -> dict:
    source = source.resolve(strict=True)
    destination = destination.resolve()
    if source == destination or source in destination.parents:
        raise ValueError("Refusing to write into the original diagnosis file or source directory")
    if destination.exists():
        raise FileExistsError("Output already exists; refusing to overwrite")
    data = source.read_bytes()
    root = ET.fromstring(data)
    nodes = [n for n in root.iter("GameDBMedicalCondition") if n.get("ID") == DIAGNOSIS_ID]
    if len(nodes) != 1:
        raise ValueError(f"Expected one native {DIAGNOSIS_ID}, found {len(nodes)}")
    entry = nodes[0]
    if entry.findtext("DepartmentRef") != DEPARTMENT_ID:
        raise ValueError("Native lead case department differs from reviewed version")
    symptoms = entry.findall("./Symptoms/GameDBSymptomRules")
    lead = [s for s in symptoms if s.findtext("GameDBSymptomRef") == REQUIRED_SYMPTOM]
    if len(lead) != 1 or lead[0].findtext("ProbabilityPercent") != "100":
        raise ValueError("Lead symptom probability not the reviewed 100%")
    treatments = {t.text for t in entry.findall("./Treatments/TreatmentRef")}
    if not REQUIRED_TREATMENTS.issubset(treatments):
        raise ValueError("Native treatment requirements changed")
    exams = entry.find("Examinations")
    if exams is None:
        raise ValueError("Native lead disease lacks examinations")
    if any(n.text == EXAM_ID for n in exams.findall("ExaminationRef")):
        raise ValueError("ABCL examination already present; do not add twice")
    before_symptoms = ET.tostring(entry.find("Symptoms"))
    before_treatments = ET.tostring(entry.find("Treatments"))
    ET.SubElement(exams, "ExaminationRef").text = EXAM_ID
    assert before_symptoms == ET.tostring(entry.find("Symptoms"))
    assert before_treatments == ET.tostring(entry.find("Treatments"))
    out = ET.Element("Database")
    out.append(entry)
    destination.write_bytes(ET.tostring(out, encoding="utf-8", xml_declaration=True))
    return {
        "status": "offline-review-only",
        "source_sha256": hashlib.sha256(data).hexdigest(),
        "output_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
        "disease_id": DIAGNOSIS_ID,
        "examination_added": EXAM_ID,
        "department_unchanged": DEPARTMENT_ID,
        "symptoms_unchanged": True,
        "treatments_unchanged": True,
        "native_admission_unverified": True,
        "gameplay_l4_authorized": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.source, args.output), indent=2))


if __name__ == "__main__":
    main()
