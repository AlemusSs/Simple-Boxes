from .properties import GROUPS
RU=['Длина основания','Ширина основания','Высота основания','Толщина стенок','Толщина дна','Внутренняя глубина','Внешние вертикальные углы','Верхние внешние края','Нижние внешние края','Внутренние вертикальные углы','Переход стенок в дно','Толщина перегородок','Высота перегородок','Глубина посадки','Зазор на сторону','Толщина стенок крышки','Толщина верха крышки','Верхние края крышки','Нижние края крышки','Внутренний переход крышки']
labels=[item[1] for group,items in GROUPS for item in items]
pairs=dict(zip(labels,RU))
pairs.update({'Create box':'Создать коробку','Dimensions':'Основные размеры','Rounding':'Скругления','Sections':'Внутренние секции','Lid':'Крышка','Display':'Отображение','Lid closed':'Крышка надета','Lid beside':'Крышка рядом','Select a box':'Выберите коробку','Sections along length':'Секций по длине','Sections along width':'Секций по ширине','Millimeters':'Миллиметры'})
TRANSLATIONS={'ru_RU':{('*',k):v for k,v in pairs.items()}}

import json
from pathlib import Path
for locale, messages in json.loads(Path(__file__).with_name("translations.json").read_text(encoding="utf8")).items():
    TRANSLATIONS[locale] = {(context, key): value for key,value in messages.items() for context in ("*", "Operator")}
