from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import json

ROOT = Path(__file__).parent
SOURCE = Path(r'F:\Все Фото третьего издания')
files = sorted(SOURCE.glob('*.jpg'))
records = []
for start in range(0, len(files), 12):
    sheet = Image.new('RGB', (1800, 1920), 'white')
    draw = ImageDraw.Draw(sheet)
    footer = Image.new('RGB', (1600, 12 * 190), 'white')
    fd = ImageDraw.Draw(footer)
    for j, path in enumerate(files[start:start+12]):
        im = Image.open(path)
        im.load()
        if im.height > im.width:
            im = im.rotate(90, expand=True)
        idx = start+j+1
        records.append({'index':idx, 'file':path.name, 'bytes':path.stat().st_size})
        thumb = ImageOps.contain(im, (590, 445))
        x, y = (j%3)*600, (j//3)*480
        sheet.paste(thumb, (x, y+30))
        draw.text((x+5,y+5), f'{idx:03d} {path.stem}', fill='black')
        w,h=im.size
        crop=im.crop((0,int(h*.77),w,int(h*.99)))
        crop=ImageOps.contain(crop,(1500,165))
        footer.paste(crop, (90,j*190+20))
        fd.text((5,j*190+60), f'{idx:03d}', fill='black')
    sheet.save(ROOT/f'sheet_{start//12+1:02d}.jpg', quality=92)
    footer.save(ROOT/f'footer_{start//12+1:02d}.jpg', quality=95)
    print(f'Finished {start+1}-{min(start+12,len(files))}', flush=True)
(ROOT/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
