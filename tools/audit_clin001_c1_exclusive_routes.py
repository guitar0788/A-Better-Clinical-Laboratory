#!/usr/bin/env python3
"""ABCL CLIN-001 native laboratory route-isolation L2 audit.

Read-only input: owner-provided Project Hospital StreamingAssets.zip and
local G1 addon XML. Public JSON output includes only IDs, tags and counts,
not original game XML. Static tags CANNOT substitute for game L4.
"""
from __future__ import annotations
import argparse
import collections
import io
import json
import pathlib
import sys
import xml.etree.ElementTree as ET
import zipfile

ABCL_ROOM_ID = "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB"
ABCL_TEST_PREFIX = "EXM_ABCL_"
ABCL_ROOM_TAG = "abcl_g1_toxicology_lab"
COMMON_ROOM_TAGS = {"stat_lab", "lab_specialist_workspace"}


def exam_records(raw: bytes):
    root = ET.fromstring(raw)
    return [e for e in root if e.tag == "GameDBExamination" and e.get("ID")]


def required_tags(e):
    return {n.text for n in e.findall("./Procedure/RequiredRoomTags/Tag") if n.text}


def required_types(e):
    return {n.text for n in e.findall("./Procedure/RequiredRoomTypeList/RequiredRoomTypeRef") if n.text}


def read_native_zip(archive: pathlib.Path):
    with zipfile.ZipFile(archive) as z:
        sources = sorted(x for x in z.namelist() if x.startswith("StreamingAssets/")
                         and x.endswith(".xml")
                         and ("Examinations.xml" in x or x.endswith("DLCExaminations.xml"))
                         and "/Database/" in x and "/Localization/" not in x)
        result = []
        for source in sources:
            for e in exam_records(z.read(source)):
                result.append((source, e))
    return result, sources


def audit_from_records(vanilla_records, room_xml: bytes, exam_xml: bytes):
    room = ET.fromstring(room_xml).find(".//*[@ID='%s']" % ABCL_ROOM_ID)
    if room is None:
        raise ValueError("Missing ABCL room type")
    room_tags = {n.text for n in room.findall("./Tags/Tag") if n.text}
    if ABCL_ROOM_TAG not in room_tags or "stat_lab" not in room_tags:
        raise ValueError("ABCL room lacks its private tag or native stat_lab contract")
    added = exam_records(exam_xml)
    added_by_id = {e.get("ID"): e for e in added}
    tests = [(e.get("ID"), e.findtext("./LabTestingExaminationRef")) for e in added
             if e.findtext("./LabTestingExaminationRef")]
    if not tests:
        raise ValueError("No ABCL sampling/testing pair")
    abcl_routes = []
    for sampling_id, linked_id in tests:
        if not sampling_id.startswith(ABCL_TEST_PREFIX) or not linked_id.startswith(ABCL_TEST_PREFIX):
            raise ValueError("ABCL sampling/testing IDs are not private")
        target = added_by_id.get(linked_id)
        if target is None:
            raise ValueError("Unresolved ABCL testing ID: " + linked_id)
        tags = required_tags(target)
        types = required_types(target)
        exclusive = bool(ABCL_ROOM_TAG in tags) and all(t == ABCL_ROOM_ID for t in types)
        abcl_routes.append({"sample": sampling_id, "test": linked_id, "tags": sorted(tags),
                            "types": sorted(types), "matches_abcl":bool(tags & room_tags or ABCL_ROOM_ID in types),
                            "requires_private_tag": exclusive})
    # Count every native sampling-to-testing link, retaining duplicate DLC records
    # for ambiguity warnings. For each distinct linked test, inspect *all* definitions.
    all_entries = collections.defaultdict(list)
    links = []
    for source,e in vanilla_records:
        k=e.get("ID")
        all_entries[k].append((source,e))
        target=e.findtext("./LabTestingExaminationRef")
        if target and not k.startswith(ABCL_TEST_PREFIX):
            links.append((source,k,target))
    ids = sorted(set(x[2] for x in links))
    report = []
    blocked = []
    unknown = []
    for ident in ids:
        defs = all_entries.get(ident, [])
        if not defs:
            unknown.append({"exam": ident, "reason":"target definition absent"})
            continue
        overlap = []
        tagsets = []
        for src,definition in defs:
            tags = required_tags(definition)
            types = required_types(definition)
            tagsets.append(sorted(tags))
            if tags & room_tags or ABCL_ROOM_ID in types:
                overlap.append(src)
            if not tags and not types:
                unknown.append({"exam": ident,"reason":"no native room tag or explicit room type"})
        if overlap:
            blocked.append({"exam":ident,"sources":sorted(set(overlap))})
        report.append({"exam":ident,"source_count":len(defs),"room_tag_sets":tagsets,
                       "overlaps_abcl_room":bool(overlap)})
    return {
        "gate":"C1 source L2 only; in-game L4 not performed",
        "vanilla_sample_links":len(links),"distinct_vanilla_test_ids":len(ids),
        "vanilla_tests_with_matching_abcl_room":blocked,
        "vanilla_tests_unresolved_or_unscoped":unknown,
        "abcl_room_tags":sorted(room_tags),"abcl_pairs":abcl_routes,
        "native_tag_isolation_l2_pass":not blocked and not unknown and bool(abcl_routes)
                                         and all(x["requires_private_tag"] for x in abcl_routes),
        "reviewed_native_tests":report,
        "l4_test_needed":True,
    }


def audit(game_zip, addon_dir):
    records,sources=read_native_zip(game_zip)
    result=audit_from_records(records,
                    (addon_dir/"ModRoomTypes.xml").read_bytes(),
                    (addon_dir/"ModExaminations.xml").read_bytes())
    result["scanned_source_paths"]=sources
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--game-zip",type=pathlib.Path,required=True)
    ap.add_argument("--addon-db",type=pathlib.Path,required=True)
    ap.add_argument("--output",type=pathlib.Path)
    a=ap.parse_args()
    x=audit(a.game_zip,a.addon_db)
    payload=json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if a.output:
        if a.output.exists(): raise SystemExit("Refusing to overwrite existing report")
        a.output.write_text(payload,encoding="utf-8")
    else: print(payload)
    if not x["native_tag_isolation_l2_pass"]:
        sys.exit(2)

if __name__ == "__main__":main()
