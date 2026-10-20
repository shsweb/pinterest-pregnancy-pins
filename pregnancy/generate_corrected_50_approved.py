import json,csv,random,io,math,os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont,ImageEnhance
import requests

R=Path('pregnancy/corrected-50-approved')
R.mkdir(parents=True,exist_ok=True)
info=json.loads(Path('pregnancy/corrected_50_approved_style_data.json').read_text())
repo='shsweb/pinterest-pregnancy-pins'
app='https://apps.apple.com/us/app/am-i-pregnant-pregnancy-quiz/id6769078846'
# Portrait photographs, downloaded individually. The fallback uses an image in this repository.
photo_urls=[
'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=900&q=84',
'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=900&q=84',
'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=900&q=84',
'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=900&q=84',
'https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=900&q=84',
'https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=900&q=84',
'https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?w=900&q=84',
'https://images.unsplash.com/photo-1529139574466-a303027c1d8b?w=900&q=84',
'https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=900&q=84',
'https://images.unsplash.com/photo-1534751516642-a1af1ef26a56?w=900&q=84',
'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=900&q=84',
'https://images.unsplash.com/photo-1548142813-c348350df52b?w=900&q=84',
'https://images.unsplash.com/photo-1568602471122-7832951cc4c5?w=900&q=84'
]
portrait=[]
for i,url in enumerate(photo_urls):
  try:
    rs=requests.get(url,timeout=15)
    rs.raise_for_status()
    im=Image.open(io.BytesIO(rs.content)).convert('RGB')
    if im.width<220 or im.height<220:continue
    # Ensure each portrait really has appropriate framing; crop will happen in layout.
    portrait.append(im)
    print('Photo loaded',i,im.size)
  except Exception as e:print('Photo unavailable',i,str(e)[:100])

# Use existing original woman-focused pin as an offline fallback only.
if not portrait:
  im=Image.open('pin-01.png').convert('RGB')
  portrait=[im.crop((0,580,450,1450))]
  print("Fallback to original woman photograph")
assert portrait

W,H=1000,1500
navy=(19,28,77); pink=(240,29,106); blush=(254,214,229); white=(255,255,255)
backdrops=[(255,228,234),(252,237,247),(231,238,255),(251,235,221),(236,253,247),(248,230,255),(255,244,215)]
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
fontb=lambda s: ImageFont.truetype(font,s)
def cover(src,w,h,anchor_x=.5,anchor_y=.34):
  scale=max(w/src.width,h/src.height)
  ww=int(src.width*scale);hh=int(src.height*scale)
  src=src.resize((ww,hh),Image.Resampling.LANCZOS)
  x=int(max(0,ww-w)*anchor_x);y=int(max(0,hh-h)*anchor_y)
  return src.crop((x,y,x+w,y+h))
def center(draw,text,y,font,fill,maxwidth=900,stroke=0):
  bounds=draw.textbbox((0,0),text,font=font,stroke_width=stroke)
  width=bounds[2]-bounds[0]
  draw.text(((W-width)//2,y),text,font=font,fill=fill,stroke_width=stroke,stroke_fill=white)
def text_fit(draw,line,max_w,begin):
  size=begin
  while draw.textbbox((0,0),line,font=fontb(size))[2]>max_w and size>38:size-=2
  return fontb(size)

rows=[]
for i,rec in enumerate(info):
  n=i+1
  bg=backdrops[(i*5+3)%len(backdrops)]
  img=Image.new('RGB',(W,H),bg); dr=ImageDraw.Draw(img)
  head=rec['head'].split('|')
  # Main reference style: large, bold editorial heading; prominent woman centered;
  # hearts/graphic doodles; rounded white/pink pill CTA across the lower area.
  dr.rounded_rectangle((16,15,984,1486),radius=72,fill=bg)
  dr.rounded_rectangle((35,34,97,97),radius=31,fill=navy)
  dr.text((66,49),str(n),font=fontb(25),fill=white,anchor='mt')
  y=102
  for part in head:
    color=pink if ((i//2)+len(part))%2 else navy
    f=text_fit(dr,part,830,92)
    center(dr,part,y,f,color)
    y+=112
  sub=rec['subtitle']
  f=text_fit(dr,sub,850,43)
  center(dr,sub,y+17,f,navy); head_end=y+85
  # photo with opaque layered mask over bottom, no tiny text in photo
  ph_top=max(380,head_end+20);ph_end=1290
  selected=portrait[i%len(portrait)]
  face=cover(selected,930,ph_end-ph_top,anchor_x=[.25,.42,.6,.53][i%4],anchor_y=.79)
  mask=Image.new('L',face.size);md=ImageDraw.Draw(mask)
  md.rounded_rectangle((0,0,face.width,face.height+90),radius=66,fill=255)
  img.paste(face,(35,ph_top),mask)
  dr=ImageDraw.Draw(img)
  # decorative hearts and a gentle pink translucent background wash
  randomizer=random.Random(i*991+7)
  for k in range(4):
    x=randomizer.choice([68,115,858,914]); yy=randomizer.randint(ph_top+95,ph_end-95)
    dr.text((x,yy),randomizer.choice(['♥','♡','?','✦']),font=fontb(randomizer.randint(38,66)),fill=pink if k%2 else (255,160,196))
  # close to reference: large high-contrast white CTA with pink outline and dark circle/arrow
  dr.rounded_rectangle((68,1293,935,1405),radius=56,fill=white,outline=pink,width=7)
  call=rec['cta']; tf=text_fit(dr,call,650,51)
  bbox=dr.textbbox((0,0),call,font=tf)
  tw=bbox[2]-bbox[0]
  dr.text(((W-tw)//2-25,1321),call,font=tf,fill=pink)
  dr.ellipse((839,1308,920,1389),fill=navy)
  dr.text((880,1328),'➜',font=fontb(41),fill=white,anchor='mt')
  center(dr,'AM I PREGNANT?  •  PREGNANCY QUIZ APP',1432,fontb(19),navy)
  out=R/f'approved-women-pin-{n:02}.png'
  img.save(out,optimize=True)
  rows.append({
    'Title':rec['title'],
    'Media URL':f'https://raw.githubusercontent.com/{repo}/main/pregnancy/corrected-50-approved/approved-women-pin-{n:02}.png',
    'Pinterest board':'Pregnancy Tips & Early Signs',
    'Thumbnail':'',
    'Description':f"{rec['explain']} Explore signs and next steps in the Am I Pregnant? Pregnancy Quiz app. A quiz cannot confirm pregnancy; use a home pregnancy test or clinician. #AmIPregnant #PregnancyQuiz #EarlyPregnancy",
    'Link':f'{app}?utm_content=pinterest_approved_women_{n:02}',
    'Publish date':'',
    'Keywords':rec['title'].lower()+', pregnancy symptoms, am i pregnant quiz'
  })
  print('Rendered',n)
fields=['Title','Media URL','Pinterest board','Thumbnail','Description','Link','Publish date','Keywords']
for name,subset in [('pinterest_50_APPROVED_WOMEN_REPLACEMENT.csv',rows),('pinterest_approved_batch1_25.csv',rows[:25]),('pinterest_approved_batch2_25.csv',rows[25:])]:
  with open(name,'w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(subset)
print('COMPLETE:',len(rows),'redesigned photo-first pins')
