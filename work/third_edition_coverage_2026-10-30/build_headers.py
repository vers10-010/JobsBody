from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
ROOT=Path(__file__).parent
files=sorted(Path(r'F:\Все Фото третьего издания').glob('*.jpg'))
for start in range(0,len(files),12):
    sheet=Image.new('RGB',(2000,2160),'white')
    d=ImageDraw.Draw(sheet)
    for j,p in enumerate(files[start:start+12]):
        im=Image.open(p)
        if im.height>im.width: im=im.rotate(90,expand=True)
        w,h=im.size
        for k,crop in enumerate([im.crop((0,0,w,int(h*.23))),im.crop((0,int(h*.77),w,h)).rotate(180)]):
            crop=ImageOps.contain(crop,(950,160))
            sheet.paste(crop,(50+k*975,j*180+15))
        d.text((2,j*180+70),str(start+j+1),fill='black')
        d.line((0,j*180,2000,j*180),fill='gray')
    sheet.save(ROOT/f'headers_{start//12+1:02d}.jpg',quality=96)
    print(start+1,flush=True)
