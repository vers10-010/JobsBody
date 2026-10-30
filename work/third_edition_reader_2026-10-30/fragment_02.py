from pathlib import Path
import sys, asyncio, json, html, hashlib
sys.dont_write_bytecode = True
import build as base

OUT = base.ROOT/'outputs/Third_Edition_Reader_2026-10-30/fragment_02'
SOURCE = base.ROOT/'source_photos/Third_Edition_2026-10-19/PXL_20261019_201620241.jpg'
EN = [
"So my original assumption as I began Job’s Body was that existing clinical research would surely shed light upon the concrete reasons why bodywork is so effective for so many conditions. More recently I have begun to experience something of a sea-change in this operating assumption. I now believe that experienced and effective bodyworkers have something very interesting to offer to recent developments in the biological, physiological, psychological, sociological, and medical sciences.",
"The first reason for this new edition of the book is that it gives me an opportunity to air some additional observations and growing convictions of my own with regard to this new way of understanding human development. One of the primary issues concerning therapy that has become clearer to me is that popular notions of science are always lagging considerably behind the latest discoveries and insights—insights which frequently up-end the concepts previously regarded to be true. By continuing to place our faith and base our actions on models that are outmoded, we often prevent ourselves from pursuing alternatives that would make our lives better. One does not tend to try things that are believed to be impossible, and previous generations of biologists have certainly placed much of the impact of the mind upon the body outside the realm of possibility.",
"These outdated popular conceptions create what I call ‘double binds in the bodymind’—misplaced ideas and efforts that our current beliefs compel us to pursue, but which cannot improve our situation because they are not aligned with the actual needs and processes of our organisms. Among these double binds that subvert our accurate self-assessment and successful self-regulation are a number of the most widely held ideas about the nature of science and the nature of human beings."
]
RU = [
'Итак, когда я начинал писать «Тело Иова», я исходил из предположения, что уже существующие клинические исследования непременно прольют свет на конкретные причины того, почему телесная работа столь эффективна при столь многих состояниях. Однако в последнее время это исходное предположение начало у меня коренным образом меняться. Теперь я считаю, что опытные специалисты, успешно практикующие телесную работу, могут внести весьма интересный вклад в новейшие направления развития биологии, физиологии, психологии, социологии и медицины.',
'Первая причина появления этого нового издания книги заключается в том, что оно даёт мне возможность высказать некоторые дополнительные наблюдения и всё более крепнущие собственные убеждения, связанные с этим новым пониманием развития человека. Один из основных вопросов, касающихся терапии, который стал для меня яснее, состоит в том, что распространённые представления о науке всегда значительно отстают от новейших открытий и идей — идей, которые нередко переворачивают понятия, прежде считавшиеся истинными. Продолжая верить устаревшим моделям и основывать на них свои действия, мы часто сами мешаем себе искать альтернативы, способные сделать нашу жизнь лучше. Люди обычно не пытаются делать то, что считают невозможным, а предыдущие поколения биологов, несомненно, относили значительную часть влияния психики (mind) на тело к области невозможного.',
'Эти устаревшие распространённые представления создают то, что я называю «двойными ловушками в единстве тела и психики» (double binds in the bodymind): ошибочные идеи и усилия, к которым нас вынуждают наши нынешние убеждения, но которые не могут улучшить наше положение, поскольку не соответствуют действительным потребностям и процессам нашего организма. Среди таких двойных ловушек, подрывающих нашу способность точно оценивать собственное состояние и успешно осуществлять саморегуляцию, — ряд наиболее распространённых представлений о природе науки и природе человека.'
]
COMMENT = 'Комментарий переводчика. Что автор здесь имеет в виду. Автор описывает изменение собственной позиции: сначала он искал в клинических исследованиях объяснение эффективности телесной работы, а теперь полагает, что опыт её практиков может, в свою очередь, обогатить науку. Оценки эффективности и состояния науки здесь принадлежат автору; в этих трёх абзацах он не приводит подтверждающих исследований. Выражение «двойные ловушки» обозначает описанное им противоречие между привычными убеждениями и потребностями организма. Это образное описание, а не название анатомического или физиологического механизма. Конкретный механизм влияния психики на тело в этом фрагменте не указан.'

async def main():
    saved = json.loads((OUT/'translation.json').read_text(encoding='utf-8'))
    assert saved['translation'] == RU and saved['comment'] == COMMENT
    assert saved['source_sha256'] == base.sha(SOURCE)
    original_hashes = {name:base.sha(OUT/name) for name in ['Перевод.txt','Оригинал.txt']}
    (OUT/'audio').mkdir(exist_ok=True)
    blocks = [{'id':f'p{i+4}', 'kind':'author', 'page':'336', 'text':t} for i,t in enumerate(RU)]
    blocks.append({'id':'comment','kind':'comment','page':'Комментарий','text':COMMENT})
    title = 'Телесная работа и наука'
    full=b''; checks=[]
    for b in blocks:
        # Preserve English terms in the written translation; pronounce them with the matching English voice.
        import re
        runs=[]; pos=0
        for m in re.finditer(r'[A-Za-z]+(?: [A-Za-z]+)*',b['text']):
            if m.start()>pos: runs.append(('ru-RU-SvetlanaNeural',b['text'][pos:m.start()]))
            runs.append(('en-US-JennyNeural',m.group())); pos=m.end()
        if pos<len(b['text']): runs.append(('ru-RU-SvetlanaNeural',b['text'][pos:]))
        pcm=b''
        for i,(voice,t) in enumerate(runs):
            if not re.search(r'\w',t): continue
            p=OUT/'audio'/f'part_{b["id"]}_{i}.mp3'
            for attempt in range(3):
                try:
                    if not p.exists() or p.stat().st_size == 0:
                        await base.edge_tts.Communicate(t,voice,rate=base.RATE,connect_timeout=20,receive_timeout=60).save(str(p))
                    decoded=base.decode(p)
                    assert len(decoded)>1000
                    pcm+=decoded; break
                except Exception:
                    if attempt==2: raise
            # Intermediate parts remain available for audit and regeneration.
        p=OUT/'audio'/f'svetlana_{b["id"]}.mp3'
        base.encode(p,pcm)
        decoded=base.decode(p)
        assert len(decoded)>base.SR*2 and any(decoded)
        checks.append({'file':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':base.sha(p),'seconds':len(decoded)/(base.SR*2),'decoded':True})
        if b['kind']=='author': full+=pcm+b'\0\0'*int(base.SR*.65)
        print(b['id']+' ready',flush=True)
    p=OUT/'audio/svetlana_author.mp3'; base.encode(p,full)
    checks.append({'file':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':base.sha(p),'seconds':len(base.decode(p))/(base.SR*2),'decoded':True})
    sections=''
    for b in blocks:
        sections+=f'<section><h2>{"Что автор здесь имеет в виду" if b["kind"]=="comment" else "Абзац "+b["id"][1:]}</h2><p>{html.escape(b["text"])}</p><audio controls preload="metadata" src="audio/svetlana_{b["id"]}.mp3"></audio></section>'
    page='<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><style>body{max-width:850px;margin:40px auto;padding:0 22px;background:#fbf8ef;color:#243e36;font:22px/1.75 Georgia}h1{line-height:1.2}h2{font:22px Segoe UI}audio{width:100%}section{margin:40px 0}small{font:16px Segoe UI}a{color:#244c3f}</style><h1>'+title+'</h1><small>Job’s Body · Третье издание · Глава 11 · Страница 336 · Фрагмент 2</small><p>Три абзаца авторского текста подряд. Голос: Светлана.</p><audio controls preload="metadata" src="audio/svetlana_author.mp3"></audio><p><a download href="audio/svetlana_author.mp3">Скачать озвучку авторского текста</a></p>'+sections+'<p><a href="../index.html">Предыдущий фрагмент</a></p><small>Исходник получен · Перевод готов · Аудио готово · Прослушивание пользователем не подтверждено. Комментарий отделён от авторского текста. Следующий фрагмент начинается: The second reason for this new edition…</small></html>'
    (OUT/'index.html').write_text(page,encoding='utf-8')
    assert all(base.sha(OUT/name)==sha for name,sha in original_hashes.items())
    saved.update(audio_ready=True, human_listened=False, blocks=blocks)
    base.save(OUT/'translation.json',saved)
    base.save(OUT/'verification.json',{'source_received':True,'translation_ready':True,'audio_ready':True,'human_listened':False,'source_sha256':base.sha(SOURCE),'source':str(SOURCE),'audio':checks,'voice':'ru-RU-SvetlanaNeural','rate':base.RATE,'translation_checked_against_source_photo':True,'browser_visual_check':False})
    print('Complete',flush=True)

if __name__=='__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
