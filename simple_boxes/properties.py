import bpy
from bpy.props import FloatProperty,IntProperty,PointerProperty,EnumProperty,StringProperty
from .builder import update,display_update
GROUPS=[('Dimensions',[('length','Length',120),('width','Width',80),('height','Height',50),('wall','Wall thickness',2),('bottom','Bottom thickness',2),('depth','Inner depth',48)]),('Rounding',[('radius','Outer corner radius',5),('base_top','Top edge radius',0),('base_bottom','Bottom edge radius',0),('inner_radius','Inner corner radius',3),('floor_radius','Floor transition radius',0)]),('Sections',[('partition','Partition thickness',2),('partition_height','Partition height',35)]),('Lid',[('seating','Seating depth',15),('clearance','Clearance per side',.3),('lid_wall','Lid wall thickness',2),('lid_top','Lid top thickness',2),('lid_top_radius','Lid top edge radius',0),('lid_bottom_radius','Lid bottom edge radius',0),('lid_transition','Lid inner transition',0)])]
class SB_Settings(bpy.types.PropertyGroup):
    pass
SB_Settings.__annotations__={}
for group,items in GROUPS:
    for key,label,default in items:
        SB_Settings.__annotations__[key]=FloatProperty(name=label,description='Millimeters',default=default,min=0 if ('radius' in key or key in {'clearance','lid_transition','base_top','base_bottom'}) else .1,max=2000,update=update)
for key,label in [('nx','Sections along length'),('ny','Sections along width')]:
    SB_Settings.__annotations__[key]=IntProperty(name=label,default=1,min=1,max=16,update=update)
for key in ('base','lid'):
    SB_Settings.__annotations__[key]=PointerProperty(type=bpy.types.Object)
SB_Settings.__annotations__['display']=EnumProperty(name='Display',items=[('CLOSED','Lid closed',''),('BESIDE','Lid beside','')],default='BESIDE',update=display_update)
SB_Settings.__annotations__['error']=StringProperty()
