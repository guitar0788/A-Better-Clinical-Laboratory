#!/usr/bin/env python3
"""Build test-only ABCL G1 + independent FA devices + owner TO004 prefabs.

No approved source image is re-encoded or altered. This program never writes to a
Project Hospital installation and never reads original game binaries. A real L3
compiled ABCL DLL is only consumed from the specified Actions artifact.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import struct
import xml.etree.ElementTree as ET
import zipfile

ROOT=Path(__file__).resolve().parents[1]
G1='ModABCLG1LeadTest/'
ART='ModABCLArt001Test/'
EXPECTED_SHA='d73b2302b896c8cf58c3230ddaa5663e02285b53'
EXPECTED_DLL='51e4bb2c49a550c591f5908dbe765409a9a2a86d0e664421059840525804ef8b'
OWNER={
    'toxicology_room_icon.png':'225b2918c448b5d36d1d8582389e8952f2baf1574d0d72935017c81eab7d8199',
    'toxicology_room_icon_inactive.png':'50c17ea8ba8b42b28295564f594713069a31c9e48fa05f3a6b623a36851b6490',
    'toxicology_floor_atlas_private_376.png':'00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd',
    'Prefabs/toxicology_small.png':'a0ec4ea41b5d96d4b755c5d244700548a6a2485d6a1d3e1bef73d8dcf09a0847',
    'Prefabs/toxicology_large.png':'3461bf9bbb8476d79e869d98f718b887a32ea88f5b0b158f185abc9f6cf85947',
}
PREFAB_HASHES={
    'room_toxicology_small.xml':'ec3be4046d90c219d28143ffd838712fc8030b3a84a05e80a4b8e65ec0141b1d',
    'room_toxicology_large.xml':'7d5c559cc60211ea37b42026c8066fbff98865be88d76ef8730350f3ac81b54d',
}
ART_ATLAS='b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651'
HARMONY1_SHA='e271d22a7c32bfca105d0e471c04eee14eec6142d37a30cd73cb7d32c7d1dd0f'


def check(test,msg):
    if not test: raise ValueError(msg)
def hash_bytes(data):return hashlib.sha256(data).hexdigest()
def png_dim(data):
    check(data.startswith(b'\x89PNG\r\n\x1a\n') and data[12:16]==b'IHDR','Not PNG')
    return struct.unpack('>IIBB',data[16:26])
def read_zip_outer(path,member):
    with zipfile.ZipFile(path) as outer:
        check(member in outer.namelist(),'Missing inner artifact '+member)
        data=outer.read(member)
    with zipfile.ZipFile(io.BytesIO(data)) as inner:
        check(len(inner.namelist())==len(set(inner.namelist())),'Duplicate inner archive names')
        return {p:inner.read(p) for p in inner.namelist()}

def check_game_xml(raw):
    root=ET.fromstring(raw)
    check(root.tag=='Database','Wrong GameDB XML root')
    return root

def make_room_xml(data):
    root=check_game_xml(data)
    rooms=root.findall('GameDBRoomType')
    check(len(rooms)==1 and rooms[0].get('ID')=='ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB',
          'Wrong G1 toxicology room')
    room=rooms[0]
    check(room.findtext('IconIndex')=='3070','Unexpected vanilla fallback icon')
    check(room.findtext('TextureID')=='491','Unexpected original floor index; refuse guess')
    room.find('TextureID').text='376'
    tags={r.findtext('Tag') for r in room.findall('./RequiredEquipment/GameDBRequiredEquipment')}
    check({'abcl_art001_digestion','abcl_art001_icp_ms'} <= tags,
          'G1 does not require both standalone devices')
    return ET.tostring(root,encoding='utf-8',xml_declaration=True)

def verify_art_xml(raw):
    root=check_game_xml(raw)
    objects=root.findall('GameDBObject')
    devs={x.get('ID'):x for x in objects}
    expected={'OBJECT_ABCL_ART001_ICP_MS':(0,1,2,3),
              'OBJECT_ABCL_ART001_DIGESTION':(4,5,6,7)}
    check(len(objects)==2 and set(devs)==set(expected),'Old workbench/invalid device count')
    for key,idxs in expected.items():
        obj=devs[key]
        check(obj.findtext('AttachedToObject')=='false' and obj.findtext('Placement')=='INDOORS',
              key+' must be independent floor-standing')
        check(tuple(int(obj.findtext('TextureID'+d,'-1')) for d in ('NW','NE','SE','SW'))==idxs,
              'Four-direction equipment tiles mismatch')
        check(obj.findtext('TextureRef')=='ASSET_TEX_ABCL_ART001_EQUIPMENT' and
              obj.findtext('SpriteShape')=='SHAPE_1_X_1', 'Equipment private atlas/size changed')
        tags={x.text for x in obj.findall('./Tags/Tag')}
        check(not(tags & {'hematoanalyzer','ui_hematoanalyzer','ui_ria','RIA','stat_lab_exam'}),
              'Equipment impersonates vanilla CBC tag')
    return root

def make_asset_xml():
    root=ET.Element('Database')
    for aid,kind,name in (
      ('ASSET_ABCL_TOXICOLOGY_ROOM_ICON','TEXTURE_CUSTOM_SPRITE','toxicology_room_icon.png'),
      ('ASSET_ABCL_TOXICOLOGY_ROOM_ICON_INACTIVE','TEXTURE_CUSTOM_SPRITE','toxicology_room_icon_inactive.png'),
      ('ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS','TEXTURE','toxicology_floor_atlas_private_376.png')):
        x=ET.SubElement(root,'GameDBAsset',ID=aid)
        ET.SubElement(x,'Type').text=kind
        ET.SubElement(x,'File').text='MOD_ROOT/Assets/ABCL/'+name
    return ET.tostring(root,encoding='utf-8',xml_declaration=True)

def verify_prefab(root,which):
    check(root.tag=='PrefabPersistentData','Unexpected supplied prefab root')
    data=ET.tostring(root,encoding='unicode')
    for key in ('OBJECT_ABCL_ART001_ICP_MS','OBJECT_ABCL_ART001_DIGESTION',
                'ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB'):
        check(key in data,which+' missing '+key)
    check('OBJECT_ABCL_ART001_WORKBENCH' not in data,which+' contains rejected workbench')

def build(g1path,artpath,to004path,g1installer,owner_dir,prefabs,out,harmony_dll):
    out=Path(out)
    check(not out.exists(),'Refuse overwrite existing output')
    check(not any(part.casefold() in ('addons','streamingassets','projecthospital_data')
                  for part in out.resolve().parts), 'Do not build in installed game')
    orig=Path(g1path)
    with zipfile.ZipFile(orig) as z:
        info=z.read('BUILD_INFO.txt').decode('utf-8-sig')
    pin=re.search(r'(?m)^CANDIDATE_SHA=([a-f0-9]{40})\s*$',info)
    dllpin=re.search(r'(?mi)^DLL_SHA256=([a-f0-9]{64})\s*$',info)
    check(pin is not None and pin.group(1)==EXPECTED_SHA, 'G1 DLL compiled from wrong C# source')
    check(dllpin is not None and dllpin.group(1).lower()==EXPECTED_DLL, 'Unexpected G1 L3 DLL hash')
    original=read_zip_outer(g1path,'ABCL_G1_AutoBuilt_TestOnly.zip')
    check(G1+'ModABCLG1LeadTest.dll' in original,'Missing compiled G1 DLL')
    check(hash_bytes(original[G1+'ModABCLG1LeadTest.dll'])==EXPECTED_DLL,'G1 DLL SHA mismatch')
    art=read_zip_outer(artpath,'ABCL_ART001_FA_Standalone_L4_TestOnly.zip')
    check(hash_bytes(art['Assets/ABCL/equipment_atlas.png'])==ART_ATLAS,'Stale/rejected FA equipment atlas')
    verify_art_xml(art['Database/ModObjectsABCL.xml'])
    files={p:b for p,b in original.items() if p.startswith(G1) and p!=G1+'0Harmony.dll'}
    # Project Hospital TitleScreenController requires a real 0Harmony.dll
    # inside the same addon directory BEFORE loading any other mod DLL.
    real_harmony=Path(harmony_dll).read_bytes()
    check(len(real_harmony)==113152 and real_harmony[:2]==b'MZ'
          and b'BSJB' in real_harmony and b'HarmonyInstance' in real_harmony
          and hash_bytes(real_harmony)==HARMONY1_SHA,
          'Code-loader prerequisite missing: require official Harmony1 net35 DLL')
    files[G1+'0Harmony.dll']=real_harmony
    files[G1+'THIRD_PARTY_HARMONY1_MIT_LICENSE.txt']=(
        ROOT/'third_party/Harmony-1.2.0.1-LICENSE.txt').read_bytes()
    files[G1+'Database/ModRoomTypes.xml']=make_room_xml(files[G1+'Database/ModRoomTypes.xml'])
    files[G1+'Database/ModAssetListsTO001.xml']=make_asset_xml()
    owner_dir=Path(owner_dir)
    for name,digest in OWNER.items():
        raw=(owner_dir/'Assets'/'ABCL'/name).read_bytes()
        check(hash_bytes(raw)==digest,'Owner-approved art hash mismatch: '+name)
        target=G1+'Assets/ABCL/'+name
        files[target]=raw
    for name,digest in PREFAB_HASHES.items():
        source=Path(prefabs[0] if name.endswith('small.xml') else prefabs[1])
        raw=source.read_bytes()
        check(hash_bytes(raw)==digest,'Owner reuploaded TO004 XML mismatch: '+name)
        verify_prefab(ET.fromstring(raw),name)
        files[G1+'Prefabs/'+name]=raw
    # V3 names/preview registrations; owner supplied preview images supersede
    # original overlay versions, but are identical to their approved hashes.
    to=read_zip_outer(to004path,'ABCL_TO004_TestOnly_Overlay.zip')
    for p in ('Database/ModAssetListsTO004.xml','Database/ModPrefabObjectsTO004.xml',
              'Database/ModStringTableEnTO004.xml','Database/ModStringTableZhHansTO004.xml'):
        check_game_xml(to[p]);files[G1+p]=to[p]
    for p in ('Database/ModAssetListsABCL.xml','Database/ModObjectsABCL.xml',
              'Database/ModStringTableEnABCLArt001.xml',
              'Database/ModStringTableZhHansABCLArt001.xml'):
        check_game_xml(art[p]);files[ART+p]=art[p]
    for p in ('Assets/ABCL/equipment_atlas.png','Assets/ABCL/icp_ms_icon.png',
              'Assets/ABCL/digestion_station_icon.png'):
        files[ART+p]=art[p]
    # Same isolated test-addon identity as earlier integration; no rejected
    # workbench GameDB or old color sets will be shipped.
    files[ART+'Database/ModAddon.xml']=(
        b'<?xml version="1.0" encoding="utf-8"?>\n'
        b'<Database><GameDBAddon ID="ADDON_MOD_ABCL_ART001_PREVIEW">'
        b'<Author>ABCL test-only freestanding equipment</Author></GameDBAddon></Database>')
    for p in ('Install-ABCL-G1.ps1',):
        files[p]=Path(g1installer).read_bytes()
    for p in ('Install-ABCL-Full-Test.ps1','INSTALL_ABCL_FULL_TEST.cmd',
              'RESTORE_ABCL_FULL_TEST.cmd','README_FIRST_CN.txt'):
        files[p]=(ROOT/'tools'/p).read_bytes()
    check(not any('workbench' in p.casefold() or p.endswith('ModColorSets.xml')
                  for p in files), 'Rejected package entry')
    manifest={
        'schema':'ABCL_OWNER_PINNED_TEST_ONLY_V1',
        'status':'OFFLINE_L2_CANDIDATE_NOT_L4',
        'native_game_L4':'NOT_RUN',
        'compiled_g1_source_sha':EXPECTED_SHA,
        'dll_sha256':EXPECTED_DLL,
        'native_loader_harmony1_sha256':HARMONY1_SHA,
        'art_source_sha':'cb3a7ab5d03e8677dcb84f486a04bf0ea5f8f622',
        'approved_art_sha256':OWNER,
        'owner_uploaded_prefab_sha256':PREFAB_HASHES,
        'equipment_atlas_sha256':ART_ATLAS,
        'room_texture_index':376,
        'independent_instruments':True,
        'excluded_rejected_workbench':True,
        'entries':{p:hash_bytes(raw) for p,raw in sorted(files.items())},
    }
    files['BUILD_INFO.json']=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p,raw in sorted(files.items()):
            entry=zipfile.ZipInfo(p,(2026,11,4,0,0,0))
            entry.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(entry,raw)
    with zipfile.ZipFile(out) as z:
        check(len(z.namelist())==len(set(z.namelist())),'Duplicate ZIP paths')
        check(set(z.namelist())==set(files),'Missing package entry')
        for p in files:check(z.read(p)==files[p],'Package byte mismatch '+p)
    return {'status':'OFFLINE_BUNDLE_AUDIT_OK_L4_NOT_RUN','entries':len(files),
            'package_sha256':hash_bytes(out.read_bytes()),
            'g1_dll_sha256':EXPECTED_DLL,'g1_source':EXPECTED_SHA}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--g1-artifact',type=Path,required=True)
    ap.add_argument('--art-artifact',type=Path,required=True)
    ap.add_argument('--to004-artifact',type=Path,required=True)
    ap.add_argument('--g1-installer',type=Path,required=True)
    ap.add_argument('--owner-art-dir',type=Path,required=True)
    ap.add_argument('--prefab-small',type=Path,required=True)
    ap.add_argument('--prefab-large',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--harmony-dll',type=Path,required=True)
    a=ap.parse_args()
    print(json.dumps(build(a.g1_artifact,a.art_artifact,a.to004_artifact,a.g1_installer,a.owner_art_dir,
                           (a.prefab_small,a.prefab_large),a.output,a.harmony_dll),indent=2))
