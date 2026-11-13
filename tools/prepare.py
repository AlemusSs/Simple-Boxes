import json
from pathlib import Path
p=Path('simple_boxes/localization.py');s=p.read_text(encoding='utf-8-sig');s+='\nimport json\nfrom pathlib import Path\nfor locale, messages in json.loads(Path(__file__).with_name("translations.json").read_text(encoding="utf8")).items():\n    TRANSLATIONS[locale] = {(context, key): value for key,value in messages.items() for context in ("*", "Operator")}\n';p.write_text(s,encoding='utf8')
p=Path('simple_boxes/ui.py');s=p.read_text(encoding='utf-8-sig').replace("text='Height: %.2f mm'%(p.seating+p.lid_top)","text=bpy.app.translations.pgettext_iface('Height')+': %.2f mm'%(p.seating+p.lid_top)");p.write_text(s,encoding='utf8')
p=Path('simple_boxes/__init__.py');p.write_text(p.read_text(encoding='utf-8-sig').replace('(0,0,1)','(0,0,2)'),encoding='utf8')
p=Path('simple_boxes/blender_manifest.toml');p.write_text(p.read_text(encoding='utf-8-sig').replace('0.0.1','0.0.2')+'\nwebsite = "https://github.com/AlemusSs/Simple_boxes"\n',encoding='utf8')
