#!/usr/bin/env python3
"""Assemble an exact-source, additive TO004 test-only overlay (NOT an installable G1 addon)."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import struct
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / 'Database'
PREFABS = ROOT / 'Prefabs'
IMAGES = ROOT / 'Assets/ABCL/Prefabs'
SCRIPT = ROOT / 'tools'
EXPECTED = {
    'Database/ModAssetListsTO004.xml',
    'Database/ModPrefabObjectsTO004.xml',
    'Database/ModStringTableEnTO004.xml',
    'Database/ModStringTableZhHansTO004.xml',
    'Prefabs/room_toxicology_small.xml',
    'Prefabs/room_toxicology_large.xml',
    'Assets/ABCL/Prefabs/toxicology_small.png',
    'Assets/ABCL/Prefabs/toxicology_large.png',
}
SCRIPTS = {
    'tools/Install-TO004-Into-G1.ps1',
    'tools/Uninstall-TO004-From-G1.ps1',
    'tools/INSTALL_TO004_TEST_ONLY.cmd',
    'tools/UNINSTALL_TO004_TEST_ONLY.cmd',
}
ORIGINAL_SHA256 = {
    'Prefabs/room_toxicology_small.xml': '1477eb5580e1002c33384f84aaa708dfbe2fb19b09ea01dcd330309295d61457',
    'Prefabs/room_toxicology_large.xml': '4454abe727234fd8f8e6a70bcfff2f58860f05dbf3f8351b99951d7725bbad8d',
}

def hashbytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def build(out: Path, source_sha: str) -> dict:
    if len(source_sha) != 40 or any(c not in '0123456789abcdef' for c in source_sha):
        raise ValueError('Must provide exact 40-digit lowercase Git source commit SHA')
    if out.exists():
        raise ValueError('Refusing to overwrite existing candidate artifact')
    if any(p.casefold() in {'streamingassets','addons'} for p in out.resolve().parts):
        raise ValueError('Refusing to write into game installation path')
    names = sorted(EXPECTED | SCRIPTS)
    files = {}
    for name in names:
        f = ROOT / name
        if not f.is_file() or f.is_symlink():
            raise ValueError('Missing/untrusted package path: ' + name)
        files[name] = f.read_bytes()
    for name,digest in ORIGINAL_SHA256.items():
        if hashbytes(files[name]) != digest:
            raise ValueError('Original user prefab has changed: ' + name)
    assets = {e.attrib['ID']: e for e in ET.fromstring(files['Database/ModAssetListsTO004.xml']).findall('GameDBAsset')}
    objects = ET.fromstring(files['Database/ModPrefabObjectsTO004.xml']).findall('GameDBPrefabObject')
    if len(assets) != 4 or len(objects) != 2:
        raise ValueError('Unexpected asset/prefab count')
    for a in assets.values():
        file = a.findtext('File')
        if not file or not file.startswith('MOD_ROOT/') or file[len('MOD_ROOT/'):] not in EXPECTED:
            raise ValueError('Unresolved asset path: '+str(file))
    for size in ('small','large'):
        name = f'Assets/ABCL/Prefabs/toxicology_{size}.png'
        b = files[name]
        if b[:8]!=b'\x89PNG\r\n\x1a\n' or b[12:16]!=b'IHDR' or struct.unpack('>IIBB',b[16:26])!=(104,104,8,6):
            raise ValueError('Not 104x104 RGBA thumbnail: '+name)
    manifest = {'source_sha':source_sha,'stage':'TO-004 ADDITIVE TEST OVERLAY ONLY, NOT A STANDALONE G1 MOD','game_L4':'NOT_RUN','entries':{name:hashbytes(data) for name,data in sorted(files.items())}}
    files['TO004_BUILD_INFO.json'] = (json.dumps(manifest,indent=2,ensure_ascii=False)+'\n').encode('utf-8')
    files['TO004_TEST_README.txt'] = (f'TO-004: addon-private TEST OVERLAY ONLY\nTO004_SOURCE_SHA={source_sha}\nRequires already-installed compatible G1 test addon.\nGame L4 NOT RUN; no Alpha/release.\nClose game, extract to any directory, run tools/INSTALL_TO004_TEST_ONLY.cmd.\nVerify menu for Laboratory, small+large prefab, thumbnails, placement, rotations and save/load.\nDo not repeat G1 patient generation. Use a disposable save.\nUninstall only after save is retired.\n').encode('utf-8')
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,11,3,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644 << 16
            z.writestr(info,data)
    with zipfile.ZipFile(out) as z:
        if set(z.namelist()) != set(files) or len(set(z.namelist())) != len(files):
            raise ValueError('Unexpected/missing archive entry')
        if any(z.read(name)!=files[name] for name in files):
            raise ValueError('Packaged entry altered')
    return {'source_sha':source_sha,'zip_sha256':hashbytes(out.read_bytes()),'files':len(files),'runtime':len(EXPECTED)}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--source-sha',required=True)
    args=parser.parse_args()
    print(json.dumps(build(args.output,args.source_sha),indent=2))