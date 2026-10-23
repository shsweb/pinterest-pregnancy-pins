from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from pathlib import Path
import csv, math
OUT=Path("images/pregnancy-women-batch7")
OUT.mkdir(parents=True,exist_ok=True)
APP="https://apps.apple.com/us/app/am-i-pregnant-pregnancy-quiz/id6769078846"
BOARD="Pregnancy Tips & Early Signs"
new=[Path("images/pregnancy-women-batch7-input/photo_%02d.jpg"%i) for i in range(1,10)]
old=[Path("images/pregnancy-women-approved")/n for n in [
"11_am_i_pregnant_woman.jpg","12_missed_period_woman.jpg","13_feeling_tired_woman.jpg",
"14_pms_or_pregnancy_woman.jpg","15_when_to_test_woman.jpg","16_late_period_woman.jpg",
"17_pregnancy_quiz_woman.jpg","18_nausea_woman.jpg","19_breast_tenderness_woman.jpg",
"20_spotting_woman.jpg"]]+[Path("images/pregnancy-women-batch2-corrected/21_bloating.jpg")]
sources=[(x,False) for x in new]+[(x,True) for x in old]
TOPICS=[
("Late Period, Negative Test?","Know what to do next","A test taken too early may be negative. Follow the kit directions for retesting."),
("Could These Be PMS Signs?","Why symptoms overlap","Cramps and breast tenderness can occur with PMS or early pregnancy."),
("No Nausea? Still Possible?","Symptoms can be different","Some people feel little nausea. A pregnancy test can provide clarity."),
("A Week After Ovulation?","Why timing matters","Testing too soon after ovulation may not give a reliable result."),
("Brown Spotting?","What could explain it?","Spotting has many possible causes. Seek care for unusual pain or bleeding."),
("Is Your Period Late?","Check your calendar","Cycles can vary. Track your dates and test when appropriate."),
("Breast Tenderness Again?","PMS or early changes?","Hormone changes can cause tenderness before a period or in pregnancy."),
("When Is a Test Reliable?","Timing makes a difference","Home tests are generally more reliable after a missed period."),
("Suddenly So Tired?","One sign with many causes","Fatigue can happen for many reasons and does not prove pregnancy."),
("Faint Line on a Test?","Read the instructions","Follow the test kit's reading time and repeat the test if instructed."),
("Cramps, No Bleeding?","What to consider","Cramps may occur for several reasons. Severe pain needs urgent medical advice."),
("Can You Have No Signs?","Early symptoms vary","Some people experience few early pregnancy symptoms."),
("Stress Delaying Your Period?","Learn about your cycle","Stress can affect periods. A pregnancy test helps if pregnancy is possible."),
("Is It Too Soon to Know?","Test timing explained","Follow home pregnancy test directions to get a more reliable result."),
("What Is a Missed Period?","Cycles aren't always exact","Cycles vary in length. A late period is not always due to pregnancy."),
("Food Aversions Suddenly?","What could it mean?","Changes in food preferences have many causes and cannot confirm pregnancy."),
("Symptoms Only at Night?","What to know","Symptoms can happen at any time and are not diagnostic."),
("Cycle Different This Month?","Notice the patterns","Cycle changes happen. Tracking dates can help you understand timing."),
("PMS Feelings, No Period?","One common question","PMS signs overlap with early pregnancy. Testing may give clarity."),
("Might You Be Pregnant?","Your next step matters","Explore possible signs, then confirm with a pregnancy test.")
]
assert len(sources)==len(TOPICS)==20
W,H=1000,1500
REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
def f(n,k="reg"):return ImageFont.truetype({"reg":REG,"bold":BOLD,"serif":SERIF}[k],n)
def lines(d,s,ff,width):
 a=[];cur=""
 for wd in s.split():
  t=(cur+" "+wd).strip()
  if cur and d.textbbox((0,0),t,font=ff)[2]>width:
   a.append(cur);cur=wd
  else:cur=t
 if cur:a.append(cur)
 return a
def center(d,s,y,ff,color):
 b=d.textbbox((0,0),s,font=ff);d.text(((1000-b[2]+b[0])/2,y),s,font=ff,fill=color)
def flower(d,x,y):
 for v in range(0,360,72):
  xx=x+17*math.cos(math.radians(v));yy=y+17*math.sin(math.radians(v))
  d.ellipse((xx-11,yy-11,xx+11,yy+11),fill="#F2BBCB")
 d.ellipse((x-8,y-8,x+8,y+8),fill="#FFEABC")
def render(number,title,sub,advice,src,has_text):
 assert src.is_file(),str(src)
 canvas=Image.new("RGB",(W,H),"#FDE9E6");d=ImageDraw.Draw(canvas)
 d.ellipse((-260,-200,385,440),fill="#F7D0D4")
 d.ellipse((725,-200,1220,450),fill="#F9D6DE")
 d.ellipse((-230,1110,360,1610),fill="#F9D8D7")
 d.ellipse((745,1100,1245,1690),fill="#F8D3D7")
 for xx,yy in ((50,250),(950,250),(44,1145),(960,1190),(90,1460),(934,1470)):
  flower(d,xx,yy)
 pict=Image.open(src).convert("RGB")
 if has_text:
  ww,hh=pict.size
  pict=pict.crop((int(ww*.09),int(hh*.285),int(ww*.91),int(hh*.715)))
 pict=ImageOps.fit(pict,(920,735),Image.Resampling.LANCZOS,centering=(.5,.48))
 shadow=Image.new("RGBA",(W,H))
 ImageDraw.Draw(shadow).rounded_rectangle((34,380,962,1130),radius=48,fill=(89,54,63,44))
 shadow=shadow.filter(ImageFilter.GaussianBlur(16))
 canvas=Image.alpha_composite(canvas.convert("RGBA"),shadow)
 m=Image.new("L",(920,735))
 ImageDraw.Draw(m).rounded_rectangle((0,0,919,734),radius=42,fill=255)
 canvas.paste(pict,(40,385),m)
 d=ImageDraw.Draw(canvas)
 d.rounded_rectangle((205,40,795,109),radius=35,fill="#FFFAF8")
 center(d,"PREGNANCY & PERIOD TIPS",58,f(26,"bold"),"#6E3941")
 sz=69
 while sz>=40:
  ff=f(sz,"serif");ls=lines(d,title,ff,890)
  if len(ls)<=2:break
  sz-=2
 y=143 if len(ls)==2 else 181
 for s in ls:center(d,s,y,ff,"#702E37");y+=sz+6
 sf=43
 while sf>=28 and d.textbbox((0,0),sub,font=f(sf,"serif"))[2]>890:sf-=1
 center(d,sub,max(312,y+5),f(sf,"serif"),"#D04D70")
 d.rounded_rectangle((106,1134,894,1278),radius=45,fill="#FFF9F6",outline="#EECAC8",width=2)
 ft=f(26);ll=lines(d,advice,ft,728)
 if len(ll)>3:ft=f(23);ll=lines(d,advice,ft,735)
 yy=1165-(len(ll)-2)*15
 for s in ll:center(d,s,yy,ft,"#65333B");yy+=37
 d.rounded_rectangle((132,1292,868,1397),radius=51,fill="#D75578",outline="#FFF3EE",width=5)
 center(d,"EXPLORE THE PREGNANCY QUIZ  >",1325,f(28,"bold"),"#FFFFFF")
 center(d,"Am I Pregnant? App  |  Find out more",1440,f(22),"#713B47")
 path=OUT/("pin_%03d.jpg"%number)
 canvas.convert("RGB").save(path,"JPEG",quality=94,optimize=True,subsampling=0)
 assert Image.open(path).size==(1000,1500)
 return path
rows=[]
for i,((title,subtitle,tip),(source,old_poster)) in enumerate(zip(TOPICS,sources),171):
 img=render(i,title,subtitle,tip,source,old_poster)
 imageurl="https://raw.githubusercontent.com/shsweb/pinterest-pregnancy-pins/main/images/pregnancy-women-batch7/"+img.name
 dest=APP+"?utm_source=pinterest&utm_medium=pin&utm_campaign=women_click_hooks_batch7&utm_content=pin_%03d"%i
 desc=tip+" Explore your symptoms with the Am I Pregnant? Pregnancy Quiz app. A quiz cannot confirm pregnancy; use a pregnancy test. #AmIPregnant #PregnancyQuiz #PregnancySymptoms"
 rows.append([title,imageurl,BOARD,"",desc,dest,"","pregnancy signs, am I pregnant quiz, late period, PMS or pregnancy"])
with open("PINTEREST_NEW_20_WOMEN_BATCH7_READY.csv","w",newline="",encoding="utf-8-sig") as h:
 w=csv.writer(h);w.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"]);w.writerows(rows)
assert len(rows)==20 and len(set(r[1] for r in rows))==20 and len(set(r[5] for r in rows))==20
assert len(list(OUT.glob("pin_*.jpg")))==20
print("SUCCESS: 20 new 1000x1500 pins and one Pinterest bulk-upload CSV.")
