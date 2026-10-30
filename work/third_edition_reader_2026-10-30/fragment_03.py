from pathlib import Path
import sys, asyncio, json, html, re, array, math
sys.dont_write_bytecode = True
import build as base

OUT=base.ROOT/'outputs/Third_Edition_Reader_2026-10-30/fragment_03'
SOURCE=base.ROOT/'source_photos/Third_Edition_2026-10-19/PXL_20261019_201620241.jpg'
EN=[
"The second reason for this new edition is the inclusion of some exciting new research and speculations from two biologists whose work is new to me, and whose ideas and findings significantly expand the possible scope of bodywork and our growing sense of a new understanding of physiology. These are scientists that are not merely challenging old beliefs. They already have left them behind and are actively thinking in some altogether new terms. Their work does not merely provide bits and pieces of data that can be taken as provisional evidence of a body/mind connection. They are whole-heartedly, and with success, pursuing the details of that connection. They are managing to combine rigorous research with a sense of intuition, to entertain clarity of thought along with an immediate awareness of their own subjective experiences. And they are asking questions that were defined as out of bounds and ignored for too long.",
"James Oschman is a cell biologist connected with the Marine Biological Laboratory in Woods Hole, Massachusetts. After experiencing what was for him the profound effects of a Rolfing series, he shifted his research focus to the study of connective tissue and its multi-dimensional roles in the human organism. His biological background and direct bodywork experience led him to some very novel ideas about what connective tissue is up to. And what he has to add to our appreciation of the complex texture of fascia and what it contributes to our health and healing goes far beyond the biomechanical and structural properties described by Ida Rolf and others cited in the first edition.",
"Candace Pert initiated the discovery of the neuropeptides, which I believe is an extremely significant scientific breakthrough in our conception of the bodymind. These information-carrying molecules circulate freely about the body, and their action at their receptor sites appears to be one of the principle connections not only between our various organs and biological processes, but also between our mental and physical dimensions. Not only does an understanding of neuropeptides lead us to the biochemical and physiological basis of our emotional lives, it also reveals specific pathways and mechanisms through which our feeling states continually impact our physiology. Far beyond a general notion of the mind affecting the body, Pert has demonstrated many concrete ways in which our emotions, thoughts, glandular secretions, immune responses, and behavioral patterns all utilize neuropeptide messages to orchestrate their interactions at every level. Our appreciation of these molecules has enormous therapeutic implications. And like Oschman, Pert has personally experienced the ways in which bodywork and other alternative approaches can effectively use these interactions to change our physical and emotional lives for the better.",
"Taken together, the fresh perspectives and discoveries of these two scientists seem to me to indicate a definite direction towards a new understanding of physiology, one in which the power of the mind is as present and concretely accounted for as that of the liver, or insulin, or the gene. And quite beyond that, I believe that their departure from the old paradigm offers some fascinating perspectives on the ways in which we envision both the varieties of human bondage and those precious bits of wiggle-room called freedom."
]
RU=[
'Вторая причина появления этого нового издания — включение в него некоторых увлекательных новых исследований и предположений двух биологов, с чьими работами я познакомился лишь недавно и чьи идеи и открытия значительно расширяют возможную сферу применения телесной работы и наше постепенно складывающееся новое понимание физиологии. Эти учёные не просто ставят под сомнение старые убеждения. Они уже оставили их позади и активно мыслят в совершенно новых категориях. Их работы не просто предоставляют разрозненные данные, которые можно было бы принять за предварительные свидетельства связи тела и психики. Они со всей увлечённостью и небезуспешно исследуют конкретные подробности этой связи. Им удаётся сочетать строгие исследования с интуицией, ясность мысли — с непосредственным осознанием собственного субъективного опыта. И они задают вопросы, которые слишком долго объявляли выходящими за допустимые рамки и оставляли без внимания.',
'Джеймс Ошман — клеточный биолог, связанный с Морской биологической лабораторией в Вудс-Хоуле, штат Массачусетс. Испытав на себе глубокое, по его собственному ощущению, воздействие серии сеансов рольфинга, он переключил основное внимание в своих исследованиях на соединительную ткань (connective tissue) и её многообразные роли в организме человека. Его знания в области биологии и непосредственный опыт телесной работы привели его к некоторым весьма новым идеям о том, что делает соединительная ткань (connective tissue). А то, что он добавляет к нашему пониманию сложной организации фасции (fascia) и её вклада в наше здоровье и исцеление, выходит далеко за пределы биомеханических и структурных свойств, описанных Идой Рольф и другими авторами, на которых я ссылался в первом издании.',
'Кэндис Перт положила начало открытию нейропептидов (neuropeptides), которое я считаю чрезвычайно значительным научным прорывом в нашем понимании единства тела и психики (bodymind). Эти молекулы, переносящие информацию, свободно циркулируют по телу, и их действие в местах расположения соответствующих рецепторов (receptor sites), по-видимому, представляет собой одно из основных связующих звеньев не только между различными органами и биологическими процессами, но и между психической и физической сторонами нашего существования. Понимание нейропептидов (neuropeptides) не только подводит нас к биохимическим и физиологическим основам нашей эмоциональной жизни, но и раскрывает конкретные пути и механизмы, посредством которых наши эмоциональные состояния постоянно влияют на физиологию. Выходя далеко за рамки общего представления о влиянии психики (mind) на тело, Перт показала множество конкретных способов, которыми наши эмоции, мысли, секреция желёз, иммунные реакции и формы поведения используют нейропептидные сигналы, чтобы согласовывать своё взаимодействие на всех уровнях. Понимание этих молекул имеет огромное значение для терапии. И, подобно Ошману, Перт на собственном опыте испытала, как телесная работа и другие альтернативные подходы могут эффективно использовать эти взаимодействия, чтобы менять нашу физическую и эмоциональную жизнь к лучшему.',
'Взятые вместе, новые взгляды и открытия этих двух учёных, как мне представляется, указывают определённое направление к новому пониманию физиологии — такому, в котором влияние психики (mind) столь же реально присутствует и столь же конкретно учитывается, как влияние печени (liver), инсулина или гена. И, кроме того, я считаю, что их отход от старой парадигмы открывает некоторые захватывающие перспективы в том, как мы представляем себе и разнообразные формы человеческой несвободы, и те драгоценные крупицы пространства для манёвра, которые называются свободой.'
]
COMMENT='Комментарий переводчика. Что автор здесь имеет в виду. Автор объясняет вторую причину нового издания и связывает её с работами Джеймса Ошмана и Кэндис Перт. Он видит в них основание для расширения своего понимания телесной работы. Оценки научного значения, исторических заслуг и терапевтической эффективности здесь принадлежат автору книги; перевод сохраняет их и не означает отдельной проверки этих утверждений. В физическом смысле автор описывает перенос химических сигналов молекулами и их действие через соответствующие рецепторы. Выражение «согласовывать взаимодействие» передаёт его образную формулировку: молекулы не принимают решений. Подробной последовательности от конкретного телесного воздействия до выделения определённого нейропептида и лечебного результата в этом отрывке нет. Конкретный механизм действия соединительной ткани здесь также не изложен. «Пространство для манёвра» в последнем абзаце — метафора человеческой свободы.'
PAGES=['336–337','337','337','337']

def prepare():
    if OUT.exists():
        saved=json.loads((OUT/'translation.json').read_text(encoding='utf-8'))
        assert saved['translation']==RU and saved['comment']==COMMENT
        return
    OUT.mkdir()
    (OUT/'Оригинал.txt').write_text('Bodywork and Science. Pages 336–337. Four paragraphs before Sweet Science.\nSource: '+str(SOURCE)+'\n\n'+'\n\n'.join(EN),encoding='utf-8-sig')
    (OUT/'Перевод.txt').write_text('Глава 11. Новые взгляды на рубеже веков\nТелесная работа и наука — окончание раздела\nСтраницы 336–337. Четыре следующих полных абзаца.\n\n'+'\n\n'.join(RU)+'\n\nЧто автор здесь имеет в виду\n\n'+COMMENT,encoding='utf-8-sig')
    base.save(OUT/'translation.json',dict(edition=3,chapter=11,pages='336–337',translation=RU,comment=COMMENT,source=str(SOURCE),source_sha256=base.sha(SOURCE),source_received=True,translation_ready=True,audio_ready=False,human_listened=False,next_heading='Sweet Science'))

async def main():
    prepare()
    (OUT/'audio').mkdir(exist_ok=True)
    saved=json.loads((OUT/'translation.json').read_text(encoding='utf-8'))
    assert saved['source_sha256']==base.sha(SOURCE)
    hashes={n:base.sha(OUT/n) for n in ['Перевод.txt','Оригинал.txt']}
    blocks=[dict(id=f'p{i+7}',kind='author',page=PAGES[i],text=t) for i,t in enumerate(RU)]
    blocks.append(dict(id='comment',kind='comment',page='Комментарий',text=COMMENT))
    full=b''; checks=[]
    for b in blocks:
        runs=[]; pos=0
        for m in re.finditer(r'[A-Za-z]+(?: [A-Za-z]+)*',b['text']):
            if m.start()>pos:runs.append(('ru-RU-SvetlanaNeural',b['text'][pos:m.start()]))
            runs.append(('en-US-JennyNeural',m.group()));pos=m.end()
        if pos<len(b['text']):runs.append(('ru-RU-SvetlanaNeural',b['text'][pos:]))
        assert ''.join(t for _,t in runs)==b['text']
        pcm=b''
        for i,(voice,t) in enumerate(runs):
            if not re.search(r'\w',t):continue
            p=OUT/'audio'/f'part_{b["id"]}_{i:02d}.mp3'
            for attempt in range(3):
                try:
                    if not p.exists() or p.stat().st_size==0:
                        await base.edge_tts.Communicate(t,voice,rate=base.RATE,connect_timeout=20,receive_timeout=60).save(str(p))
                    part=base.decode(p);assert len(part)>1000
                    pcm+=part;break
                except Exception:
                    if attempt==2:raise
        p=OUT/'audio'/f'svetlana_{b["id"]}.mp3';base.encode(p,pcm)
        decoded=base.decode(p);samples=array.array('h',decoded)
        peak=max(abs(s) for s in samples);rms=math.sqrt(sum(s*s for s in samples)/len(samples))
        assert len(decoded)>base.SR*2 and peak>100 and rms>10
        checks.append(dict(file=p.relative_to(OUT).as_posix(),bytes=p.stat().st_size,sha256=base.sha(p),seconds=len(decoded)/(base.SR*2),peak_pcm16=peak,rms_pcm16=rms,decoded=True))
        if b['kind']=='author':full+=pcm+b'\0\0'*int(base.SR*.65)
        print(b['id']+' ready',flush=True)
    p=OUT/'audio/svetlana_author.mp3';base.encode(p,full)
    checks.append(dict(file=p.relative_to(OUT).as_posix(),bytes=p.stat().st_size,sha256=base.sha(p),seconds=len(base.decode(p))/(base.SR*2),decoded=True))
    sections=''
    for b in blocks:
        label='Что автор здесь имеет в виду' if b['kind']=='comment' else 'Абзац '+b['id'][1:]+' · стр. '+b['page']
        sections+=f'<section><h2>{label}</h2><p>{html.escape(b["text"])}</p><audio controls preload="metadata" src="audio/svetlana_{b["id"]}.mp3"></audio></section>'
    page='<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Телесная работа и наука — окончание</title><style>body{max-width:850px;margin:40px auto;padding:0 22px;background:#fbf8ef;color:#243e36;font:22px/1.75 Georgia}h1{line-height:1.2}h2{font:22px Segoe UI}audio{width:100%}section{margin:40px 0}small{font:16px Segoe UI}a{color:#244c3f}</style><h1>Телесная работа и наука — окончание</h1><small>Job’s Body · Третье издание · Глава 11 · Страницы 336–337 · Фрагмент 3</small><p>Четыре абзаца авторского текста подряд. Голос: Светлана.</p><audio controls preload="metadata" src="audio/svetlana_author.mp3"></audio><p><a download href="audio/svetlana_author.mp3">Скачать озвучку авторского текста</a></p>'+sections+'<p><a href="../fragment_02/index.html">Предыдущий фрагмент</a></p><small>Исходник получен · Перевод готов · Аудио готово · Прослушивание пользователем не подтверждено.<br>Следующее место продолжения: Sweet Science, стр. 337. Комментарий отделён от авторского текста.</small></html>'
    assert all((OUT/r).exists() for r in re.findall(r'(?:src|href)="([^"]+)"',page))
    (OUT/'index.html').write_text(page,encoding='utf-8')
    assert all(base.sha(OUT/n)==h for n,h in hashes.items())
    saved.update(audio_ready=True,blocks=blocks)
    base.save(OUT/'translation.json',saved)
    base.save(OUT/'verification.json',dict(source_received=True,translation_ready=True,audio_ready=True,human_listened=False,source=str(SOURCE),source_sha256=base.sha(SOURCE),source_photo_visually_checked=True,audio=checks,voice='ru-RU-SvetlanaNeural',english_voice='en-US-JennyNeural',rate=base.RATE,reader_links_exist=True,browser_visual_check=False))
    print('Complete',flush=True)

if __name__=='__main__':
    prepare()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
