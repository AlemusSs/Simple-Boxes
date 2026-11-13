import bpy
from .geometry import prism,bevel,subtract,validate
from .dimensions import clamp,cells
BUSY=set()

def place(p):
    if not p.base or not p.lid: return
    p.lid.location=(0,0,(p.height-p.seating)*.001) if p.display=='CLOSED' else ((p.length+2*(p.clearance+p.lid_wall)+10)*.001,0,0)

def display_update(p,context): place(p)

def update(p,context):
    key=p.id_data.as_pointer()
    if key in BUSY or not p.base or not p.lid: return
    BUSY.add(key); temps=[]
    try:
        clamp(p)
        base=prism('temporary',p.length,p.width,0,p.height,p.radius); temps.append(base)
        limit=min(p.wall,p.height-p.depth)/3
        bevel(base,min(p.base_top,limit),p.height); bevel(base,min(p.base_bottom,limit),0)
        floor=p.height-p.depth
        # A shared upper cavity leaves lower equal-sized cells and joined partitions.
        if p.partition_height < p.depth-.001:
            cut=prism('cut',p.length-2*p.wall,p.width-2*p.wall,floor+p.partition_height,p.height+1,max(p.inner_radius,p.radius-p.wall))
            subtract(base,cut)
        for x,y,sx,sy in cells(p):
            cut=prism('cut',sx,sy,floor,p.height+1,max(p.inner_radius,p.radius-p.wall) if p.nx*p.ny==1 else p.inner_radius)
            bevel(cut,min(p.floor_radius,sx/4,sy/4,p.depth/3),floor)
            cut.location.x=x*.001; cut.location.y=y*.001
            subtract(base,cut)
        inner_x=p.length+2*p.clearance; inner_y=p.width+2*p.clearance
        lid=prism('temporary',inner_x+2*p.lid_wall,inner_y+2*p.lid_wall,0,p.seating+p.lid_top,p.radius+p.clearance+p.lid_wall); temps.append(lid)
        bevel(lid,min(p.lid_top_radius,p.lid_top/3,p.lid_wall/3),p.seating+p.lid_top)
        bevel(lid,min(p.lid_bottom_radius,p.lid_wall/3),0)
        cut=prism('cut',inner_x,inner_y,-1,p.seating,p.radius+p.clearance)
        # Keep the fitting envelope outside the complete base corner profile.
        bevel(cut,min(p.lid_transition,p.clearance/2,p.lid_top/3),p.seating)
        subtract(lid,cut)
        for obj in temps: validate(obj.data)
        for target,source in zip((p.base,p.lid),temps):
            old=target.data; target.data=source.data
            if old.users==0: bpy.data.meshes.remove(old)
        p.error=''; place(p)
    except Exception as exc:
        p.error=str(exc)
        print('Simple_boxes:',exc)
    finally:
        for obj in temps:
            mesh=obj.data; bpy.data.objects.remove(obj,do_unlink=True)
            if mesh.users==0: bpy.data.meshes.remove(mesh)
        BUSY.discard(key)
