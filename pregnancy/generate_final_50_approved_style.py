from pathlib import Path
import io,os,random,json,csv,math
import requests
from PIL import Image,ImageDraw,ImageFont,ImageEnhance,ImageFilter
import numpy as np
import cv2

BASE=Path("pregnancy/final-50-approved-style")
BASE.mkdir(parents=True,exist_ok=True)
PHOTOS_DIR=Path("pregnancy/final-women-portraits")
PHOTOS_DIR.mkdir(parents=True,exist_ok=True)
DATA=json.loads(Path("pregnancy/corrected_50_approved_style_data.json").read_text())
REPO="shsweb/pinterest-pregnancy-pins"
APP="https://apps.apple.com/us/app/am-i-pregnant-pregnancy-quiz/id6769078846"
# Carefully selected Unsplash female portrait / beauty imagery; male portraits omitted.
IDS=[
"photo-1534528741775-53994a69daeb",
"photo-1524504388940-b1c1722653e1",
"photo-1517841905240-472988babdf9",
"photo-1544005313-94ddf0286df2",
"photo-1531123897727-8f129e1688ce",
"photo-1524250502761-1ac6f2e30d43",
"photo-1529626455594-4ff0802cfb7e",
"photo-1534751516642-a1af1ef26a56",
"photo-1487412720507-e7ab37603c6f",
"photo-1548142813-c348350df52b",
"photo-1515886657613-9f3515b0c78f",
"photo-1487222477894-8943e31ef7b2",
"photo-1494790108377-be9c29b29330",
"photo-1580489944761-15a19d654956",
"photo-1438761681033-6461ffad8d80",
"photo-1508214751196-bcfd4ca60f91",
"photo-1502685104226-ee32379fefbe",
"photo-1516726817505-f5ed825624d8",
"photo-1529139574466-a303027c1d8b",
"photo-1551836022-d5d88e9218df",
"photo-1566492031773-4f4e44671857",
"photo-1515377905703-c4788e51af15",
"photo-1507003211169-0a1dd7228f2d" # possible man - explicitly exclude
]
IDS=IDS[:-1]
fallback_ids=IDS[:6]
images=[]
for idx,photo_id in enumerate(IDS,1):
  fname=PHOTOS_DIR/f"woman-{idx:02}.jpg"
  try:
    url=f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w=1500&q=90"
    response=requests.get(url,timeout=18,headers={"User-Agent":"Mozilla/5.0"})
    response.raise_for_status()
    im=Image.open(io.BytesIO(response.content)).convert("RGB")
    if min(im.size)<500:
      print("SKIPPING SMALL IMAGE",idx,im.size)
      continue
    im.save(fname,quality=94)
    images.append(im)
    print("PHOTO READY",idx,im.size)
  except Exception as exc:
    print("PHOTO ERROR",idx,str(exc)[:180])
if len(images)<5:
  raise RuntimeError("Only "+str(len(images))+" female portraits downloaded; cannot ensure diverse source quality.")

# Filter images without confidently detected faces, keeping many unique real female portraits.
cascade=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
def crop_face(im):
  sw=min(650,im.width)
  small=im.resize((sw,int(im.height*sw/im.width)))
  gray=cv2.cvtColor(np.asarray(small),cv2.COLOR_RGB2GRAY)
  det=cascade.detectMultiScale(gray,1.08,5,minSize=(46,46))
  sx=im.width/small.width;sy=im.height/small.height
  if len(det):
    x,y,w,h=max(det,key=lambda r:r[2]*r[3])
    cx=(x+w/2)*sx;cy=(y+h/2)*sy
    face_size=w*sx
    # Size photo around face, leaving shoulders visible
    cw=min(im.width,max(face_size*2.4,im.width*.72))
    ch=cw*1.5
    if ch>im.height:ch=im.height;cw=ch/1.5
    xx=max(0,min(im.width-cw,cx-cw/2))
    yy=max(0,min(im.height-ch,cy-ch*.52))
    im=im.crop((int(xx),int(yy),int(xx+cw),int(yy+ch)))
  else:
    # landscape pictures are not good for a full-bleed tall portrait. center-crop.
    if im.width>im.height/1.5:
      cw=im.height/1.5;xx=(im.width-cw)//2
      im=im.crop((int(xx),0,int(xx+cw),im.height))
  target=(1000,1500)
  ratio=max(target[0]/im.width,target[1]/im.height)
  im=im.resize((math.ceil(im.width*ratio),math.ceil(im.height*ratio)),Image.Resampling.LANCZOS)
  l=(im.width-1000)//2;t=(im.height-1500)//2
  return im.crop((l,t,l+1000,t+1500))

def font(size):
  for fp in (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
  ):
    if os.path.exists(fp): return ImageFont.truetype(fp,size)
  return ImageFont.load_default()

PINK=(247,18,103);NAVY=(15,25,79)
def put_center(d,s,y,color,target_size,max_width=900):
  f=font(target_size)
  while d.textbbox((0,0),s,font=f)[2]>max_width and target_size>35:
    target_size-=2;f=font(target_size)
  tw=d.textbbox((0,0),s,font=f)[2]
  d.text(((1000-tw)//2,y),s,font=f,fill=color)
  return target_size

def title_case(s):
  txt=s.strip().title()
  txt=txt.replace("Hcg","hCG").replace("Pms","PMS").replace("Dpo","DPO")
  return txt

# For every pin, photo must be full-bleed with headline above the face and all labels legible.
rows=[]
for ii,entry in enumerate(DATA):
  n=ii+1
  picture=crop_face(images[(ii*7+(ii//len(images)))%len(images)])
  picture=ImageEnhance.Color(picture).enhance(1.1)
  picture=ImageEnhance.Contrast(picture).enhance(1.03)
  # Soft warm / pink wash harmonizes non-pastel source photos.
  warm=Image.new("RGB",(1000,1500),(255,220,231))
  picture=Image.blend(picture,warm,.075)
  # Preserve woman portrait in the body. Fade only the top header where the copy goes.
  overlay=Image.new("RGBA",(1000,1500),(0,0,0,0))
  grad=Image.new("L",(1,1500))
  # top white overlay is strongest to y=300 then drops to zero before the face.
  for yy in range(1500):
    if yy<=260: alpha=249
    elif yy<550: alpha=round(249*(550-yy)/290)
    else: alpha=0
    grad.putpixel((0,yy),alpha)
  opacity=grad.resize((1000,1500))
  top=Image.new("RGBA",(1000,1500),(255,237,246,0))
  top.putalpha(opacity)
  picture=Image.alpha_composite(picture.convert("RGBA"),top)
  d=ImageDraw.Draw(picture)
  rng=random.Random(n*294)
  # pale reference-style decorative hearts, kept at margins not covering face.
  for kk in range(7):
    x=rng.choice([48,85,110,860,895,926])
    y=rng.randint(440,1240)
    mark=rng.choice(["♥","♡","?"])
    d.text((x,y),mark,font=font(rng.randint(31,65)),fill=(246,25,114,rng.randint(165,230)))
  # Number badge at top left
  d.ellipse((26,26,107,107),fill=NAVY)
  sn=str(n)
  nf=font(36 if n<10 else 29)
  w=d.textbbox((0,0),sn,font=nf)[2]
  d.text((67-w/2,44),sn,font=nf,fill="white")

  headlines=[title_case(z) for z in entry["head"].split("|")]
  # Keep headline short and high-contrast, with large reference-like mixed-case styling.
  head_y=88 if len(headlines)>1 else 140
  for j,line in enumerate(headlines):
    put_center(d,line,head_y+(j*108),NAVY if j%2==0 else PINK,103 if len(line)<17 else 83,900)
  desc_y=head_y+len(headlines)*109+8
  subtitle=entry["subtitle"]
  # One- or two-line subtitle with pink emphasis
  if len(subtitle)>25 and " " in subtitle:
    mid=len(subtitle)//2
    idx=min((i for i,ch in enumerate(subtitle) if ch==" "),key=lambda x:abs(x-mid))
    parts=[subtitle[:idx],subtitle[idx+1:]]
  else:parts=[subtitle]
  for j,part in enumerate(parts):
    put_center(d,part,desc_y+j*61,PINK,52,890)
  # Pink-white contrast CTA; absolutely inside canvas with 35px safe margins.
  d.rounded_rectangle((38,1300,963,1445),radius=73,fill=(255,255,255,252),outline=PINK,width=9)
  d.ellipse((830,1315,947,1432),fill=NAVY)
  d.line((864,1375,914,1375),fill="white",width=13)
  d.line((898,1358,916,1375),fill="white",width=13)
  d.line((898,1392,916,1375),fill="white",width=13)
  cta=entry["cta"]
  ff=font(66)
  while d.textbbox((0,0),cta,font=ff)[2]>685:
    ff=font(ff.size-2)
  bb=d.textbbox((0,0),cta,font=ff)
  tw=bb[2]-bb[0]
  d.text(((830-tw)//2,1337),cta,font=ff,fill=PINK)
  filename=f"approved-style-pin-{n:02}.jpg"
  picture.convert("RGB").save(BASE/filename,quality=93,subsampling=0,optimize=True)
  desc=(f"{entry['title']}. {entry['explain']} Explore signs and next steps with the Am I Pregnant? Pregnancy Quiz app. "
        "A quiz cannot diagnose pregnancy; use a home pregnancy test or a clinician for confirmation. "
        "#AmIPregnant #PregnancyQuiz #EarlyPregnancy")
  rows.append({
    "Title":entry["title"],
    "Media URL":f"https://raw.githubusercontent.com/{REPO}/main/pregnancy/final-50-approved-style/{filename}",
    "Pinterest board":"Pregnancy Tips & Early Signs",
    "Thumbnail":"",
    "Description":desc[:490],
    "Link":f"{APP}?utm_source=pinterest&utm_medium=organic&utm_content=approved_final_{n:02}",
    "Publish date":"",
    "Keywords":entry["title"].lower()+", pregnancy symptoms, pregnancy quiz"
  })
  print("RENDERED",n,filename)
fields=["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"]
for name,rr in [
 ("pinterest_50_FINAL_APPROVED_STYLE.csv",rows),
 ("pinterest_25_FINAL_BATCH1.csv",rows[:25]),
 ("pinterest_25_FINAL_BATCH2.csv",rows[25:])
]:
  with open(name,"w",newline="",encoding="utf-8-sig") as f:
    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rr)
# useful review montage for face diversity and headlines; native thumbnails only for QC.
montage=Image.new("RGB",(200*10,300*5),(245,242,247))
for k in range(50):
  im=Image.open(BASE/f"approved-style-pin-{k+1:02}.jpg")
  im.thumbnail((200,300))
  montage.paste(im,((k%10)*200,(k//10)*300))
montage.save("pregnancy/final_50_approved_contact_sheet.jpg",quality=87,optimize=True)
print("COMPLETE 50 FULL RESOLUTION IMAGES + THREE CSVs; unique photos:",len(images))
