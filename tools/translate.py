import bpy,sys,os,json,urllib.request,urllib.parse,concurrent.futures
sys.path.insert(0,os.getcwd())
from simple_boxes.localization import pairs
keys=list(pairs)
locales=[x[1] for x in bpy.app.translations.locales if x] if False else list(bpy.app.translations.locales)
def translate(locale):
    if locale in ('en_US','ru_RU'): return locale,None
    target=locale.split('_')[0]
    target={'zh':'zh-CN' if 'CN' in locale else 'zh-TW','sr':'sr','pt':'pt'}.get(target,target)
    url='https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl='+target+'&dt=t&q='+urllib.parse.quote('\n'.join(keys))
    try:
        with urllib.request.urlopen(url,timeout=25) as response: data=json.load(response)
        lines=''.join(x[0] for x in data[0]).split('\n')
        if len(lines)!=len(keys): raise ValueError('translation count mismatch')
        return locale,dict(zip(keys,lines))
    except Exception as exc: print('FAILED',locale,str(exc));return locale,None
out={'ru_RU':pairs}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    for locale,result in pool.map(translate,locales):
        if result: out[locale]=result
with open('simple_boxes/translations.json','w',encoding='utf8') as f: json.dump(out,f,ensure_ascii=False,indent=2)
print('TRANSLATED',len(out),'OF',len(locales),locales)
