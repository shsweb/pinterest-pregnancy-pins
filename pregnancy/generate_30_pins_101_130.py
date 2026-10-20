from pathlib import Path
import os, random, csv, math, base64, html, textwrap
from PIL import Image
from io import BytesIO
import cairosvg
import json

DATA=json.loads("[{\"id\":101,\"title\":\"6 DPO: Is It Too Early for Symptoms?\",\"head\":[\"ONLY 6 DPO?\",\"READ THIS\"],\"eyebrow\":\"TWO-WEEK WAIT\",\"bullets\":[\"Six days past ovulation is very early\",\"Most symptoms cannot confirm pregnancy\",\"Wait until the right time to test\"],\"key\":\"6 dpo pregnancy signs\"},{\"id\":102,\"title\":\"12 DPO and a Negative Test?\",\"head\":[\"12 DPO NEGATIVE?\",\"WHAT NOW?\"],\"eyebrow\":\"TESTING QUESTIONS\",\"bullets\":[\"Ovulation estimates are not exact\",\"An early negative may need repeating\",\"Follow your test directions and cycle dates\"],\"key\":\"12 dpo negative test\"},{\"id\":103,\"title\":\"14 DPO: Should You Test Today?\",\"head\":[\"14 DPO?\",\"TEST TODAY?\"],\"eyebrow\":\"TEST TIMING\",\"bullets\":[\"Your expected period date matters\",\"Cycle and ovulation timing can vary\",\"Home test directions come first\"],\"key\":\"14 dpo pregnancy test\"},{\"id\":104,\"title\":\"Period 5 Days Late: First Steps\",\"head\":[\"5 DAYS LATE?\",\"3 NEXT STEPS\"],\"eyebrow\":\"MISSED PERIOD\",\"bullets\":[\"Review your normal cycle length\",\"Consider taking a home pregnancy test\",\"Ask a clinician if uncertainty continues\"],\"key\":\"5 days late period\"},{\"id\":105,\"title\":\"A Week Late and Still Negative?\",\"head\":[\"A WEEK LATE\",\"BUT NEGATIVE?\"],\"eyebrow\":\"LATE PERIOD FAQ\",\"bullets\":[\"Late periods have several possible causes\",\"Repeat the test according to instructions\",\"Seek advice if your period stays absent\"],\"key\":\"one week late negative test\"},{\"id\":106,\"title\":\"Very Light Period: Pregnancy or Not?\",\"head\":[\"LIGHT PERIOD?\",\"COULD IT BE?\"],\"eyebrow\":\"BLEEDING QUESTIONS\",\"bullets\":[\"Flow can vary between cycles\",\"Light bleeding cannot confirm pregnancy\",\"Test if pregnancy is possible\"],\"key\":\"light period pregnant\"},{\"id\":107,\"title\":\"Brown Discharge Before a Period?\",\"head\":[\"BROWN SPOTTING?\",\"WHAT IT MEANS\"],\"eyebrow\":\"CYCLE CLARITY\",\"bullets\":[\"Brown discharge can be older blood\",\"Timing and associated symptoms matter\",\"Get advice about unusual bleeding\"],\"key\":\"brown spotting before period\"},{\"id\":108,\"title\":\"Pink Spotting Before Your Period?\",\"head\":[\"PINK SPOTTING?\",\"WHAT NEXT?\"],\"eyebrow\":\"SPOTTING GUIDE\",\"bullets\":[\"Spotting has several possible causes\",\"Color alone cannot confirm pregnancy\",\"Heavy bleeding or pain needs care\"],\"key\":\"pink spotting pregnancy period\"},{\"id\":109,\"title\":\"Pregnancy Test After Drinking Water?\",\"head\":[\"DID WATER\",\"AFFECT YOUR TEST?\"],\"eyebrow\":\"TEST ACCURACY\",\"bullets\":[\"Very diluted urine may affect early tests\",\"Follow your brand's urine guidance\",\"Retest if the result was uncertain\"],\"key\":\"diluted urine pregnancy test\"},{\"id\":110,\"title\":\"Expired Pregnancy Test: Can You Trust It?\",\"head\":[\"TEST EXPIRED?\",\"CHECK THIS\"],\"eyebrow\":\"HOME TEST BASICS\",\"bullets\":[\"Always check the expiration date\",\"Storage and instructions also matter\",\"Use a valid test for clearer results\"],\"key\":\"expired pregnancy test\"},{\"id\":111,\"title\":\"Reading a Test After 10 Minutes?\",\"head\":[\"CHECKED TOO LATE?\",\"READ THIS\"],\"eyebrow\":\"TEST LINES\",\"bullets\":[\"Results have a specific reading window\",\"Late changes can be misleading\",\"Follow the instructions or retest\"],\"key\":\"pregnancy test after time window\"},{\"id\":112,\"title\":\"Digital vs Strip Pregnancy Tests\",\"head\":[\"DIGITAL OR\",\"TEST STRIP?\"],\"eyebrow\":\"WHICH TEST\",\"bullets\":[\"Both types look for pregnancy hormone\",\"Different brands have different instructions\",\"Timing is more important than guessing\"],\"key\":\"digital vs strip pregnancy test\"},{\"id\":113,\"title\":\"Ovulation Test Positive: Pregnant?\",\"head\":[\"POSITIVE OPK?\",\"PREGNANT?\"],\"eyebrow\":\"TEST COMPARISON\",\"bullets\":[\"Ovulation tests are not pregnancy tests\",\"LH and hCG are different hormones\",\"Use a pregnancy test to check pregnancy\"],\"key\":\"positive ovulation test pregnant\"},{\"id\":114,\"title\":\"When Does hCG Become Detectable?\",\"head\":[\"WHEN DOES\",\"hCG SHOW UP?\"],\"eyebrow\":\"HORMONE TIMELINE\",\"bullets\":[\"Hormone levels rise after implantation\",\"Test sensitivity and timing both matter\",\"Wait for the recommended testing date\"],\"key\":\"hcg detectable pregnancy test\"},{\"id\":115,\"title\":\"What Does 2 Weeks Pregnant Mean?\",\"head\":[\"2 WEEKS\",\"PREGNANT?\"],\"eyebrow\":\"PREGNANCY DATING\",\"bullets\":[\"Pregnancy weeks use the last period date\",\"Conception usually happens later\",\"Dating can be refined by a clinician\"],\"key\":\"two weeks pregnant meaning\"},{\"id\":116,\"title\":\"Is Metallic Taste a Pregnancy Sign?\",\"head\":[\"METALLIC TASTE?\",\"ONE EARLY SIGN?\"],\"eyebrow\":\"SYMPTOM CHECK\",\"bullets\":[\"Taste changes may have many explanations\",\"This symptom does not prove pregnancy\",\"Review timing and use a home test\"],\"key\":\"metallic taste early pregnancy\"},{\"id\":117,\"title\":\"Vivid Dreams: A Pregnancy Symptom?\",\"head\":[\"VIVID DREAMS?\",\"IS IT A SIGN?\"],\"eyebrow\":\"SLEEP AND CYCLE\",\"bullets\":[\"Dream changes have many possible causes\",\"Sleep disruption is not a reliable sign\",\"Testing matters more than one symptom\"],\"key\":\"vivid dreams pregnancy symptom\"},{\"id\":118,\"title\":\"Acne Before a Missed Period?\",\"head\":[\"SUDDEN ACNE?\",\"PMS OR MORE?\"],\"eyebrow\":\"HORMONE QUESTIONS\",\"bullets\":[\"Hormonal changes can affect skin\",\"Breakouts happen outside pregnancy too\",\"One skin change cannot tell you\"],\"key\":\"acne early pregnancy or period\"},{\"id\":119,\"title\":\"Hot Flashes or Pregnancy?\",\"head\":[\"FEELING HOT?\",\"KNOW THE FACTS\"],\"eyebrow\":\"BODY CHANGES\",\"bullets\":[\"Temperature sensations have many causes\",\"Pregnancy is not diagnosed by warmth\",\"Check your cycle and testing timeline\"],\"key\":\"feeling hot early pregnancy\"},{\"id\":120,\"title\":\"Basal Body Temperature Stays High?\",\"head\":[\"TEMP STAYS HIGH?\",\"WHAT IT MEANS\"],\"eyebrow\":\"BBT TRACKING\",\"bullets\":[\"Temperature shifts follow ovulation\",\"Illness and sleep can affect readings\",\"A home test is still needed\"],\"key\":\"basal body temperature pregnancy\"},{\"id\":121,\"title\":\"Short Luteal Phase: What to Know\",\"head\":[\"SHORT LUTEAL\",\"PHASE?\"],\"eyebrow\":\"CYCLE EDUCATION\",\"bullets\":[\"Cycle phases vary between people\",\"Apps estimate rather than diagnose\",\"Discuss persistent concerns with a clinician\"],\"key\":\"short luteal phase\"},{\"id\":122,\"title\":\"Cycles 24 vs 35 Days: Is It Normal?\",\"head\":[\"24-DAY OR\",\"35-DAY CYCLE?\"],\"eyebrow\":\"PERIOD TRACKING\",\"bullets\":[\"Cycle length differs across people\",\"Compare dates over several months\",\"Get care for persistent changes\"],\"key\":\"menstrual cycle length variation\"},{\"id\":123,\"title\":\"Does Exercise Change Period Timing?\",\"head\":[\"MORE EXERCISE?\",\"LATE PERIOD?\"],\"eyebrow\":\"CYCLE HABITS\",\"bullets\":[\"Major activity changes can affect cycles\",\"Other causes of a late period exist\",\"Test if pregnancy is possible\"],\"key\":\"exercise delayed period\"},{\"id\":124,\"title\":\"Period Late After Illness?\",\"head\":[\"SICK LAST WEEK?\",\"PERIOD LATE?\"],\"eyebrow\":\"CYCLE CHANGES\",\"bullets\":[\"Illness and stress may change timing\",\"A late period is not proof of pregnancy\",\"Use a test if pregnancy is possible\"],\"key\":\"illness delayed menstrual period\"},{\"id\":125,\"title\":\"Unprotected Sex: Your Testing Timeline\",\"head\":[\"UNPROTECTED SEX?\",\"WHEN TO TEST\"],\"eyebrow\":\"TEST TIMELINE\",\"bullets\":[\"Testing immediately is too early\",\"Track when exposure occurred\",\"For unclear cycles test about 21 days later\"],\"key\":\"when to test after unprotected sex\"},{\"id\":126,\"title\":\"Can a Short Period Mean Pregnancy?\",\"head\":[\"PERIOD ONLY\",\"2 DAYS?\"],\"eyebrow\":\"LIGHT BLEEDING\",\"bullets\":[\"Shorter bleeding can have many causes\",\"Flow length cannot confirm pregnancy\",\"Test if pregnancy is possible\"],\"key\":\"two day period pregnant\"},{\"id\":127,\"title\":\"Period Symptoms Disappeared Suddenly?\",\"head\":[\"PMS VANISHED?\",\"WHAT NOW?\"],\"eyebrow\":\"SYMPTOM SHIFTS\",\"bullets\":[\"Symptoms change from cycle to cycle\",\"A sudden shift does not prove pregnancy\",\"Focus on test timing rather than guesses\"],\"key\":\"PMS symptoms disappeared pregnancy\"},{\"id\":128,\"title\":\"Bleeding After Sex: What to Know\",\"head\":[\"SPOTTING AFTER\",\"SEX?\"],\"eyebrow\":\"BLEEDING HEALTH\",\"bullets\":[\"Bleeding after sex has several causes\",\"It is not a reliable pregnancy sign\",\"Recurring bleeding deserves medical advice\"],\"key\":\"spotting after sex causes\"},{\"id\":129,\"title\":\"Missed Period With a Regular Cycle?\",\"head\":[\"REGULAR CYCLE\",\"NOW LATE?\"],\"eyebrow\":\"MISSED PERIOD\",\"bullets\":[\"Even regular cycles can vary\",\"A missed period is a reason to test\",\"Seek guidance for ongoing missed periods\"],\"key\":\"regular period suddenly late\"},{\"id\":130,\"title\":\"Free Am I Pregnant Quiz: Start Here\",\"head\":[\"AM I PREGNANT?\",\"TAKE THE QUIZ\"],\"eyebrow\":\"FREE IPHONE QUIZ\",\"bullets\":[\"Explore common signs and cycle questions\",\"Understand when to take a real test\",\"The quiz gives guidance not diagnosis\"],\"key\":\"am i pregnant free quiz iphone\"}]")
ROOT=Path('pregnancy/next-30-oct-2026')
ROOT.mkdir(parents=True,exist_ok=True)
REPO='shsweb/pinterest-pregnancy-pins'
APP='https://apps.apple.com/us/app/am-i-pregnant-pregnancy-quiz/id6769078846'
BOARD='Pregnancy Tips & Early Signs'

palette=[
('#ffe5ec','#a91f64','#3f1937','#fff7f8'),
('#c7efff','#1174ba','#13385a','#f4fcff'),
('#fff0b7','#ad5516','#442a35','#fffaf1'),
('#e7dbff','#7850b8','#32224f','#faf6ff'),
('#ffd7d7','#c1346a','#4c2241','#fff6f8'),
('#d8f9ea','#147c69','#173f46','#f6fffc'),
('#f6e0ff','#8b43a0','#42264e','#fffaff'),
('#ffe2bc','#ba5a3c','#502d39','#fffaf3'),
('#d1ebfb','#5264b7','#252c62','#f6faff'),
('#fad9e8','#af4b77','#493047','#fff9fb'),
]
def esc(s):return html.escape(str(s),quote=False)
def t(x,y,s,size=45,color='#222',weight=800,anchor='start',spacing=0):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="DejaVu Sans" font-weight="{weight}" font-size="{size}" fill="{color}" letter-spacing="{spacing}">{esc(s)}</text>'
def rounded(x,y,w,h,fill,r=30,stroke='none',sw=0,opacity=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>'
def circle(x,y,r,fill,op=1):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" opacity="{op}"/>'
def fmt_head(head,x,y,font=82,gap=99,anchor='start',color='#231e32'):
    return ''.join(t(x,y+i*gap,line,font,color,900,anchor) for i,line in enumerate(head))
def photo(i,geometry,clip='clipphoto'):
    p=Path(f'pin-{(i%10)+1:02d}.png')
    if not p.exists():return ''
    im=Image.open(p).convert('RGB').crop((0,0,448,1500))
    out=BytesIO();im.save(out,format='JPEG',quality=77,optimize=True)
    b=base64.b64encode(out.getvalue()).decode()
    x,y,w,h=geometry
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,{b}" clip-path="url(#{clip})"/>'
def symbols(kind,accent,dark):
    if kind==0:
        return '<g transform="translate(0 0)">'+circle(180,215,105,'#ffffff',.25)+t(180,240,'?',110,accent,900,'middle')+'</g>'
    if kind==1:
        return '<g>'+rounded(645,675,220,250,'#fff',34)+rounded(645,675,220,66,accent,34)+t(753,726,'CALENDAR',20,'#fff',900,'middle')+t(752,825,'12  13',31,dark,800,'middle')+t(753,892,'14  15',31,dark,800,'middle')+'</g>'
    if kind==2:
        return '<g transform="rotate(-20 755 775)">'+rounded(580,723,345,100,'#ffffff',50)+rounded(634,747,123,53,'#ffd7e4',18)+rounded(781,747,37,53,'#e3e1ec',7)+rounded(788,756,7,36,accent,2)+'</g>'
    if kind==3:
        return '<g>'+circle(765,755,135,'#fff',.65)+t(765,785,'?',150,accent,900,'middle')+'</g>'
    if kind==4:
        return '<g>'+circle(760,790,145,'#fff',.63)+t(760,832,'+',140,accent,800,'middle')+'</g>'
    return '<g>'+circle(770,770,160,'#fff',.64)+t(770,813,'✓',144,accent,800,'middle')+'</g>'
def dots(seed,accent):
    rng=random.Random(seed); s=''
    for q in range(24):
        x=rng.randint(40,970); y=rng.randint(80,1380);r=rng.randint(2,9)
        s+=circle(x,y,r,accent,round(rng.uniform(.06,.27),2))
    return s
def bullet_lines(bullets,x,y,w=795,fontsize=38,line_gap=112,dark='#222',accent='#a62672'):
    chunks=[]
    for j,b in enumerate(bullets):
        yy=y+j*line_gap
        chunks.append(circle(x+18, yy-14,19,accent))
        chunks.append(t(x+18,yy-6,'✓',21,'#fff',800,'middle'))
        words=b.split()
        lines=[];line=''
        for word in words:
            if len(line+' '+word)>int(w/(fontsize*.54)):
                lines.append(line);line=word
            else:line=(line+' '+word).strip()
        lines.append(line)
        for k,line in enumerate(lines):
            chunks.append(t(x+51,yy+k*(fontsize+10),line,fontsize,dark,700))
    return ''.join(chunks)
def layout(data, n, colors):
    bg,accent,dark,light=colors
    head=data['head']; bullets=data['bullets']
    mode=n%6
    h1=font_title=76 if max(map(len,head))<18 else 66
    elems=[]
    if mode==0: # Editorial split with lifestyle photo
        elems.append(rounded(0,0,1000,1500,light,0))
        elems.append('<clipPath id="clipphoto"><rect x="0" y="0" width="438" height="1500"/></clipPath>')
        elems.append(photo(n,(0,0,438,1500)))
        elems.append(rounded(439,0,16,1500,accent,0,opacity=.37))
        elems.append(circle(970,350,175,accent,.1))
        elems.append(t(506,160,'THE PREGNANCY EDIT',22,accent,900))
        elems.append(rounded(508,248,360,59,bg,30))
        elems.append(t(530,287,data['eyebrow'][:22],21,accent,900))
        elems.append(fmt_head(head,510,412,63,83,'start',dark))
        elems.append(rounded(510,600,140,9,accent,5))
        elems.append(bullet_lines(bullets,505,760,450,31,140,dark,accent))
    elif mode==1: # Cinematic oversized hero photo panel
        elems.append(rounded(0,0,1000,1500,bg,0))
        elems.append(circle(900,260,290,'#fff',.36))
        elems.append(t(500,143,data['eyebrow'],28,accent,900,'middle',2))
        elems.append(fmt_head(head,500,260,85,103,'middle',dark))
        elems.append('<clipPath id="clipphoto"><rect x="95" y="500" width="810" height="530" rx="55"/></clipPath>')
        elems.append(photo(n,(95,500,810,530)))
        elems.append(rounded(75,1010,850,280,light,36))
        elems.append(bullet_lines(bullets,125,1080,735,29,72,dark,accent))
    elif mode==2: # Bold card + illustration and editorial bullets
        elems.append(rounded(0,0,1000,1500,bg,0))
        elems.append(circle(830,780,310,accent,.11))
        elems.append(circle(120,1100,300,'#fff',.25))
        elems.append(rounded(65,66,490,69,accent,34))
        elems.append(t(310,112,data['eyebrow'],25,'#fff',900,'middle'))
        elems.append(fmt_head(head,65,268,90,108,'start',dark))
        elems.append(symbols(n%6,accent,dark))
        elems.append(rounded(61,1000,876,310,light,43))
        elems.append(bullet_lines(bullets,105,1080,750,30,77,dark,accent))
    elif mode==3: # Double comparison cards / note panels
        elems.append(rounded(0,0,1000,1500,dark,0))
        elems.append(circle(105,600,325,accent,.29));elems.append(circle(930,920,420,accent,.21))
        elems.append(t(500,141,data['eyebrow'],27,bg,900,'middle',2))
        elems.append(fmt_head(head,500,284,86,103,'middle','#fff'))
        elems.append(rounded(52,535,431,615,light,46))
        elems.append(rounded(517,535,431,615,bg,46))
        elems.append(rounded(88,577,342,56,accent,26))
        elems.append(t(258,616,'WHAT TO NOTICE',24,'#fff',900,'middle'))
        elems.append(rounded(552,577,342,56,accent,26))
        elems.append(t(723,616,'NEXT STEP',25,'#fff',900,'middle'))
        for q,b in enumerate(bullets[:2]):
            lines=textwrap.wrap(b,width=19)
            yy=735+q*188
            elems.append(circle(131,yy-13,11,accent))
            for m,line in enumerate(lines):elems.append(t(161,yy+m*43,line,31,dark,700))
        for q,line in enumerate(textwrap.wrap(bullets[2],width=18)):
            elems.append(t(560,755+q*48,line,35,dark,800))
        elems.append(circle(730,985,62,accent,.18))
        elems.append(t(730,1010,'✓',68,accent,800,'middle'))
        elems.append(t(500,1222,'Your cycle and symptoms are only part of the story',23,'#f4daed',600,'middle'))
    elif mode==4: # Tall photo right and left headline + cards
        elems.append(rounded(0,0,1000,1500,light,0))
        elems.append(circle(870,320,270,bg,.6))
        elems.append('<clipPath id="clipphoto"><rect x="525" y="178" width="435" height="750" rx="100"/></clipPath>')
        elems.append(photo(n,(525,178,435,750)))
        elems.append(rounded(55,74,445,64,bg,31))
        elems.append(t(275,114,data['eyebrow'][:23],24,accent,900,'middle'))
        elems.append(fmt_head(head,65,310,72,106,'start',dark))
        for j,b in enumerate(bullets):
            yy=915+j*120
            elems.append(rounded(70,yy,852,100,bg,27))
            elems.append(circle(123,yy+50,26,accent))
            elems.append(t(123,yy+59,str(j+1),25,'#fff',900,'middle'))
            elems.append(t(175,yy+62,b[:41],28,dark,800))
    else: # Strong large step typographic poster
        elems.append(rounded(0,0,1000,1500,bg,0))
        elems.append(circle(900,90,300,'#fff',.34))
        elems.append(circle(80,1140,290,accent,.08))
        elems.append(rounded(60,70,610,69,dark,33))
        elems.append(t(365,116,data['eyebrow'],26,'#fff',900,'middle'))
        elems.append(fmt_head(head,66,267,90,112,'start',dark))
        elems.append(symbols(n%6,accent,dark))
        for j,b in enumerate(bullets):
            yy=940+j*122
            elems.append(rounded(60,yy,879,96,light,22,stroke=accent,sw=2))
            elems.append(circle(114,yy+48,28,accent))
            elems.append(t(114,yy+58,str(j+1),31,'#fff',900,'middle'))
            elems.append(t(160,yy+61,b[:43],28,dark,800))
    # CTA and branding draw over each design for consistency.
    elems.append(rounded(68,1360,864,103,dark if mode!=3 else '#fff',51))
    elems.append(t(500,1427,'TAKE THE FREE PREGNANCY QUIZ   →',37,'#fff' if mode!=3 else dark,900,'middle'))
    if mode not in (0,3):elems.append(t(500,1334,'QUIZ = INFORMATION ONLY  ·  USE A TEST TO CONFIRM',18,dark,600,'middle'))
    if mode==0:elems.append(t(515,1338,'A quiz cannot confirm pregnancy.',20,dark,600))
    if mode==3:elems.append(t(500,1338,'A quiz cannot confirm pregnancy.',18,'#fff',600,'middle'))
    elems.append(t(500,53,'AM I PREGNANT?  ·  IPHONE APP',19,dark if mode not in (3,) else '#fff',900,'middle',1))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1500" viewBox="0 0 1000 1500">
    <defs><linearGradient id="g" x2="1" y2="1"><stop stop-color="{light}"/><stop offset="1" stop-color="{bg}"/></linearGradient></defs>
    {''.join(elems)}</svg>"""
fields=['Title','Media URL','Pinterest board','Thumbnail','Description','Link','Publish date','Keywords']
rows=[]
for i,d in enumerate(DATA):
    ident=d['id']; n=i+2
    svg=layout(d,n,palette[(i*3+1)%len(palette)])
    dest=ROOT/f'pregnancy-pin-{ident:02}.png'
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(dest))
    desc=(f"{d['title']}. {'. '.join(d['bullets'])}. "
          f"Explore the Am I Pregnant? Pregnancy Quiz app to understand possible signs and plan your next steps. "
          f"This quiz is informational and cannot diagnose pregnancy; confirm with a test or clinician. "
          f"#AmIPregnant #PregnancyQuiz #PregnancySymptoms")
    rows.append({'Title':d['title'],'Media URL':f"https://raw.githubusercontent.com/{REPO}/main/pregnancy/next-30-oct-2026/pregnancy-pin-{ident:02}.png",
         'Pinterest board':BOARD,'Thumbnail':'','Description':desc[:497],
         'Link':f"{APP}?utm_content=pinterest_pin_{ident:02}",'Publish date':'','Keywords':d['key']+', pregnancy quiz, pregnancy symptoms'})
    print('generated',dest)
with open('pinterest_30_new_pins_101_130.csv','w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
print('COMPLETE',len(rows),'ADDITIONAL PIN DESIGNS AND CSV')
