"""Read-only asset checks and review sheets; never modifies sticker artwork."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, zipfile, hashlib

root = Path(__file__).resolve().parent
qa = root / 'qa'
qa.mkdir(exist_ok=True)
expected = [f'{i:02}.png' for i in range(1, 41)] + ['main.png', 'tab.png']
release = json.loads((root/'release.json').read_text(encoding='utf-8-sig'))
rows = []
for name in expected:
    path = root/'output'/name
    with Image.open(path) as im:
        alpha = im.getchannel('A')
        box = alpha.getbbox()
        w,h=im.size
        margins=[box[0],box[1],w-box[2],h-box[3]]
        target=(240,240) if name=='main.png' else (96,74) if name=='tab.png' else (370,320)
        row=dict(file=name, mode=im.mode, size=list(im.size), dpi=list(im.info.get('dpi', (0,0))), bytes=path.stat().st_size,
                 alpha_extrema=list(alpha.getextrema()), transparent_pixels=alpha.histogram()[0], margins=margins,
                 sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        row['pass']=im.size==target and im.mode=='RGBA' and min(row['dpi'])>=72 and row['bytes']<=1000000 and row['alpha_extrema']==[0,255] and min(margins)>0
        if name not in ('main.png','tab.png'):
            row['pass'] = row['pass'] and min(margins)>=10
        rows.append(row)
for bg,label in [('#ffffff','light'),('#243440','dark')]:
    for page in range(2):
        sheet=Image.new('RGB',(1480,1750),bg)
        draw=ImageDraw.Draw(sheet)
        for j in range(20):
            idx=page*20+j
            im=Image.open(root/'output'/expected[idx]).convert('RGBA')
            x=(j%4)*370;y=(j//4)*350
            sheet.paste(im,(x,y),im)
            draw.text((x+12,y+323),expected[idx],fill='white' if label=='dark' else 'black')
        sheet.save(qa/f'{label}-{page+1}.png')
with zipfile.ZipFile(root/'kaberadio-pop-vol1-40.zip') as z:
    zip_ok=sorted(z.namelist())==sorted(expected) and z.testzip() is None and all(z.read(n)==(root/'output'/n).read_bytes() for n in expected)
    zip_bytes=(root/'kaberadio-pop-vol1-40.zip').stat().st_size
def count(s): return sum(1 if ord(c)<128 else 2 for c in s)
text_counts={k:count(release[k]) for k in ('title_ja','description_ja','title_en','description_en')}
text_ok=all(v<= (40 if k.startswith('title') else 160) for k,v in text_counts.items())
report=dict(date='2026-09-28',guideline='https://creator.line.me/ja/guideline/sticker/',files=rows,zip_exact_match=zip_ok,zip_bytes=zip_bytes,text_counts=text_counts,text_pass=text_ok,pass_all=all(r['pass'] for r in rows) and zip_ok and zip_bytes<=60000000 and text_ok)
(qa/'final-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='files'},ensure_ascii=False))
print('Smallest sticker margin:',min(min(r['margins']) for r in rows[:40]))
print('Largest file:',max(r['bytes'] for r in rows))
