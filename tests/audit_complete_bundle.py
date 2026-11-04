#!/usr/bin/env python3
"""Independent ABCL native test bundle audit, no mutation of owner resources.

Test states: PASS only for L1/L2/verified build evidence; actual game L4 is
always UNKNOWN unless externally supplied by a real game test.
"""
import hashlib
import io
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile
import struct

G1='ModABCLG1LeadTest/'
ART='ModABCLArt001Test/'
OWNER={
    G1+'Assets/ABCL/toxicology_room_icon.png': '225b2918c448b5d36d1d8582389e8952f2baf1574d0d72935017c81eab7d8199',
    G1+'Assets/ABCL/toxicology_room_icon_inactive.png': '50c17ea8ba8b42b28295564f594713069a31c9e48fa05f3a6b623a36851b6490',
    G1+'Assets/ABCL/toxicology_floor_atlas_private_376.png': '00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd',
    G1+'Assets/ABCL/Prefabs/toxicology_small.png': 'a0ec4ea41b5d96d4b755c5d244700548a6a2485d6a1d3e1bef73d8dcf09a0847',
    G1+'Assets/ABCL/Prefabs/toxicology_large.png': '3461bf9bbb8476d79e869d98f718b887a32ea88f5b0b158f185abc9f6cf85947',
    ART+'Assets/ABCL/equipment_atlas.png': 'b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651',
    G1+'Prefabs/room_toxicology_small.xml': 'ec3be4046d90c219d28143ffd838712fc8030b3a84a05e80a4b8e65ec0141b1d',
    G1+'Prefabs/room_toxicology_large.xml': '7d5c559cc60211ea37b42026c8066fbff98865be88d76ef8730350f3ac81b54d',
}
EXPECTED_SOURCE='aada123989f835feb38d8a7d38b1b338e14cc75f'
EXPECTED_DLL='72cf86abb5bbb539a5b364aaf314b8f36a4746ca2caab955b191de754ff602c7'
HARMONY1_SHA='e271d22a7c32bfca105d0e471c04eee14eec6142d37a30cd73cb7d32c7d1dd0f'


def h(x):return hashlib.sha256(x).hexdigest()
def check(ok,message):
    if not ok:raise ValueError(message)
def validate_native_loader(files):
    key=G1+'0Harmony.dll'
    check(key in files, 'FATAL: Original Project Hospital will skip G1 code without 0Harmony.dll')
    data=files[key]
    check(len(data)==113152 and data[:2]==b'MZ' and b'BSJB' in data and
          b'HarmonyInstance' in data and h(data)==HARMONY1_SHA,
          'FATAL: official nonempty Harmony1 net35 binary missing or altered')
    check(G1+'THIRD_PARTY_HARMONY1_MIT_LICENSE.txt' in files,
          'Harmony MIT license missing')

def audit_bytes(files):
    check('BUILD_INFO.json' in files,'no manifest')
    m=json.loads(files['BUILD_INFO.json'])
    check(m['compiled_g1_source_sha']==EXPECTED_SOURCE,'stale compiled G1 source')
    check(m['dll_sha256']==EXPECTED_DLL,'wrong expected DLL hash')
    check(m['native_game_L4']=='NOT_RUN','fake L4 status')
    check(m['schema']=='ABCL_OWNER_PINNED_TEST_ONLY_V1','schema')
    check(set(m['entries'])==set(files)-{'BUILD_INFO.json'},'untracked/duplicate/missing package files')
    for n,expected in m['entries'].items():check(n in files and h(files[n])==expected,'manifest hash '+n)
    for n,expected in OWNER.items():check(n in files and h(files[n])==expected,'owner original source changed '+n)
    check(h(files[G1+'ModABCLG1LeadTest.dll'])==EXPECTED_DLL,'stale/prepatch DLL')
    validate_native_loader(files)
    check(m.get('native_loader_harmony1_sha256')==HARMONY1_SHA,'Native code-loader manifest not pinned')
    check(not any('workbench' in n.lower() or 'ModColorSets.xml' in n for n in files),'rejected workbench files')
    for n in files:
        check(not(n.startswith('/') or '..' in n.split('/') or '\\' in n),'unsafe path')
        check(n.startswith((G1,ART)) or n in {'BUILD_INFO.json','Install-ABCL-Full-Test.ps1',
              'Install-ABCL-G1.ps1','INSTALL_ABCL_FULL_TEST.cmd','RESTORE_ABCL_FULL_TEST.cmd',
              'README_FIRST_CN.txt'},'non-ABCL game overwrite')
    room=ET.fromstring(files[G1+'Database/ModRoomTypes.xml']).find('GameDBRoomType')
    check(room is not None and room.get('ID')=='ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB','room type ID')
    check(room.findtext('TextureID')=='376' and room.findtext('IconIndex')=='3070','room floor/list private bridge IDs')
    required={x.findtext('Tag') for x in room.findall('./RequiredEquipment/GameDBRequiredEquipment')}
    check({'abcl_art001_icp_ms','abcl_art001_digestion'}<=required,'independent instrument room requirements')
    assets=ET.fromstring(files[G1+'Database/ModAssetListsTO001.xml'])
    bindings={x.get('ID'):(x.findtext('Type'),x.findtext('File')) for x in assets.findall('GameDBAsset')}
    check(bindings=={
    'ASSET_ABCL_TOXICOLOGY_ROOM_ICON':('TEXTURE_CUSTOM_SPRITE','MOD_ROOT/Assets/ABCL/toxicology_room_icon.png'),
    'ASSET_ABCL_TOXICOLOGY_ROOM_ICON_INACTIVE':('TEXTURE_CUSTOM_SPRITE','MOD_ROOT/Assets/ABCL/toxicology_room_icon_inactive.png'),
    'ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS':('TEXTURE','MOD_ROOT/Assets/ABCL/toxicology_floor_atlas_private_376.png'),
    }, 'GameDB room sprite/floor binding mismatch')
    for key in ['toxicology_room_icon.png','toxicology_room_icon_inactive.png']:
        raw=files[G1+'Assets/ABCL/'+key]
        check(struct.unpack('>IIBB',raw[16:26])==(64,64,8,6),'incorrect opaque owner sprite type')
    obj=ET.fromstring(files[ART+'Database/ModObjectsABCL.xml'])
    actual={x.get('ID'):x for x in obj.findall('GameDBObject')}
    check(set(actual)=={'OBJECT_ABCL_ART001_ICP_MS','OBJECT_ABCL_ART001_DIGESTION'}, 'obsolete attached workbench')
    for key,tiles,tag in [('OBJECT_ABCL_ART001_ICP_MS',(0,1,2,3),'abcl_art001_icp_ms'),
                         ('OBJECT_ABCL_ART001_DIGESTION',(4,5,6,7),'abcl_art001_digestion')]:
        x=actual[key]
        check(x.findtext('AttachedToObject')=='false' and x.findtext('Placement')=='INDOORS','device not independent')
        check(x.findtext('TextureRef')=='ASSET_TEX_ABCL_ART001_EQUIPMENT','wrong equipment atlas asset')
        check(tuple(int(x.findtext('TextureID'+d)) for d in ['NW','NE','SE','SW'])==tiles,'device atlas orientation')
        check(tag in {e.text for e in x.findall('Tags/Tag')},'missing private device tag')
        check(x.find('AttachmentSlot') is None,'old attachment slot')
    obj_tags={v for x in actual.values() for v in [e.text for e in x.findall('Tags/Tag')]}
    check(not(obj_tags & {'ui_hematoanalyzer','ui_ria','hematoanalyzer','RIA'}),'equipment impersonates original')
    # Confirm prefab ID->asset path->approved preview and 2 correct source XMLs.
    pref=ET.fromstring(files[G1+'Database/ModPrefabObjectsTO004.xml'])
    ps={e.get('ID'):e for e in pref.findall('GameDBPrefabObject')}
    check(set(ps)=={'PREFAB_ABCL_TO004_TOXICOLOGY_SMALL','PREFAB_ABCL_TO004_TOXICOLOGY_LARGE'},'TO004 prefab identities')
    check({(e.findtext('DisplayedSizeX'),e.findtext('DisplayedSizeY')) for e in ps.values()}=={('8','6'),('12','6')},'TO004 size mismatch')
    asset=ET.fromstring(files[G1+'Database/ModAssetListsTO004.xml'])
    registered={e.get('ID'):e.findtext('File') for e in asset.findall('GameDBAsset')}
    for size,label in [('small','SMALL'),('large','LARGE')]:
        check(registered.get('ASSET_ABCL_TO004_PREFAB_ICON_'+label)==
              'MOD_ROOT/Assets/ABCL/Prefabs/toxicology_'+size+'.png','prefab thumbnail ref mismatch')
        check(registered.get('ASSET_ABCL_TO004_PREFAB_TOXICOLOGY_'+label)==
              'MOD_ROOT/Prefabs/room_toxicology_'+size+'.xml','prefab XML ref mismatch')
        x=ET.fromstring(files[G1+'Prefabs/room_toxicology_'+size+'.xml'])
        check(x.tag=='PrefabPersistentData','prefab source bad root')
        xml=ET.tostring(x,encoding='unicode')
        check('OBJECT_ABCL_ART001_WORKBENCH' not in xml,'rejected attached workbench in prefab')
        for k in ('OBJECT_ABCL_ART001_ICP_MS','OBJECT_ABCL_ART001_DIGESTION','ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB'):
            check(k in xml,'prefab missing referenced independent object '+k)
    for code,expected in [('En','Toxicology Laboratory'),('ZhHans','临床毒理实验室')]:
        loc=ET.fromstring(files[G1+'Database/ModStringTable'+code+'TO004.xml'])
        strings=[x.findtext('Text') for x in loc.findall('.//GameDBLocalizedString')]
        check(strings==[expected,expected], 'prefab labels regressed')
    check('ALREADY INSTALLED' in files['Install-ABCL-Full-Test.ps1'].decode('utf-8'), 'installer lacks idempotence')
    check('_ABCL_OWNER_BACKUP_' in files['Install-ABCL-Full-Test.ps1'].decode('utf-8'), 'installer no protected backup')
    return {'package_files':len(files),'approved_art':5,'prefabs':2,'devices':2,'l3_sha':EXPECTED_SOURCE,
            'l3_dll':EXPECTED_DLL,'room_id':room.get('ID'),'floor_tile':376,'l4':'NOT_RUN'}

def audit_zip(path):
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        check(len(names)==len(set(names)),'duplicate zip entries')
        return audit_bytes({n:z.read(n) for n in names})

if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser();a.add_argument('archive',type=Path);opt=a.parse_args()
    print(json.dumps(audit_zip(opt.archive),ensure_ascii=False,indent=2))
