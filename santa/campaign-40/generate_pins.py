"""Generate forty original vertical Pinterest Christmas posters for Call Santa."""
from pathlib import Path
from html import escape
from math import sin, cos, pi
import random, io
import cairosvg
from PIL import Image, ImageOps, ImageDraw

OUT = Path("santa/campaign-40/images")
OUT.mkdir(parents=True, exist_ok=True)
# Headline, subheadline, category, illustrated scene
PINS = [
 ("WHO ATE","SANTA'S COOKIES?","FUNNY SANTA","cookie"),
 ("SANTA HAS","A SILLY QUESTION","FUNNY SANTA","jokes"),
 ("DON'T TELL","THE REINDEER!","FUNNY SANTA","reindeer"),
 ("ELF ON","THE LOOSE!","FUNNY SANTA","elf"),
 ("SANTA'S","MILK MUSTACHE","FUNNY SANTA","cookie"),
 ("READY FOR","A SLEIGH RIDE?","NORTH POLE ADVENTURE","sleigh"),
 ("THE REINDEER","RESCUE MISSION","NORTH POLE ADVENTURE","reindeer"),
 ("INSIDE SANTA'S","TOY WORKSHOP","NORTH POLE ADVENTURE","workshop"),
 ("A SECRET","NORTH POLE CALL","NORTH POLE ADVENTURE","phone"),
 ("DASH THROUGH","THE SNOW!","NORTH POLE ADVENTURE","snowman"),
 ("YOUR PHONE","IS RINGING!","SANTA VIDEO CALL","phone"),
 ("SANTA ACTUALLY","TALKS BACK!","SANTA VIDEO CALL","phone"),
 ("ASK SANTA","ANYTHING!","SANTA VIDEO CALL","jokes"),
 ("CALL SANTA","TOGETHER!","SANTA VIDEO CALL","family"),
 ("SAY HELLO TO","MRS. CLAUS!","SANTA VIDEO CALL","mrs"),
 ("MEET JINGLE","THE ELF!","NORTH POLE FRIENDS","elf"),
 ("CALL COMET","THE REINDEER!","NORTH POLE FRIENDS","reindeer"),
 ("MRS. CLAUS","SAYS HELLO!","NORTH POLE FRIENDS","mrs"),
 ("ELVES ARE","UP TO SOMETHING!","NORTH POLE FRIENDS","workshop"),
 ("A MAGICAL","NORTH POLE HELLO","NORTH POLE FRIENDS","star"),
 ("BEDTIME CALL","FROM SANTA","CHRISTMAS EVE MAGIC","bedtime"),
 ("STORY TIME","WITH SANTA","CHRISTMAS EVE MAGIC","book"),
 ("COUNT DOWN","TO CHRISTMAS!","CHRISTMAS EVE MAGIC","advent"),
 ("A CALL AT","JUST THE RIGHT TIME","CHRISTMAS EVE MAGIC","clock"),
 ("MAKE TONIGHT","EXTRA MAGICAL","CHRISTMAS EVE MAGIC","moon"),
 ("TELL SANTA","YOUR WISH LIST","SANTA KEEPSAKES","letter"),
 ("YOUR VERY OWN","SANTA LETTER","SANTA KEEPSAKES","letter"),
 ("ARE YOU ON THE","NICE LIST?","SANTA KEEPSAKES","certificate"),
 ("SAVE THAT","SANTA REACTION!","SANTA KEEPSAKES","camera"),
 ("A CHRISTMAS","CARD TO TREASURE","SANTA KEEPSAKES","certificate"),
 ("FLY SANTA'S","MAGICAL SLEIGH!","PLAY & CREATE","sleigh"),
 ("COLOR A","CHRISTMAS SCENE","PLAY & CREATE","color"),
 ("OPEN A NEW","ADVENT SURPRISE","PLAY & CREATE","advent"),
 ("A NEW VOICE","FROM SANTA","PLAY & CREATE","voice"),
 ("CHAT WHEN","IT'S QUIET","PLAY & CREATE","phone"),
 ("SANTA KNOWS","EVERYONE'S NAME!","FAMILY CHRISTMAS","family"),
 ("CHRISTMAS FUN","FOR SIBLINGS","FAMILY CHRISTMAS","family"),
 ("SANTA SPEAKS","YOUR LANGUAGE","FAMILY CHRISTMAS","world"),
 ("TRY A LITTLE","CHRISTMAS MAGIC","FAMILY CHRISTMAS","gift"),
 ("YOUR NEW","FAMILY TRADITION","FAMILY CHRISTMAS","tree"),
]
assert len(PINS) == 40

PALETTES = [
 ("#57112d","#e83847","#ffe9a5","#ffffff"),
 ("#0a3347","#087e8b","#ffe3b0","#ffffff"),
 ("#1f3850","#3d69b1","#ffe7a3","#ffffff"),
 ("#3e245f","#ae4aa2","#ffe9bb","#ffffff"),
 ("#21452e","#2e9471","#fce4a7","#ffffff"),
 ("#692717","#d47149","#fff2ba","#ffffff"),
 ("#18244c","#6159ad","#ffd38e","#ffffff"),
 ("#4c1027","#bb2752","#f9e29d","#ffffff"),
]
SVG = []
def emit(t): SVG.append(t)
def rect(x,y,w,h,fill,rx=0,opacity=1,stroke=None,sw=0):
    emit(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" opacity="{opacity}"' + (f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>')
def circle(x,y,r,fill,opacity=1,stroke=None,sw=0):
    emit(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" opacity="{opacity}"' + (f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>')
def path(d,fill,stroke=None,sw=0,opacity=1):
    emit(f'<path d="{d}" fill="{fill}" opacity="{opacity}"'+(f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else '')+'/>')
def text(x,y,content,sz=50,fill="white",weight=800,anchor="middle",spacing=0):
    emit(f'<text x="{x}" y="{y}" fill="{fill}" font-size="{sz}" font-weight="{weight}" font-family="DejaVu Sans,Arial,sans-serif" text-anchor="{anchor}" letter-spacing="{spacing}">{escape(str(content))}</text>')
def group(x,y,s=1,rot=0):
    emit(f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">')
def close(): emit('</g>')
def sparkle(x,y,r=18,color="#ffeba7"):
    path(f'M {x} {y-r} Q {x+r*.25} {y-r*.2} {x+r} {y} Q {x+r*.25} {y+r*.2} {x} {y+r} Q {x-r*.25} {y+r*.2} {x-r} {y} Q {x-r*.25} {y-r*.2} {x} {y-r} Z',color)

def santa(x,y,s=1):
    group(x,y,s)
    ellipse=''; 
    circle(0,118,148,"#b11b38")
    path("M-134 125 Q-154 260 -80 286 L87 286 Q147 216 134 120", "#a91a37")
    path("M-138 154 Q0 215 138 154", "none", "#fff9ee",27)
    circle(-65,66,45,"#fff9eb");circle(65,66,45,"#fff9eb")
    circle(0,-18,112,"#f6c09e")
    path("M-114 -34 Q-110 -180 5 -182 Q115 -166 128 -56 Q53 -86 -114 -34","#cd2440")
    circle(122,-75,32,"#fff9ef")
    rect(-122,-61,244,38,"#fff9ed",20)
    circle(-42,0,9,"#2c363b");circle(41,0,9,"#2c363b")
    path("M-75 -32 Q-42 -53 -17 -30 M18 -29 Q48 -51 78 -31","none","#f7f4e7",15)
    circle(0,39,15,"#e8a38b")
    path("M-110 46 Q-125 166 0 196 Q120 166 110 46 Q57 125 0 104 Q-62 122 -110 46","#fff9ee")
    path("M0 78 Q-51 48 -75 88 Q-35 137 0 100 Q30 133 78 86 Q52 46 0 78","#fff9ef")
    path("M-26 130 Q0 145 26 130","none","#a45450",5)
    close()

def elf(x,y,s=1):
    group(x,y,s)
    circle(0,160,108,"#2d8f66")
    path("M-110 -5 Q-92 -142 19 -196 L98 -42Z","#24a775")
    circle(40,-137,19,"#ffe4a7")
    circle(-102,17,33,"#f7c39a");circle(106,17,33,"#f7c39a")
    circle(0,14,102,"#f5c79c")
    circle(-35,-5,7,"#303c45");circle(40,-5,7,"#303c45")
    path("M-29 40 Q0 72 31 37","none","#ad5547",7)
    path("M-97 93 Q0 139 100 91","none","#eabf64",24)
    path("M-22 128 L0 165 L23 126","none","#ffeeac",14)
    close()

def reindeer(x,y,s=1):
    group(x,y,s)
    path("M-90 -70Q-158 -171 -130 -216 M-124 -143L-188 -176 M78 -73Q155 -169 135 -229 M132 -145L190 -171",
         "none","#b57745",19)
    circle(-102,-14,37,"#b7844a");circle(98,-14,37,"#b7844a")
    circle(0,53,121,"#ab6d42")
    path("M-65 70Q0 20 65 70Q78 159 0 185Q-75 151 -65 70","#e1b78c")
    circle(-41,25,10,"#222e39");circle(46,25,10,"#222e39")
    circle(0,94,25,"#f04e64")
    path("M-17 131Q0 145 18 131","none","#663c38",6)
    rect(-78,177,157,35,"#bc2c45",16)
    circle(0,195,12,"#f9d07a")
    close()

def present(x,y,s=1,angle=0):
    group(x,y,s,angle)
    rect(-90,-86,180,170,"#f05b65",13)
    rect(-16,-87,32,171,"#f9d975")
    rect(-99,-28,198,37,"#f9d975",8)
    path("M0-86Q-110-159-95-89Q-66-50 0-86 Q91-165 96-89Q73-43 0-86","#f9d975")
    close()

def cookie(x,y,s=1):
    group(x,y,s)
    circle(0,0,92,"#f4c57f")
    circle(-35,-24,12,"#6d3e2d");circle(26,-49,13,"#6d3e2d")
    circle(46,28,15,"#75422d");circle(-22,45,13,"#75422d")
    circle(-52,17,7,"#8e4b2e");circle(15,5,10,"#8e4b2e")
    close()

def phone(x,y,s=1):
    group(x,y,s,9)
    rect(-170,-284,340,575,"#19253a",45,1,"#ffdc9a",12)
    rect(-154,-263,308,537,"#255775",35)
    circle(0,-40,134,"#337e86",.5)
    santa(0,-120,.56)
    rect(-98,110,195,39,"#ecf8f2",19,.85)
    text(0,136,"SANTA • LIVE",14,"#1d4a50",900)
    circle(-95,212,32,"#ebf6ef");circle(0,212,40,"#e34051");circle(95,212,32,"#ecf6ee")
    path("M-18 217Q0 197 19 216","none","white",8)
    text(-95,218,"♪",24,"#23637c",900); text(95,220,"▣",25,"#23637c",900)
    close()

def sleigh(x,y,s=1):
    group(x,y,s)
    path("M-219 100L196 100Q182 160 135 170H-165Q-202 170-219 100","#b81c3e")
    path("M-248 160Q-220 210-158 202H199Q245 202 251 163","none","#ffe0a3",18)
    path("M-171 -8Q-171 90-70 92H205Q225-3 180-57H-140Z","#d23850")
    rect(-185,-85,337,36,"#ffe4a7",18)
    santa(-45,-138,.43)
    present(134,-64,.4)
    close()

def tree(x,y,s=1):
    group(x,y,s)
    rect(-21,135,42,120,"#824b36",7)
    for j,(w,h) in enumerate([(145,-130),(186,-47),(216,43)]):
        path(f"M0{h-205}L-{w} {h+90}L{w} {h+90}Z",["#2eaa7b","#15966b","#0d765c"][j])
    for dx,dy,c in [(-65,-70,"#ffd681"),(80,30,"#ff6686"),(-108,127,"#ffd681"),(56,155,"#ffd681"),(50,-145,"#ff6686")]:
        circle(dx,dy,13,c)
    sparkle(0,-347,43)
    close()

def letter(x,y,s=1):
    group(x,y,s,-7)
    rect(-225,-150,450,322,"#fff8df",28,1,"#e5bd70",10)
    path("M-205-130L0 28 L205 -130","none","#d7ae63",16)
    path("M-208 140L-54 26 M208 140L57 26","none","#e1c180",14)
    circle(0,32,53,"#b72548")
    text(0,47,"S",45,"#fff8da",900)
    close()

def certificate(x,y,s=1):
    group(x,y,s,-7)
    rect(-222,-245,444,488,"#fff8d9",22,1,"#f4ce83",12)
    rect(-199,-218,398,444,"none",9,1,"#d2ad64",3)
    sparkle(0,-137,45,"#e4ad49")
    text(0,-36,"OFFICIAL",31,"#765a3e")
    text(0,21,"NICE LIST",43,"#b42a40",900)
    path("M-127 79H126","none","#d3b276",5)
    text(0,126,"CERTIFICATE",25,"#635641",900)
    circle(0,205,21,"#b72745")
    close()

def book(x,y,s=1):
    group(x,y,s)
    path("M-238-131Q-98-183 0-122Q108-179 239-131V180Q97 129 0 199Q-89 131-238 180Z","#fff5dc")
    path("M0-125V193 M-212-76Q-110-118-34-73 M38-73Q128-117 209-78 M-210-27Q-114-62-35-26 M37-23Q140-68 208-27",
         "none","#c7a76a",9)
    sparkle(0,-220,44)
    close()

def snowman(x,y,s=1):
    group(x,y,s)
    circle(0,124,114,"#edfaff")
    circle(0,-44,83,"#f6fcff")
    rect(-92,-160,183,34,"#172c48",9)
    rect(-54,-250,105,101,"#172c48",8)
    circle(-27,-58,9,"#25364b");circle(30,-58,9,"#25364b")
    path("M0-30L79-7L0-8Z","#f48f48")
    path("M-65 11Q0 51 65 12","none","#d54e5e",9)
    circle(0,91,9,"#415872");circle(0,147,9,"#415872")
    close()

def advent(x,y,s=1):
    group(x,y,s,-3)
    rect(-215,-236,430,470,"#fff2da",27)
    rect(-214,-231,430,78,"#bf2950",23)
    text(0,-179,"DECEMBER",38,"white",900)
    for j in range(3):
        for k in range(4):
            px=-157+k*104; py=-98+j*119
            rect(px-39,py-43,81,98,["#e65d66","#277e77","#dca94d"][(j+k)%3],11)
            text(px,py+10,str(j*4+k+1),38,"white",900)
    close()

def clock(x,y,s=1):
    group(x,y,s)
    circle(0,0,200,"#f6e9be",1,"#f3ca76",15)
    circle(0,0,168,"#fff7e0")
    for a in range(12):
        ang=(a*30-90)*pi/180
        circle(cos(ang)*139,sin(ang)*139,6,"#ad6e62")
    path("M0-108L0 4L85 59","none","#b42f4d",14)
    circle(0,0,15,"#b42f4d")
    sparkle(210,-180,34)
    close()

def moon(x,y,s=1):
    group(x,y,s)
    circle(0,0,174,"#ffe2a1")
    circle(68,-58,166,"#21436b")
    sparkle(-173,-168,24);sparkle(161,132,36)
    close()

def mrs(x,y,s=1):
    group(x,y,s)
    circle(0,105,151,"#318c72")
    circle(0,0,115,"#f4c29e")
    circle(0,-105,100,"#f3f7e5")
    path("M-113-78Q0-202 118-78Z","#e7ece5")
    circle(-42,3,10,"#223846");circle(42,3,10,"#223846")
    path("M-65 10Q-45 21-22 10 M22 10Q43 21 66 10","none","#e8f6e9",6)
    path("M-40 68Q0 100 40 68","none","#99443e",8)
    circle(0,38,14,"#e6a88b")
    rect(-65,116,130,135,"#fff4d3",25)
    close()

def palette_icon(x,y,s=1):
    group(x,y,s)
    path("M-195 30Q-195-198 23-207Q211-199 207-30Q200 35 132 46Q69 53 89 125Q109 209 5 214Q-201 203-195 30","#fff3dd")
    for dx,dy,c in [(-103,-70,"#ed5172"),(-27,-126,"#fed477"),(71,-114,"#62a882"),(140,-43,"#85a5eb"),(-113,63,"#d879bb")]:
        circle(dx,dy,30,c)
    circle(19,78,49,"#c99d77")
    close()

def camera(x,y,s=1):
    group(x,y,s)
    rect(-230,-156,460,310,"#fff6df",42)
    rect(-88,-187,177,61,"#fff6df",22)
    circle(0,0,108,"#276b80")
    circle(0,0,67,"#aee3e0")
    circle(168,-91,21,"#e64d67")
    sparkle(171,-202,41)
    close()

def voice(x,y,s=1):
    group(x,y,s)
    rect(-75,-202,150,287,"#f7dfaa",75)
    rect(-42,-170,85,223,"#fff1d6",43)
    path("M-131-10Q-136 133 0 139Q134 133 131-10 M0 139V209 M-88 212H88","none","#fff1d6",21)
    for p in [-1,1]:
        path(f"M{p*170}-101Q{p*230}-10 {p*172} 81 M{p*216}-146Q{p*303}-6 {p*218} 134","none","#ffd46f",13)
    close()

def world(x,y,s=1):
    group(x,y,s)
    circle(0,0,196,"#7ac6c0")
    path("M-170-43Q-80-187-44-111L-54 0L18 35L-37 159Q-164 93-170-43","#377c69")
    path("M20-175Q151-188 191-43L103 10L89 110L43 169L17 80L77 22L13-12Z","#3c956a")
    path("M-196 0H196 M-140-135Q0 0-140 135 M140-135Q0 0 140 135","none","#dcfbda",4,.53)
    sparkle(182,-179,35)
    close()

SCENE = {
"phone":phone,"cookie":lambda x,y,s: (santa(x-85,y,s*.88),cookie(x+195,y+90,s*.75)),
"jokes":lambda x,y,s:(santa(x-65,y,s*.93),speech(x+175,y-150,s*.65)),
"reindeer":lambda x,y,s:(reindeer(x,y,s*.92),sparkle(x+195,y-160,31)),
"elf":lambda x,y,s:(elf(x-65,y,s),present(x+155,y+140,s*.68)),
"sleigh":sleigh,"workshop":lambda x,y,s:(elf(x-130,y,s*.83),present(x+165,y+60,s*.94),sparkle(x,y-242,35)),
"snowman":lambda x,y,s:(snowman(x-70,y,s),santa(x+190,y+130,s*.4)),
"mrs":mrs,"star":lambda x,y,s:(moon(x-20,y,s*.8),sparkle(x+160,y+190,76),sparkle(x-200,y-230,34)),
"bedtime":lambda x,y,s:(book(x,y,s),moon(x+140,y-180,s*.35)),
"book":book,"advent":advent,"clock":clock,"moon":moon,
"letter":letter,"certificate":certificate,"camera":camera,"color":palette_icon,
"voice":voice,"world":world,
"family":lambda x,y,s:(phone(x-95,y,s*.8),sparkle(x+192,y-140,45),present(x+196,y+161,s*.67)),
"gift":lambda x,y,s:(present(x,y,s*1.45),sparkle(x+168,y-181,43)),
"tree":tree
}
def speech(x,y,s):
    group(x,y,s,-12)
    rect(-170,-110,340,183,"#fff8e5",45)
    path("M-55 64L-109 157L24 66","#fff8e5")
    text(0,-17,"HO HO",49,"#b82948",900)
    text(0,44,"HO!",54,"#b82948",900)
    close()

def design(i,pin):
    global SVG
    SVG=[]
    headline1,headline2,theme,scene=pin
    c1,c2,gold,white=PALETTES[(i*5+i//5)%len(PALETTES)]
    rng=random.Random(29180+i*371)
    emit(f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1500" viewBox="0 0 1000 1500">')
    emit(f'<defs><linearGradient id="bg" x1="0" y1="0" x2="{(i%4+1)*.2}" y2="1"><stop stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')
    emit(f'<radialGradient id="halo"><stop stop-color="{gold}" stop-opacity=".73"/><stop offset="1" stop-color="{gold}" stop-opacity="0"/></radialGradient>')
    emit('<filter id="shade"><feDropShadow dx="0" dy="20" stdDeviation="24" flood-color="#14162a" flood-opacity=".3"/></filter></defs>')
    rect(0,0,1000,1500,"url(#bg)")
    circle(490,830,540,"url(#halo)",.30)
    # Five varying decorative layouts; consistent legible headline and CTA placement
    mode=i%5
    if mode==0:
        path("M0 610Q420 535 1000 613V1110Q510 1240 0 1144Z","#fff6dd",opacity=.10)
        circle(50,560,190,"#fff",.045);circle(945,910,210,"#fff",.058)
    elif mode==1:
        path("M0 470Q500 780 1000 470L1000 1194Q550 1060 0 1210Z","#091c35",opacity=.16)
        rect(45,45,910,1406,"none",40,1,gold,6)
    elif mode==2:
        path("M0 780Q340 565 625 741T1000 741V1280H0Z","#fff6de",opacity=.10)
        rect(52,62,896,1340,"none",42,.55,"white",3)
    elif mode==3:
        circle(500,770,368,"#ffedb1",.10,white,7)
        path("M0 1196Q500 1083 1000 1187V1500H0Z","#f7e5c0",opacity=.1)
    else:
        path("M0 468L1000 558V1037L0 1147Z","#ffffff",opacity=.095)
        circle(500,780,352,"#fff5c4",.08)
    for j in range(78):
        px=rng.randint(18,982);py=rng.randint(20,1320)
        r=rng.choice([2,3,4,5,7])
        circle(px,py,r,"#fff8e7",rng.uniform(.22,.72))
    for j in range(8):
        px=rng.randint(30,960);py=rng.choice([rng.randint(410,580),rng.randint(1100,1230)])
        sparkle(px,py,rng.randint(9,22),gold)
    rect(135,65,730,60,gold,30,.95)
    text(500,106,theme,25,"#503039",900,spacing=2)
    if mode in (1,4):
        circle(90,198,28,"#fee0ad",.8);circle(903,306,42,"#ffe9bb",.4)
    s1=70 if len(headline1)>14 else (78 if len(headline1)>11 else 92)
    s2=68 if len(headline2)>15 else (78 if len(headline2)>11 else 91)
    text(500,244,headline1,s1,"#ffffff",900)
    text(500,351,headline2,s2,gold,900)
    text(500,413,"A LITTLE CHRISTMAS MAGIC",26,"#ffffff",700,spacing=3)
    # Artwork central panel
    if mode in (0,2):
        circle(500,823,333,"#fff4df",.11)
    if mode==4:
        path("M110 650Q500 468 889 650L852 1130Q505 1231 149 1118Z","#0b213b",opacity=.18)
    emit('<g filter="url(#shade)">')
    SCENE[scene](500,825,.95 if scene not in ("tree","world","voice","star") else 1.1)
    emit('</g>')
    # display legible story punchline distinct to each Pin number
    tags = {
        "cookie":"ASK SANTA WHO DID IT!","jokes":"ASK HIM A FUNNY QUESTION","reindeer":"MEET THE REINDEER",
        "elf":"SAY HI TO THE ELVES","sleigh":"JOIN THE ADVENTURE","workshop":"NORTH POLE FUN",
        "phone":"HE LISTENS & REPLIES","family":"SHARE THE MAGIC","mrs":"MEET MRS. CLAUS",
        "star":"A NORTH POLE SURPRISE","snowman":"A SNOWY ADVENTURE","bedtime":"COZY NIGHT CALLS",
        "book":"LET SANTA READ A STORY","advent":"DAILY CHRISTMAS SURPRISES",
        "clock":"PLAN A SURPRISE CALL","moon":"MAKE BEDTIME MAGICAL","letter":"SANTA WRITES IT DOWN",
        "certificate":"PRINT A KEEPSAKE","camera":"SAVE THE REACTION",
        "color":"FUN FESTIVE COLORING","voice":"A DAILY HELLO FROM SANTA",
        "world":"SANTA SPEAKS 9 LANGUAGES","gift":"FREE TO TRY","tree":"MAKE MEMORIES TOGETHER"
    }
    rect(123,1208,754,57,"#fff9e3",29)
    text(500,1245,tags[scene],25,"#654333",900,spacing=1)
    rect(91,1300,818,128,gold,57,1,"#fff6df",5)
    text(500,1361,"TRY CALL SANTA",47,"#6b1d31",900)
    text(500,1398,"iPHONE & iPAD  •  FREE TO TRY",21,"#734b39",800,spacing=1)
    emit('</svg>')
    return ''.join(SVG)

for i,pin in enumerate(PINS):
    img=OUT/f"santa-40-{i+1:02d}.png"
    cairosvg.svg2png(bytestring=design(i,pin).encode("utf-8"),write_to=str(img),output_width=1000,output_height=1500)
    with Image.open(img) as test:
        assert test.size == (1000,1500),img
    print(f"OK {i+1:02d} {img.stat().st_size:,} bytes")
# 8 columns x 5 rows, compact visual contact sheet
thumb_w=210; thumb_h=315; gap=12
sheet=Image.new("RGB",(gap+8*(thumb_w+gap),gap+5*(thumb_h+gap)),(245,241,233))
for i in range(40):
    with Image.open(OUT/f"santa-40-{i+1:02d}.png") as original:
        thumb=original.convert("RGB").resize((thumb_w,thumb_h),Image.Resampling.LANCZOS)
    x=gap+(i%8)*(thumb_w+gap);y=gap+(i//8)*(thumb_h+gap)
    sheet.paste(thumb,(x,y))
sheet.save(OUT/"contact-sheet.jpg",quality=88,optimize=True)
print("ALL 40 IMAGES + CONTACT SHEET COMPLETE")
