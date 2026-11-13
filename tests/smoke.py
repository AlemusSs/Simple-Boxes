import bpy,sys,os,time
sys.path.insert(0,os.getcwd())
import simple_boxes
from simple_boxes.geometry import validate
simple_boxes.register()
bpy.ops.simple_boxes.create()
p=bpy.context.object.sb_settings
for nx,ny in [(1,1),(2,1),(2,2),(3,2),(4,4)]:
    start=time.perf_counter(); p.nx=nx;p.ny=ny
    assert not p.error,p.error
    for obj in (p.base,p.lid): validate(obj.data)
    assert abs(p.base.dimensions.x-p.length*.001)<1e-5
    print('PASS sections',nx,ny,'seconds',time.perf_counter()-start)
for radius in (0,.5,1000):
    p.radius=radius
    assert not p.error,p.error
    print('PASS radius',radius)
p.radius=5;p.base_top=.3;p.base_bottom=.3;p.floor_radius=.3;p.lid_top_radius=.3;p.lid_bottom_radius=.3
assert not p.error,p.error
p.depth=1000
assert p.depth<=p.height-.1+.0001
p.display='CLOSED'
assert abs(p.lid.location.z-(p.height-p.seating)*.001)<1e-6
mesh=p.lid.data;p.display='BESIDE';assert p.lid.data==mesh
for i in range(2): bpy.ops.simple_boxes.create()
assert len([o for o in bpy.data.objects if o.sb_owner==o])==3
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.getcwd(),'tests','saved.blend'))
bpy.ops.wm.open_mainfile(filepath=os.path.join(os.getcwd(),'tests','saved.blend'))
p=bpy.context.object.sb_settings;p.length=135
assert not p.error,p.error
simple_boxes.unregister();simple_boxes.register();simple_boxes.unregister()
print('ALL TESTS PASSED',bpy.app.version_string)
