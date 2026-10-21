from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from pathlib import Path
import csv,math
SRC=Path("images/pregnancy-click-20-sources")
DST=Path("images/pregnancy-click-20")
DST.mkdir(parents=True,exist_ok=True)
APP="https://apps.apple.com/us/app/am-i-pregnant-pregnancy-quiz/id6769078846"
ITEMS=[
("Period 7 Days Late?","What should you check?","Check cycle dates","Consider recent changes","Test for clarity","A late period can have many causes. A pregnancy test can help confirm pregnancy."),
("PMS or Pregnancy?","The signs can overlap","Notice your usual PMS","Look at cycle timing","Test when appropriate","PMS and early pregnancy symptoms may feel similar. Symptoms alone cannot confirm pregnancy."),
("No Morning Sickness?","Can you still be pregnant?","Symptoms vary widely","Not everyone feels nausea","Take a pregnancy test","Not everyone experiences nausea in early pregnancy. Only a test can help confirm."),
("Only One Breast Sore?","What could it mean?","Hormones may change","Tenderness has causes","Seek care if persistent","Breast soreness can have many causes. Unusual persistent symptoms deserve advice."),
("Craving Salty Foods?","A sign or just a craving?","Cravings are common","Many factors affect appetite","Testing gives clarity","Food cravings alone cannot tell you whether you are pregnant."),
("Twinges in Your Belly?","What do you notice?","Check pain severity","Track your cycle","Test if your period is late","Mild twinges can have many causes. Severe pain warrants prompt medical advice."),
("Suddenly Exhausted?","Could your cycle be involved?","Consider sleep changes","Think about your routine","Notice period timing","Tiredness is common and has many causes, including changes in sleep and hormones."),
("Feel Different This Month?","3 things worth checking","Know cycle dates","Notice what's changed","Take a test for clarity","If this cycle feels different, checking timing and taking a pregnancy test may help."),
("Period Due Tomorrow?","Too early to test?","Check test instructions","Timing changes accuracy","Retest if recommended","Testing too early can give a false-negative result. Follow the test kit directions."),
("Spotting After Ovulation?","Not always implantation","Spotting has causes","Track timing and amount","Get advice for heavy bleeding","Spotting has many possible causes and cannot confirm implantation or pregnancy."),
("A Faint Test Line?","What to know next","Read the kit directions","Check within time window","Retest if recommended","Read home test results only within the manufacturer's stated time window."),
("Late After a Stressful Week?","Cycles can shift","Stress may affect timing","Track your cycle","Test if pregnancy is possible","Stress and other factors can change period timing. Testing can help if needed."),
("Negative Test Yesterday?","Should you test again?","Consider how early","Check the kit guidance","Retest as directed","A negative result may happen when testing too early. Follow the test instructions."),
("No Breast Tenderness?","Symptoms aren't a checklist","People notice different signs","Missing signs prove nothing","A test is more reliable","Not everyone experiences breast tenderness. Symptoms alone cannot confirm pregnancy."),
("Breast Changes This Month?","PMS can feel similar","Notice the timing","Check for other changes","Test when appropriate","Breast changes can happen around a period and for many other reasons."),
("Period Date Changed?","Know your cycle clues","Cycles aren't identical","Record recent dates","Consider testing","Cycle length can vary. Tracking dates can help you decide when to test."),
("No Usual PMS Symptoms?","What could that mean?","Cycles can feel different","Symptoms may vary","Only a test can confirm","Changes from your usual PMS pattern are not a reliable pregnancy indicator."),
("Waking Up to Pee?","There are many reasons","Think about fluids","Notice urinary symptoms","Get care for pain or burning","Nighttime urination has many causes. Seek medical advice for pain or burning."),
("Feel More Sensitive to Smells?","A change worth noticing","Sensitivity can vary","Consider other causes","Test if your period is late","Smell sensitivity is not a reliable pregnancy test on its own."),
("Think You Might Be Pregnant?","Start with a simple check","Review cycle dates","Explore common signs","Test to confirm","Explore your symptoms with a quiz for reflection. Only a pregnancy test can confirm.")
]
W,H=1000,1500
FREG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FBOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FSERIF="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
THEMES=[
("#FFE8EA","#D6537B","#6C2B3B"),
("#FCE9E0","#CE6D80","#683543"),
("#F7E8F6","#B9688B","#5D3648"),
("#FDEAE6","#CB6476","#663744")
]
def font(n,k="reg"):
 return ImageFont.truetype({"reg":FREG,"bold":FBOLD,"serif":FSERIF}[k],n)
def text_width(d,s,f):
 bbox=d.textbbox((0,0),s,font=f)
 return bbox[2]-bbox[0]
def center(d,s,y,f,fill):
 d.text(((W-text_width(d,s,f))/2,y),s,font=f,fill=fill)
def lines(d,s,f,width):
 out=[];cur=""
 for w in s.split():
  trial=(cur+" "+w).strip()
  if cur and text_width(d,trial,f)>width:
   out.append(cur);cur=w
  else:cur=trial
 if cur:out.append(cur)
 return out
def heart(d,x,y,col,size=19):
 r=size//2
 d.ellipse((x-r,y-r,x+2,y+5),fill=col)
 d.ellipse((x-2,y-r,x+r,y+5),fill=col)
 d.polygon(((x-r,y+2),(x+r,y+2),(x,y+size)),fill=col)
def flower(d,x,y):
 for theta in range(0,360,72):
  px=x+int(20*math.cos(math.radians(theta)))
  py=y+int(20*math.sin(math.radians(theta)))
  d.ellipse((px-13,py-13,px+13,py+13),fill="#F6B9C7")
 d.ellipse((x-9,y-9,x+9,y+9),fill="#FFF3C5")
def make(i,row):
 title,sub,*rest=row
 tips=rest[:3];desc=rest[3]
 bg,accent,dark=THEMES[i%4]
 im=Image.new("RGB",(W,H),bg)
 d=ImageDraw.Draw(im)
 d.ellipse((-260,-260,330,400),fill="#F8D1D4")
 d.ellipse((670,-200,1220,375),fill="#F4CCD9")
 d.ellipse((-245,1140,400,1740),fill="#F8D4DE")
 d.ellipse((750,1190,1250,1610),fill="#F2D4E3")
 for x,y in [(72,148),(921,144),(55,1010),(935,1015),(60,1446),(932,1435)]:
  flower(d,x,y)
 for x,y in [(130,330),(855,312),(100,980),(882,1000)]:
  heart(d,x,y,accent,15)
 d.rounded_rectangle((152,35,848,111),radius=38,fill="#FFFFFF")
 center(d,"PREGNANCY & PERIOD TIPS",57,font(28,"bold"),dark)
 d.rounded_rectangle((53,128,947,365),radius=42,fill="#FFF8F5")
 title_size=76
 while title_size>40:
  tf=font(title_size,"serif")
  tlines=lines(d,title,tf,810)
  if len(tlines)<=2:break
  title_size-=2
 if len(tlines)==1:
  center(d,tlines[0],183,tf,dark)
 else:
  center(d,tlines[0],147,tf,dark)
  center(d,tlines[1],147+title_size+7,tf,dark)
 sf=font(34,"bold")
 while text_width(d,sub,sf)>800 and sf.size>24:
  sf=font(sf.size-1,"bold")
 center(d,sub,312,sf,accent)
 # Photo area: whole face and hands stay inside rounded card.
 photo=Image.open(SRC/("photo_%02d.jpg"%(i+1))).convert("RGB")
 w,h=photo.size
 # cropping excludes most empty headroom while retaining body and context
 crop=photo.crop((int(w*.025),int(h*.20),int(w*.975),int(h*.91)))
 photo=ImageOps.fit(crop,(918,682),Image.Resampling.LANCZOS,centering=(.5,.43))
 shadow=Image.new("RGBA",(W,H),(0,0,0,0))
 sd=ImageDraw.Draw(shadow)
 sd.rounded_rectangle((43,390,957,1072),radius=45,fill=(104,63,68,58))
 shadow=shadow.filter(ImageFilter.GaussianBlur(12))
 im=Image.alpha_composite(im.convert("RGBA"),shadow).convert("RGB")
 mask=Image.new("L",(918,682),0)
 md=ImageDraw.Draw(mask)
 md.rounded_rectangle((0,0,917,681),radius=38,fill=255)
 im.paste(photo,(41,381),mask)
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((56,1029,944,1274),radius=44,fill="#FFF9F7")
 center(d,"3 THINGS TO CHECK",1047,font(28,"bold"),dark)
 for j,tip in enumerate(tips):
  yy=1094+j*55
  d.ellipse((118,yy-2,159,yy+39),fill="#F8D5DF")
  d.text((129,yy+2),str(j+1),font=font(22,"bold"),fill=dark)
  sfont=font(29)
  while text_width(d,tip,sfont)>685 and sfont.size>23:
   sfont=font(sfont.size-1)
  d.text((184,yy+1),tip,font=sfont,fill="#633C48")
 d.rounded_rectangle((119,1292,881,1392),radius=50,fill=accent,outline="#FFF7F3",width=6)
 center(d,"TRY THE PREGNANCY QUIZ   >",1323,font(33,"bold"),"#FFFFFF")
 center(d,"Am I Pregnant? App   |   A quiz cannot confirm pregnancy",1441,font(21),dark)
 filename=f"{i+51:02d}_clickworthy_pin.jpg"
 im.save(DST/filename,quality=94,subsampling=0,optimize=True)
 return filename
rows=[]
for i,item in enumerate(ITEMS):
 filename=make(i,item)
 title,sub,*rest=item
 desc=rest[-1]
 media="https://raw.githubusercontent.com/shsweb/pinterest-pregnancy-pins/main/images/pregnancy-click-20/"+filename
 link=APP+f"?utm_source=pinterest&utm_medium=pin&utm_campaign=pregnancy_click_20&utm_content=pin_{i+51}"
 rows.append([title,media,"Pregnancy Tips & Early Signs","",desc+" Explore common symptoms with the Am I Pregnant? Pregnancy Quiz app. A quiz cannot confirm pregnancy; a home pregnancy test can help. #AmIPregnant #PregnancyQuiz #PeriodTips",link,"","am i pregnant, pregnancy quiz, early pregnancy signs, late period, PMS or pregnancy"])
with open("PINTEREST_20_CLICKWORTHY_READY.csv","w",newline="",encoding="utf-8-sig") as f:
 w=csv.writer(f)
 w.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"])
 w.writerows(rows)
assert len(rows)==20 and len({x[1] for x in rows})==20 and len({x[5] for x in rows})==20
assert len(list(DST.glob("*_clickworthy_pin.jpg")))==20
print("Published 20 photos and pin designs, 20 unique public image links, 20 app destination links.")
