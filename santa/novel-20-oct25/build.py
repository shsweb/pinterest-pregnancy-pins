from pathlib import Path
import json,csv
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter
P=Path(__file__).resolve().parent
M=json.loads((P/'manifest.json').read_text())
assert len(M)==20
O=P/'images';O.mkdir(exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
def fit(d,s,width,initial):
 for size in range(initial,23,-1):
  f=ImageFont.truetype(FONT,size)
  a=d.textbbox((0,0),s,font=f,stroke_width=4)
  if a[2]-a[0] <= width:return f
 raise ValueError(s)
def center(d,text,y,sz,col):
 f=fit(d,text,830,sz)
 d.text((500,y+7),text,anchor='mm',font=f,fill='#2b0b13',stroke_width=7,stroke_fill='#2b0b13')
 d.text((500,y),text,anchor='mm',font=f,fill=col,stroke_width=3,stroke_fill='#fff4cb')
def icon(d,x,y):
 d.ellipse((x-38,y-27,x+17,y+29),fill='white')
 d.ellipse((x-8,y-27,x+43,y+27),fill='white')
 d.ellipse((x+23,y-8,x+50,y+13),fill='#ba0929')
 d.ellipse((x-4,y-51,x+31,y-19),fill='white')
 d.line((x+3,y-31,x+22,y-55),fill='white',width=8)
for i,item in enumerate(M,1):
 file=P/'sources'/f'{i:02}.png'
 assert file.exists(),file
 with Image.open(file) as src:
  src.load()
  assert src.width>=1000 and src.height>=1500,src.size
  src=src.convert('RGB')
 bg=ImageOps.fit(src,(1000,1500),Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(22)).convert('RGBA')
 fg=ImageOps.contain(src,(1000,1500),Image.Resampling.LANCZOS).convert('RGBA')
 bg.alpha_composite(fg,((1000-fg.width)//2,(1500-fg.height)//2))
 ov=Image.new('RGBA',(1000,1500),(0,0,0,0));d=ImageDraw.Draw(ov)
 d.rounded_rectangle((45,47,955,386),radius=45,fill=(22,61,47,242),outline='#ffdb8a',width=7)
 d.rounded_rectangle((59,59,941,372),radius=34,outline='#fff9e8',width=2)
 center(d,'CALL SANTA &',157,94,'#ff4c39')
 center(d,item['title'],280,86,'#ffde48')
 d.rounded_rectangle((51,1136,949,1253),radius=52,fill='#fff5dd',outline='#ffc478',width=7)
 sub='A Magical Christmas Video Call!'
 d.text((500,1192),sub,anchor='mm',font=fit(d,sub,824,51),fill='#af1029')
 d.rounded_rectangle((48,1286,952,1453),radius=77,fill='#f5c86c')
 d.rounded_rectangle((60,1298,940,1441),radius=70,fill='#ba0829',outline='#fff5e7',width=5)
 icon(d,163,1370)
 d.text((578,1346),'Try Call Santa',anchor='mm',font=fit(d,'Try Call Santa',620,62),fill='white')
 d.text((578,1400),'on iPhone',anchor='mm',font=fit(d,'on iPhone',550,52),fill='white')
 out=O/f'santa-novel-{i:02}.png'
 Image.alpha_composite(bg,ov).convert('RGB').save(out,'PNG',optimize=True)
 with Image.open(out) as check:
  assert check.size==(1000,1500)
  check.verify()
 print('VERIFIED',out)
root='https://raw.githubusercontent.com/shsweb/pinterest-pregnancy-pins/main/santa/novel-20-oct25/images/'
app='https://apps.apple.com/us/app/call-santa-talk-video/id6808839679'
with (P/'pinterest_santa_novel_20_READY.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f,quoting=csv.QUOTE_ALL)
 w.writerow(['Title','Media URL','Pinterest board','Thumbnail','Description','Link','Publish date','Keywords'])
 for i,it in enumerate(M,1):
  w.writerow([f'{it["title"].title()} | Call Santa Video Fun',root+f'santa-novel-{i:02}.png','Christmas Activities for Kids','',f'Enjoy a festive {it["title"].lower()} activity and share a magical video call with Santa. Explore Call Santa: Talk & Video on iPhone.',app+f'?ct=pinterest-novel-oct25-{i:02}','','Santa video call,Christmas kids activities,Call Santa iPhone,Christmas fun'])
sheet=Image.new('RGB',(1220,1530),'#fff6ed')
for j in range(20):
 with Image.open(O/f'santa-novel-{j+1:02}.png') as im:
  thumb=im.resize((228,342),Image.Resampling.LANCZOS)
 sheet.paste(thumb,(10+(j%5)*244,8+(j//5)*381))
sheet.save(P/'preview_20.jpg',quality=90)
print('ALL 20 COMPLETE')
