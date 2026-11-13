import bpy,sys,os,math
sys.path.insert(0,os.getcwd())
import simple_boxes
from simple_boxes.geometry import prism,bevel,validate
simple_boxes.register()
for radius in (0,5):
    obj=prism('test',120,80,0,50,radius)
    bevel(obj,.5,50);bevel(obj,.5,0)
    # Quarter circle has seven distinct height levels at each rounded edge.
    levels=sorted(set(round(v.co.z,8) for v in obj.data.vertices))
    assert len(levels)==14,levels
    validate(obj.data)
    print('PASS curved profiles',radius,len(levels))
bpy.ops.simple_boxes.create();p=bpy.context.object.sb_settings
p.depth=49.5
assert abs(p.depth-49.5)<.001
p.base_top=.3;p.base_bottom=.3;p.floor_radius=.3;p.lid_top_radius=.3;p.lid_bottom_radius=.3;p.lid_transition=.1
assert not p.error,p.error
for obj in (p.base,p.lid): validate(obj.data)
print('PASS all edge rounding and independent depth')
assert len([c for c in __import__('simple_boxes.ui',fromlist=['CLASSES']).CLASSES if getattr(c,'bl_label','') in {'Dimensions','Display'}])==0
print('PASS main panel layout structure')
simple_boxes.unregister()
