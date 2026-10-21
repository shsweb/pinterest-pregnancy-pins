from PIL import Image
from pathlib import Path
import csv
source=Path("images/pregnancy-women-batch2-source")
dest=Path("images/pregnancy-women-batch2")
dest.mkdir(parents=True,exist_ok=True)
items=[["21_bloating","Feeling Bloated? What Could It Mean?","Bloating can happen for many reasons and cannot confirm pregnancy."],["22_mild_cramps","Mild Cramps? PMS or Something Else?","Mild cramps can happen for many reasons; consider a pregnancy test if your period is late."],["23_smell_sensitivity","Sensitive to Smells? Pregnancy Signs Explained","Smell sensitivity has many possible causes. A pregnancy test can help clarify."],["24_frequent_urination","Peeing More Often? What Could It Mean?","Frequent urination can have many causes, not just pregnancy."],["25_mood_changes","Mood Changes? PMS or Pregnancy?","Mood changes can occur with PMS and pregnancy. Symptoms alone cannot confirm."],["26_appetite_changes","Appetite Changes? Early Pregnancy Questions","Cravings and food aversions can have different causes. Explore your symptoms."],["27_headaches","More Headaches? Know the Possible Reasons","Headaches are common and do not on their own indicate pregnancy."],["28_sleep_changes","Sleeping Differently? Your Cycle and Sleep","Sleep changes can have many causes. Track your cycle and symptoms."],["29_negative_test","Negative Test but No Period? What Next?","A negative test may occur when taken too early. Follow the test instructions for retesting."],["30_cycle_uncertainty","Not Sure About Your Cycle? Start Here","Track period dates and learn when it makes sense to take a pregnancy test."]]
url="https://raw.githubusercontent.com/shsweb/pinterest-pregnancy-pins/main/images/pregnancy-women-batch2/"
app="https://apps.apple.com/us/app/am-i-pregnant-pregnancy-quiz/id6769078846"
rows=[]
for i,(name,title,desc) in enumerate(items,21):
    img=Image.open(source/(name+".jpg")).convert("RGB")
    img.thumbnail((1000,1500),Image.Resampling.LANCZOS)
    bg=Image.new("RGB",(1000,1500),(252,234,231))
    x=(1000-img.width)//2
    y=(1500-img.height)//2
    bg.paste(img,(x,y))
    filename=name+".jpg"
    bg.save(dest/filename,quality=94,subsampling=0,optimize=True)
    rows.append([title,url+filename,"Pregnancy Tips & Early Signs","",desc+" Explore the Am I Pregnant? Pregnancy Quiz app for self-reflection. A quiz cannot confirm pregnancy. #AmIPregnant #PregnancyTips",app+"?utm_source=pinterest&utm_medium=pin&utm_content=women_pin_"+str(i),"","early pregnancy signs, am i pregnant quiz, pregnancy test, menstrual cycle"])
with open("pinterest_10_women_batch2_FIXED.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f)
    w.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"])
    w.writerows(rows)
assert len(rows)==10 and len({r[1] for r in rows})==10 and len({r[5] for r in rows})==10
print("Generated 10 portrait 1000x1500 images and matching unique destination links")
