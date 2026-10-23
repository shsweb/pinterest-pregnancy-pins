#!/usr/bin/env python3
"""Create 20 original photo-led Pinterest pins and a complete one-file bulk CSV."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import csv, math

BASE = Path("images/pregnancy-new20-2026")
OUT = BASE / "pins"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1000, 1500
APP = "https://apps.apple.com/us/app/am-i-pregnant-pregnancy-quiz/id6769078846"
URL = "https://raw.githubusercontent.com/shsweb/pinterest-pregnancy-pins/main/images/pregnancy-new20-2026/pins/"
BOARD = "Pregnancy Tips & Early Signs"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
def ff(n, kind="regular"):
    return ImageFont.truetype({"regular": REG, "bold": BOLD, "serif": SERIF}[kind], n)
def centered(d, text, y, font, color):
    box=d.textbbox((0,0),text,font=font)
    d.text(((W-(box[2]-box[0]))/2,y),text,font=font,fill=color)
def wrap(d, s, font, width):
    lines=[]; part=""
    for word in s.split():
        nextpart=(part+" "+word).strip()
        if part and d.textbbox((0,0),nextpart,font=font)[2] > width:
            lines.append(part); part=word
        else: part=nextpart
    if part: lines.append(part)
    return lines
def flower(d, x, y, size, pink):
    for a in range(0,360,72):
        xx=x+math.cos(math.radians(a))*size*.6
        yy=y+math.sin(math.radians(a))*size*.6
        r=size*.34
        d.ellipse((xx-r,yy-r,xx+r,yy+r),fill=pink)
    d.ellipse((x-6,y-6,x+6,y+6),fill="#FFE4A0")
def heart(d, x, y, sz, color):
    d.arc((x-sz,y-sz*.8,x+sz*.15,y+sz*.45),170,360,fill=color,width=5)
    d.arc((x-sz*.15,y-sz*.8,x+sz,y+sz*.45),180,370,fill=color,width=5)
    d.line([(x-sz*.82,y),(x,y+sz*.85),(x+sz*.82,y)],fill=color,width=5,joint="curve")

# Unique question-led headlines written in polished English. All claims are non-diagnostic.
IDEAS = [
 ("1 Day Late?","Too early to test?","Tests can be less reliable when taken very early. Check the instructions.","When can I test one day after a missed period?"),
 ("5 Days Late?","What should you do?","A late period has several possible causes. Testing can offer clarity.","Five days late: testing and next steps"),
 ("A Faint Test Line?","How should you read it?","Check the test's reading window. If unsure, repeat as directed.","Faint pregnancy test lines and reading instructions"),
 ("Cramps, No Period?","What could explain it?","Cramping can happen for many reasons, including before a period.","Cramps without a period: possible explanations"),
 ("PMS or Pregnancy?","Why signs overlap","Breast tenderness and cramping may happen with either.","PMS versus early pregnancy symptoms"),
 ("Feeling Off Today?","Notice the changes","Symptoms alone cannot tell you whether you are pregnant.","Feeling different: early signs and what to do"),
 ("Morning Nausea?","Could it be a sign?","Nausea can have many causes. A test can help if your period is late.","Nausea and possible early pregnancy signs"),
 ("Smells Feel Stronger?","What might it mean?","Sensitivity to smells is not a reliable sign on its own.","Smell sensitivity and early pregnancy questions"),
 ("Unusual Tiredness?","What might cause it?","Fatigue can have many causes, including poor sleep and hormonal changes.","Unusual fatigue: PMS or pregnancy?"),
 ("Breasts Feel Tender?","PMS or pregnancy?","Hormone changes may cause tenderness before a period or in pregnancy.","Breast tenderness before a period or in pregnancy"),
 ("Spotting or Period?","Timing can matter","Light bleeding can have different causes. Seek care for severe pain or heavy bleeding.","Spotting versus a period: key differences"),
 ("Negative Test Again?","Should you retest?","Testing early can miss pregnancy. Follow the kit's retesting directions.","Negative pregnancy test with a late period"),
 ("Cycles Not Regular?","Track your timing","Tracking cycle dates may help you choose when to test.","Irregular cycles and pregnancy test timing"),
 ("Food Suddenly Off?","Possible explanations","Food aversions can have several causes and do not confirm pregnancy.","Food aversions and pregnancy signs"),
 ("Mood Swings Lately?","What might be behind it?","Mood changes can happen with PMS, stress, and pregnancy.","Mood swings: PMS versus possible pregnancy"),
 ("No Symptoms Yet?","Can you still test?","Some people notice few early symptoms. A test is what confirms.","No early pregnancy symptoms: what to know"),
 ("Bloating Again?","Understand your cycle","Bloating may occur before a period or for many other reasons.","Bloating before a period versus pregnancy"),
 ("Peeing More Often?","Common explanations","Frequent urination has many causes and is not conclusive.","Frequent urination: early pregnancy questions"),
 ("When to Retest?","Timing made simple","Read your pregnancy test instructions for when to repeat a test.","When to repeat a home pregnancy test"),
 ("Still Unsure?","Start with the basics","Reflect on symptoms, note your cycle, and use a test for confirmation.","Am I pregnant? Signs, cycles, and next steps"),
]
assert len(IDEAS)==20
ROWS=[]
for i, (headline, subtitle, info, seo) in enumerate(IDEAS):
    num=51+i
    palette=[
        ("#FBEAE5","#F7CBCE","#D75B7D","#6D2836"),
        ("#FAE9ED","#F5CAD7","#D3517A","#642837"),
        ("#FBEEE8","#F4D2CC","#D75D75","#6E3440"),
        ("#F9E9EF","#EFCBDD","#CD557E","#623047"),
    ][i%4]
    base,bloom,button,ink=palette
    im=Image.new("RGB",(W,H),base)
    d=ImageDraw.Draw(im)
    d.ellipse((-245,-215,345,370),fill=bloom)
    d.ellipse((785,-155,1220,310),fill="#F8D8D9")
    d.ellipse((-220,1195,345,1670),fill="#F8D4D6")
    d.ellipse((790,1160,1280,1710),fill="#F7D8E6")
    for x,y,r in [(70,80,18),(922,117,15),(72,1090,14),(934,1094,14),(68,1470,14),(925,1440,18)]:
        flower(d,x,y,r,bloom)
    # Headline and photo separated so no text overlaps women's faces.
    d.rounded_rectangle((212,39,790,112),radius=37,fill="#FFFFFF")
    centered(d,"PREGNANCY & PERIOD TIPS",60,ff(26,"bold"),"#71404B")
    fs=77
    while fs>=41:
        font=ff(fs,"serif")
        lines=wrap(d,headline,font,906)
        if len(lines)<=2: break
        fs-=2
    if len(lines)==1: y=178
    else: y=136
    for line in lines:
        centered(d,line,y,font,ink)
        y+=fs+10
    sf=47
    while sf>27 and d.textbbox((0,0),subtitle,font=ff(sf,"serif"))[2]>872: sf-=1
    centered(d,subtitle,322 if len(lines)==1 else min(356,y+1),ff(sf,"serif"),button)
    # ten new photographic subjects, each displayed twice in different contexts.
    photo_file=BASE/f"bg_{i%10+1:02d}.jpg"
    source=Image.open(photo_file).convert("RGB")
    # Center biased slightly upward, preserving face and hairstyle.
    photo=ImageOps.fit(source,(942,684),Image.Resampling.LANCZOS,centering=(.5,.45+(i//10)*.025))
    mask=Image.new("L",photo.size,0)
    md=ImageDraw.Draw(mask)
    md.rounded_rectangle((0,0,941,683),radius=36,fill=255)
    im.paste(photo,(29,424),mask)
    d=ImageDraw.Draw(im)
    # Readable insight box and strong CTA.
    d.rounded_rectangle((105,1117,895,1278),radius=47,fill="#FFF8F5")
    body_font=ff(28)
    body_lines=wrap(d,info,body_font,711)
    if len(body_lines)>3:
        body_font=ff(25)
        body_lines=wrap(d,info,body_font,724)
    y=1163-(len(body_lines)-2)*14
    for line in body_lines:
        centered(d,line,y,body_font,ink)
        y+=38
    d.rounded_rectangle((142,1292,858,1394),radius=51,fill=button,outline="#FFFFFF",width=5)
    centered(d,"TAKE THE PREGNANCY QUIZ  >",1326,ff(28,"bold"),"#FFFFFF")
    centered(d,"Am I Pregnant? App   |   Explore your signs",1441,ff(20),"#713C47")
    filename=f"pin_{num:02d}.jpg"
    path=OUT/filename
    im.save(path,format="JPEG",quality=94,optimize=True,subsampling=0)
    assert path.stat().st_size>60000
    media=URL+filename
    dest=APP+f"?utm_source=pinterest&utm_medium=organic&utm_campaign=pregnancy_new20_2026&utm_content=pin_{num}"
    description=(seo+". "+info+" Explore the Am I Pregnant? Pregnancy Quiz app. "
                  "A quiz is not a pregnancy test. #AmIPregnant #PregnancyQuiz #PregnancySigns")
    ROWS.append([headline+" | "+subtitle,media,BOARD,"",description,dest,"",
                 "am i pregnant, pregnancy signs, pregnancy quiz, early pregnancy, period"])
csv_path="PINTEREST_NEW_20_PINS_READY.csv"
with open(csv_path,"w",newline="",encoding="utf-8-sig") as f:
    writer=csv.writer(f)
    writer.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"])
    writer.writerows(ROWS)
assert len(ROWS)==20 and len({r[1] for r in ROWS})==20 and len({r[5] for r in ROWS})==20
assert len(list(OUT.glob("pin_*.jpg")))==20
print("SUCCESS: 20 distinct 1000x1500 images, 20 public GitHub image URLs, 20 unique App Store destination links")
