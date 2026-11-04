"""ABCL TO-001 exact accepted PNG contract; no derivative sprites."""
from pathlib import Path
import hashlib
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "assets/to001/owner_approved_20261104"
CS = (ROOT / "src/ABCLG1Panel.cs").read_text("utf-8")
ROOM = CS.split("internal sealed class G1ToxicologyRoomIconAdapter", 1)[1].split(
    "internal sealed class G1ToxicologyPrivateFloorIconAdapter", 1)[0]
LOADER = CS.split("internal sealed class G1ApprovedPrivateTexture", 1)[1].split(
    "// TO-001: optional additive UI-only adapter.", 1)[0]
FLOOR = CS.split("internal sealed class G1ToxicologyPrivateFloorIconAdapter", 1)[1]

PINS = {
    "toxicology_room_icon.png": "c2c6c83cb0f8c2ca49dce7184bdd4f71df1c71a20ecf0c38e05337df6a48f62b",
    "toxicology_room_icon_inactive.png": "eb37ce261299f7df2ac87c61272168f71b5faca5de1578b71a172a8d75e861eb",
}

class ApprovedShadowRoomIcons(unittest.TestCase):
    def test_approved_exact_original_bytes(self):
        for name, digest in PINS.items():
            with self.subTest(name=name):
                raw = (ART / name).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)
                self.assertEqual(raw[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(raw[12:16], b"IHDR")
                self.assertEqual(struct.unpack(">IIBB", raw[16:26]), (64,64,8,6))
                self.assertIn(digest, ROOM)

    def test_opaque_color_face_and_allowed_outer_shadow(self):
        # Decode PNG with standard-library only; check original pixels rather
        # than inventing a newer repaint process. Alpha outside face is valid.
        import zlib
        for name, face in (("toxicology_room_icon.png",(201,63,61)),
                           ("toxicology_room_icon_inactive.png",(153,153,153))):
            raw=(ART/name).read_bytes(); pos=8; idat=b""
            while pos < len(raw):
                size=struct.unpack(">I",raw[pos:pos+4])[0]
                kind=raw[pos+4:pos+8]; body=raw[pos+8:pos+8+size]
                pos+=12+size
                if kind==b"IDAT": idat+=body
                if kind==b"IEND":break
            decoded=zlib.decompress(idat)
            rows=[]; offset=0; prev=[0]*256
            for y in range(64):
                kind=decoded[offset]; offset+=1
                row=list(decoded[offset:offset+256]); offset+=256
                for i in range(256):
                    a=row[i-4] if i>=4 else 0
                    b=prev[i]; c=prev[i-4] if i>=4 else 0
                    if kind==1: row[i]=(row[i]+a)&255
                    elif kind==2: row[i]=(row[i]+b)&255
                    elif kind==3: row[i]=(row[i]+((a+b)//2))&255
                    elif kind==4:
                        p=a+b-c; pa=abs(p-a);pb=abs(p-b);pc=abs(p-c)
                        row[i]=(row[i]+(a if pa<=pb and pa<=pc else b if pb<=pc else c))&255
                    elif kind!=0: self.fail("unsupported PNG filter")
                rows.append(row);prev=row
            opaque=[(x,y) for y,row in enumerate(rows) for x in range(64)
                    if row[4*x+3]==255]
            self.assertEqual(len(opaque),1890)
            self.assertEqual(tuple(rows[12][4*12:4*12+4]),face+(255,))
            self.assertEqual(tuple(rows[0][0:4]),(0,0,0,0))
            self.assertTrue(any(0<rows[y][4*x+3]<255
                                for y in range(54,63) for x in range(30,60)),
                            "approved right/bottom shadow missing")

    def test_runtime_renders_actual_source_not_recomputed_old_palette(self):
        self.assertIn("Sprite.Create(approved,", LOADER)
        self.assertIn("new Rect(0f, 0f, 64f, 64f)", LOADER)
        self.assertIn("SHA256.Create()", LOADER)
        self.assertNotIn("CreateNativeRoomGlyph", LOADER)
        self.assertNotIn("SetPixels32", LOADER)
        self.assertNotIn("File.WriteAllBytes", CS)
        self.assertIn("MaxNativeRoomIconSide = 30f", ROOM)
        self.assertIn("targetRoomItem.m_roomDatabaseID == RoomId", ROOM)
        self.assertIn("cachedSpriteProperty.SetValue(cachedSegmentImage, sprite, null)", ROOM)
        self.assertIn("cachedLegacySpriteProperty.SetValue(cachedLegacyImage, sprite, null)", ROOM)

    def test_existing_floor_pass_unchanged(self):
        self.assertIn("00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd", FLOOR)
        self.assertIn("material.mainTexture = atlas", FLOOR)
        self.assertNotIn("sharedMaterial.mainTexture =", FLOOR)

if __name__ == "__main__":
    unittest.main()
