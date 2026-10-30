from pathlib import Path
import sys, json, asyncio, re, subprocess, hashlib, wave, math, array, shutil
sys.dont_write_bytecode = True
sys.path.insert(0,r'C:\Users\vers1\Documents\Codex\2026-08-31\gt\work\tts_runtime')
sys.path.insert(0,str(Path(__file__).parent/'runtime'))
import edge_tts
from PIL import Image

ROOT=Path(r'C:\Work\JobsBody')
WORK=Path(__file__).parent
OUT=ROOT/'outputs/Third_Edition_Reader_2026-10-30'
FF=Path(r'C:\Users\vers1\Documents\Codex\2026-08-31\gt\work\audio_runtime\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe')
RATE='-15%'
SR=24000
VOICE={'dmitry':('Дмитрий','ru-RU-DmitryNeural','en-US-GuyNeural'),'svetlana':('Светлана','ru-RU-SvetlanaNeural','en-US-JennyNeural')}
BLOCKS=[
 {'id':'heading','kind':'heading','page':'335–336','text':'Глава 11. Новые взгляды на рубеже веков. Новая физиология.'},
 {'id':'p1','kind':'author','page':'335','text':'Вот уже немногим более десяти лет книга «Тело Иова» ищет свой путь в мире, и меня чрезвычайно радует то, как её приняли. Меня также воодушевляет, сколько разговоров с отдельными людьми и групповых семинаров она дала мне возможность провести.'},
 {'id':'p2','kind':'author','page':'335','text':'То, что, по-видимому, складывается из бесед, переписки, лекций и практических занятий, поводом для которых стала эта книга, оказалось для меня очень приятной неожиданностью. Я думал, что буду говорить о том, как практическое знание физиологии может обогатить различные подходы к телесной работе и повысить их эффективность. Вместо этого я обнаруживаю гораздо более широкое, открытое исследование всей совокупности возможностей человеческой жизни и развития, на которые указывают самые разные виды альтернативной терапии.'},
 {'id':'p3','kind':'author','page':'335–336','text':'Я встречаю общее понимание многих тем, которые пытался выразить в «Теле Иова», и глубокий интерес к физиологии совершенно нового рода. В основе этой идеи «новой физиологии» лежит включение ряда исходных предположений, которые часто систематически исключаются из теорий, определяющих направление клинических исследований: 1) что психика (mind) существует вполне реально и, где бы она ни проявлялась, участвует в мире предметов и событий в той же мере, что и любой элемент периодической таблицы; 2) что способность к разумному различению (discriminating intelligence) присутствует во всех формах жизни; 3) что преобладающие способы мышления и эмоциональные состояния непосредственно и существенным образом влияют на физическое развитие и функционирование моего тела; 4) что изменения моих физиологических функций непосредственно и динамически влияют на характер моих мыслей и эмоциональных состояний; 5) что существуют конкретные действия — как со стороны психики, так и со стороны тела, — способные значительно улучшить взаимодействие и устойчивость моего единства тела и психики (bodymind); и 6) что улучшение этого взаимодействия не только укрепляет наше здоровье и способствует личностному развитию, но и значительно расширяет воспринимаемый нами мир, делая его более содержательным и многогранным.'},
 {'id':'comment','kind':'comment','page':'Комментарий','text':'Комментарий переводчика. Что автор здесь имеет в виду. Автор предлагает расширить рамки рассмотрения телесной работы: учитывать взаимное влияние физиологических процессов, мыслей и эмоциональных состояний. Он прямо называет перечисленные положения исходными предположениями. Этот фрагмент сам по себе не доказывает их и не объясняет конкретные механизмы влияния. Словом bodymind он обозначает тело и психику как взаимосвязанное целое. Это не название отдельной анатомической структуры.'},
]

def save(p,obj): p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def decode(p):
    return subprocess.run([str(FF),'-v','error','-i',str(p),'-f','s16le','-ac','1','-ar',str(SR),'pipe:1'],check=True,capture_output=True).stdout
def encode(p,pcm):
    subprocess.run([str(FF),'-v','error','-f','s16le','-ac','1','-ar',str(SR),'-i','pipe:0','-c:a','libmp3lame','-b:a','128k','-y',str(p)],input=pcm,check=True,capture_output=True)

async def main():
    if OUT.exists() and not (OUT/'translation.json').exists():
        raise RuntimeError('Unexpected existing output directory')
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'audio').mkdir(exist_ok=True)
    (OUT/'originals').mkdir(exist_ok=True)
    (WORK/'tts_parts').mkdir(exist_ok=True)
    save(OUT/'translation.json',{'edition':3,'chapter':11,'scope':'Первые три полных абзаца; не вся глава','blocks':BLOCKS,'human_listened':False})
    (OUT/'Перевод.txt').write_text('\n\n'.join(b['text'] for b in BLOCKS),encoding='utf-8-sig')
    sources=[]
    for name,rotation in [('PXL_20261019_201603392.MP.jpg',180),('PXL_20261019_201620241.jpg',90)]:
        p=ROOT/'source_photos/Third_Edition_2026-10-19'/name
        im=Image.open(p).rotate(rotation,expand=True)
        dest=OUT/'originals'/name
        im.save(dest,quality=96)
        sources.append({'file':f'originals/{name}','source':str(p),'source_sha256':sha(p),'rotation_degrees':rotation,'derived_image':True})
    voices={}; qa=[]
    for key,(label,ru,en) in VOICE.items():
        clips=[];complete=b''
        for b in BLOCKS:
            runs=[];pos=0
            for match in re.finditer(r'[A-Za-z]+(?: [A-Za-z]+)*',b['text']):
                if match.start()>pos:runs.append((ru,b['text'][pos:match.start()]))
                runs.append((en,match.group()));pos=match.end()
            if pos<len(b['text']):runs.append((ru,b['text'][pos:]))
            assert ''.join(t for v,t in runs)==b['text']
            pcm=b''
            for i,(voice,text) in enumerate(runs):
                if not re.search(r'\w',text):continue
                p=WORK/'tts_parts'/f'{key}_{b["id"]}_{i:02d}.mp3'
                for attempt in range(3):
                    try:
                        await edge_tts.Communicate(text,voice,rate=RATE,connect_timeout=20,receive_timeout=60).save(str(p))
                        part=decode(p)
                        assert len(part)>SR*.08*2
                        break
                    except Exception:
                        if attempt==2:raise
                        await asyncio.sleep(2)
                pcm+=part
            p=OUT/'audio'/f'{key}_{b["id"]}.mp3'
            encode(p,pcm)
            decoded=decode(p); samples=array.array('h',decoded)
            duration=len(decoded)/(SR*2)
            peak=max(abs(s) for s in samples)
            rms=math.sqrt(sum(s*s for s in samples)/len(samples))
            assert duration>1 and peak>100 and rms>10
            clips.append({'id':b['id'],'src':f'audio/{p.name}','duration':duration})
            qa.append({'file':p.name,'bytes':p.stat().st_size,'sha256':sha(p),'seconds':duration,'peak_pcm16':peak,'rms_pcm16':rms,'decoded':True,'human_listened':False})
            complete+=pcm+b'\0\0'*int(SR*.65)
            print(f'{key}: {b["id"]} ready ({duration:.1f}s)',flush=True)
        full=OUT/'audio'/f'{key}_full.mp3'
        encode(full,complete)
        assert len(decode(full))>0
        voices[key]={'label':label,'clips':clips,'download':f'audio/{full.name}'}
    data={'blocks':BLOCKS,'voices':voices,'sources':sources,'defaultVoice':'dmitry'}
    save(OUT/'reader-data.json',data)
    template=(WORK/'reader.html').read_text(encoding='utf-8')
    (OUT/'index.html').write_text(template.replace('/*READER_DATA*/',json.dumps(data,ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')
    (OUT/'Открыть ридер.cmd').write_bytes('@echo off\r\nstart "" "%~dp0index.html"\r\n'.encode('ascii'))
    (OUT/'НАЧАТЬ ЗДЕСЬ.txt').write_text('Третье издание Job’s Body. Глава 11, страницы 335–336: первые три полных абзаца.\nОткройте index.html или «Открыть ридер.cmd».\nВ поле «Голос» выберите Дмитрия или Светлану и нажмите «Слушать».\nТекст перевода полный для выбранных трёх абзацев. Комментарий переводчика отделён; его озвучку можно выключить.\nЭто самостоятельный ридер третьего издания. Основной ридер первого издания не менялся.\nОзвучка создана Microsoft Edge TTS; русский текст — Дмитрий / Светлана, английские вставки — Guy / Jenny. Темп синтеза −15%.\nСостояние: исходник получен; перевод готов; аудио готово. Прослушивание пользователем не подтверждено.\n',encoding='utf-8-sig')
    save(OUT/'verification.json',{'source_received':True,'translation_ready':True,'audio_ready':True,'human_listened':False,'scope':'Три полных абзаца страниц 335–336, заголовок и комментарий переводчика','voices':VOICE,'rate':RATE,'audio':qa,'source_photos_unchanged':all(sha(Path(s['source']))==s['source_sha256'] for s in sources),'full_line_readability_not_audited':True})
    print('Reader ready',flush=True)

if __name__=='__main__':asyncio.run(main())
