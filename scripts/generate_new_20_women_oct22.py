from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, csv
W,H=1000,1500
ROOT=Path("images/pregnancy-women-batch6-new")
ROOT.mkdir(parents=True,exist_ok=True)
TEMPLATE=Image.open("images/pregnancy-women-batch2-corrected/21_bloating.jpg").convert("RGB").resize((W,H),Image.Resampling.LANCZOS)
F_SERIF="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size,path=F_SERIF):
    return ImageFont.truetype(path,size)
def wrap(d,text,ft,width):
    words=text.split(); lines=[]; cur=""
    for word in words:
        nxt=(cur+" "+word).strip()
        if cur and d.textbbox((0,0),nxt,font=ft)[2]>width:
            lines.append(cur);cur=word
        else:cur=nxt
    if cur:lines.append(cur)
    return lines
def center(d,text,y,ft,fill):
    b=d.textbbox((0,0),text,font=ft)
    d.text(((W-(b[2]-b[0]))/2,y),text,font=ft,fill=fill)
def draw_pin(index,title,subtitle,caption):
    result=TEMPLATE.copy()
    photo=Image.open(f"assets/new-women-2026-10/photo_{index:02d}.jpg").convert("RGB")
    ow,oh=photo.size
    crop=photo.crop((int(ow*.065),int(oh*.045),int(ow*.935),int(oh*.805)))
    ratio=max(W/crop.width,790/crop.height)
    crop=crop.resize((math.ceil(crop.width*ratio),math.ceil(crop.height*ratio)),Image.Resampling.LANCZOS)
    ww,hh=crop.size
    cx=(ww-W)//2;cy=(hh-790)//2
    crop=crop.crop((cx,cy,cx+W,cy+790))
    # Smoothing into the original watercolor floral background.
    mask=Image.new("L",(W,790),0)
    for y in range(790):
        a=min(255,round(y/70*255),round((790-y)/70*255))
        a=max(0,a)
        ImageDraw.Draw(mask).line([(0,y),(W,y)],fill=a,width=1)
    result.paste(crop,(0,350),mask)
    d=ImageDraw.Draw(result)
    # Fully remove earlier poster wording; keep the top logo, CTA and border flourishes.
    d.rounded_rectangle((43,133,957,377),radius=48,fill=(255,230,230))
    fs=82
    while fs>=38:
        title_font=font(fs)
        lines=wrap(d,title,title_font,862)
        if len(lines)<=2:break
        fs-=2
    y=148 if len(lines)>1 else 166
    for line in lines:
        center(d,line,y,title_font,(105,34,40)); y+=fs+5
    sub_font=font(43)
    while sub_font.size>25 and d.textbbox((0,0),subtitle,font=sub_font)[2]>840:
        sub_font=font(sub_font.size-1)
    center(d, min(338,max(281,y+9)), sub_font,(210,75,109)) if False else None
    center(d,subtitle,min(336,max(281,y+9)),sub_font,(210,75,109))
    # Draw subtle hearts alongside central portrait as in the approved example.
    def heart(x,y,size):
        color=(214,73,109)
        d.arc((x-size,y-size//2,x,y+size//2),180,360,fill=color,width=5)
        d.arc((x,y-size//2,x+size,y+size//2),180,360,fill=color,width=5)
        d.line([(x-size,y),(x,y+int(size*1.12)),(x+size,y)],fill=color,width=5)
    heart(230,485,22);heart(755,522,20)
    # Replace explanation while retaining the exact wide pink CTA and footer.
    d.rounded_rectangle((107,1105,895,1270),radius=45,fill=(249,216,213))
    d.rounded_rectangle((129,1130,873,1262),radius=44,fill=(255,249,246))
    body_font=font(28,F_REG)
    copy=wrap(d,caption,body_font,692)
    if len(copy)>3:
        body_font=font(25,F_REG);copy=wrap(d,caption,body_font,700)
    y=1163-(len(copy)-2)*15
    for line in copy:
        center(d,line,y,body_font,(94,38,44));y+=38
    filename=f"pin_{index+150:03d}.jpg"
    result.save(ROOT/filename,quality=94,optimize=True,subsampling=0)
    return filename
PINS=[
("No Morning Sickness?","Could you still be pregnant?","Not everyone experiences nausea. A pregnancy test can help confirm."),
("Breast Changes?","PMS or early pregnancy?","Breast changes can happen with PMS or pregnancy; symptoms often overlap."),
("Faint Pregnancy Test Line?","What might it mean?","Read your test result within the time window in its instructions."),
("Can Stress Delay a Period?","Understand cycle changes","Stress can affect cycle timing. Test if pregnancy is possible."),
("Extra Sleepy Lately?","An early sign to consider","Tiredness is common and can have many different causes."),
("Period Symptoms, No Period?","Why can that happen?","Cramping and bloating may occur before bleeding begins."),
("Are Home Tests Accurate?","Timing really matters","Home pregnancy tests are reliable when used as directed."),
("Longer Cycle Than Usual?","What should you do?","Cycle length can vary. Track dates and consider taking a test."),
("Mild Pelvic Pressure?","What could cause it?","Pelvic pressure has many causes. Seek care for severe or persistent pain."),
("When Should You Retest?","After a negative result","If your period is late, follow your test's retesting instructions."),
("Pregnancy Signs Very Early?","Why timing matters","Symptoms alone cannot confirm pregnancy or when it began."),
("Can Ovulation Dates Shift?","Learn about your cycle","Ovulation timing can vary, even with generally regular periods."),
("Sensitive to Odors?","A change to notice","Smell sensitivity can change for many reasons."),
("Tracking Your Period?","Know your cycle better","Record the first day of bleeding to understand your cycle."),
("Feeling Flushed Lately?","Body temperature changes","Feeling warmer can have several causes and doesn't prove pregnancy."),
("Craving Certain Foods?","PMS or pregnancy?","Food cravings alone are not a reliable pregnancy sign."),
("Symptoms Come and Go?","Why signs can change","Changing symptoms cannot confirm or rule out pregnancy."),
("Period Late After Travel?","Why routine can matter","Travel and routine changes may affect cycle timing."),
("Unsure When Period Is Due?","Find your next step","If pregnancy is possible, take a test at the appropriate time."),
("Positive Home Test?","What to do next","Contact a healthcare professional to discuss care and next steps."),
]
APP="https://apps.apple.com/us/app/am-i-pregnant-pregnancy-quiz/id6769078846"
rows=[]
for n,(title,subtitle,desc) in enumerate(PINS,1):
    fname=draw_pin(n,title,subtitle,desc)
    url="https://raw.githubusercontent.com/shsweb/pinterest-pregnancy-pins/main/images/pregnancy-women-batch6-new/"+fname
    link=APP+f"?utm_source=pinterest&utm_medium=pin&utm_campaign=pregnancy_women_batch6&utm_content=pin_{n+50}"
    rows.append([title,url,"Pregnancy Tips & Early Signs","",desc+" Explore early pregnancy signs and next steps with the Am I Pregnant? Pregnancy Quiz. Only a pregnancy test can confirm pregnancy. #AmIPregnant #PregnancyQuiz",link,"","pregnancy quiz, am i pregnant, early signs, pregnancy test, period"])
with open("PINTEREST_NEW_20_WOMEN_BATCH6_UPLOAD.csv","w",newline="",encoding="utf-8-sig") as file:
    writer=csv.writer(file)
    writer.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"])
    writer.writerows(rows)
assert len(rows)==20
assert len({r[1] for r in rows})==20
assert len({r[5] for r in rows})==20
assert len(list(ROOT.glob("pin_*.jpg")))==20
print("Generated and verified 20 new women-photo pins, 20 unique image links, 20 unique App Store destinations.")
