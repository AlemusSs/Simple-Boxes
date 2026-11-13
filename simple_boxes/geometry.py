import bpy, bmesh, math

def prism(name, x, y, z0, z1, radius):
    r = max(0, min(radius, x/2-0.001, y/2-0.001))
    points=[]
    if r < 0.0001:
        points=[(-x/2,-y/2),(x/2,-y/2),(x/2,y/2),(-x/2,y/2)]
    else:
        for cx,cy,start in [(x/2-r,y/2-r,0),(-x/2+r,y/2-r,90),(-x/2+r,-y/2+r,180),(x/2-r,-y/2+r,270)]:
            for i in range(13):
                a=math.radians(start+i*90/12)
                points.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    n=len(points)
    verts=[(a*.001,b*.001,z*.001) for z in (z0,z1) for a,b in points]
    faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts,[],faces); mesh.update()
    obj=bpy.data.objects.new(name,mesh); bpy.context.scene.collection.objects.link(obj)
    obj["sb_profile"]=[x,y,z0,z1,r,0.0,0.0]
    return obj

def bevel(obj, radius, z):
    if radius<=0: return
    x,y,z0,z1,r,top,bottom=obj['sb_profile']
    radius=min(radius,(z1-z0)/3,min(x,y)/4)
    if abs(z-z1)<1e-6: top=radius
    else: bottom=radius
    obj['sb_profile']=[x,y,z0,z1,r,top,bottom]
    def contour(inset,height):
        rr=max(0,r-inset); xx=x/2-inset; yy=y/2-inset
        if r==0:
            return [(a*.001,b*.001,height*.001) for a,b in [(-xx,-yy),(xx,-yy),(xx,yy),(-xx,yy)]]
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


def subtract(obj, cutter):
    mod=obj.modifiers.new('Cavity','BOOLEAN'); mod.operation='DIFFERENCE'; mod.solver='EXACT'; mod.object=cutter
    deps=bpy.context.evaluated_depsgraph_get(); deps.update()
    mesh=bpy.data.meshes.new_from_object(obj.evaluated_get(deps),depsgraph=deps)
    old=obj.data; obj.modifiers.remove(mod); obj.data=mesh; bpy.data.meshes.remove(old)
    data=cutter.data; bpy.data.objects.remove(cutter,do_unlink=True); bpy.data.meshes.remove(data)

def validate(mesh):
    bm=bmesh.new(); bm.from_mesh(mesh)
    bmesh.ops.dissolve_limit(bm,angle_limit=0.00001,verts=list(bm.verts),edges=list(bm.edges),use_dissolve_boundaries=False)
    good=all(e.is_manifold for e in bm.edges) and all(f.calc_area()>1e-15 for f in bm.faces)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(mesh); bm.free()
    if not good: raise ValueError('Generated mesh is not manifold or contains degenerate faces')

