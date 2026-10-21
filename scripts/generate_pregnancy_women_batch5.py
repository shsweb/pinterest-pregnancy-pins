from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path
import csv, math

OUT=Path("images/pregnancy-women-batch5")
OUT.mkdir(parents=True,exist_ok=True)
SRC=Path("images/pregnancy-women-batch5-sources")
W,H=1000,1500
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
APP="https://apps.apple.com/us/app/am-i-pregnant-pregnancy-quiz/id6769078846"
ITEMS=[
("Pregnant Without Symptoms?","Early signs can vary","Some people notice few early signs. A pregnancy test can confirm."),
("When Is a Test Accurate?","Timing really matters","Results are generally more reliable after a missed period."),
("Late Period After Stress?","Why cycles can shift","Stress and other factors can affect period timing."),
("Testing Before Your Period?","What you should know","Early testing can miss a pregnancy. Follow your test instructions."),
("Evaporation Line or Positive?","Read results on time","Read your test within the time window in its instructions."),
("A Faint Line on Your Test?","Understand your result","A faint line read on time may be positive. Follow the instructions."),
("How Soon Can You Test?","After sex and conception","A pregnancy test needs time to detect pregnancy hormones."),
("Ovulation or Pregnancy?","Why symptoms overlap","Hormonal changes can create similar sensations."),
("Does Nausea Mean Pregnancy?","Not always","Nausea has many possible causes and cannot confirm pregnancy."),
("Cramps But No Bleeding?","What to consider","Cramps can have several causes, including period-related changes."),
("When to Retest?","After a negative result","If your period stays late, follow the kit's retesting guidance."),
("Cycle Changes This Month?","Common reasons","Cycles may shift with stress, illness, and routine changes."),
("First-Morning Test?","When it may help","First-morning urine may help when testing early."),
("Late Period After Travel?","Routine changes matter","Travel and sleep changes can affect your cycle."),
("Can Stress Delay a Period?","Body and cycle","Stress is one of several factors that can affect period timing."),
("Positive Pregnancy Test?","What happens next","Consider arranging care with a healthcare professional."),
("Symptoms Come and Go?","Patterns can vary","Symptoms fluctuate and cannot confirm pregnancy by themselves."),
("Your Period Feels Different?","Track what changed","Note unusual changes and seek medical advice if concerned."),
("Negative Test, Still Late?","Next steps","Retesting may help if you tested too early."),
("Questions About Your Cycle?","Start with the basics","Track dates and use a test when pregnancy is possible.")
]
assert len(ITEMS)==20
def font(size,which="regular"):
    return ImageFont.truetype({"regular":FONT,"bold":BOLD,"serif":SERIF}[which],size)
def wrap(d,t,f,maxwidth):
    out=[]; words=t.split(); accum=""
    for w in words:
        cand=(accum+" "+w).strip()
        if accum and d.textbbox((0,0),cand,font=f)[2]>maxwidth:
            out.append(accum);accum=w
        else:accum=cand
    if accum:out.append(accum)
    return out
def centered(d,txt,y,f,color):
    box=d.textbbox((0,0),txt,font=f)
    d.text(((W-(box[2]-box[0]))/2,y),txt,font=f,fill=color)
def flower(d,x,y,s):
    for angle in range(0,360,72):
        px=x+math.cos(math.radians(angle))*s*.6
        py=y+math.sin(math.radians(angle))*s*.6
        d.ellipse((px-s*.34,py-s*.34,px+s*.34,py+s*.34),fill="#F3C7CD")
    d.ellipse((x-s*.21,y-s*.21,x+s*.21,y+s*.21),fill="#F7E2A7")
def branch(d,x,y,mirror=False):
    sign=-1 if mirror else 1
    d.line((x,y,x+sign*80,y-130),fill="#8D9A85",width=6)
    for idx in range(4):
        yy=y-idx*29
        xx=x+sign*idx*20
        d.ellipse((xx+sign*5-19,yy-30,xx+sign*5+19,yy+12),fill="#A7B4A2")
        d.ellipse((xx+sign*28-16,yy-12,xx+sign*28+16,yy+22),fill="#90A391")
def make_pin(j,title,subtitle,body):
    number=j+51
    src=SRC/f"photo_{j+1:02d}.jpg"
    assert src.exists(),src
    # 1000x1500: Pinterest recommended 2:3 ratio.
    base=Image.new("RGB",(W,H),"#FBE5E4")
    draw=ImageDraw.Draw(base)
    for y in range(H):
        blend=y/H
        col=(int(250+4*blend),int(231+7*blend),int(227+7*blend))
        draw.line((0,y,W,y),fill=col)
    draw.ellipse((-240,-260,400,425),fill="#F5CED1")
    draw.ellipse((730,-190,1240,365),fill="#F8D7DE")
    draw.ellipse((-200,1130,330,1650),fill="#F8D2D9")
    draw.ellipse((685,1110,1250,1700),fill="#F5D2D8")
    branch(draw,30,460)
    branch(draw,950,455,True)
    branch(draw,70,1480)
    branch(draw,940,1480,True)
    for x,y,s in [(130,91,23),(868,100,19),(90,1175,16),(911,1163,16)]:
        flower(draw,x,y,s)
    # Use a unique, newly generated woman lifestyle photo for each pin.
    source=Image.open(src).convert("RGB")
    photo=ImageOps.fit(source,(920,730),method=Image.Resampling.LANCZOS,centering=(0.5,0.53))
    mask=Image.new("L",(920,730),0)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,919,729),radius=46,fill=255)
    base.paste(photo,(40,405),mask)
    draw=ImageDraw.Draw(base)
    # Typography is typeset in Pillow; no model-generated misspellings.
    draw.rounded_rectangle((214,44,786,112),radius=34,fill="#FFFBF9")
    centered(draw,"PREGNANCY & PERIOD TIPS",64,font(25,"bold"),"#69323E")
    size=69
    while True:
        main_font=font(size,"serif")
        title_lines=wrap(draw,title,main_font,910)
        if (len(title_lines)<=2 and size>=40) or size<=40:break
        size-=2
    assert len(title_lines)<=2,(title,title_lines)
    y=155 if len(title_lines)==2 else 201
    for line in title_lines:
        centered(draw,line,y,main_font,"#752632")
        y+=size+10
    subsize=40
    while draw.textbbox((0,0),subtitle,font=font(subsize,"serif"))[2]>880:
        subsize-=2
    centered(draw,subtitle,max(320,y+4),font(subsize,"serif"),"#CE5272")
    draw.rounded_rectangle((114,1143,886,1273),radius=43,fill="#FFF8F6")
    body_font=font(26)
    text_lines=wrap(draw,body,body_font,700)
    if len(text_lines)>3:
        body_font=font(24)
        text_lines=wrap(draw,body,body_font,740)
    assert len(text_lines)<=3,body
    yy=1180-(len(text_lines)-2)*15
    for line in text_lines:
        centered(draw,line,yy,body_font,"#65303C")
        yy+=35
    draw.rounded_rectangle((139,1297,861,1392),radius=48,fill="#D75275",outline="#FFF4F1",width=5)
    centered(draw,"EXPLORE THE PREGNANCY QUIZ  >",1327,font(28,"bold"),"#FFFFFF")
    centered(draw,"Am I Pregnant? App  |  Find out more",1440,font(21),"#763A48")
    name=f"{number:02d}_pregnancy_pin.jpg"
    base.save(OUT/name,quality=95,subsampling=0,optimize=True)
    assert Image.open(OUT/name).size==(1000,1500)
    return name
rows=[]
for j,(title,subtitle,body) in enumerate(ITEMS):
    filename=make_pin(j,title,subtitle,body)
    imgurl="https://raw.githubusercontent.com/shsweb/pinterest-pregnancy-pins/main/images/pregnancy-women-batch5/"+filename
    link=APP+"?utm_source=pinterest&utm_medium=pin&utm_campaign=pregnancy_women_batch5&utm_content=pin_"+str(j+51)
    rows.append([title,imgurl,"Pregnancy Tips & Early Signs","",body+" Explore the Am I Pregnant? Pregnancy Quiz app to reflect on your symptoms. A quiz cannot confirm pregnancy. #AmIPregnant #PregnancyQuiz",link,"","am I pregnant, pregnancy quiz, early pregnancy signs, pregnancy test, period"])
with open("pinterest_20_women_batch5_READY.csv","w",newline="",encoding="utf-8-sig") as f:
    writer=csv.writer(f)
    writer.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"])
    writer.writerows(rows)
assert len(rows)==20 and len(set(x[1] for x in rows))==20 and len(set(x[5] for x in rows))==20
# Preview montage of final rendered images for quality review
thumb=(190,285)
sheet=Image.new("RGB",(5*thumb[0],4*thumb[1]),"white")
for j in range(20):
    piece=Image.open(OUT/f"{j+51:02d}_pregnancy_pin.jpg").convert("RGB").resize(thumb,Image.Resampling.LANCZOS)
    sheet.paste(piece,((j%5)*thumb[0],(j//5)*thumb[1]))
sheet.save(OUT/"preview_contact_sheet.jpg",quality=93)
print("PASS: 20 different lifestyle photos, 20 fully typeset 1000x1500 pins, 20 distinct public image URL paths and 20 distinct app tracking URLs.")
