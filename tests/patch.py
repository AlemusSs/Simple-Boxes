from pathlib import Path
p=Path('simple_boxes/geometry.py');s=p.read_text(encoding='utf-8-sig');s=s.replace('return obj','obj["sb_profile"]=[x,y,z0,z1,r,0.0,0.0]\n    return obj',1)
a=s.index('    bm=bmesh.new(); bm.from_mesh(obj.data)',s.index('def bevel'));b=s.index('\ndef subtract',a)
s=s[:a]+'''    x,y,z0,z1,r,top,bottom=obj['sb_profile']
    radius=min(radius,(z1-z0)/3,min(x,y)/4)
    if abs(z-z1)<1e-6: top=radius
    else: bottom=radius
    obj['sb_profile']=[x,y,z0,z1,r,top,bottom]
    def contour(inset,height):
        rr=max(0,r-inset); xx=x/2-inset; yy=y/2-inset
        pts=[]
        for cx,cy,start in [(xx-rr,yy-rr,0),(-xx+rr,yy-rr,90),(-xx+rr,-yy+rr,180),(xx-rr,-yy+rr,270)]:
            for i in range(13):
                angle=math.radians(start+i*90/12)
                # Retain a tiny round corner to avoid coincident ring vertices.
                cr=max(rr,0.00001)
                pts.append(((cx+cr*math.cos(angle))*.001,(cy+cr*math.sin(angle))*.001,height*.001))
        return pts
    rings=[]
    if bottom:
        for i in range(7):
            t=i*math.pi/12
            rings.append(contour(bottom*(1-math.sin(t)),z0+bottom*(1-math.cos(t))))
    else: rings.append(contour(0,z0))
    if top:
        for i in range(7):
            t=i*math.pi/12
            rings.append(contour(top*(1-math.cos(t)),z1-top+top*math.sin(t)))
    else: rings.append(contour(0,z1))
    n=len(rings[0]); verts=[v for ring in rings for v in ring]
    faces=[tuple(reversed(range(n))),tuple(range((len(rings)-1)*n,len(rings)*n))]
    for j in range(len(rings)-1):
        for i in range(n): faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    old=obj.data; mesh=bpy.data.meshes.new('Rounded profile'); mesh.from_pydata(verts,[],faces);mesh.update();obj.data=mesh
    bpy.data.meshes.remove(old)

''' + s[b:]
s=s.replace('    good=all(e.is_manifold','    bmesh.ops.dissolve_limit(bm,angle_limit=0.00001,verts=list(bm.verts),edges=list(bm.edges),use_dissolve_boundaries=False)\n    good=all(e.is_manifold')
p.write_text(s,encoding='utf-8')
p=Path('simple_boxes/ui.py');s=p.read_text(encoding='utf-8-sig');s=s.replace('        if p and p.error:', '''        if p:
            self.layout.prop(p,'display',expand=True)
            self.layout.use_property_split=True
            for key,label,default in GROUPS[0][1]:
                if key!='bottom': self.layout.prop(p,key)
        if p and p.error:''');s=s.replace("enumerate(GROUPS+[('Display',[]) ])","enumerate(GROUPS[1:])");p.write_text(s,encoding='utf-8')
p=Path('simple_boxes/dimensions.py');s=p.read_text(encoding='utf-8-sig');s=s.replace('    p.bottom=min(p.bottom,p.height-.1)\n    p.depth=min(p.depth,p.height-p.bottom)','    p.depth=min(p.depth,max(.1,p.height-.1))');p.write_text(s,encoding='utf-8')
p=Path('simple_boxes/builder.py');s=p.read_text(encoding='utf-8-sig').replace('min(p.wall,p.bottom)/3','min(p.wall,p.height-p.depth)/3');p.write_text(s,encoding='utf-8')
p=Path('tests/smoke.py');s=p.read_text(encoding='utf-8-sig').replace('p.height-p.bottom+.0001','p.height-.1+.0001');p.write_text(s,encoding='utf-8')
