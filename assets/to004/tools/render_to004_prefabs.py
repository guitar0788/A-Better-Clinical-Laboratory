#!/usr/bin/env python3
"""TO-004 isometric native-scale drawings from immutable owner room XML.

Only reads the two XML files; writes fully editable layered SVGs and 104x104 RGBA PNGs.
Original Project Hospital art is used as a visual reference, not copied into files.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape
import hashlib, json
import cairosvg
from PIL import Image

OUT=Path(__file__).resolve().parent
ROOMS={"small":("room_toxicology_small.xml",8),"large":("room_toxicology_large.xml",12)}
EXPECTED={"small":"1477eb5580e1002c33384f84aaa708dfbe2fb19b09ea01dcd330309295d61457", "large":"4454abe727234fd8f8e6a70bcfff2f58860f05dbf3f8351b99951d7725bbad8d"}
C={
    "steel":"#7a939a","outline":"#5c696b", "top":"#f0f3ef","left":"#bdc9c8","right":"#9baeb0",
    "glass":"#80b5bb","screen":"#609daa","teal":"#7babb0","cream":"#e9ddd4","red":"#b86963",
    "taupe":"#a69b94","dark":"#455661", "yellow":"#c9a15d"
}

def h(s): return hashlib.sha256(s).hexdigest()
def f(v): return f"{v:.2f}".rstrip('0').rstrip('.')
def xy(p): return f"{f(p[0])},{f(p[1])}"
def pts(*p): return ' '.join(map(xy,p))
def col(c):return C.get(c,c)
def poly(points,fill,stroke='#677276',width=.24,extra=''):
    return f'<polygon points="{pts(*points)}" fill="{col(fill)}" stroke="{col(stroke)}" stroke-width="{f(width)}" stroke-linejoin="round" {extra}/>'
def line(a,b,stroke,width=.25,extra=''):
    return f'<path d="M{xy(a)} L{xy(b)}" stroke="{col(stroke)}" stroke-width="{f(width)}" stroke-linecap="round" fill="none" {extra}/>'
def circ(x,y,r,fill,stroke='none',sw=.2,extra=''):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{col(fill)}" stroke="{col(stroke)}" stroke-width="{f(sw)}" {extra}/>'
def rect(x,y,w,he,fill,stroke='none',sw=.22,r=0,extra=''):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(he)}" rx="{f(r)}" fill="{col(fill)}" stroke="{col(stroke)}" stroke-width="{f(sw)}" {extra}/>'

@dataclass
class Layout:
    key:str; xml:Path; roomw:int; roomh:int; xmin:int; ymin:int
    floors:list; walls:list; items:list; all_ids:Counter
    pitchx:float; pitchy:float; anchorx:float; anchory:float

    def p(self,x,y,z=0):
        x=float(x)-self.xmin; y=float(y)-self.ymin
        return self.anchorx+(x-y)*self.pitchx,self.anchory+(x+y)*self.pitchy-z
    def tile(self,x,y):
        return [self.p(x,y),self.p(x+1,y),self.p(x+1,y+1),self.p(x,y+1)]


def get_layout(key,xml):
    raw=xml.read_bytes(); assert h(raw)==EXPECTED[key],f"source XML CHANGED for {key}"
    root=ET.fromstring(raw)
    room=root.find('./m_rooms/PrefabRoom'); xmin=int(room.findtext('./m_positionBottom/m_x')); ymin=int(room.findtext('./m_positionBottom/m_y'))
    xmax=int(room.findtext('./m_positionTop/m_x')); ymax=int(room.findtext('./m_positionTop/m_y'))
    w,hgt=xmax-xmin+1,ymax-ymin+1
    assert w==(8 if key=='small' else 12) and hgt==6
    floors=[]
    for ft in root.findall('./m_tiles/PrefabTile'):
        p=ft.find('./m_position');x,y=int(p.findtext('m_x')),int(p.findtext('m_y'))
        fid=ft.find('./m_floorType/GameDBPointer'); floor_id=fid.get('ID') if fid is not None else ''
        mc=ft.find('./m_materialColor'); rgb=[float(mc.findtext(k, '0')) for k in ('r','g','b')]
        floors.append((x,y,floor_id,rgb))
    walls=[]
    for wall in root.findall('./m_tileWalls/PrefabTileWalls'):
        po=wall.find('./m_position');x,y=int(po.findtext('m_x')),int(po.findtext('m_y'))
        for t in ['m_wallSW','m_wallSE','m_doorSW','m_doorSE']:
            nd=wall.find('./'+t+'/GameDBPointer')
            if nd is not None and nd.get('ID'):
                walls.append((x,y,t,nd.get('ID')))
    items=[]; seen=Counter()
    for comp in root.findall('./m_compositeObjects/CompositeObjectPersistentData'):
        g=comp.find('./m_compositeObject/GameDBPointer')
        if g is None:continue
        name=g.get('ID');x=int(comp.findtext('./m_position/m_x'));y=int(comp.findtext('./m_position/m_y'))
        direction=comp.findtext('./m_orientation','NW')
        items.append((x,y,'composite',name,direction)); seen[name]+=1
    for cell in root.findall('./m_tileObjects/PrefabTileObjects'):
        x=int(cell.findtext('./m_position/m_x'));y=int(cell.findtext('./m_position/m_y'))
        for kind in ['m_centerObject','m_attachmentObject','m_objectNE','m_objectSE','m_objectNW','m_objectSW']:
            el=cell.find('./'+kind)
            if el is None:continue
            g=el.find('./m_gameDBObject/GameDBPointer')
            if g is None:continue
            name=g.get('ID');direction=el.findtext('./m_orientation',kind[8:] if kind.startswith('m_object') else 'NW')
            items.append((x,y,'wall' if kind.startswith('m_object') else ('attachment' if kind=='m_attachmentObject' else 'center'),name,direction));seen[name]+=1
    # original prefab bounds (not the recorded m_size, which includes exterior margin).
    dx=(90.5 if key=='small' else 93.2)/(w+hgt)
    dy=(3.43 if key=='small' else 2.62)
    anchorx=52-(w-hgt)*dx/2
    return Layout(key,xml,w,hgt,xmin,ymin,floors,walls,items,seen,dx,dy,anchorx,33.7 if key=='small' else 34.1)

class Scene:
    def __init__(self,L):self.L=L; self.output=[]
    def emit(self,s): self.output.append(s)
    def group(self,name,attrs='',parts=''):
        self.emit(f'<g id="{name}" {attrs}>\n{parts}\n</g>')
    def floor(self):
        L=self.L
        corners=[L.p(L.xmin,L.ymin),L.p(L.xmin+L.roomw,L.ymin),L.p(L.xmin+L.roomw,L.ymin+L.roomh),L.p(L.xmin,L.ymin+L.roomh)]
        self.emit('<g id="floor-and-foundations" inkscape:groupmode="layer" inkscape:label="Floors and foundation">')
        shadow=[(x,y+4.0) for x,y in corners]
        self.emit(poly(shadow,'#25272c','#26292a',.2,extra='opacity=".50"'))
        for v in [L.p(L.xmin+L.roomw,L.ymin),L.p(L.xmin+L.roomw,L.ymin+L.roomh),L.p(L.xmin,L.ymin+L.roomh)]:
            pass
        self.emit(poly([corners[1],corners[2],(corners[2][0],corners[2][1]+3.8),(corners[1][0],corners[1][1]+3.8)],'#475057','#30383c',.22))
        self.emit(poly([corners[2],corners[3],(corners[3][0],corners[3][1]+3.8),(corners[2][0],corners[2][1]+3.8)],'#333e44','#30383c',.2))
        self.emit(poly(corners,'#d7e1e0','#707f83',.42))
        fl={(x,y):(obj,rgb) for (x,y,obj,rgb) in L.floors}
        for x in range(L.xmin,L.xmin+L.roomw):
          for y in range(L.ymin,L.ymin+L.roomh):
            ft,rgb=fl.get((x,y),('',[0,0,0]))
            if 'CERAMIC_MED' in ft: color='#d4e0e5'
            elif 'CONCRETE' in ft:color='#e4dcd5'
            elif 'CERAMIC' in ft:color='#e5e9e7'
            else:color='#dce4e2'
            if (x+y)%3==0:color={'#d4e0e5':'#d8e3e6','#e4dcd5':'#e7ded6','#e5e9e7':'#ecedeb','#dce4e2':'#e1e7e4'}[color]
            a,b,c,d=L.tile(x,y)
            self.emit(poly([a,b,c,d],color,'#b7c7c9',.17))
            # subtle differentiated grout reflections (each tile actual xml coordinate)
            if (x+y)%4==0:self.emit(line((a[0]+.12,a[1]+.15),(b[0]-.13,b[1]+.1),'#f4f8f6',.14))
        self.emit('</g>')
    def outer_walls(self):
        L=self.L; z=10.8 if L.key=='small' else 9.8
        p=L.p
        a=p(L.xmin,L.ymin); b=p(L.xmin+L.roomw,L.ymin);d=p(L.xmin,L.ymin+L.roomh)
        self.emit('<g id="back-walls" inkscape:groupmode="layer" inkscape:label="Original back walls">')
        self.emit(poly([a,d,(d[0],d[1]-z),(a[0],a[1]-z)],'#cbb3a6','#55585d',.35))
        self.emit(poly([a,b,(b[0],b[1]-z),(a[0],a[1]-z)],'#e8d1c2','#56585d',.35))
        # subtle panel shading and wall trims
        for i in range(1,L.roomh):
          q=p(L.xmin,L.ymin+i);self.emit(line(q,(q[0],q[1]-z),'#9b8f88',.14,extra='opacity=".42"'))
        for i in range(1,L.roomw):
          q=p(L.xmin+i,L.ymin);self.emit(line(q,(q[0],q[1]-z),'#a89b93',.14,extra='opacity=".40"'))
        self.emit(line((a[0],a[1]-z),(b[0],b[1]-z),'#524d4e',.65))
        self.emit(line((a[0],a[1]-z),(d[0],d[1]-z),'#625552',.65))
        self.emit(line(a,b,'#a58a7e',.3));self.emit(line(a,d,'#99867c',.3))
        # Native wall windows, precisely where corresponding XML doors carry window ids
        for x,y,t,identifier in L.walls:
          if 'WINDOW' not in identifier or 'GLASS_WALL' in identifier:continue
          if t not in ('m_doorSW','m_doorSE'):continue
          if x != L.xmin and y!=L.ymin:continue
          if t=='m_doorSW' and y==L.ymin:
             aa=p(x,y);bb=p(x+1,y)
          elif t=='m_doorSE' and x==L.xmin:
             aa=p(x,y);bb=p(x,y+1)
          else:continue
          # window fits back wall region; no invented geometry
          q1=(aa[0]+.2,aa[1]-z*.71);q2=(bb[0]-.2,bb[1]-z*.71)
          q3=(bb[0]-.2,bb[1]-z*.35);q4=(aa[0]+.2,aa[1]-z*.35)
          self.emit(poly([q1,q2,q3,q4],'#6da5a8','#61787b',.27,extra='opacity=".85"'))
          self.emit(line((q1[0]+.3,q1[1]+.15),(q2[0]-.3,q2[1]+.15),'#cee5dd',.22))
        self.emit('</g>')
    def internal_walls(self):
        L=self.L
        ws=[(x,y,t,i) for x,y,t,i in L.walls if (x>L.xmin and x<L.xmin+L.roomw and y>=L.ymin and y<L.ymin+L.roomh) or (y>L.ymin and y<L.ymin+L.roomh and x>=L.xmin and x<L.xmin+L.roomw)]
        self.emit('<g id="room-divider-architecture" inkscape:groupmode="layer" inkscape:label="Actual glass and inner partitions">')
        # Distinct original segmented glass dividers, rather than a generic empty room.
        for x,y,t,i in ws:
            if not t.startswith('m_wall'): continue
            if t=='m_wallSE':a,b=L.p(x,y),L.p(x,y+1)
            else:a,b=L.p(x,y),L.p(x+1,y)
            paired='m_door'+t[-2:]
            doorid=next((ii for xx,yy,tt,ii in L.walls if xx==x and yy==y and tt==paired), '')
            isglass=bool(doorid) and ('GLASS' in doorid or 'WINDOW' in doorid)
            if isglass:
                plane=[(a[0],a[1]-.7),(b[0],b[1]-.7),(b[0],b[1]-7.0),(a[0],a[1]-7.0)]
                self.emit(poly(plane,'#83bbc2','#47858d',.26,extra='opacity=".42"'))
                self.emit(line((a[0],a[1]-7),(b[0],b[1]-7),'#609fa7',.42,extra='opacity=".8"'))
                self.emit(line((a[0],a[1]-4),(b[0],b[1]-4),'#c1edef',.2,extra='opacity=".85"'))
                self.emit(line((a[0],a[1]-.7),(a[0],a[1]-7),'#3c8390',.38,extra='opacity=".72"'))
            else:
                self.emit(line(a,b,'#b1a4a0',.34,extra='opacity=".8"'))
                self.emit(line((a[0],a[1]-5),(b[0],b[1]-5),'#a9b6b8',.2,extra='opacity=".55"'))
        # Actual door/window edges from XML: no extra entrances or random wall cuts.
        for x,y,t,i in L.walls:
            if not t.startswith('m_door'):continue
            if t=='m_doorSE':aa,bb=L.p(x,y),L.p(x,y+1)
            else:aa,bb=L.p(x,y),L.p(x+1,y)
            if 'GLASS' in i or 'WINDOW' in i:
              self.emit(line((aa[0],aa[1]-1),(bb[0],bb[1]-1),'#4f9aa3',.4,extra='opacity=".66"'))
              if 'DOOR' in i and 'WINDOW' not in i:
                mid=((aa[0]+bb[0])/2,(aa[1]+bb[1])/2)
                self.emit(circ(mid[0],mid[1]-3.3,.24,'#f0f7f1'))
        self.emit('</g>')
    # little equipment shape helper use iso cuboids to keep consistent with genuine isometric reference.
    def box(self,cx,cy,w=.7,d=.68,z=4,top='#e5eceb',west='#c0cdcb',east='#9eafb2',stroke='#627275',line_width=.23):
        L=self.L; P=lambda dx,dy,height: (cx+(dx-dy)*L.pitchx,cy+(dx+dy)*L.pitchy-height)
        a=P(-w/2,-d/2,z);b=P(w/2,-d/2,z);c=P(w/2,d/2,z);d0=P(-w/2,d/2,z)
        bp=P(w/2,-d/2,0);cp=P(w/2,d/2,0);dp=P(-w/2,d/2,0)
        return poly([b,c,cp,bp],east,stroke,line_width)+poly([d0,c,cp,dp],west,stroke,line_width)+poly([a,b,c,d0],top,stroke,line_width)
    def top_line(self,cx,cy,w=.5,d=.5,height=3,shift=.12,color='#788d92'):
        L=self.L
        p=lambda x,y,z: (cx+(x-y)*L.pitchx,cy+(x+y)*L.pitchy-z)
        return line(p(-w/2,-d/2,height),p(w/2,-d/2,height),color,.2)
    def office_chair(self,cx,cy):
        d=''
        d+=circ(cx,cy+1.65,.55,'#505f61')
        for x in [-1.1,1.1]:d+=line((cx,cy+1.2),(cx+x,cy+2.1),'#5b6b6f',.4)
        d+=line((cx,cy+.7),(cx,cy-2.25),'#52666a',.4)
        d+=self.box(cx,cy+.7,.49,.48,1.0,'#a2b7bb','#7a9ca1','#6c858a')
        d+=rect(cx-1,cy-4.25,2.15,3.05,'#8faeb1','#576d72',.24,r=.5)
        d+=line((cx-.65,cy-3.6),(cx+.7,cy-3.6),'#c2d5d4',.2)
        return d
    def instrument(self,cx,cy,id):
        d=''
        if 'HEMATOLOGY' in id:
            d+=self.box(cx,cy,.76,.73,5.3,'#f0f2ef','#c7d3d1','#a3b8b8')
            d+=poly([(cx-.7,cy-5.8),(cx+.34,cy-5.8),(cx+1.12,cy-4.6),(cx-.08,cy-4.72)],'#80b5b8','#668e94',.22)
            d+=rect(cx-.43,cy-5.78,.86,.75,'#538b92','#607f82',.17,r=.09)
            d+=line((cx-.25,cy-5.62),(cx+.17,cy-5.62),'#daeeed',.16)
            d+=rect(cx+.67,cy-3.05,.36,.22,'#d8a38c',r=.09)
        elif id=='OBJECT_RIA':
            d+=self.box(cx,cy,.66,.73,4.7,'#eef3ef','#c5d1ce','#90aab1')
            d+=poly([(cx-.9,cy-4.2),(cx+.13,cy-4.8),(cx+1.0,cy-3.8),(cx-.04,cy-3.25)],'#7ab3b5','#6c8b8e',.14)
            d+=rect(cx-.27,cy-4.67,.58,.27,'#334f57')
            d+=circ(cx+.58,cy-3.6,.23,'#bf756f')
        elif 'THERMAL_CYCLER' in id:
            d+=self.box(cx,cy,.62,.7,4.6,'#edf2ee','#c6d3d0','#9bb7b9')
            d+=poly([(cx-.48,cy-4.7),(cx+.1,cy-5),(cx+.62,cy-4.2),(cx+.05,cy-4.0)],'#aac4c4','#798d94',.17)
            d+=rect(cx+.5,cy-2.92,.35,.25,'#609aa5')
        elif id=='OBJECT_PRINTER':
            d+=self.box(cx,cy,.6,.67,2.5,'#ecede9','#b1c2c1','#8da5a7')
            d+=line((cx-.75,cy-2.3),(cx+.4,cy-2.6),'#4c7079',.22)
            d+=poly([(cx-.48,cy-2.8),(cx+.2,cy-3.15),(cx+.48,cy-2.65),(cx-.2,cy-2.36)],'#fafaf5','#8ea1a1',.13)
        elif id=='OBJECT_PC':
            d+=self.box(cx,cy,.44,.45,.7,'#dfe8e7','#a7babb','#92adaf')
            d+=line((cx,cy-.45),(cx,cy-4.4),'#52696b',.43)
            d+=poly([(cx-.98,cy-5.9),(cx+.65,cy-5.9),(cx+.65,cy-3.8),(cx-.98,cy-3.8)],'#465c62','#243c42',.26)
            d+=rect(cx-.75,cy-5.6,1.15,1.5,'#7cb5bb',r=.08)
            d+=line((cx-.4,cy-5.16),(cx+.22,cy-5.16),'#bce3e6',.17)
            d+=poly([(cx-.9,cy-2.4),(cx+.05,cy-2.7),(cx+.87,cy-2.25),(cx-.1,cy-1.9)],'#aebcbd','#738589',.13)
        elif id=='OBJECT_TABLE_LAMP':
            d+=line((cx-.55,cy),(cx-.04,cy-4.2),'#5a7172',.36)
            d+=poly([(cx-.7,cy-4.45),(cx+.7,cy-4.55),(cx+1.15,cy-3.7),(cx-.7,cy-3.48)],'#f2edd6','#978d82',.2)
        elif id in ('OBJECT_LAB_EQUIPMENT','OBJECT_LAB_EQUIPMENT2','OBJECT_LAB_BURETTES','OBJECT_SURGERY_INSTRUMENTS'):
            # true piece silhouettes on a native lab table, not generic cubes
            d+=self.box(cx,cy,.72,.68,.46,'#c4d3ce','#9cacab','#7b999a')
            if 'BURETTES' in id:
                d+=line((cx,cy-1),(cx,cy-5.9),'#5c8787',.33)
                for dx in [-.6,.05,.7]:
                    d+=line((cx+dx,cy-1.45),(cx+dx,cy-5.2),'#639eaa',.28)
                    d+=circ(cx+dx,cy-1.4,.2,'#c06e67')
            elif 'SURGERY' in id:
                for dx in [-.75,-.2,.35,.8]:
                    d+=line((cx+dx,cy-2.0),(cx+dx+.4,cy-3.2),'#768d9e',.32)
                    d+=circ(cx+dx+.4,cy-3.2,.12,'#e2e9e4')
            else:
                for dx,color in [(-.65,'#a7c7c7'),(-.1,'#bc716b'),(.44,'#729eb6')]:
                    d+=rect(cx+dx,cy-3.4, .39, 2.0,color,'#638b91',.16,r=.15)
                    d+=rect(cx+dx-.05,cy-3.6, .47,.44,'#eee9e0','#8c9e9f',.12,r=.1)
                if '2' in id:d+=poly([(cx-.2,cy-3.8),(cx+.83,cy-3.85),(cx+1.0,cy-3.2),(cx-.16,cy-3.08)],'#89babc','#658a8f',.13)
        else:
            d+=self.box(cx,cy,.6,.6,3.2)
        return d
    def largefurniture(self,cx,cy,id):
        d=''
        if id in ('OBJECT_LAB_SINK','OBJECT_SINK_KITCHEN'):
            d+=self.box(cx,cy,.78,.84,3.3,'#f0f0ea','#c2cbc7','#8daab0')
            d+=poly([(cx-.88,cy-3.6),(cx-.2,cy-4.04),(cx+.48,cy-3.6),(cx-.18,cy-3.14)],'#a5c8c9','#6f9b9e',.18)
            d+=line((cx+.3,cy-4.2),(cx+.3,cy-5.2),'#718989',.35)
            d+=line((cx+.3,cy-5.2),(cx-.2,cy-5.1),'#718989',.3)
            d+=circ(cx-.24,cy-4.3,.15,'#d9eeed')
        elif 'FRIDGE' in id:
            d+=self.box(cx,cy,.73,.67,8.3,'#f1f2ec','#d9dfdb','#a4b6b8')
            d+=poly([(cx-.91,cy-7.0),(cx+.37,cy-7.9),(cx+.86,cy-6.1),(cx-.39,cy-5.3)],'#8bbabc','#537d83',.2)
            d+=line((cx-.7,cy-6.6),(cx+.37,cy-7.3),'#d7edef',.2)
            d+=rect(cx+.65,cy-4.3,.22,1.85,'#c4d5d5',r=.06)
        elif 'SCRUBS_SHELF' in id or id=='OBJECT_LAB_SHELF':
            tall='TALL' in id
            height=8.8 if tall else 6.4
            d+=self.box(cx,cy,.72,.73,height,'#ecf0ed','#d0d9d5','#9bafb4')
            # vertical open front & two color-coded supply bands
            for ix in range(3 if tall else 2):
                yy=cy-height+1.55+ix*(height-2.0)/(3 if tall else 2)
                d+=line((cx-.8,yy),(cx+.57,yy-.55),'#64858a',.18)
                for dx,clr in [(-.35,'#6babb3'),(.05,'#c6a678'),(.4,'#bd8480')]:
                    d+=rect(cx+dx,yy-.93,.28,.72,clr,'#8b9b9d',.11,r=.05)
            d+=line((cx+.75,cy-height+.4),(cx+.8,cy-.7),'#cddfdd',.2)
        elif 'OXYGEN_TANK' in id:
            d+=rect(cx-.36,cy-6,.8,5.7,'#6baca4','#577b7b',.23,r=.4)
            d+=line((cx-.2,cy-5.85),(cx+.4,cy-5.85),'#d8ece7',.26)
            d+=line((cx+.04,cy-6.45),(cx+.04,cy-5.96),'#516c6f',.3)
        elif 'TRASH_BIN' in id or id=='OBJECT_PLASTIC_HAMPER':
            red='04' in id
            d+=self.box(cx,cy,.55,.55,2.8 if red else 3.3,('#be7770' if red else '#c4c5b9'),('#a45756' if red else '#a3a6a2'),('#7f4c50' if red else '#868f91'))
            d+=line((cx-.48,cy-2.8),(cx+.3,cy-3.3),'#e7d5ce',.18)
        elif id=='OBJECT_INSTRUMETNS_TABLE':
            d+=self.box(cx,cy,.85,.75,3.4,'#e6ebe6','#a1b1b1','#839da0')
            for xx in [-.45,.3]:d+=line((cx+xx,cy-2.5),(cx+xx,cy+.05),'#708b90',.2)
        elif id=='OBJECT_TABLE_SQUERE':
            d+=self.box(cx,cy,.91,.89,2.7,'#eef0e9','#bac9c6','#94aeb0')
            d+=line((cx-1,cy-1),(cx-.55,cy+1),'#759497',.15)
        elif id in ('OBJECT_LAB_CABINET','OBJECT_LAB_HALF_DESK','OBJECT_CABINET_DOORS','OBJECT_CABINET_DRAWERS','OBJECT_EQUIPMENT_CABINET'):
            half='HALF_DESK' in id
            height=3.0 if half else 4.1
            d+=self.box(cx,cy,.9,.89,height,'#e5e9e6','#bec9c6','#929da1')
            for dx in [-.53,.15]:
                d+=line((cx+dx,cy-height+1.5),(cx+dx+.52,cy-height+1.45),'#8f9897',.19)
                d+=circ(cx+dx+.22,cy-height+1.7,.13,'#777d7d')
        else:d+=self.box(cx,cy,.67,.67,3.2)
        return d
    def wall_object(self,cx,cy,id):
        """Draw only owner-saved wall attachment objects, never introduce new ones."""
        cy=cy-4.7
        d=''
        if 'SHELF_WALL' in id or 'CABINET_WALL' in id:
            d+=self.box(cx,cy,.63,.34,2.7,'#e5ece9','#a5c4c4','#91abae')
            for xx,color in [(-.48,'#6a9eaa'),(.04,'#b77166'),(.4,'#c5b58e')]:
                d+=rect(cx+xx,cy-2.95,.27,.68,color,'#7b9599',.1,r=.08)
        elif 'CLOCK' in id:
            d+=circ(cx,cy-2.5,.87,'#fcf9f1','#707c80',.25)
            d+=line((cx,cy-2.5),(cx+.24,cy-2.85),'#55646a',.16)
        elif 'NOTICE_BOARD' in id or 'POSTER_' in id:
            d+=rect(cx-1.05,cy-4.0,2.05,2.45,'#eeeae0','#867d76',.24,r=.12)
            d+=rect(cx-.75,cy-3.7,1.46,.42,'#7caeb5',r=.07)
            for k in range(3):
                d+=line((cx-.67,cy-2.85+k*.37),(cx+.52,cy-2.85+k*.37),'#ab8f83',.13)
        elif 'DEZINFECTION' in id:
            d+=rect(cx-.4,cy-3.8,.8,2.5,'#e2e7e6','#859a9c',.2,r=.16)
            d+=rect(cx-.25,cy-2.96,.5,.54,'#7db9b8')
        else: d+=self.box(cx,cy,.52,.3,2.8)
        return d

    def all_objects(self):
        L=self.L
        self.emit('<g id="xml-placed-furniture" inkscape:groupmode="layer" inkscape:label="Actual XML furniture and equipment">')
        # XML elements stay one-to-one with SVG object groups, even if a composite's parts are rendered separately.
        vals=[]
        for x,y,kind,obj,angle in L.items:
            depth=(x-L.xmin)+(y-L.ymin)
            rank={'wall':-1,'composite':0,'center':1,'attachment':2}.get(kind,1)
            vals.append((depth,x,y,rank,obj,angle,kind))
        vals.sort()
        for i,(depth,x,y,rank,obj,angle,kind) in enumerate(vals):
            cx,cy=L.p(x+.5,y+.5)
            if kind=='wall': picture=self.wall_object(cx,cy,obj)
            elif kind=='composite':picture=self.largefurniture(cx,cy,obj)
            elif obj=='OBJECT_CHAIR_SMALL':picture=self.office_chair(cx,cy)
            elif obj in ['OBJECT_PC','OBJECT_PRINTER','OBJECT_HEMATOLOGY_ANALYZER','OBJECT_RIA','OBJECT_THERMAL_CYCLER','OBJECT_TABLE_LAMP','OBJECT_LAB_BURETTES','OBJECT_LAB_EQUIPMENT','OBJECT_LAB_EQUIPMENT2','OBJECT_SURGERY_INSTRUMENTS']:
                # attachment object: visually sits on underlying laboratory counter, never a newly added machine
                picture=self.instrument(cx,cy-2.0 if kind=='attachment' else cy,obj)
            else:picture=self.largefurniture(cx,cy,obj)
            attr=f'data-xml-id="{escape(obj)}" data-kind="{kind}" data-tile="{x},{y}" data-facing="{escape(angle)}"'
            self.group(f'object-{i:03d}',attr,picture)
        self.emit('</g>')
    def render(self):
        L=self.L
        self.emit(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" version="1.1" width="104" height="104" viewBox="0 0 104 104" data-layout="{L.key}" data-room-width="{L.roomw}" data-room-height="{L.roomh}" data-xml-sha256="{EXPECTED[L.key]}">
<title>Clinical toxicology laboratory — {L.roomw} × {L.roomh} owner-authored prefab</title><desc>Original layered isometric sprite faithfully based on room, wall, door, furniture and equipment locations from owner-supplied saved XML. No original game imagery copied.</desc>
<defs>
<linearGradient id="window-glass" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#cae4e1"/><stop offset=".52" stop-color="#78b2b9"/><stop offset="1" stop-color="#497b84"/></linearGradient>
</defs>''')
        self.floor();self.outer_walls();self.internal_walls();self.all_objects()
        # thin, neutral upper outline akin to vanilla prefab. No text embedded in gameplay sprite.
        self.emit('</svg>')
        return '\n'.join(self.output).encode('utf-8')

def build():
    import sys
    inputs=Path(sys.argv[1]) if len(sys.argv)>1 else OUT.parent/"Prefabs"
    outputs=Path(sys.argv[2]) if len(sys.argv)>2 else OUT.parent
    outputs.mkdir(parents=True,exist_ok=True)
    hashes={}
    for key,(src,w) in ROOMS.items():
        xml=inputs/src
        L=get_layout(key,xml)
        svgb=Scene(L).render()
        svg=outputs/'art_sources'/f'toxicology_{key}.svg'
        svg.parent.mkdir(parents=True,exist_ok=True)
        svg.write_bytes(svgb)
        rawpng=cairosvg.svg2png(bytestring=svgb,output_width=416,output_height=416)
        import io
        im=Image.open(io.BytesIO(rawpng)).convert('RGBA')
        img=im.resize((104,104),Image.Resampling.LANCZOS)
        png=outputs/'Assets'/'ABCL'/'Prefabs'/f'toxicology_{key}.png'
        png.parent.mkdir(parents=True,exist_ok=True)
        img.save(png,optimize=False)
        root=ET.fromstring(xml.read_bytes())
        tile_count=len(root.findall('./m_tiles/PrefabTile'))
        room=root.find('./m_rooms/PrefabRoom')
        lo=[int(room.findtext('m_positionBottom/m_x')),int(room.findtext('m_positionBottom/m_y'))]
        hi=[int(room.findtext('m_positionTop/m_x')),int(room.findtext('m_positionTop/m_y'))]
        hashes[key]={
            'room_bounds':[lo,hi], 'size':[L.roomw,L.roomh], 'tile_count':tile_count,
            'object_count':len(L.items), 'object_ids':dict(L.all_ids),
            'source_sha256':EXPECTED[key],
            'icon_sha256':h(png.read_bytes()), 'icon_pixels':[104,104],
            'svg_sha256':h(svgb),
            'revision':'TO-004 L4 rejected previews reworked; XML-derived original isometric art'
        }
    outmanifest=outputs/'art_sources'/'manifest.json'
    outmanifest.write_text(json.dumps(hashes,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(hashes,indent=2,ensure_ascii=False))

if __name__=='__main__':build()
