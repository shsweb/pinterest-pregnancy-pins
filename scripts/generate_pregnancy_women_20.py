from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path
import csv, math
OUT=Path("images/pregnancy-women-batch4"); OUT.mkdir(parents=True,exist_ok=True)
S1="images/pregnancy-women-approved/"
S2="images/pregnancy-women-batch2-corrected/"
sources=[S1+x for x in [
"11_am_i_pregnant_woman.jpg","12_missed_period_woman.jpg","13_feeling_tired_woman.jpg",
"14_pms_or_pregnancy_woman.jpg","15_when_to_test_woman.jpg","16_late_period_woman.jpg",
"17_pregnancy_quiz_woman.jpg","18_nausea_woman.jpg","19_breast_tenderness_woman.jpg",
"20_spotting_woman.jpg"]]+[S2+x for x in [
"21_bloating.jpg","22_mild_cramps.jpg","23_smell_sensitivity.jpg",
"24_frequent_urination.jpg","25_mood_changes.jpg","26_appetite_changes.jpg",
"27_headaches.jpg","28_sleep_changes.jpg","29_negative_test.jpg",
"30_cycle_uncertainty.jpg"]]
data=[
("Feeling Dizzy?","What could it mean?","Dizziness can have many causes. It cannot confirm pregnancy."),
("Lower Back Pain?","PMS or pregnancy?","Back pain has many causes. Symptoms alone cannot confirm pregnancy."),
("Metallic Taste?","A change to notice","A metallic taste can happen for many reasons."),
("White Discharge?","What is normal?","Discharge varies during the cycle. Seek care for pain or unusual odor."),
("Constipated Lately?","What could it mean?","Constipation has many causes. Notice your overall symptoms."),
("Heartburn?","A change to notice","Heartburn can have many causes. Testing gives better clarity."),
("Feeling Warmer?","What to know","Temperature changes can happen throughout the cycle."),
("Breakouts or Acne?","Hormones and skin","Skin changes occur for many reasons and cannot prove pregnancy."),
("Tender Nipples?","A change to notice","Hormone changes may cause tenderness before a period or in pregnancy."),
("Extra Thirsty?","What could it mean?","Unusual ongoing thirst deserves medical advice."),
("Bloating After Ovulation?","Understand your cycle","Bloating can happen at different times in your cycle."),
("Period Three Days Late?","What to do next","Periods can be late for several reasons. Consider testing."),
("Signs Before a Missed Period?","Why timing matters","Early pregnancy signs overlap with PMS. A test is more reliable."),
("Cramps but No Period?","What could it mean?","Cramps have many causes. Testing may provide clarity."),
("Sudden Food Aversions?","What to know","Food aversions do not confirm pregnancy."),
("Feeling More Emotional?","PMS or pregnancy?","Mood changes can be linked to hormones and stress."),
("Irregular Periods?","Track your cycle","Tracking dates can help you understand your cycle."),
("Took a Test Too Soon?","When to test again","An early test can miss pregnancy. Follow the kit directions."),
("Late Period, No Symptoms?","What to know","Symptoms vary. A pregnancy test can give an answer."),
("Morning or Evening Test?","Test timing explained","Follow test instructions; early testing may need morning urine.")
]
W,H=1000,1500
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
def f(n,kind="reg"):return ImageFont.truetype({"reg":FONT,"bold":BOLD,"serif":SERIF}[kind],n)
def wrap(d,s,ff,width):
 words=s.split();lines=[];cur=""
 for w in words:
  nxt=(cur+" "+w).strip()
  if cur and d.textbbox((0,0),nxt,font=ff)[2]>width:lines.append(cur);cur=w
  else:cur=nxt
 if cur:lines.append(cur)
 return lines
def center(d,s,y,ff,color):
 b=d.textbbox((0,0),s,font=ff);d.text(((W-(b[2]-b[0]))/2,y),s,font=ff,fill=color)
def draw_pin(i,title,sub,desc,src):
 base=Image.new("RGB",(W,H),"#FDE9E6");d=ImageDraw.Draw(base)
 d.ellipse((-200,-215,380,360),fill="#F7D2D4")
 d.ellipse((730,-160,1220,345),fill="#FAD7E0")
 d.ellipse((-205,1150,390,1700),fill="#F7D7DD")
 d.ellipse((710,1100,1200,1620),fill="#F9D9D9")
 for x,y in [(60,250),(936,245),(75,1120),(925,1120),(70,1430),(935,1440)]:
  for t in range(0,360,72):
   xx=x+math.cos(math.radians(t))*18; yy=y+math.sin(math.radians(t))*18
   d.ellipse((xx-11,yy-11,xx+11,yy+11),fill="#F3BBCB")
  d.ellipse((x-9,y-9,x+9,y+9),fill="#FFF7D5")
 photo=Image.open(src).convert("RGB")
 sw,sh=photo.size
 photo=photo.crop((round(sw*.06),round(sh*.279),round(sw*.94),round(sh*.724)))
 photo=ImageOps.fit(photo,(944,715),method=Image.Resampling.LANCZOS,centering=(.5,.51))
 mask=Image.new("L",(944,715));md=ImageDraw.Draw(mask);md.rounded_rectangle((0,0,944,715),radius=39,fill=255)
 base.paste(photo,(28,413),mask)
 d=ImageDraw.Draw(base)
 d.rounded_rectangle((196,40,804,112),radius=34,fill="#FFFFFF")
 center(d,"PREGNANCY & PERIOD TIPS",60,f(27,"bold"),"#743B46")
 size=74
 while size>=38:
  ff=f(size,"serif");ls=wrap(d,title,ff,900)
  if len(ls)<=2:break
  size-=2
 yy=148 if len(ls)==2 else 184
 for line in ls:
  center(d,line,yy,ff,"#722A36");yy+=size+6
 ss=46
 while ss>=28 and d.textbbox((0,0),sub,font=f(ss,"serif"))[2]>880:ss-=1
 center(d,sub,max(331,yy+3),f(ss,"serif"),"#D05276")
 d.rounded_rectangle((112,1136,888,1272),radius=42,fill="#FFF9F6")
 df=f(27,"reg");dls=wrap(d,desc,df,712)
 if len(dls)>3:df=f(24,"reg");dls=wrap(d,desc,df,730)
 dy=1171-(len(dls)-2)*15
 for line in dls:center(d,line,dy,df,"#652D39");dy+=35
 d.rounded_rectangle((126,1292,874,1390),radius=50,fill="#D75477",outline="#FFF5F1",width=4)
 center(d,"EXPLORE THE PREGNANCY QUIZ  >",1322,f(29,"bold"),"#FFFFFF")
 center(d,"Am I Pregnant? App  |  Find out more",1435,f(21), "#783C47")
 fname=f"{i+31:02d}_women_pin.jpg"
 base.save(OUT/fname,quality=94,optimize=True,subsampling=0)
 return fname
rows=[]
APP="https://apps.apple.com/us/app/am-i-pregnant-pregnancy-quiz/id6769078846"
for j,(title,sub,desc) in enumerate(data):
 filename=draw_pin(j,title,sub,desc,sources[j])
 imgurl="https://raw.githubusercontent.com/shsweb/pinterest-pregnancy-pins/main/images/pregnancy-women-batch4/"+filename
 landing=APP+"?utm_source=pinterest&utm_medium=pin&utm_campaign=pregnancy_women_batch4&utm_content=pin_"+str(j+31)
 rows.append([title,imgurl,"Pregnancy Tips & Early Signs","",desc+" Explore the Am I Pregnant? Pregnancy Quiz app. Only a pregnancy test can confirm pregnancy. #AmIPregnant #PregnancyQuiz",landing,"","pregnancy quiz, early pregnancy signs, missed period, PMS or pregnancy"])
with open("pinterest_women_20_READY.csv","w",newline="",encoding="utf-8-sig") as h:
 w=csv.writer(h)
 w.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"])
 w.writerows(rows)
assert len(rows)==20 and len(set(x[1] for x in rows))==20 and len(set(x[5] for x in rows))==20
assert len(list(OUT.glob("*_women_pin.jpg")))==20
print("Verified 20 Pinterest PNG alternatives in JPG form, 20 hosted image URL paths and 20 unique App Store tracking links.")
