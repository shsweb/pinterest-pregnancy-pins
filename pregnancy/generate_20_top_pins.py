from pathlib import Path
import os, random, csv, math, base64, html, textwrap
from PIL import Image
from io import BytesIO
import cairosvg
import json

DATA=json.loads("[{\"id\":81,\"title\":\"10 DPO and Wondering If You're Pregnant?\",\"head\":[\"10 DPO?\",\"TOO SOON?\"],\"eyebrow\":\"TWO-WEEK WAIT\",\"bullets\":[\"Symptoms at 10 DPO are not proof\",\"An early negative may be inconclusive\",\"Testing after a missed period is more reliable\"],\"key\":\"10 DPO pregnancy symptoms\"},{\"id\":82,\"title\":\"Period Due Tomorrow: Test or Wait?\",\"head\":[\"PERIOD DUE\",\"TOMORROW?\"],\"eyebrow\":\"TEST OR WAIT\",\"bullets\":[\"Tests vary in early sensitivity\",\"Testing before a missed period can miss pregnancy\",\"Use the instructions for your test\"],\"key\":\"test before expected period\"},{\"id\":83,\"title\":\"How Soon After Sex Can You Test?\",\"head\":[\"HOW SOON\",\"CAN YOU TEST?\"],\"eyebrow\":\"TEST TIMING\",\"bullets\":[\"Testing straight after sex is too early\",\"Timing depends on when pregnancy hormone rises\",\"If cycles are unclear test about 21 days later\"],\"key\":\"how soon after sex pregnancy test\"},{\"id\":84,\"title\":\"Can You Get Pregnant During Your Period?\",\"head\":[\"PREGNANT\",\"ON YOUR PERIOD?\"],\"eyebrow\":\"FERTILITY FACTS\",\"bullets\":[\"Pregnancy is possible during period sex\",\"Cycles and ovulation dates can vary\",\"A period tracker is not contraception\"],\"key\":\"pregnant during period\"},{\"id\":85,\"title\":\"What Does an Invalid Pregnancy Test Mean?\",\"head\":[\"INVALID\",\"TEST RESULT?\"],\"eyebrow\":\"CONTROL LINE GUIDE\",\"bullets\":[\"A missing control line means the test is invalid\",\"Follow your test instructions carefully\",\"Use a new test if necessary\"],\"key\":\"invalid pregnancy test no control line\"},{\"id\":86,\"title\":\"Discharge Before Period: What Changes?\",\"head\":[\"DISCHARGE\",\"BEFORE PERIOD?\"],\"eyebrow\":\"CYCLE BASICS\",\"bullets\":[\"Discharge varies during your cycle\",\"Its appearance alone cannot diagnose pregnancy\",\"Unusual odor or pain deserves medical advice\"],\"key\":\"white discharge before period\"},{\"id\":87,\"title\":\"Can You Be Pregnant While Breastfeeding?\",\"head\":[\"BREASTFEEDING\",\"AND PREGNANT?\"],\"eyebrow\":\"POSTPARTUM CYCLES\",\"bullets\":[\"Ovulation can return before a first period\",\"Breastfeeding is not always contraception\",\"Test if pregnancy is possible\"],\"key\":\"pregnant while breastfeeding\"},{\"id\":88,\"title\":\"Late Period After Emergency Contraception?\",\"head\":[\"PERIOD LATE\",\"AFTER PLAN B?\"],\"eyebrow\":\"CYCLE CHANGES\",\"bullets\":[\"Emergency contraception can shift timing\",\"Bleeding patterns may change temporarily\",\"Test if your period is significantly late\"],\"key\":\"late period after emergency contraception\"},{\"id\":89,\"title\":\"Can You Be Pregnant on the Pill?\",\"head\":[\"ON THE PILL\",\"BUT UNSURE?\"],\"eyebrow\":\"CONTRACEPTION FAQ\",\"bullets\":[\"No contraceptive method is 100% effective\",\"Missed pills and interactions can matter\",\"Check your leaflet and test if concerned\"],\"key\":\"pregnancy on birth control pill\"},{\"id\":90,\"title\":\"Implantation Spotting or Period?\",\"head\":[\"SPOTTING OR\",\"PERIOD?\"],\"eyebrow\":\"KNOW THE DIFFERENCE\",\"bullets\":[\"Color alone cannot tell you the cause\",\"Bleeding can have several explanations\",\"Heavy bleeding or severe pain needs care\"],\"key\":\"implantation bleeding vs period\"},{\"id\":91,\"title\":\"Ovulation Pain vs Early Pregnancy Signs\",\"head\":[\"OVULATION OR\",\"PREGNANCY?\"],\"eyebrow\":\"BODY SIGNALS\",\"bullets\":[\"Twinges can happen around ovulation\",\"Cramps are not a reliable pregnancy sign\",\"Review cycle timing and test when due\"],\"key\":\"ovulation pain pregnancy cramps\"},{\"id\":92,\"title\":\"Nausea Before a Missed Period?\",\"head\":[\"NAUSEA BEFORE\",\"YOUR PERIOD?\"],\"eyebrow\":\"SYMPTOM CLARITY\",\"bullets\":[\"Nausea can happen for many reasons\",\"An isolated symptom proves nothing\",\"Check your period timing before testing\"],\"key\":\"nausea before missed period\"},{\"id\":93,\"title\":\"Positive Pregnancy Test: What's Next?\",\"head\":[\"POSITIVE TEST?\",\"3 NEXT STEPS\"],\"eyebrow\":\"NEXT STEPS\",\"bullets\":[\"Read the test directions to confirm the result\",\"Arrange appropriate prenatal care\",\"Ask a clinician about any concerns\"],\"key\":\"what to do after positive pregnancy test\"},{\"id\":94,\"title\":\"Stopped Birth Control, Period Is Late?\",\"head\":[\"STOPPED THE PILL?\",\"PERIOD LATE?\"],\"eyebrow\":\"CYCLE RESET\",\"bullets\":[\"Periods can take time to settle\",\"Pregnancy can occur before cycles feel regular\",\"Take a test if there was a chance of pregnancy\"],\"key\":\"late period after stopping pill\"},{\"id\":95,\"title\":\"Can You Be Pregnant Without Nausea?\",\"head\":[\"NO NAUSEA?\",\"STILL PREGNANT?\"],\"eyebrow\":\"MYTH OR FACT\",\"bullets\":[\"Not everyone gets morning sickness\",\"Early symptoms differ widely\",\"Absence of nausea cannot rule out pregnancy\"],\"key\":\"pregnant without morning sickness\"},{\"id\":96,\"title\":\"Pregnancy Symptoms Come and Go?\",\"head\":[\"SYMPTOMS COME\",\"AND GO?\"],\"eyebrow\":\"BODY CHANGES\",\"bullets\":[\"Symptoms can change from day to day\",\"PMS and pregnancy signs can overlap\",\"A home test is more useful than guessing\"],\"key\":\"pregnancy symptoms come and go\"},{\"id\":97,\"title\":\"Could Pre-Ejaculate Cause Pregnancy?\",\"head\":[\"CAN PRE-CUM\",\"CAUSE PREGNANCY?\"],\"eyebrow\":\"FERTILITY FAQ\",\"bullets\":[\"Pregnancy is possible from pre-ejaculate\",\"Withdrawal is not a reliable contraceptive\",\"Seek timely advice if pregnancy is unwanted\"],\"key\":\"pregnancy from precum\"},{\"id\":98,\"title\":\"How Are Pregnancy Weeks Counted?\",\"head\":[\"PREGNANCY\",\"WEEKS EXPLAINED\"],\"eyebrow\":\"DATE BASICS\",\"bullets\":[\"Dating usually starts from the last period\",\"Ovulation commonly occurs later\",\"A clinician can refine your due date\"],\"key\":\"pregnancy weeks counted\"},{\"id\":99,\"title\":\"Does a Blood Test Detect Pregnancy Earlier?\",\"head\":[\"BLOOD TEST VS\",\"HOME TEST?\"],\"eyebrow\":\"KNOW YOUR TESTS\",\"bullets\":[\"Blood and urine tests both detect hCG\",\"Blood tests may detect pregnancy earlier\",\"A clinician can advise which is appropriate\"],\"key\":\"blood versus urine pregnancy test\"},{\"id\":100,\"title\":\"No Period After Breastfeeding Changes?\",\"head\":[\"NO PERIOD\",\"AFTER WEANING?\"],\"eyebrow\":\"POSTPARTUM FACTS\",\"bullets\":[\"Cycles may return at different times\",\"Ovulation can happen before bleeding returns\",\"Testing helps if pregnancy is possible\"],\"key\":\"missed period after weaning\"}]")
ROOT=Path('pregnancy/top-20-oct-2026')
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
    ident=d['id']; n=i+5
    svg=layout(d,n,palette[(i*7+6)%len(palette)])
    dest=ROOT/f'pregnancy-pin-{ident:02}.png'
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(dest))
    desc=(f"{d['title']}. {'. '.join(d['bullets'])}. "
          f"Explore the Am I Pregnant? Pregnancy Quiz app to understand possible signs and plan your next steps. "
          f"A quiz cannot diagnose pregnancy; confirm with a home pregnancy test or clinician. "
          f"#AmIPregnant #PregnancyQuiz #PregnancySymptoms")
    rows.append({'Title':d['title'],'Media URL':f"https://raw.githubusercontent.com/{REPO}/main/pregnancy/top-20-oct-2026/pregnancy-pin-{ident:02}.png",
         'Pinterest board':BOARD,'Thumbnail':'','Description':desc[:497],
         'Link':f"{APP}?utm_content=pinterest_pin_{ident:02}",'Publish date':'','Keywords':d['key']+', pregnancy quiz, pregnancy symptoms'})
    print('generated',dest)
with open('pinterest_20_top_pins.csv','w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
print('COMPLETE',len(rows),'ADDITIONAL PIN DESIGNS AND CSV')
