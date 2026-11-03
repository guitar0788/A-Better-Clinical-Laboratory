#!/usr/bin/env python3
"""Bundle an *owner-test-only* ART001/G1 additive ZIP from SHA-pinned L2.

The bundle is for one disposable-save L4, NOT an Alpha release, and is never
installed by this Python code. Eight frame art and original FA source are
preserved verbatim. The installer refuses preexisting resources and missing G1.
"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

SHA="cb3a7ab5d03e8677dcb84f486a04bf0ea5f8f622"
FILES=(
    "Database/ModObjectsABCL.xml",
    "Database/ModAssetListsABCL.xml",
    "Database/ModStringTableEnABCLArt001.xml",
    "Database/ModStringTableZhHansABCLArt001.xml",
    "Assets/ABCL/equipment_atlas.png",
    "Assets/ABCL/icp_ms_icon.png",
    "Assets/ABCL/digestion_station_icon.png",
)
ROOT=Path(__file__).resolve().parents[1]
INSTALL_CMD=r"""@echo off
setlocal
echo ABCL ART001 Standalone - owner L4 test ONLY. Close Project Hospital first.
echo Requires the already-installed full ABCL G1 test addon.
set /p "GAME_ROOT=Enter Project Hospital folder containing ProjectHospital_Data: "
if not defined GAME_ROOT exit /b 1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\Install-ART001-Standalone-Into-G1.ps1" -GameRoot "%GAME_ROOT%"
if errorlevel 1 (
 echo ART001 installation stopped. No manual copying or forced overwrite.
 pause
 exit /b 1
)
echo Test in a disposable hospital ONLY; never treat this as Alpha release.
pause
"""
UNINSTALL_CMD=r"""@echo off
setlocal
echo Close Project Hospital and retire disposable ART001 save before uninstall.
set /p "GAME_ROOT=Enter Project Hospital folder containing ProjectHospital_Data: "
if not defined GAME_ROOT exit /b 1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\Uninstall-ART001-Standalone-From-G1.ps1" -GameRoot "%GAME_ROOT%"
if errorlevel 1 (
 echo ART001 uninstall refused a changed or unowned file. Nothing should be manually deleted.
 pause
 exit /b 1
)
pause
"""
README="""ABCL ART-001 — FA submitted four-view standalone machines, TEST ONLY
FA frozen source SHA: cb3a7ab5d03e8677dcb84f486a04bf0ea5f8f622

This package contains exactly TWO standalone private cabinet machines, no
separate instrument workbench, copied FA private 8-direction atlas, and two
provisional 64px NW thumbnails. Owner approved FA SOURCE SUBMISSION ONLY,
not visual game quality. Original CBC/G1 rooms and TO-004 V3 are untouched.

1. EXIT the game. Back up your disposable test hospital, if necessary.
2. Extract this ZIP OUTSIDE the game install; double-click
   INSTALL_ART001_STANDALONE_TEST.cmd, enter the Project Hospital game ROOT.
3. An installed matching ModABCLG1LeadTest is mandatory. If absent, STOP.
   If any ART001 resource exists from a previous failed test, STOP:
   NEVER overwrite or manually delete unknown files.
4. In disposable save: two independent build-menu items (not tabletop);
   place and rotate each NW/NE/SE/SW; check 1x1 footprint/ground contact,
   staff free adjacent access and animations, original labs/CBC unchanged.
   Save, quit, reload once. Note DLC/Workshop set actually enabled.
5. If failed, capture FIRST failure + screenshot + output_log/Player.log.
   Do not repeat previously accepted G1 lead-patient workflow.
6. Close game, retire temporary save, run UNINSTALL_ART001_STANDALONE_TEST.cmd.
   It removes only exactly seven SHA-matching owned new ART files.

The package is NOT an Alpha 0.1 release and has not been accepted by game L4.
No proprietary original Project Hospital assets, Harmony, clinical C# or key.
"""


def sha(b):
    return hashlib.sha256(b).hexdigest()


def build(source: Path, output: Path):
    source=Path(source).resolve(strict=True)
    output=Path(output).resolve()
    if output.exists():
        raise FileExistsError("Will not overwrite an earlier test package")
    if any(p.lower() in ("addons","streamingassets","projecthospital_data")
           for p in output.parts):
        raise ValueError("Never generate package inside a live game folder")
    manifestpath=source/"ART001_TS_INTEGRATION_MANIFEST.json"
    info=json.loads(manifestpath.read_text("utf-8"))
    if (info["status"]!="G1_RESOURCE_OVERLAY_CANDIDATE_L2_ONLY_NOT_INSTALLABLE"
        or info["frozen_FA_sha"]!=SHA
        or info["independent_game_L4"]!="NOT_RUN"):
        raise ValueError("Incorrect source, unexpected L4 claim or version")
    listed=info["generated_runtime_XML_and_asset_sha256"]
    if set(listed)!=set(FILES):
        raise ValueError("Expected exactly seven own resource files")
    pkg={}
    for name in FILES:
        p=source/name
        if not p.is_file() or p.is_symlink():
            raise ValueError("Missing/unsafe resource: "+name)
        raw=p.read_bytes()
        if sha(raw)!=listed[name]:
            raise ValueError("ART001 source resource SHA differs: "+name)
        pkg[name]=raw
    if sha(pkg["Assets/ABCL/equipment_atlas.png"])!=(
        "b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651"):
        raise ValueError("FA owner-submitted original diagnostic atlas changed")
    pkg["ART001_TS_INTEGRATION_MANIFEST.json"]=manifestpath.read_bytes()
    for name in ("Install-ART001-Standalone-Into-G1.ps1",
                 "Uninstall-ART001-Standalone-From-G1.ps1"):
        pkg["tools/"+name]=(ROOT/"tools"/name).read_bytes()
    pkg["INSTALL_ART001_STANDALONE_TEST.cmd"]=INSTALL_CMD.encode("utf-8")
    pkg["UNINSTALL_ART001_STANDALONE_TEST.cmd"]=UNINSTALL_CMD.encode("utf-8")
    pkg["READ_ME_ART001_TEST_ONLY.txt"]=README.encode("utf-8")
    if len(pkg)!=13 or any(x.lower().endswith((".dll",".aes",".key")) for x in pkg):
        raise ValueError("Unexpected game binary/proprietary/key data")
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,"w",compression=zipfile.ZIP_DEFLATED,
                         compresslevel=8) as z:
        for name, raw in sorted(pkg.items()):
            obj=zipfile.ZipInfo(name, date_time=(2026,11,3,15,0,0))
            obj.compress_type=zipfile.ZIP_DEFLATED
            obj.external_attr=0o644 << 16
            z.writestr(obj,raw)
    with zipfile.ZipFile(output,"r") as z:
        if len(z.namelist())!=len(set(z.namelist())) or set(z.namelist())!=set(pkg):
            raise ValueError("Duplicate or missing ART ZIP entries")
        for name, raw in pkg.items():
            if z.read(name)!=raw:
                raise ValueError("Staged art changed in final package: "+name)
    return {"package":str(output),"sha256":sha(output.read_bytes()),
            "entries":len(pkg),"files":list(sorted(pkg)),
            "owner_visual_L4":"NOT_RUN","game_assembly_or_g1_dll_included":False}


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--stage",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(build(args.stage,args.out),indent=2))
