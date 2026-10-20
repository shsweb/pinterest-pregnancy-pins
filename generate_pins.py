from PIL import Image, ImageDraw, ImageFont
import os, csv, math, random, textwrap
os.makedirs("images/pregnancy-quiz",exist_ok=True)
ROOT="/usr/share/fonts/truetype/dejavu/"
FONT=ROOT+"DejaVuSans.ttf"
BOLD=ROOT+"DejaVuSans-Bold.ttf"
ITEMS=[
("Am I Pregnant?","Early signs & what to do next","Early signs can overlap with PMS. Take a pregnancy test to confirm.","01_early_signs.png"),
("Late Period?","5 things to consider","Stress, cycle changes, medication and pregnancy can affect your period.","02_late_period.png"),
("Pregnancy Test","When should you take one?","Testing after a missed period often gives a more reliable result.","03_pregnancy_test.png"),
("Early Symptoms","What might you notice?","Fatigue, nausea and breast tenderness can have many causes.","04_early_symptoms.png"),
("PMS or Pregnancy?","Why they can feel similar","Cramps and breast tenderness can occur with either.","05_pms_vs_pregnancy.png"),
("Missed Your Period?","Your next-step checklist","Check your dates, take a home test and follow its instructions.","06_missed_period.png"),
("Pregnancy Signs","Symptoms that overlap","Only a test can confirm pregnancy. Symptoms alone cannot.","07_symptoms_overlap.png"),
("Am I Pregnant Quiz","Explore what you notice","A quick self-reflection quiz, not a pregnancy diagnosis.","08_pregnancy_quiz.png"),
("Waiting to Test?","What you should know","Testing too early can mean a negative result even if pregnant.","09_waiting_to_test.png"),
("Could I Be Pregnant?","Start with the basics","Learn possible signs, then confirm with a pregnancy test.","10_could_i_be_pregnant.png")
]
THEMES=[
("#FBECE8","#CB7880","#562E4F"),("#FFF1EC","#BA778B","#5C3853"),
("#FBEBF1","#C4779B","#533A55"),("#F6ECF8","#9277A9","#483652"),
("#FFF0E6","#D18A7B","#624450"),("#F7EEF0","#B47689","#563344"),
("#F2EAF7","#A47EB2","#523951"),("#FDECF1","#BD708A","#4E3448"),
("#FEF1E7","#C58E8A","#563E4A"),("#FBEDED","#B87E97","#543C52")
]
def rgb(h):return tuple(int(h[i:i+2],16) for i in (1,3,5))
def f(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
def center(draw,text,y,font,color):
    b=draw.textbbox((0,0),text,font=font)
    draw.text(((1000-(b[2]-b[0]))/2,y),text,font=font,fill=color)
def fit_title(draw,title,y,color):
    size=85
    while draw.textbbox((0,0),title,font=f(size,True))[2]>870 and size>45:size-=2
    center(draw,title,y,f(size,True),color)
def wrap_lines(draw,text,maxw,font):
    words=text.split(); lines=[]; cur=""
    for word in words:
        nxt=(cur+" "+word).strip()
        if draw.textbbox((0,0),nxt,font=font)[2]>maxw and cur:lines.append(cur);cur=word
        else:cur=nxt
    if cur:lines.append(cur)
    return lines
def icon(draw,idx,accent):
    c=rgb(accent)
    # Decorative simplified editorial illustration in a bordered round pastel medallion.
    draw.ellipse((305,525,695,915),fill="#FFFFFF",outline=accent,width=9)
    if idx in (1,5,8):
        draw.rounded_rectangle((390,605,615,838),radius=23,fill="#FFF7F9",outline=accent,width=10)
        draw.rectangle((420,660,585,670),fill=accent)
        for x in (442,498,555):
            for y in (714,765,810):
                draw.ellipse((x-9,y-9,x+9,y+9),fill=accent)
        draw.ellipse((492,741,535,784),fill="#EFA2AD")
    elif idx in (2,9):
        draw.rounded_rectangle((410,625,590,824),radius=42,fill="#FFE8ED",outline=accent,width=12)
        draw.rounded_rectangle((445,671,555,700),radius=7,fill="white",outline=accent,width=3)
        draw.rectangle((466,673,479,699),fill=accent)
        draw.rectangle((509,673,522,699),fill=accent)
    elif idx in (4,6):
        draw.line((405,742,595,742),fill=accent,width=12)
        draw.ellipse((400,653,492,745),outline=accent,width=11)
        draw.ellipse((504,653,596,745),outline=accent,width=11)
        center(draw,"?",765,f(48,True),accent)
    elif idx in (7,):
        draw.rounded_rectangle((408,629,592,816),radius=27,outline=accent,width=12,fill="#FFF4F8")
        for y in (682,737,788):
            draw.ellipse((444,y-11,468,y+13),fill=accent)
            draw.line((484,y,556,y),fill=accent,width=8)
    else:
        draw.arc((385,614,615,852),30,170,fill=accent,width=15)
        draw.arc((412,620,585,810),195,355,fill=accent,width=12)
        draw.ellipse((473,702,527,756),fill="#DF9CAB")
        draw.line((490,726,507,743,542,701),fill=accent,width=13,joint="curve")
for idx,(title,subtitle,copy,name) in enumerate(ITEMS):
    bg,accent,ink=THEMES[idx]
    im=Image.new("RGB",(1000,1500),rgb(bg));d=ImageDraw.Draw(im)
    d.ellipse((-190,-170,420,380),fill="#F4D8D9")
    d.ellipse((750,-135,1220,360),fill="#F9D5DF")
    d.ellipse((-170,1170,330,1620),fill="#F6DAD3")
    d.ellipse((735,1170,1130,1560),fill="#F1D6E8")
    for k in range(16):
        x=(k*151+idx*67)%950+22
        y=(k*197+idx*39)%1480
        if abs(x-500)>365 or y<280 or y>1280:
            d.ellipse((x,y,x+8,y+8),fill=accent)
    d.rounded_rectangle((128,119,872,195),radius=36,fill="white")
    center(d,"PREGNANCY & PERIOD TIPS",136,f(30,True),accent)
    fit_title(d,title,278,ink)
    sfont=f(43,True)
    lines=wrap_lines(d,subtitle,830,sfont)
    for j,line in enumerate(lines):center(d,line,403+j*56,sfont,accent)
    icon(d,idx,accent)
    d.rounded_rectangle((88,970,912,1180),radius=48,fill="#FFFFFF")
    detailfont=f(32)
    for j,line in enumerate(wrap_lines(d,copy,730,detailfont)):
        center(d,line,1016+j*48,detailfont,ink)
    d.rounded_rectangle((155,1219,845,1336),radius=51,fill=accent)
    center(d,"TRY THE PREGNANCY QUIZ  >",1258,f(31,True),"white")
    center(d,"Am I Pregnant? App  |  Find out more",1395,f(22,True),ink)
    im.save("images/pregnancy-quiz/"+name,format="PNG",optimize=True)
DEST="https://apps.apple.com/us/app/am-i-pregnant-pregnancy-quiz/id6769078846"
with open("pinterest_bulk_ready.csv","w",newline="",encoding="utf-8-sig") as h:
    w=csv.writer(h)
    w.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"])
    for title,sub,detail,name in ITEMS:
        w.writerow([title+" | "+sub,"https://raw.githubusercontent.com/shsweb/pinterest-pregnancy-pins/main/images/pregnancy-quiz/"+name,"Pregnancy Tips & Early Signs","",title+" — "+sub+". "+detail+" Explore the Am I Pregnant? Pregnancy Quiz app. This quiz does not confirm pregnancy. #AmIPregnant #PregnancyTest",DEST,"","pregnancy signs, pregnancy quiz, early pregnancy, missed period"])
print("Created",len(ITEMS),"pins and CSV")
