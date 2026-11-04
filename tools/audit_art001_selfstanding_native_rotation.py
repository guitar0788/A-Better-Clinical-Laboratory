#!/usr/bin/env python3
"""ART001 native four-direction operator position contract (source-only).

Cross-checked against user-provided *original* Project Hospital ILSpy:
  Lopital.TileObject.TransformUsePositionForDirection(Vector2i, Direction)
  GameDBObject.OnPostLoad (auto-rotation of UseOffsetX/Y from NW)
  Lopital.Floor.CanPlaceObject (accessibility requires a free/reachable tile)
Does not assert real pathfinding, sprites, animation contact or gameplay L4.
"""
import argparse
import json
import math
from pathlib import Path
from xml.etree import ElementTree as ET

DIRS = ("NW", "NE", "SE", "SW")
EXPECTED = {
    "OBJECT_ABCL_ART001_ICP_MS": ((0,1,2,3), -0.7),
    "OBJECT_ABCL_ART001_DIGESTION": ((4,5,6,7), -0.65),
}
EXPECTED_ORIGINAL_ACCESS = (-1, 0)


def rotate(v, d):
    x, y = v
    if d == "NW":
        return (x, y)
    if d == "NE":
        return (-y, x)
    if d == "SE":
        return (-x, -y)
    if d == "SW":
        return (y, -x)
    raise ValueError("Unknown native four-way direction")


def assert_safe(ok, message):
    if not ok:
        raise ValueError(message)


def numeric(obj, tag, default=0.0):
    raw = obj.findtext(tag)
    v = default if raw is None else float(raw)
    assert_safe(math.isfinite(v), "Non-finite game-object use offset: " + tag)
    return v


def validate(source):
    root = ET.parse(source).getroot()
    assert_safe(root.tag == "Database", "Expected Database")
    objs = root.findall("GameDBObject")
    assert_safe(len(objs) == 2 and {o.get("ID") for o in objs} == set(EXPECTED),
                "Exactly two independent ABCL center objects required")
    report = {}
    for obj in objs:
        key = obj.get("ID")
        slots, intended_xnw = EXPECTED[key]
        assert_safe(obj.findtext("AttachedToObject") == "false"
                    and obj.findtext("Placement") == "INDOORS",
                    "Floor-standing model, not tabletop parent: " + key)
        assert_safe(obj.findtext("SpriteShape") == "SHAPE_1_X_1",
                    "One-tile placement source assumption changed: " + key)
        assert_safe(obj.find("AttachmentSlot") is None and
                    obj.find("ConnectedSlots") is None,
                    "Old tabletop/forced direction dependency is present: " + key)
        assert_safe((obj.findtext("AccessPositionsHaveToBeFree") or "false").lower()
                    == "false",
                    "Original single-side placement semantics unexpectedly strict: " + key)
        accesses = obj.findall("AccessPositions/AccessPosition")
        assert_safe(len(accesses) == 1, "Exactly one source operator access tile: " + key)
        point = tuple(int(e.findtext(t)) for e, t in
                      ((accesses[0], "m_x"), (accesses[0], "m_y")))
        assert_safe(point == EXPECTED_ORIGINAL_ACCESS,
                    "Operator access differs from native independent-machine precedent: " + key)
        assert_safe(all(int(obj.findtext("TextureID" + d)) == slot
                        for d, slot in zip(DIRS, slots)),
                    "NW/NE/SE/SW atlas index mismatch: " + key)
        xnw = numeric(obj, "UseOffsetXNW")
        ynw = numeric(obj, "UseOffsetYNW")
        assert_safe(abs(xnw - intended_xnw) < 1e-6 and abs(ynw) < 1e-6,
                    "FA staff use-offset provenance changed: " + key)
        offsets = {}
        pos = {}
        for direction in DIRS:
            projected = rotate((xnw, ynw), direction)
            provided = (numeric(obj, "UseOffsetX" + direction),
                        numeric(obj, "UseOffsetY" + direction))
            if direction != "NW":
                # OnPostLoad fills X/Y if *both* values are zero. An explicit
                # conflicting value overrides that native automatic rotation.
                assert_safe((provided == (0.0, 0.0)
                             or all(abs(a-b) <= 1e-6
                                    for a,b in zip(provided, projected))),
                            "Conflicting explicit per-direction staff offsets: " + key)
            offsets[direction] = list(projected)
            p = rotate(point, direction)
            assert_safe(abs(p[0]) + abs(p[1]) == 1,
                        "Operator access left one-tile adjacent perimeter")
            pos[direction] = list(p)
        report[key] = {
            "native_access_tile_relative_to_device": pos,
            "expected_use_offsets_from_native_OnPostLoad": offsets,
            "placement_access_gate": "REQUIRES_FREE_AND_ACCESSIBLE_DIRECTIONAL_TILE",
            "actual_usable_room_path": "NOT_TESTED_L4",
            "sprite_rotation_appearance": "NOT_TESTED_L4",
        }
    return {
        "status": "NATIVE_SOURCE_SEMANTICS_TESTED_NOT_GAMEPLAY_L4",
        "objects": report,
        "original_engine_methods": [
            "Lopital.TileObject.TransformUsePositionForDirection",
            "GameDBObject.OnPostLoad",
            "Lopital.Floor.CanPlaceObject"
        ],
        "safe_for_occupied_staff_tile": False,
        "game_L4": "NOT_RUN",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate(args.candidate)
    message = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.exists():
            raise FileExistsError("Refusing to replace earlier source evidence")
        args.output.write_text(message, encoding="utf-8")
    print(message, end="")
