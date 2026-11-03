#!/usr/bin/env python3
"""Original ABCL source-derived isometric prefab thumbnail illustrations.

No textures, sprites, art or binaries from Project Hospital are read or copied.
Room tile/object XY data is taken from the author's own saved prefab XMLs.
Each SVG is editable; each RGBA icon is antialiased from the SVG at 6x.
This is a *layout illustration*, not an in-game screenshot or proof of L4.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from io import BytesIO
import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Assets'/'ABCL'/'Prefabs'
SVGOUT=ROOT/'art_sources'
PREVIEW=ROOT/'previews'
ROOMTYPE='ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB'
COLORS={
 'floor_a': '#edf0f1', 'floor_b': '#d5dfe5', 'floor_c':'#dbe5ef',
 'wall':'#e8e9e8','wall_d':'#a4b3ba','outline':'#67757e',
 'worktop':'#e9f1f1', 'workedge':'#78909a', 'steel':'#d6e0e5',
 'metal':'#9fadb9','screen':'#8cadb4','accent':'#b76b6b'
}

def point(x,y,u=10.,v=5.):return (150 + (x-y)*u, 48 + (x+y)*v)
def points_s(q):return ' '.join(f'{x:.2f},{y:.2f}' for x,y in q)
def poly(points,fill,stroke=None,sw=1):
 return f'<polygon points="{points_s(points)}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else '')+'/>'
def line(p,q,color,sw=1,opacity=1):return f'<path d="M {p[0]:.2f},{p[1]:.2f} L {q[0]:.2f},{q[1]:.2f}" fill="none" stroke="{color}" stroke-width="{sw}" opacity="{opacity}" stroke-linecap="round"/>'
def dot(p,r,fill,stroke=None):return f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{r:.2f}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width=".55"' if stroke else '')+'/>'
def diamond(cx,cy,s=0.6):
 a=s*9;b=s*4.6
 return [(cx,cy-b),(cx+a,cy),(cx,cy+b),(cx-a,cy)]
def cube(cx,cy,w=5.5,h=3.,height=8,top='#f5f8f8',right='#a2b1b8',left='#c5d2d8',stroke='#70818b'):
 # Isometric cabinet, raised above the floor.
 t=(cx,cy-height)
 toppts=[(cx,cy-height-h),(cx+w,cy-height),(cx,cy-height+h),(cx-w,cy-height)]
 lower=[(x,y+height) for x,y in toppts]
 a=poly([toppts[3],toppts[2],lower[2],lower[3]],left,stroke,'.6')
 b=poly([toppts[1],toppts[2],lower[2],lower[1]],right,stroke,'.6')
 c=poly(toppts,top,stroke,'.6')
 return a+b+c

def extract(xmlpath):
 root=ET.parse(xmlpath).getroot()
 room=root.find('./m_rooms/PrefabRoom')
 rt=room.find('./m_roomType/GameDBPointer').attrib['ID']
 if rt!=ROOMTYPE:raise ValueError('Unexpected room type '+rt)
 lo=(int(room.findtext('m_positionBottom/m_x')),int(room.findtext('m_positionBottom/m_y')))
 hi=(int(room.findtext('m_positionTop/m_x')),int(room.findtext('m_positionTop/m_y')))
 tiles={}
 for t in root.findall('./m_tiles/PrefabTile'):
  x=int(t.findtext('m_position/m_x'));y=int(t.findtext('m_position/m_y'))
  tpe=t.find('./m_floorType/GameDBPointer').attrib['ID'];
  color=t.find('./m_materialColor')
  rr=float(color.findtext('r')); gg=float(color.findtext('g'));bb=float(color.findtext('b'))
  tiles[(x,y)]=(tpe,(rr,gg,bb))
 objects=[]
 for t in root.findall('./m_tileObjects/PrefabTileObjects'):
  x=int(t.findtext('m_position/m_x'));y=int(t.findtext('m_position/m_y'))
  for child in t:
   if child.tag=='m_position':continue
   ptr=child.find('./m_gameDBObject/GameDBPointer')
   if ptr is None:continue
   objects.append((x,y,ptr.attrib.get('ID',''),child.tag))
 for child in root.findall('./m_compositeObjects/CompositeObjectPersistentData'):
  ptr=child.find('./m_compositeObject/GameDBPointer')
  if ptr is None:continue
  objects.append((int(child.findtext('m_position/m_x')),int(child.findtext('m_position/m_y')),ptr.attrib.get('ID',''),'composite'))
 return lo,hi,tiles,objects

def obj_parts(x,y,o,kind):
 # Render from actual tile positions; all shapes are original SVG artwork.
 cx,cy=point(x+.5,y+.5)
 s=[]
 if 'CHAIR' in o:
  s.append(line((cx,cy+1),(cx,cy+4),'#566a70',.8))
  s.append(poly(diamond(cx,cy-1,.30),'#92acac','#657779','.5'))
  s.append(line((cx-2,cy-2),(cx-2,cy-6),'#7b9896',1.6))
 elif any(k in o for k in ['WORKBENCH','TABLE_SQUERE','LAB_HALF_DESK','INSTRUMETNS_TABLE','LAB_CABINET','LAB_SHELF','CABINET','FRIDGE','SCRUBS_SHELF']):
  height=6 if any(k in o for k in ['FRIDGE','SCRUBS_SHELF','CABINET_WALL']) else 4.5
  s.append(cube(cx,cy,5.6,2.8,height,'#edf2f3','#a4b4bd','#c8d4d9'))
  if 'FRIDGE' in o:
   s.append(line((cx+1.5,cy-height+2),(cx+1.5,cy-1),'#687780',.8))
  elif 'SHELF' in o:
   s.append(line((cx-3,cy-height+4),(cx+2,cy-height+2),'#8c9fa6',.9))
 elif 'HEMATOLOGY_ANALYZER' in o or o=='OBJECT_RIA' or 'THERMAL_CYCLER' in o:
  s.append(cube(cx,cy,5.6,3.5,7.5,'#f2f5f4','#879da6','#c1d1d7'))
  s.append(poly(diamond(cx-1,cy-8.0,.18),'#7a9297','#57676a','.4'))
  if 'HEMATOLOGY' in o:
   for j in range(3):s.append(dot((cx-3+j*2,cy-10+j*.35),.7,'#cb8b87'))
  elif 'RIA' in o:
   s.append(dot((cx+1,cy-9),1.5,'#6b959c'))
  else:
   s.append(poly(diamond(cx+1,cy-10,.19),'#b08375'))
 elif 'PC' in o:
  s.append(line((cx,cy),(cx,cy-3.8),'#82939b',.8))
  s.append(poly([(cx-3,cy-7.5),(cx+1,cy-6.3),(cx+1,cy-2.2),(cx-3,cy-3.5)],'#58767e','#738890','.6'))
  s.append(poly([(cx-2.3,cy-6.7),(cx+.3,cy-5.9),(cx+.3,cy-3.0),(cx-2.3,cy-3.9)],'#a9c7cd'))
 elif 'LAB_SINK' in o or 'SINK_KITCHEN' in o:
  s.append(cube(cx,cy,5,2.5,4,'#f3f5f4','#94aab2','#becbd0'))
  s.append(poly(diamond(cx,cy-5,.25),'#739ca9','#9caeb4','.5'))
 elif any(k in o for k in ['TRASH_BIN','HAMPER','DEZINFECTION']):
  s.append(cube(cx,cy,2.8,1.8,4,'#e4e7e6','#8d9da4','#b4c0c4'))
 elif 'PRINTER' in o:
  s.append(cube(cx,cy,3.5,2.4,3.5,'#ecf0f0','#9cafb5','#bac8cc'))
 elif any(k in o for k in ['LAMP','CLOCK','POSTER','NOTICE']):
  s.append(dot((cx,cy-4),2.2,'#c7dedf','#8b9e9f'))
 elif 'LAB_EQUIPMENT' in o or 'BURETTES' in o or 'SURGERY_INSTRUMENTS' in o:
  s.append(poly(diamond(cx,cy-2.4,.27),'#d5e8e7','#a2b6b9','.5'))
  for dx,dy,c in [(-1,0,'#7fa1b0'),(1,-.6,'#c47c78'),(0,1,'#b9c4cb')]:s.append(dot((cx+dx,cy-4+dy),.8,c))
 else:
  s.append(cube(cx,cy,2.5,1.3,3,'#eef1ef','#a7b4b7','#c3ced1'))
 return ''.join(s)

def svg_room(xmlpath):
 lo,hi,tiles,objs=extract(xmlpath)
 # Transparent 104x104 canvas coordinates; inner isometric plane drawn at native-like size.
 sx=hi[0]-lo[0]+1;sy=hi[1]-lo[1]+1
 pts=[point(lo[0],lo[1]),point(hi[0]+1,lo[1]),point(hi[0]+1,hi[1]+1),point(lo[0],hi[1]+1)]
 minx=min(p[0] for p in pts); maxx=max(p[0] for p in pts)
 miny=min(p[1] for p in pts); maxy=max(p[1] for p in pts)
 # Compose in world coordinates then frame entire room into the original icon silhouette area.
 parts=[]
 outer=[point(lo[0],lo[1]),point(hi[0]+1,lo[1]),point(hi[0]+1,hi[1]+1),point(lo[0],hi[1]+1)]
 parts.append(poly([(x+1.2,y+7) for x,y in outer],'#34464e','#34464e','2'))
 parts.append(poly(outer,'#b9c7cd','#82959f','.65'))
 for (x,y),(ft,cl) in sorted(tiles.items(),key=lambda kv:(kv[0][0]+kv[0][1],kv[0][0])):
  a=[point(x,y),point(x+1,y),point(x+1,y+1),point(x,y+1)]
  c=('#e0e8e9' if 'CERAMIC_MED' in ft else '#c5cfd1')
  if 'CONCRETE_BRICK' in ft:c='#bfc8cb'
  parts.append(poly(a,c,'#b1bdc2','.28'))
 # Walls raised only along top/back side; room boundaries are author authored XY.
 h=11
 for x in range(lo[0],hi[0]+1):
  p=point(x,lo[1]);q=point(x+1,lo[1])
  parts.append(poly([(p[0],p[1]-h),(q[0],q[1]-h),q,p],'#e6eaeb','#8e9fa6','.5'))
  parts.append(line((p[0],p[1]-h),(q[0],q[1]-h),'#a76d6a',1.3,.83))
 for y in range(lo[1],hi[1]+1):
  p=point(lo[0],y);q=point(lo[0],y+1)
  parts.append(poly([(p[0],p[1]-h),(q[0],q[1]-h),q,p],'#d5e0e2','#82979e','.5'))
  parts.append(line((p[0],p[1]-h),(q[0],q[1]-h),'#ad7d7b',1.3,.78))
 priority={'composite':0,'m_centerObject':1,'m_attachmentObject':2,'m_objectSE':3,'m_objectSW':3,'m_objectNW':3,'m_objectNE':3}
 for x,y,o,k in sorted(objs,key=lambda t:(t[0]+t[1],priority.get(t[3],3))):
  if (x,y) not in tiles:continue
  # Avoid drawing irrelevant wall decor excessively, but depict fixtures and workstations.
  parts.append(obj_parts(x,y,o,k))
 # A thin outer architectural rim to help legibility at 104px.
 p0,p1,p2,p3=outer
 parts.append(line(p1,p2,'#455863',1.4,.92));parts.append(line(p2,p3,'#465861',1.6,.9))
 # fit viewbox to shapes with some air on all sides.
 max_obj_height=19
 vb_x=minx-8;vb_y=miny-max_obj_height-6;vb_w=maxx-minx+16;vb_h=maxy-miny+max_obj_height+17
 # fixed 104 transparent box; preserve the original icon ~100x70 placement.
 vb_w = max(vb_w,vb_h*1.30)
 out=['<svg xmlns="http://www.w3.org/2000/svg" width="104" height="104" viewBox="'+f'{vb_x:.2f} {vb_y:.2f} {vb_w:.2f} {vb_h:.2f}'+ '">',
 '<!-- ABCL TO-004 original illustration, derived from owner-authored layout coordinates. -->',
 '<defs><filter id="shadow" x="-30%" y="-60%" width="160%" height="200%"><feGaussianBlur stdDeviation="2"/></filter></defs>',
 f'<path d="M {p0[0]+1:.2f},{p0[1]+11:.2f} L {p1[0]+1:.2f},{p1[1]+11:.2f} L {p2[0]+1:.2f},{p2[1]+11:.2f} L {p3[0]+1:.2f},{p3[1]+11:.2f}Z" fill="#202b32" opacity=".13" filter="url(#shadow)"/>',
 *parts,'</svg>']
 return '\n'.join(out),{'room_bounds':[lo,hi], 'size':[sx,sy], 'tile_count':len(tiles), 'object_count':len(objs), 'object_ids':dict(collections.Counter(o for _,_,o,_ in objs))}

def main():
 OUT.mkdir(parents=True,exist_ok=True);SVGOUT.mkdir(parents=True,exist_ok=True);PREVIEW.mkdir(parents=True,exist_ok=True)
 man={}
 examples=[]
 for k in ('small','large'):
  source=ROOT/'Prefabs'/('room_toxicology_'+k+'.xml')
  s,data=svg_room(source)
  svg=SVGOUT/('toxicology_'+k+'.svg');svg.write_text(s,encoding='utf-8')
  raw=cairosvg.svg2png(bytestring=s.encode('utf-8'),output_width=624,output_height=624)
  image=Image.open(BytesIO(raw)).convert('RGBA').resize((104,104),Image.Resampling.LANCZOS)
  # Subdued 16-step RGB palette; preserve all antialiased alpha coverage.
  image.putdata([(r//16*16,g//16*16,b//16*16,a) for r,g,b,a in image.getdata()])
  out=OUT/('toxicology_'+k+'.png');image.save(out,optimize=True)
  # A no-text original asset; preview only includes labels outside the actual icon.
  examples.append(image.resize((416,416),Image.Resampling.NEAREST))
  man[k]={**data,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
          'icon_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
          'icon_pixels':image.size,'svg_sha256':hashlib.sha256(svg.read_bytes()).hexdigest()}
 cover=Image.new('RGB',(900,530),'#eef1f3');d=ImageDraw.Draw(cover)
 for i,(k,a) in enumerate(zip(('small','large'),examples)):
  x=30+i*445;cover.paste(a,(x,40),a)
  d.text((x+12,462),('8 x 6 — compact' if k=='small' else '12 x 6 — extended'),fill='#354651')
 d.text((30,503),'Original ABCL layout illustrations · not in-game screenshots · 104×104 native export',fill='#63747c')
 cover.save(PREVIEW/'to004_layout_review.png',optimize=True)
 (ROOT/'art_sources'/'manifest.json').write_text(json.dumps(man,indent=2)+'\n',encoding='utf8')
 print(json.dumps(man,indent=2))

if __name__=='__main__':main()