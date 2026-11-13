import bpy
from .builder import update
from .properties import GROUPS

def settings(context):
    obj=context.object
    owner=obj.sb_owner if obj else None
    return owner.sb_settings if owner else None

class SB_Create(bpy.types.Operator):
    bl_idname='simple_boxes.create'; bl_label='Create box'; bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        base=bpy.data.objects.new('Box base',bpy.data.meshes.new('Box base'))
        lid=bpy.data.objects.new('Box lid',bpy.data.meshes.new('Box lid'))
        context.collection.objects.link(base); context.collection.objects.link(lid)
        base.location=context.scene.cursor.location
        lid.parent=base
        base.sb_owner=base; lid.sb_owner=base
        p=base.sb_settings; p.base=base; p.lid=lid
        update(p,context)
        for obj in context.selected_objects: obj.select_set(False)
        base.select_set(True); context.view_layer.objects.active=base
        return {'FINISHED'}

class SB_Main(bpy.types.Panel):
    bl_label='Simple_boxes'; bl_idname='SB_PT_main'; bl_space_type='VIEW_3D'; bl_region_type='UI'; bl_category='Simple_boxes'
    def draw(self,context):
        self.layout.operator('simple_boxes.create')
        p=settings(context)
        if p:
            self.layout.prop(p,'display',expand=True)
            self.layout.use_property_split=True
            for key,label,default in GROUPS[0][1]:
                if key!='bottom': self.layout.prop(p,key)
        if p and p.error: self.layout.label(text=p.error,icon='ERROR')

CLASSES=[SB_Create,SB_Main]
def draw_group(self,context):
    p=settings(context)
    if not p: self.layout.label(text='Select a box'); return
    self.layout.use_property_split=True
    for key in self.fields: self.layout.prop(p,key)
    if self.bl_label=='Lid': self.layout.label(text=bpy.app.translations.pgettext_iface('Height')+': %.2f mm'%(p.seating+p.lid_top))
for index,(name,items) in enumerate(GROUPS[1:]):
    fields=[x[0] for x in items]
    if name=='Sections': fields=['nx','ny']+fields
    if name=='Display': fields=['display']
    cls=type('SB_Group'+str(index),(bpy.types.Panel,),dict(bl_label=name,bl_idname='SB_PT_group'+str(index),bl_parent_id='SB_PT_main',bl_space_type='VIEW_3D',bl_region_type='UI',bl_category='Simple_boxes',bl_options={'DEFAULT_CLOSED'},fields=fields,draw=draw_group))
    CLASSES.append(cls)
