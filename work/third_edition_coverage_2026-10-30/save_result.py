from pathlib import Path
import json
from collections import Counter

root = Path(__file__).parent
manifest = json.loads((root/'manifest.json').read_text(encoding='utf-8'))
assert len(manifest) == 245
front = {
    1: 'Передняя обложка: THIRD EDITION',
    2: 'Пустая внутренняя сторона обложки и About Job’s Body (отзывы)',
    3: 'Фронтиспис и титульная страница',
    4: 'Выходные данные и The Further Embodiment of Job',
    5: 'Посвящение и Preface to the Expanded Edition',
    6: 'Цитата и начало Contents',
    7: 'Продолжение Contents',
    8: 'Окончание Contents',
    9: 'xiv–xv: Acknowledgments и начало Foreword',
    10: 'xvi–xvii: окончание Foreword и начало Introduction',
    11: 'xviii–xix: Introduction',
    12: 'xx–xxi: Introduction',
    13: 'xxii–xxiii: Introduction',
    14: 'xxiv–xxv: Introduction',
    15: 'xxvi–xxvii: Introduction',
    16: 'xxviii–xxix: Introduction',
    17: 'xxx–xxxi: окончание Introduction',
    244: 'Задняя обложка',
    245: 'Общий вид задней обложки, корешка и передней обложки',
}
sections = [
    (1,20,'1. Job’s Dilemma'), (21,58,'2. Skin'),
    (59,90,'3. Connective Tissue'), (91,108,'4. Bone'),
    (109,144,'5. Muscle'), (145,182,'6. Nerve'),
    (183,244,'7. Muscle As Sense Organ'), (245,262,'8. The Sense of Effort'),
    (263,276,'9. Sensory Engrams'),
    (277,334,'10. Movements Toward Disease and Movements Toward Health'),
    (335,380,'11. Further Views at the Turn of the Century'),
    (381,408,'12. Sweet Science'), (409,418,'Epilogue: Job’s Body'),
    (419,426,'Appendix: Managing Multiple Sclerosis'),
    (427,435,'Notes'), (436,441,'Sources of Illustrations'),
    (442,446,'Works Cited, Additional Works Cited и пустая страница перед Index'),
    (447,450,'Index'), (451,451,'About the Author'),
]
rows=[]
seen=[]
for m in manifest:
    i=m['index']
    r=dict(m)
    if 18 <= i <= 243:
        pages=[1] if i==18 else [2*i-36,2*i-35]
        seen.extend(pages)
        r['arabic_pages']=pages
        r['description']=('xxxii (пустая) и 1' if i==18 else f'{pages[0]}–{pages[1]}')
        r['number_basis']='Визуальная последовательность разворотов; видимые номера, где напечатаны; для страниц без номера — соседние страницы и оглавление.'
    else:
        r['arabic_pages']=[]
        r['description']=front[i]
    rows.append(r)
counts=Counter(seen)
missing=sorted(set(range(1,452))-counts.keys())
repeated=sorted(p for p,c in counts.items() if c>1)
assert not missing and not repeated and len(seen)==451
result={
    'date':'2026-10-30', 'source':r'F:\Все Фото третьего издания',
    'edition':'Job’s Body, Deane Juhan, Third Edition',
    'image_count':245, 'arabic_page_range':[1,451],
    'missing_arabic_pages':missing, 'repeated_arabic_pages':repeated,
    'method':'Все 245 фото декодированы и визуально просмотрены на обзорных листах; отдельно просмотрены полосы с номерами каждого разворота. Оглавление и конечные разделы сверены. Номера ненумерованных страниц определены по месту в последовательности и оглавлению.',
    'scope_limit':'Проверено наличие страниц. Не выполнена построчная проверка читаемости всех слов, подписей, резкости и возможного обрезания мелких фрагментов у краёв. Физический экземпляр не обследован; неизвестные вставки вне сфотографированной последовательности не исключаются.',
    'originals_modified':False, 'photos':rows,
}
(root/'coverage.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
lines=[
    'Job’s Body — проверка полноты фотографий третьего издания',
    'Дата: 30 октября 2026 года',
    r'Исходная папка: F:\Все Фото третьего издания',
    '',
    'РЕЗУЛЬТАТ: по постраничной последовательности комплект полный.',
    'Просмотрены все 245 фотографий JPG. Все файлы успешно декодированы.',
    'Представлены страницы 1–451; пропусков и повторов страниц в этой последовательности не обнаружено.',
    'Есть начальные материалы: отзывы, фронтиспис, титульная страница, выходные данные, посвящение, предисловия, оглавление, благодарности, Foreword и Introduction до xxxi, пустая xxxii.',
    'Есть передняя и задняя обложки, корешок; общий снимок обложки повторяет её отдельные изображения.',
    '',
    'КАК ПРОВЕРЕНО',
    result['method'],
    'Соответствие фотографий страницам приведено ниже и в coverage.json. Порядковые номера фотографий — сортировка имён файлов по возрастанию.',
    'Наличие 451 номера проверено также по сформированной карте: каждый номер встречается один раз. Это проверка карты после визуального просмотра, а не независимое распознавание текста.',
    '',
    'ГРАНИЦЫ ВЫВОДА',
    result['scope_limit'],
    'Некоторые кадры перевёрнуты. На рабочих листах повёрнуты только уменьшенные изображения, исходные файлы не изменены.',
    'Для начальных страниц без напечатанного номера не приписывались выдуманные римские номера.',
    '',
    'СОСТАВ ПО РАЗДЕЛАМ',
]
for a,b,title in sections: lines.append(f'{a}–{b}: {title}')
lines += ['', 'КАРТА ФОТОГРАФИЙ']
for r in rows: lines.append(f"{r['index']:03d} | {r['file']} | {r['description']}")
lines += ['', 'ИЗМЕНЕНИЯ ФАЙЛОВ',
    'Оригиналы на F: не изменялись и не копировались в качестве резервной копии.',
    'В этой новой рабочей папке созданы только обзорные изображения, служебные сценарии, manifest.json, coverage.json и настоящий отчёт.',
    'Эта запись — результат проверки, подготовленный Codex; не журнал исходных реплик переписки.',
]
(root/'Результат проверки.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8-sig')
print(json.dumps({'photos':len(rows),'pages':len(seen),'missing':missing,'repeated':repeated,'report':str(root/'Результат проверки.txt')},ensure_ascii=True))
