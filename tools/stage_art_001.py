#!/usr/bin/env python3
"""Stage ART-001 original sprite/object proof outside the live game folders.

This is an offline artifact for layout and reference review, NOT a game installer.
No existing user or game file is changed. Python 3 standard library only.
"""
import argparse
import shutil
import tempfile
from pathlib import Path

from generate_art_001_svg import generate

ROOT = Path(__file__).resolve().parents[1]
DB_SOURCE = ROOT / "assets" / "art001" / "Database"
FILES = (
    "ModAssetListsABCL.xml",
    "ModObjectsABCL.xml",
    "ModStringTableEnABCLArt001.xml",
    "ModStringTableZhHansABCLArt001.xml",
    "ModColorSets.xml",
)
ADDON = """<?xml version="1.0" encoding="utf-8"?>
<Database><GameDBAddon ID="ADDON_MOD_ABCL_ART001_PREVIEW">
<Author>ABCL original-art proof (not for installation)</Author>
</GameDBAddon></Database>
"""


def stage(output):
    output = Path(output).expanduser().resolve()
    if output.exists():
        raise FileExistsError("Refusing to overwrite an existing directory: " + str(output))
    if "StreamingAssets" in output.parts or "Addons" in output.parts:
        raise ValueError("Refusing to stage into live game/Addon directories")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="abcl-art001-", dir=str(output.parent)) as tmp:
        temp = Path(tmp) / output.name
        temp.mkdir()
        generate(temp)
        db = temp / "Database"
        db.mkdir()
        (db / "ModAddon.xml").write_text(ADDON, encoding="utf-8")
        for name in FILES:
            shutil.copyfile(DB_SOURCE / name, db / name)
        (temp / "NOT_FOR_GAME_INSTALL.txt").write_text(
            "ART-001 offline proof only. Do not copy into the live game Addons. "
            "L3 loader and L4 staff-placement/interaction gates are not passed.\n",
            encoding="utf-8",
        )
        temp.rename(output)
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    print(stage(args.output))


if __name__ == "__main__":
    main()
