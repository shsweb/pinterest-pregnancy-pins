from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import math
import csv

PHOTOS=Path("images/pregnancy-women-batch5-photos")
OUT=Path("images/pregnancy-women-batch5-final")
OUT.mkdir(parents=True,exist_ok=True)
W,H=1000,1500
REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
APP="https://apps.apple.com/us/app/am-i-pregnant-pregnancy-quiz/id6769078846"
BOARD="Pregnancy Tips & Early Signs"
PINS=[
("Could I Be Pregnant?","Early clues to consider","Symptoms can overlap with PMS. Only a pregnancy test can confirm pregnancy."),
("Period Late Again?","What should you do next?","Cycle timing can vary. A home pregnancy test can provide more clarity."),
("Signs After Ovulation?","Why timing matters","Changes after ovulation are not proof of pregnancy. Know when to test."),
("Why Am I So Tired?","One symptom, many causes","Tiredness can happen for many reasons. Consider your cycle timing."),
("PMS or Pregnancy?","Why signs can overlap","Bloating, cramps and mood changes may happen with either."),
("Breast Changes?","What could they mean?","Hormones can affect breast tenderness before a period or in early pregnancy."),
("Feeling Different Lately?","Notice your body's signals","Pay attention to your cycle. Symptoms alone cannot confirm pregnancy."),
("First Pregnancy Test?","Know when to check","Follow the instructions and test at an appropriate time for clearer results."),
("Negative Test, Still Late?","What to consider next","An early test can be negative. Follow the kit's retesting guidance."),
("Cramps, No Period?","Possible explanations","Cramps may have many causes. A pregnancy test can help if pregnancy is possible."),
("Feeling Queasy?","Could it mean pregnancy?","Nausea can have many causes and is not a reliable sign on its own."),
("Irregular Cycles?","Start with your dates","Tracking your period can help you recognize changes in your cycle."),
("Bloated or PMS?","What to pay attention to","Bloating alone does not tell you whether you are pregnant."),
("Too Early to Test?","Timing can change results","Testing early can miss a pregnancy. Check the kit instructions."),
("Missed Period?","A simple next-step checklist","Check cycle dates, consider a test, and follow up if needed."),
("Spotting Between Periods?","What you should know","Spotting has many causes. Seek medical care for heavy bleeding or pain."),
("Reading a Test Result?","Avoid common mistakes","Read results within the time window stated in your test instructions."),
("Unsure About Your Symptoms?","Start with a few questions","A symptom quiz offers reflection, but only testing can confirm pregnancy."),
("Tracking Your Period?","Find patterns over time","Record your cycle dates to better understand when your period is due."),
("Think You Might Be Pregnant?","Explore your next steps","Understand possible signs and the right time to take a pregnancy test.")
]
assert len(PINS)==20

def font(size,style="reg"):
    return ImageFont.truetype({"reg":REG,"bold":BOLD,"serif":SERIF}[style],size)

def centered(draw,txt,y,f,color):
    b=draw.textbbox((0,0),txt,font=f)
    draw.text(((W-(b[2]-b[0]))/2,y),txt,font=f,fill=color)

def wrap(draw,s,f,maxw):
    lines=[];line=""
    for word in s.split():
        t=(line+" "+word).strip()
        if line and draw.textbbox((0,0),t,font=f)[2]>maxw:
            lines.append(line);line=word
        else:
            line=t
    if line:lines.append(line)
    return lines

def corner_flower(d,x,y,size=20):
    for deg in range(0,360,60):
        xx=x+size*.68*math.cos(math.radians(deg))
        yy=y+size*.68*math.sin(math.radians(deg))
        d.ellipse((xx-size*.38, yy-size*.38,xx+size*.38,yy+size*.38),fill="#EBA6BA")
    d.ellipse((x-6,y-6,x+6,y+6),fill="#FFF3CC")

def heart(d,cx,cy,r=21,col="#D35C78"):
    d.ellipse((cx-r,cy-r,cx+3,cy+8),outline=col,width=4)
    d.ellipse((cx-3,cy-r,cx+r,cy+8),outline=col,width=4)
    d.line((cx-r,cy+3,cx,cy+r*1.4,cx+r,cy+3),fill=col,width=4,joint="curve")

def make(i,pin):
    title,subtitle,advice=pin
    number=51+i
    base=Image.new("RGB",(W,H),"#FCE9E6")
    d=ImageDraw.Draw(base)
    d.ellipse((-320,-280,405,530),fill="#F7D2D3")
    d.ellipse((750,-220,1270,500),fill="#FAD4DE")
    d.ellipse((-250,1070,420,1730),fill="#F7D0D5")
    d.ellipse((700,1120,1320,1640),fill="#F8D5DE")
    for x,y in [(61,92),(934,110),(66,1186),(928,1184),(91,1442),(926,1462)]:
        corner_flower(d,x,y,20)
    for x,y in [(107,345),(872,350)]:
        heart(d,x,y,18)
    photo=Image.open(PHOTOS/f"photo_{i+1:02d}.jpg").convert("RGB")
    # Fit source into a dedicated photo panel, preserving the subject centrally.
    photo=ImageOps.fit(photo,(946,741),method=Image.Resampling.LANCZOS,centering=(0.5,0.49))
    mask=Image.new("L",photo.size,0)
    m=ImageDraw.Draw(mask)
    m.rounded_rectangle((0,0,945,740),radius=45,fill=255)
    base.paste(photo,(27,399),mask)
    d=ImageDraw.Draw(base)
    d.rounded_rectangle((194,34,806,107),radius=37,fill="#FFFAF9")
    centered(d,"PREGNANCY & PERIOD TIPS",55,font(27,"bold"),"#74434A")
    headline_size=70
    while headline_size>=38:
        hf=font(headline_size,"serif")
        ls=wrap(d,title,hf,890)
        if len(ls)<=2:break
        headline_size-=2
    assert len(ls)<=2
    yy=150 if len(ls)>1 else 185
    for line in ls:
        centered(d,line,yy,hf,"#692A34")
        yy+=headline_size+4
    sfsize=43
    while sfsize>=26 and d.textbbox((0,0),subtitle,font=font(sfsize,"serif"))[2]>880:sfsize-=1
    centered(d,subtitle,max(322,yy+6),font(sfsize,"serif"),"#D05479")
    d.rounded_rectangle((105,1132,895,1277),radius=42,fill="#FFF8F5")
    df=font(27)
    dl=wrap(d,advice,df,730)
    if len(dl)>3:
        df=font(24)
        dl=wrap(d,advice,df,742)
    assert len(dl)<=4
    yy=1155+(3-len(dl))*15
    for line in dl:
        centered(d,line,yy,df,"#62373E")
        yy+=36
    d.rounded_rectangle((120,1294,880,1397),radius=50,fill="#CF5374",outline="#FFF9F8",width=4)
    centered(d,"EXPLORE THE PREGNANCY QUIZ  >",1325,font(29,"bold"),"#FFFFFF")
    centered(d,"Am I Pregnant? App  |  Find out more",1435,font(21),"#763C48")
    file=OUT/f"{number:02d}_pregnancy_woman.jpg"
    base.save(file,format="JPEG",quality=95,optimize=True,subsampling=0)
    assert Image.open(file).size==(1000,1500)
    return file.name

rows=[]
urlbase="https://raw.githubusercontent.com/shsweb/pinterest-pregnancy-pins/main/images/pregnancy-women-batch5-final/"
for i,(title,sub,advice) in enumerate(PINS):
    name=make(i,(title,sub,advice))
    destination=APP+f"?utm_source=pinterest&utm_medium=pin&utm_campaign=pregnancy_women_batch5&utm_content=pin_{51+i}"
    description=f"{title} {sub}. {advice} Explore the Am I Pregnant? Pregnancy Quiz app for general information. A quiz is not a pregnancy test. #AmIPregnant #PregnancyTips #PregnancyQuiz"
    rows.append([title,urlbase+name,BOARD,"",description,destination,"","am i pregnant, pregnancy quiz, early pregnancy symptoms, period, pregnancy test"])
assert len(rows)==20 and len({r[1] for r in rows})==20 and len({r[5] for r in rows})==20
with open("PINTEREST_20_PREGNANCY_WOMEN_BATCH5_READY.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f)
    w.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"])
    w.writerows(rows)
print("SUCCESS 20 distinct 1000x1500 pins; 20 public URLs; 20 app links; final CSV ready.")
