from PIL import Image,ImageDraw,ImageFont
import csv
from pathlib import Path
PATH=Path('images/pregnancy-women-batch5-approved')
with open('PINTEREST_20_APPROVED_STYLE_REPLACEMENT.csv',encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
subs=[
'What might affect timing','PMS or something else','What you may notice',
'A symptom to consider','Timing matters','Cycle tracking tips',
'PMS or pregnancy','What next','What to know','When to check again',
'Cravings and aversions','What could it mean','Understand your timing',
'Understand your next steps','Changes you may notice','Every body is different',
'Know the limitations','A simple next step','Listen to your body','Take the next step'
]
fpath='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
def font(n):return ImageFont.truetype(fpath,n)
def lines(d,s,f,maxw):
    result=[];cur=''
    for word in s.split():
        z=(cur+' '+word).strip()
        if cur and d.textbbox((0,0),z,font=f)[2]>maxw:result.append(cur);cur=word
        else:cur=z
    if cur:result.append(cur)
    return result
def cent(d,s,y,f,fill):
    b=d.textbbox((0,0),s,font=f)
    d.text(((1000-(b[2]-b[0]))//2,y),s,font=f,fill=fill)
assert len(rows)==20 and len(subs)==20
for idx,(row,sub) in enumerate(zip(rows,subs),51):
    p=PATH/f'pin_{idx}.jpg'
    im=Image.open(p).convert('RGB')
    assert im.size==(1000,1500)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((43,133,957,380),radius=48,fill=(255,230,230))
    size=74
    while size>35:
        ft=font(size)
        l=lines(d,row['Title'],ft,847)
        if len(l)<=2:break
        size-=2
    if len(l)>1:
        size=min(size,64)
        ft=font(size)
        l=lines(d,row['Title'],ft,847)
        y=152
    else:y=164
    for line in l:
        cent(d,line,y,ft,(105,34,40))
        y+=size+6
    sf=font(40)
    while d.textbbox((0,0),sub,font=sf)[2]>837 and sf.size>27:sf=font(sf.size-1)
    subtitle_y=309 if len(l)>1 else 287
    cent(d,sub,subtitle_y,sf,(210,75,109))
    im.save(p,quality=94,optimize=True,subsampling=0)
print('REPAIRED',len(rows),'headlines with safe-area margins')
