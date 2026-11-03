#!/usr/bin/env python3
"""TO004 L2 contract tests; no game owned assets required."""
from collections import Counter
import json
import hashlib
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from PIL import Image,ImageChops

BASE=Path(__file__).resolve().parents[1]
DB=BASE/'Database'
OVER=BASE
TYPE='ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB'
FILES={
 'small':('room_toxicology_small.xml','toxicology_small.png',(8,6),(10,7),54,25000,'1477eb5580e1002c33384f84aaa708dfbe2fb19b09ea01dcd330309295d61457'),
 'large':('room_toxicology_large.xml','toxicology_large.png',(12,6),(13,7),72,30000,'4454abe727234fd8f8e6a70bcfff2f58860f05dbf3f8351b99951d7725bbad8d'),
}
class Check(unittest.TestCase):
 def test_saved_prefab_bytes_and_room(self):
  for k,(filename,_,size,rawsize,tilecount,_,sha) in FILES.items():
   with self.subTest(k=k):
    p=OVER/'Prefabs'/filename
    self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),sha)
    doc=ET.parse(p).getroot()
    self.assertEqual(doc.tag,'PrefabPersistentData')
    self.assertEqual((int(doc.findtext('./m_size/m_x')),int(doc.findtext('./m_size/m_y'))),rawsize)
    self.assertEqual(len(doc.findall('./m_tiles/PrefabTile')),tilecount)
    self.assertEqual(len(doc.findall('./m_rooms/PrefabRoom')),1)
    room=doc.find('./m_rooms/PrefabRoom')
    self.assertEqual(room.find('./m_roomType/GameDBPointer').attrib['ID'],TYPE)
    lo=(int(room.findtext('m_positionBottom/m_x')),int(room.findtext('m_positionBottom/m_y')))
    hi=(int(room.findtext('m_positionTop/m_x')),int(room.findtext('m_positionTop/m_y')))
    self.assertEqual((hi[0]-lo[0]+1,hi[1]-lo[1]+1),size)
    self.assertEqual({x.attrib['ID'] for x in doc.findall('.//GameDBPointer') if x.attrib['ID'].startswith('ROOM_TYPE_')},{TYPE})
    self.assertFalse(any(x.attrib['ID'].startswith('OBJECT_ABCL_ART001') for x in doc.findall('.//GameDBPointer')))
 def test_private_additive_resources(self):
  db=ET.parse(DB/'ModAssetListsTO004.xml').getroot()
  assets=db.findall('./GameDBAsset'); self.assertEqual(len(assets),4)
  ids=[x.attrib['ID'] for x in assets]
  self.assertEqual(len(set(ids)),4)
  for a in assets:
   self.assertTrue(a.attrib['ID'].startswith('ASSET_ABCL_TO004_'))
   self.assertIn(a.findtext('Type'),('PREFAB','TEXTURE_CUSTOM_PREFAB_SPRITE'))
   f=a.findtext('File')
   self.assertTrue(f.startswith('MOD_ROOT/'))
   self.assertTrue((OVER/f[len('MOD_ROOT/'):]).is_file(),f)
 def test_prefab_object_xml_contract(self):
  prefabs=ET.parse(DB/'ModPrefabObjectsTO004.xml').getroot().findall('GameDBPrefabObject')
  self.assertEqual(len(prefabs),2)
  assets={x.attrib['ID']:x for x in ET.parse(DB/'ModAssetListsTO004.xml').getroot().findall('GameDBAsset')}
  for p,k in zip(prefabs,('small','large')):
   f,im,size,_,_,price,_=FILES[k]
   self.assertEqual(p.attrib['ID'],'PREFAB_ABCL_TO004_TOXICOLOGY_'+k.upper())
   self.assertEqual((int(p.findtext('DisplayedSizeX')),int(p.findtext('DisplayedSizeY'))),size)
   self.assertEqual(int(p.findtext('Cost')),price)
   self.assertEqual(int(p.findtext('IconIndex')),-1)
   self.assertIsNone(p.find('PrefabNW'))
   self.assertEqual(p.find('Tags/Tag').text,'ui_prefab_lab')
   self.assertTrue(all(p.findtext(x)=='true' for x in ('LayerFloors','LayerWalls','LayerDoors','LayerObjects')))
   ref=p.findtext('PrefabAssetRef');icon=p.findtext('CustomIconAssetRef')
   self.assertEqual(assets[ref].findtext('File'),f'MOD_ROOT/Prefabs/{f}')
   self.assertEqual(assets[icon].findtext('File'),f'MOD_ROOT/Assets/ABCL/Prefabs/{im}')
 def test_icons(self):
  pics=[]
  for k,(_,pic,_,_,_,_,_) in FILES.items():
   image=Image.open(OVER/'Assets'/'ABCL'/'Prefabs'/pic)
   self.assertEqual((image.size,image.mode),((104,104),'RGBA'))
   self.assertLess(image.getbbox()[0],20)
   self.assertGreater(image.getbbox()[2],85)
   self.assertIsNotNone(image.getbbox())
   self.assertEqual(image.getpixel((0,0))[3],0)
   pics.append(image)
  self.assertIsNotNone(ImageChops.difference(pics[0],pics[1]).getbbox())
 def test_l10n_and_no_dev_labels(self):
  pl=ET.parse(DB/'ModPrefabObjectsTO004.xml').getroot()
  keys={x.findtext('AbbreviationLocID') for x in pl.findall('GameDBPrefabObject')}
  for s,code in [('ModStringTableEnTO004.xml','en'),('ModStringTableZhHansTO004.xml','zh-Hans')]:
   root=ET.parse(DB/s).getroot().find('GameDBStringTable')
   self.assertEqual(root.findtext('LanguageCode'),code)
   locs=root.findall('./LocalizedStrings/GameDBLocalizedString')
   self.assertEqual({q.findtext('LocID') for q in locs},keys)
   for q in locs:
    t=q.findtext('Text')
    self.assertTrue(t)
    self.assertNotIn('ABCL',t.upper())
    self.assertNotIn('TEST',t.upper())
 def test_xml_derived_vector_object_locations_and_manifest(self):
  manifest=json.loads((OVER/'art_sources/manifest.json').read_text('utf-8'))
  for key,(filename,pic,roomsize,_,_,_,rawsha) in FILES.items():
   with self.subTest(variant=key):
    saved=ET.parse(OVER/'Prefabs'/filename).getroot()
    expected=Counter()
    for comp in saved.findall('./m_compositeObjects/CompositeObjectPersistentData'):
     ptr=comp.find('./m_compositeObject/GameDBPointer')
     if ptr is None or not ptr.get('ID'): continue
     x=comp.findtext('./m_position/m_x'); y=comp.findtext('./m_position/m_y')
     expected[(ptr.get('ID'),f'{x},{y}','composite')]+=1
    for cell in saved.findall('./m_tileObjects/PrefabTileObjects'):
     x=cell.findtext('./m_position/m_x'); y=cell.findtext('./m_position/m_y')
     for kind in ('m_attachmentObject','m_centerObject','m_objectSW','m_objectSE','m_objectNW','m_objectNE'):
      obj=cell.find(kind)
      if obj is None:continue
      ptr=obj.find('./m_gameDBObject/GameDBPointer')
      if ptr is None or not ptr.get('ID'):continue
      norm='attachment' if kind=='m_attachmentObject' else ('wall' if kind.startswith('m_object') else 'center')
      expected[(ptr.get('ID'),f'{x},{y}',norm)]+=1
    svg=(OVER/'art_sources'/f'toxicology_{key}.svg').read_bytes()
    vector=ET.fromstring(svg)
    actual=Counter((e.attrib['data-xml-id'],e.attrib['data-tile'],e.attrib['data-kind'])
                   for e in vector.iter() if 'data-xml-id' in e.attrib)
    self.assertEqual(actual,expected)
    self.assertEqual(vector.attrib['data-xml-sha256'],rawsha)
    self.assertEqual((vector.attrib['width'],vector.attrib['height']),('104','104'))
    self.assertEqual((int(vector.attrib['data-room-width']),int(vector.attrib['data-room-height'])),roomsize)
    self.assertEqual(manifest[key]['source_sha256'],rawsha)
    self.assertEqual(manifest[key]['object_count'],sum(expected.values()))
    self.assertEqual(manifest[key]['icon_sha256'],hashlib.sha256((OVER/'Assets/ABCL/Prefabs'/pic).read_bytes()).hexdigest())
    self.assertEqual(manifest[key]['svg_sha256'],hashlib.sha256(svg).hexdigest())
 def test_previews_not_rejected_old_art(self):
  old={'small':'e77e1f0ccd0828b58ba50b00298defd63029753520fd03c48ba2b08dbe860765',
       'large':'f38cc29403c85806f42e3e0aadd3a5d74f7d2c3e2090c9c7658edb2497d22b1c'}
  for key, (_,pic,_,_,_,_,_) in FILES.items():
   sprite=OVER/'Assets/ABCL/Prefabs'/pic
   self.assertNotEqual(hashlib.sha256(sprite.read_bytes()).hexdigest(),old[key])
   img=Image.open(sprite)
   self.assertGreater(img.getbbox()[3],83)
 def test_no_scope_creep(self):
  files={x.relative_to(OVER).as_posix() for x in OVER.rglob('*') if x.is_file() and x.relative_to(OVER).parts[0] in ('Assets','Prefabs','Database')}
  self.assertEqual(len(files),8)
  self.assertTrue(all(x.startswith(('Assets/ABCL/Prefabs/','Prefabs/','Database/')) for x in files))
  self.assertTrue(all(not x.lower().endswith(('.dll','.aes','.key','.exe')) for x in files))

if __name__=='__main__':unittest.main(verbosity=2)
