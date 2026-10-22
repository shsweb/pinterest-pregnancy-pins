#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path
import csv, math
OUT=Path("images/pregnancy-women-batch5-clickworthy")
OUT.mkdir(parents=True,exist_ok=True)
PHOTOS=Path("images/pregnancy-women-batch5-photos")
DATA=[["Period Late After Stress?","Here's what to know","Stress can shift cycle timing. A test helps if pregnancy is possible."],["Feeling Different Lately?","Which signs matter?","Many early changes overlap with PMS. Symptoms alone cannot confirm pregnancy."],["Bloating Before Your Period?","Know the possible causes","Bloating can happen with PMS and for many other reasons."],["Tested Negative Yesterday?","Could it be too early?","Testing too early may miss pregnancy. Follow your test instructions."],["PMS or Pregnancy Signs?","Why they can feel alike","Tender breasts, cramps, and mood shifts can occur with both."],["Tired Even After Sleep?","What could be behind it?","Fatigue is common and has many possible causes."],["Light Spotting This Week?","What to pay attention to","Spotting has several possible causes. Seek care for severe pain or heavy bleeding."],["Cravings Suddenly Changed?","Hormones and appetite","Food cravings alone cannot tell you whether you are pregnant."],["Breasts Feel Different?","What changes can mean","Breast changes may occur before a period or in early pregnancy."],["Cycle a Week Late?","Plan your next step","If pregnancy is possible, a home test may help clarify."],["Nauseous in the Morning?","Look beyond one symptom","Nausea has many possible causes. A test helps confirm pregnancy."],["Is It Too Early to Test?","Timing really matters","Testing after a missed period is usually more reliable."],["Cramps, No Bleeding Yet?","What could it mean?","Cramps may occur for different reasons. Notice timing and other symptoms."],["New Sensitivity to Smells?","A change worth noting","Smell sensitivity can happen for different reasons."],["More Bathroom Trips?","Why it might happen","Frequent urination has several causes, not only pregnancy."],["Sudden Food Aversions?","Listen to your body","Changes in food preferences alone cannot confirm pregnancy."],["See a Faint Test Line?","Read the result carefully","Check the result within the test's reading window and follow its instructions."],["Period Shorter Than Usual?","Cycles can vary","Period length can change. Consider testing if pregnancy is possible."],["Wondering When to Retest?","Here's a simple guide","If testing very early, follow the kit guidance on when to repeat."],["Not Sure if You're Pregnant?","Start with your symptoms","Explore common signs with the quiz, then use a test to confirm."]]
W,H=1000,1500
REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
def font(n,kind="regular"):
    return ImageFont.truetype({"regular":REG,"bold":BOLD,"serif":SERIF}[kind],n)
def wrap(draw,text,f,maxw):
    lines=[];line=""
    for word in text.split():
        candidate=(line+" "+word).strip()
        if line and draw.textbbox((0,0),candidate,font=f)[2]>maxw:
            lines.append(line);line=word
        else:line=candidate
    if line:lines.append(line)
    return lines
def center(draw,text,y,f,color):
    bb=draw.textbbox((0,0),text,font=f)
    draw.text(((W-(bb[2]-bb[0]))/2,y),text,font=f,fill=color)
def flower(d,x,y,s):
    for a in range(0,360,72):
        px=x+math.cos(math.radians(a))*s*.62
        py=y+math.sin(math.radians(a))*s*.62
        d.ellipse((px-s*.31,py-s*.31,px+s*.31,py+s*.31),fill="#F2BFCB")
    d.ellipse((x-s*.19,y-s*.19,x+s*.19,y+s*.19),fill="#F5D99D")
def heart(d,x,y,s,color):
    d.ellipse((x-s*.4,y-s*.3,x,y+s*.15),fill=color)
    d.ellipse((x,y-s*.3,x+s*.4,y+s*.15),fill=color)
    d.polygon([(x-s*.4,y),(x+s*.4,y),(x,y+s*.64)],fill=color)
def draw_pin(i,title,subtitle,explanation):
    photo=Image.open(PHOTOS/f"photo_{i+1:02d}.jpg").convert("RGB")
    img=Image.new("RGB",(W,H),"#FCE9E5")
    d=ImageDraw.Draw(img)
    d.ellipse((-240,-170,440,520),fill="#F7D3D5")
    d.ellipse((710,-130,1300,410),fill="#F9D9E2")
    d.ellipse((-250,1090,370,1720),fill="#F9D5D9")
    d.ellipse((740,1145,1230,1670),fill="#F6D0D7")
    for x,y,s in [(60,210,17),(932,186,20),(78,1080,18),(928,1064,16),(78,1460,18),(927,1445,17)]:
        flower(d,x,y,s)
    for x,y in [(88,343),(918,345),(90,1233),(917,1234)]:
        heart(d,x,y,19,"#E78CA4")
    # Photo card: each design uses a completely new source photograph.
    photo=ImageOps.fit(photo,(918,745),Image.Resampling.LANCZOS,centering=(.5,.5))
    mask=Image.new("L",(918,745),0)
    md=ImageDraw.Draw(mask)
    md.rounded_rectangle((0,0,917,744),radius=45,fill=255)
    img.paste(photo,(41,392),mask)
    d=ImageDraw.Draw(img)
    # Top category capsule
    d.rounded_rectangle((206,46,794,115),radius=34,fill="#FFFFFF")
    center(d,"PREGNANCY & PERIOD TIPS",64,font(25,"bold"),"#803B4D")
    # Natural language click-worthy headline, sized to prevent clipping.
    sz=72
    while sz>40:
        titlef=font(sz,"serif")
        tlines=wrap(d,title,titlef,910)
        if len(tlines)<=2:break
        sz-=2
    ty=144 if len(tlines)==2 else 170
    for line in tlines:
        center(d,line,ty,titlef,"#6E2C38")
        ty+=sz+10
    subsize=43
    while subsize>27 and d.textbbox((0,0),subtitle,font=font(subsize,"serif"))[2]>890:
        subsize-=1
    center(d,subtitle,max(317,ty+2),font(subsize,"serif"),"#CC5174")
    # Bottom reading panel. No tiny or AI-created text.
    d.rounded_rectangle((112,1135,888,1270),radius=45,fill="#FFF9F5")
    explanatory=font(27)
    xlines=wrap(d,explanation,explanatory,712)
    if len(xlines)>3:
        explanatory=font(24)
        xlines=wrap(d,explanation,explanatory,722)
    ypos=1170-max(0,len(xlines)-2)*16
    for line in xlines:
        center(d,line,ypos,explanatory,"#5D303B")
        ypos+=36
    d.rounded_rectangle((142,1291,858,1392),radius=49,fill="#D95678",outline="#FFF4F0",width=5)
    center(d,"EXPLORE THE PREGNANCY QUIZ  >",1324,font(27,"bold"),"#FFFFFF")
    center(d,"Am I Pregnant? App  |  Find out more",1436,font(21),"#783C48")
    name=f"{i+51:02d}_women_click_pin.jpg"
    img.save(OUT/name,quality=94,subsampling=0,optimize=True)
    return name
app="https://apps.apple.com/us/app/am-i-pregnant-pregnancy-quiz/id6769078846"
rows=[]
for i,(title,sub,explanation) in enumerate(DATA):
    filename=draw_pin(i,title,sub,explanation)
    media="https://raw.githubusercontent.com/shsweb/pinterest-pregnancy-pins/pregnancy-women-click-pins-20261022/images/pregnancy-women-batch5-clickworthy/"+filename
    dest=app+"?utm_source=pinterest&utm_medium=pin&utm_campaign=pregnancy_women_clicks_20&utm_content=pin_"+str(i+51)
    description=explanation+" Explore common symptoms and next steps with the Am I Pregnant? Pregnancy Quiz app. The quiz does not diagnose pregnancy; use a pregnancy test to confirm. #AmIPregnant #PregnancyQuiz #PregnancySigns"
    rows.append([title,media,"Pregnancy Tips & Early Signs","",description,dest,"","pregnancy quiz, am i pregnant, pregnancy symptoms, early pregnancy, missed period"])
assert len(rows)==20 and len(set(row[1] for row in rows))==20 and len(set(row[5] for row in rows))==20
assert len(list(OUT.glob("*.jpg")))==20
with open("PINTEREST_20_NEW_WOMEN_CLICK_STYLE_READY.csv","w",encoding="utf-8-sig",newline="") as f:
    w=csv.writer(f)
    w.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"])
    w.writerows(rows)
print("Success: 20 unique full-size pins and 20 unique App Store URLs.")
