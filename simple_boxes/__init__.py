bl_info={'name':'Simple_boxes','author':'Alemus','version':(0,0,2),'blender':(3,6,0),'location':'View3D > Sidebar > Simple_boxes','description':'Parametric printable boxes and removable lids','category':'Add Mesh'}
import bpy
from .properties import SB_Settings
from .ui import CLASSES
from .localization import TRANSLATIONS

def register():
    bpy.utils.register_class(SB_Settings)
    bpy.types.Object.sb_settings=bpy.props.PointerProperty(type=SB_Settings)
    bpy.types.Object.sb_owner=bpy.props.PointerProperty(type=bpy.types.Object)
    for cls in CLASSES: bpy.utils.register_class(cls)
    bpy.app.translations.register(__package__,TRANSLATIONS)

def unregister():
    bpy.app.translations.unregister(__package__)
    for cls in reversed(CLASSES): bpy.utils.unregister_class(cls)
    del bpy.types.Object.sb_owner
    del bpy.types.Object.sb_settings
    bpy.utils.unregister_class(SB_Settings)
