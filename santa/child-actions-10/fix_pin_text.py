"""Cover generated pseudo-text with crisp, verified English on ten Pinterest images."""
from pathlib import Path
import random
from PIL import Image, ImageDraw, ImageFont

BASE=Path(__file__).resolve().parent
SRC=BASE/'images'
DST=BASE/'corrected'
DST.mkdir(exist_ok=True)
POSTERS=[
 (("VIDEO CALL","SANTA!"),"A Magical Call from the North Pole"),
 (("BAKE COOKIES","WITH SANTA!"),"Show Santa Your Christmas Cookies!"),
 (("WRITE A LETTER","TO SANTA!"),"Tell Santa Your Christmas Wishes!"),
 (("GOOD NIGHT","WITH SANTA!"),"Call Santa Before Bedtime!"),
 (("WATCH SANTA'S","SLEIGH!"),"Call Santa Before His Big Flight!"),
 (("ASK SANTA","ANYTHING!"),"What Would You Ask Santa?"),
 (("EXPLORE THE","NORTH POLE!"),"Your Adventure Starts with Santa!"),
 (("MEET SANTA'S","PET FRIENDS!"),"Show Your Puppy to Santa!"),
 (("BUILD A","SNOWMAN!"),"Show Santa What You Made!"),
 (("OPEN A","SURPRISE GIFT!"),"Share a Magical Moment with Santa!")]
FF='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
assert Path(FF).exists(), FF
def fit(d,s,maxw,maxh,size,stroke=0):
 for sz in range(size,22,-1):
  f=ImageFont.truetype(FF,sz)
  b=d.textbbox((0,0),s,font=f,stroke_width=stroke)
  if b[2]-b[0]<=maxw and b[3]-b[1]<=maxh:return f
 raise ValueError("Text cannot fit: "+s)
def strip(im,start,end,color,a,b):
 lay=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
 for y in range(start,end):
  t=(y-start)/max(1,end-start-1)
  d.line((0,y,999,y),fill=(*color,round(a+(b-a)*t)))
 return Image.alpha_composite(im,lay)
def centered(d,y,s,face,maxsize):
 f=fit(d,s,820,118,maxsize,6)
 bb=d.textbbox((0,0),s,font=f,stroke_width=6)
 x=(1000-(bb[2]-bb[0]))/2-bb[0]; yy=y-bb[1]
 for k in range(11,0,-2):
  d.text((x,yy+k),s,font=f,fill='#58101f',stroke_width=8,stroke_fill='#3d1020')
 d.text((x,yy),s,font=f,fill=face,stroke_width=6,stroke_fill='#8d1230')
def emblem(d,cx,cy):
 d.ellipse((cx-40,cy-20,cx+34,cy+43),fill='white')
 d.ellipse((cx-46,cy-20,cx-3,cy+26),fill='white')
 d.ellipse((cx-3,cy-23,cx+43,cy+31),fill='white')
 d.ellipse((cx+26,cy-4,cx+52,cy+20),fill='#ce112f')
 d.ellipse((cx+1,cy-53,cx+42,cy-22),fill='white')
 d.line((cx+1,cy-28,cx+9,cy-48),fill='white',width=7)
for i,(lines,subtitle) in enumerate(POSTERS,1):
 original=SRC/f'child-action-{i:02}.png'
 assert original.exists(),original
 with Image.open(original) as photo:
  assert photo.size==(1000,1500),photo.size
  image=photo.convert('RGBA')
 # Opaque headline/footer regions block all unrecognizable AI-generated writing.
 image=strip(image,0,470,(19,27,41),249,245)
 image=strip(image,470,550,(19,27,41),245,0)
 image=strip(image,1050,1120,(58,12,22),0,249)
 image=strip(image,1120,1500,(58,12,22),252,252)
 p=Image.new('RGBA',image.size,(0,0,0,0));d=ImageDraw.Draw(p)
 d.rounded_rectangle((38,33,962,474),radius=51,fill=(4,51,46,255),outline='#fbd377',width=9)
 d.rounded_rectangle((52,47,948,460),radius=42,outline='#fff2c7',width=3)
 rng=random.Random(10898+i*83)
 for _ in range(29):
  x=rng.choice([rng.randint(75,118),rng.randint(875,924)])
  y=rng.randint(65,431); r=rng.choice([3,5,7])
  d.ellipse((x-r,y-r,x+r,y+r),fill=rng.choice(['#ffd478','#fff8df','#f2b9a6']))
 d.rounded_rectangle((245,62,755,112),radius=24,fill='#86172a',outline='#ffdf9e',width=3)
 d.text((500,86),'CHRISTMAS MAGIC',anchor='mm',font=ImageFont.truetype(FF,23),fill='#fff9e7')
 image=Image.alpha_composite(image,p); d=ImageDraw.Draw(image)
 centered(d,148,lines[0],'#fff5da',96)
 centered(d,276,lines[1],'#ffd369',116)
 d.rounded_rectangle((231,430,769,441),radius=5,fill='#f3c45b')
 # Rebuild both callout and CTA with actual typeset English.
 panel=Image.new('RGBA',image.size,(0,0,0,0));d=ImageDraw.Draw(panel)
 d.rounded_rectangle((53,1101,947,1218),radius=50,fill='#fff7de',outline='#ffc464',width=6)
 d.rounded_rectangle((70,1115,930,1204),radius=41,outline='#d39351',width=2)
 sf=fit(d,subtitle,818,58,51)
 d.text((500,1159),subtitle,font=sf,anchor='mm',fill='#a21428')
 d.rounded_rectangle((48,1265,952,1444),radius=80,fill='#f7d984')
 d.rounded_rectangle((56,1273,944,1437),radius=73,fill='#a70027',outline='#fff9e3',width=5)
 for yy in range(1282,1330):
  t=(yy-1282)/48
  d.line((130,yy,870,yy),fill=(int(244-40*t),int(25-12*t),int(56-24*t)),width=1)
 d.rounded_rectangle((69,1285,931,1425),radius=67,outline='#ffb661',width=3)
 emblem(d,156,1363)
 cta='Try Call Santa on iPhone'
 cf=fit(d,cta,653,90,45)
 d.text((577,1356),cta,font=cf,anchor='mm',fill='white',stroke_width=1,stroke_fill='#fff9e7')
 image=Image.alpha_composite(image,panel).convert('RGB')
 dest=DST/f'child-action-fixed-{i:02}.png'
 image.save(dest,'PNG',optimize=True)
 with Image.open(dest) as check:
  assert check.size==(1000,1500)
  check.verify()
 assert dest.stat().st_size>100000, dest
 print('PASS',dest.name,dest.stat().st_size,lines,subtitle)
assert len(list(DST.glob('child-action-fixed-*.png')))==10
print('ALL 10 CORRECTED PINS VALIDATED')
