import json,zipfile,hashlib
from pathlib import Path
version='0.0.2';root=Path('simple_boxes');out=Path('dist');out.mkdir(exist_ok=True)
for legacy in (False,True):
    name=f'Simple_boxes_{version}'+('_legacy' if legacy else '')+'.zip'
    with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED) as z:
        for p in root.iterdir():
            if p.suffix not in ('.py','.json','.toml'):continue
            if legacy and p.suffix=='.toml':continue
            z.write(p,('simple_boxes/' if legacy else '')+p.name)
        z.write('LICENSE',('simple_boxes/' if legacy else '')+'LICENSE')
p=out/f'Simple_boxes_{version}.zip'
entry=dict(id='simple_boxes',schema_version='1.0.0',name='Simple_boxes',tagline='Create parametric printable boxes with removable lids',version=version,type='add-on',maintainer='Alemus',license=['SPDX:GPL-3.0-or-later'],blender_version_min='4.2.0',website='https://github.com/AlemusSs/Simple_boxes',archive_url=f'https://github.com/AlemusSs/Simple_boxes/releases/download/v{version}/{p.name}',archive_size=p.stat().st_size,archive_hash='sha256:'+hashlib.sha256(p.read_bytes()).hexdigest())
Path('index.json').write_text(json.dumps(dict(version='v1',blocklist=[],data=[entry]),indent=2),encoding='utf8')
