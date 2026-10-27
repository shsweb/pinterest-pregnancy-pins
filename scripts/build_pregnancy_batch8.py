from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path
import math, csv

ROOT=Path("images/pregnancy-women-batch8-sources")
OUT=Path("images/pregnancy-women-batch8")
OUT.mkdir(parents=True,exist_ok=True)
SERIF="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
APP="https://apps.apple.com/us/app/am-i-pregnant-pregnancy-quiz/id6769078846"
W,H=1000,1500
TOPICS=[
("2 Days Late?","What should you check?","A short delay can have many causes. A test may help if pregnancy is possible."),
("Period Due Today?","Feeling different?","Early symptoms can overlap with PMS. Test at an appropriate time."),
("Light Spotting?","What to do next","Spotting can have many causes. Seek care for heavy bleeding or severe pain."),
("A Faint Line?","Understanding a test","Read results within the time stated by your test instructions."),
("Morning Pregnancy Test?","Does timing matter?","First-morning urine may help if you are testing very early."),
("Tender Breasts, No Period?","PMS or pregnancy?","Breast tenderness can occur with PMS and early pregnancy."),
("Cramping After Ovulation?","Why it may happen","Cramps alone cannot tell you whether you are pregnant."),
("Nausea Comes and Goes?","What might it mean?","Nausea can have many causes and is not a pregnancy diagnosis."),
("Smells Seem Stronger?","One possible early change","A heightened sense of smell isn't enough to confirm pregnancy."),
("Waking Up Tired?","Could hormones be involved?","Fatigue has many possible causes. Consider your cycle and timing."),
("PMS Signs, No Period?","Here's what to know","Similar symptoms can happen before a period and in pregnancy."),
("Brown Discharge?","Common explanations","Brown discharge often contains older blood. Ask a clinician if concerned."),
("Can Stress Delay a Period?","Cycle timing explained","Stress can affect cycle timing, as can other factors."),
("Testing Too Early?","Why timing matters","A very early pregnancy test may be negative. Follow instructions."),
("Still Negative, Still Late?","What next?","Follow test directions for retesting and speak to a clinician if needed."),
("How Soon Do Signs Start?","Symptoms vary by person","Some people notice little or nothing early on. Testing confirms."),
("Cycle Not Regular?","When can you test?","When dates are uncertain, follow the test instructions for timing."),
("Bloated at Night?","What could be behind it?","Bloating is common for different reasons, including PMS."),
("Just One Symptom?","Don't jump to conclusions","One symptom cannot confirm pregnancy. Testing provides clarity."),
("Not Sure What to Do?","Start with your next step","Check your cycle dates and consider a pregnancy test when appropriate.")
]

def face_font(n,kind="serif"):
    return ImageFont.truetype({"serif":SERIF,"sans":SANS,"bold":BOLD}[kind],n)

def split_lines(d,text,font,width):
    lines=[];cur=""
    for word in text.split():
        trial=(cur+" "+word).strip()
        if cur and d.textbbox((0,0),trial,font=font)[2]>width:
            lines.append(cur);cur=word
        else:cur=trial
    if cur:lines.append(cur)
    return lines

def centered(d,text,y,fo,color):
    w=d.textbbox((0,0),text,font=fo)[2]
    d.text(((W-w)//2,y),text,fill=color,font=fo)

def heart(d,x,y,s):
    color="#D86B88"
    d.arc((x-s*.45,y-s*.50,x,y+s*.2),175,360,fill=color,width=5)
    d.arc((x,y-s*.50,x+s*.45,y+s*.2),180,365,fill=color,width=5)
    d.line((x-s*.43,y-s*.02,x,y+s*.68,x+s*.43,y-s*.02),fill=color,width=5,joint="curve")

def pin(index,title,subtitle,description):
    im=Image.new("RGB",(W,H),"#FCE9E5");d=ImageDraw.Draw(im)
    d.ellipse((-270,-200,400,450),fill="#F8D9D7")
    d.ellipse((750,-180,1320,395),fill="#F9D3DC")
    d.ellipse((-290,1125,380,1715),fill="#F6D5DA")
    d.ellipse((700,1165,1210,1680),fill="#F8D7DF")
    for x,y,s in ((93,180,24),(902,190,29),(63,1137,21),(918,1158,19)):
        heart(d,x,y,s)
    d.rounded_rectangle((180,45,820,115),radius=35,fill="#FFFFFF")
    centered(d,"PREGNANCY & PERIOD TIPS",66,face_font(27,"bold"),"#6D303D")
    fs=73
    while fs>=39:
        headline=face_font(fs)
        ls=split_lines(d,title,headline,890)
        if len(ls)<=2: break
        fs-=2
    y=174 if len(ls)==1 else 143
    for line in ls:
        centered(d,line,y,headline,"#692B34")
        y+=fs+10
    ss=42
    while ss>26 and d.textbbox((0,0),subtitle,font=face_font(ss))[2]>865:
        ss-=2
    centered(d,subtitle,365,face_font(ss),"#CB4C72")
    photo=Image.open(ROOT/f"photo_{index:02d}.jpg").convert("RGB")
    # Subject-safe editorial crop: the original is a portrait photo with top and bottom breathing room.
    content=ImageOps.fit(photo,(936,704),method=Image.Resampling.LANCZOS,centering=(.5,.50))
    mask=Image.new("L",(936,704),0)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,935,703),radius=43,fill=255)
    im.paste(content,(32,418),mask)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((108,1145,892,1280),radius=43,fill="#FFF9F7")
    descfont=face_font(28,"sans")
    dl=split_lines(d,description,descfont,720)
    if len(dl)>3:
        descfont=face_font(25,"sans")
        dl=split_lines(d,description,descfont,735)
    yy=1172 if len(dl)>=3 else 1190
    for line in dl:
        centered(d,line,yy,descfont,"#63323B")
        yy+=38
    d.rounded_rectangle((130,1300,870,1397),radius=48,fill="#D55778",outline="#FFF3F0",width=5)
    centered(d,"EXPLORE THE PREGNANCY QUIZ  >",1332,face_font(28,"bold"),"#FFFFFF")
    centered(d,"Am I Pregnant? App  |  Find out more",1440,face_font(21,"sans"),"#713746")
    dest=OUT/f"pin_{190+index}.jpg"
    im.save(dest,quality=95,subsampling=0,optimize=True)
    return dest

rows=[]
for i,(title,subtitle,description) in enumerate(TOPICS,1):
    dest=pin(i,title,subtitle,description)
    number=190+i
    media=f"https://raw.githubusercontent.com/shsweb/pinterest-pregnancy-pins/main/images/pregnancy-women-batch8/pin_{number}.jpg"
    link=APP+f"?utm_source=pinterest&utm_medium=pin&utm_campaign=women_batch8&utm_content=pin_{number}"
    rows.append([title,media,"Pregnancy Tips & Early Signs","",description+" Explore the Am I Pregnant? Pregnancy Quiz app for general information and self-reflection. A quiz cannot confirm pregnancy. #AmIPregnant #PregnancyQuiz",link,"","am i pregnant, pregnancy quiz, early pregnancy signs, pregnancy test, period symptoms"])
with open("PINTEREST_20_NEW_WOMEN_BATCH8_READY.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f)
    w.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"])
    w.writerows(rows)
assert len(rows)==20
assert len({r[0] for r in rows})==20
assert len({r[1] for r in rows})==20
assert len({r[5] for r in rows})==20
assert len(list(OUT.glob("*.jpg")))==20
assert all((OUT/f"pin_{i}.jpg").stat().st_size>150000 for i in range(191,211))
print("Success: 20 unique 1000x1500 JPEGs and matching CSV with unique app tracking links")
