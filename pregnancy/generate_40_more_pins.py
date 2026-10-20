from pathlib import Path
import os, random, csv, math, base64, html, textwrap
from PIL import Image
from io import BytesIO
import cairosvg
import json

DATA=json.loads("[{\"id\":41,\"title\":\"Why Is My Period 3 Days Late?\",\"head\":[\"3 DAYS LATE?\",\"WHAT NOW?\"],\"eyebrow\":\"LATE PERIOD GUIDE\",\"bullets\":[\"Cycles can naturally shift by a few days\",\"Stress and illness can change timing\",\"Test if pregnancy is possible\"],\"key\":\"period three days late\"},{\"id\":42,\"title\":\"Cramps but No Period: What to Check\",\"head\":[\"CRAMPS BUT\",\"NO PERIOD?\"],\"eyebrow\":\"SYMPTOM CLUES\",\"bullets\":[\"Cramps can have several causes\",\"Check where you are in your cycle\",\"A test may help if your period is late\"],\"key\":\"cramps without period\"},{\"id\":43,\"title\":\"Pregnancy Test at Night: Does It Work?\",\"head\":[\"TESTING AT\",\"NIGHT?\"],\"eyebrow\":\"TESTING FACTS\",\"bullets\":[\"Read your test's instructions first\",\"Early testing may need concentrated urine\",\"Retest if the result is unclear\"],\"key\":\"pregnancy test at night\"},{\"id\":44,\"title\":\"Can Stress Really Delay a Period?\",\"head\":[\"STRESSED AND\",\"PERIOD LATE?\"],\"eyebrow\":\"CYCLE MYTHS\",\"bullets\":[\"Stress can affect menstrual timing\",\"Cycle changes have other causes too\",\"Take a test if pregnancy is possible\"],\"key\":\"stress late period\"},{\"id\":45,\"title\":\"Late Ovulation, Late Period?\",\"head\":[\"OVULATED LATE?\",\"READ THIS\"],\"eyebrow\":\"CYCLE TIMING\",\"bullets\":[\"Ovulation dates can vary by cycle\",\"Period predictions are only estimates\",\"Testing is better than guessing\"],\"key\":\"late ovulation period\"},{\"id\":46,\"title\":\"Faint Pregnancy Test Line?\",\"head\":[\"FAINT LINE?\",\"NEXT STEPS\"],\"eyebrow\":\"TEST RESULT GUIDE\",\"bullets\":[\"Read within the instructed time window\",\"Follow the manufacturer's directions\",\"Retest or ask a clinician if unsure\"],\"key\":\"faint pregnancy test\"},{\"id\":47,\"title\":\"Only One Day Late: Should You Test?\",\"head\":[\"JUST ONE\",\"DAY LATE?\"],\"eyebrow\":\"PERIOD TIMING\",\"bullets\":[\"One day can fall within normal variation\",\"Testing after a missed period is best\",\"An early negative may need repeating\"],\"key\":\"one day late period\"},{\"id\":48,\"title\":\"Missed a Birth Control Pill?\",\"head\":[\"MISSED A PILL?\",\"WHAT NEXT?\"],\"eyebrow\":\"CONTRACEPTION FAQ\",\"bullets\":[\"Advice depends on pill type and timing\",\"Follow your pill leaflet promptly\",\"Ask a pharmacist about next steps\"],\"key\":\"missed birth control pill\"},{\"id\":49,\"title\":\"Irregular Periods: When to Test\",\"head\":[\"IRREGULAR\",\"CYCLES?\"],\"eyebrow\":\"TESTING TIPS\",\"bullets\":[\"Expected period dates may be unclear\",\"Note possible pregnancy exposure timing\",\"Ask a clinician if uncertainty persists\"],\"key\":\"irregular cycles pregnancy test\"},{\"id\":50,\"title\":\"How Soon Can Symptoms Start?\",\"head\":[\"HOW SOON DO\",\"SIGNS BEGIN?\"],\"eyebrow\":\"EARLY SYMPTOMS\",\"bullets\":[\"Symptoms vary between people\",\"Many signs overlap with PMS\",\"Only testing helps confirm pregnancy\"],\"key\":\"how soon pregnancy symptoms\"},{\"id\":51,\"title\":\"Early Negative Test: What It Means\",\"head\":[\"NEGATIVE\",\"TOO EARLY?\"],\"eyebrow\":\"TESTING CLARITY\",\"bullets\":[\"Very early tests can miss a pregnancy\",\"Follow the test's timing guidance\",\"Retest if your period does not start\"],\"key\":\"negative early pregnancy test\"},{\"id\":52,\"title\":\"Period Symptoms or Something Else?\",\"head\":[\"PERIOD SIGNS\",\"OR NOT?\"],\"eyebrow\":\"PMS EXPLAINED\",\"bullets\":[\"Cramps and bloating are not specific\",\"Cycle symptoms can change month to month\",\"Take a test when pregnancy is possible\"],\"key\":\"PMS signs late period\"},{\"id\":53,\"title\":\"What Is hCG? Pregnancy Test Basics\",\"head\":[\"WHAT IS\",\"hCG?\"],\"eyebrow\":\"TEST SCIENCE\",\"bullets\":[\"Home tests look for pregnancy hormone\",\"Timing affects detection\",\"Follow instructions for reliable results\"],\"key\":\"hCG pregnancy hormone\"},{\"id\":54,\"title\":\"Read a Pregnancy Test Correctly\",\"head\":[\"READ YOUR\",\"TEST RIGHT\"],\"eyebrow\":\"HOME TEST 101\",\"bullets\":[\"Check the expiration date\",\"Use the instructed reading window\",\"Understand the control indicator\"],\"key\":\"how to read pregnancy test\"},{\"id\":55,\"title\":\"Two Tests Show Different Results?\",\"head\":[\"TWO TESTS\",\"DISAGREE?\"],\"eyebrow\":\"RESULTS EXPLAINED\",\"bullets\":[\"Testing timing can affect outcomes\",\"Different brands have different sensitivity\",\"Retest or speak to a clinician\"],\"key\":\"conflicting pregnancy tests\"},{\"id\":56,\"title\":\"Late Period After Traveling?\",\"head\":[\"TRAVELED AND\",\"LATE?\"],\"eyebrow\":\"CYCLE CHANGES\",\"bullets\":[\"Routine changes may influence cycles\",\"Not every late period is pregnancy\",\"Use a test if pregnancy is possible\"],\"key\":\"period late after travel\"},{\"id\":57,\"title\":\"Spotting Between Periods: Basics\",\"head\":[\"SPOTTING\",\"BETWEEN CYCLES?\"],\"eyebrow\":\"KNOW YOUR BODY\",\"bullets\":[\"Spotting has many possible causes\",\"Notice the timing and amount\",\"Seek medical advice for unusual bleeding\"],\"key\":\"spotting between periods\"},{\"id\":58,\"title\":\"When Should You Repeat a Test?\",\"head\":[\"SHOULD YOU\",\"RETEST?\"],\"eyebrow\":\"TESTING TIMELINE\",\"bullets\":[\"Testing early can create uncertainty\",\"Follow the retesting instructions\",\"Get medical advice if results stay unclear\"],\"key\":\"when to repeat pregnancy test\"},{\"id\":59,\"title\":\"Pregnancy Quiz: What Can It Tell You?\",\"head\":[\"WHAT CAN A\",\"QUIZ TELL YOU?\"],\"eyebrow\":\"QUIZ VS TEST\",\"bullets\":[\"Explore common symptoms and timing\",\"Organize questions before testing\",\"A quiz cannot diagnose pregnancy\"],\"key\":\"online pregnancy quiz\"},{\"id\":60,\"title\":\"3 Things to Track Before Testing\",\"head\":[\"BEFORE YOU\",\"TAKE A TEST\"],\"eyebrow\":\"3 THINGS TO NOTE\",\"bullets\":[\"First day of your last period\",\"When your next period was expected\",\"When you took or plan a test\"],\"key\":\"what to track before pregnancy test\"},{\"id\":61,\"title\":\"Feeling Lightheaded? Possible Causes\",\"head\":[\"DIZZY OR\",\"LIGHTHEADED?\"],\"eyebrow\":\"BODY SIGNALS\",\"bullets\":[\"Many things can cause lightheadedness\",\"This symptom cannot confirm pregnancy\",\"Seek help for severe or persistent symptoms\"],\"key\":\"dizziness early pregnancy\"},{\"id\":62,\"title\":\"Breast Changes Before a Missed Period\",\"head\":[\"BREASTS FEEL\",\"DIFFERENT?\"],\"eyebrow\":\"SYMPTOM CHECK\",\"bullets\":[\"Tenderness can occur with PMS\",\"Changes can vary across cycles\",\"Use a test if you miss your period\"],\"key\":\"breast changes early pregnancy\"},{\"id\":63,\"title\":\"Smells Suddenly Seem Stronger?\",\"head\":[\"EVERY SMELL\",\"FEELS STRONG?\"],\"eyebrow\":\"SENSORY CHANGES\",\"bullets\":[\"Smell sensitivity has various causes\",\"Some people notice it in pregnancy\",\"A home test offers more clarity\"],\"key\":\"sense of smell pregnancy\"},{\"id\":64,\"title\":\"Constipation: PMS or Pregnancy?\",\"head\":[\"CONSTIPATED?\",\"COULD IT BE?\"],\"eyebrow\":\"DIGESTIVE SYMPTOMS\",\"bullets\":[\"Digestion can change for many reasons\",\"One symptom cannot identify pregnancy\",\"Review timing and test if needed\"],\"key\":\"constipation pregnancy sign\"},{\"id\":65,\"title\":\"Lower Back Ache: Is It a Sign?\",\"head\":[\"BACK ACHES?\",\"KNOW THE FACTS\"],\"eyebrow\":\"EARLY SIGNS\",\"bullets\":[\"Back discomfort has many causes\",\"It is not a reliable early sign alone\",\"Consider testing if your period is late\"],\"key\":\"back pain pregnancy symptoms\"},{\"id\":66,\"title\":\"Frequent Urination: What to Know\",\"head\":[\"PEEING MORE\",\"THAN USUAL?\"],\"eyebrow\":\"SYMPTOM GUIDE\",\"bullets\":[\"Urinary changes have different causes\",\"Burning or fever needs medical advice\",\"Only a pregnancy test can confirm\"],\"key\":\"frequent urination pregnancy\"},{\"id\":67,\"title\":\"Should You Test Before a Missed Period?\",\"head\":[\"TEST BEFORE\",\"YOUR PERIOD?\"],\"eyebrow\":\"EARLY TESTING\",\"bullets\":[\"Very early testing may miss pregnancy\",\"Check your brand's directions\",\"Retest after a missed period if needed\"],\"key\":\"testing before missed period\"},{\"id\":68,\"title\":\"Bleeding vs a Period: Why It Matters\",\"head\":[\"BLEEDING OR\",\"A PERIOD?\"],\"eyebrow\":\"CYCLE QUESTIONS\",\"bullets\":[\"Bleeding patterns can vary\",\"Bleeding alone cannot determine pregnancy\",\"Seek care for heavy bleeding or pain\"],\"key\":\"bleeding early pregnancy or period\"},{\"id\":69,\"title\":\"No Morning Sickness: Is That Normal?\",\"head\":[\"NO NAUSEA?\",\"STILL POSSIBLE?\"],\"eyebrow\":\"SYMPTOM FACTS\",\"bullets\":[\"Not everyone has morning sickness\",\"Symptoms differ from person to person\",\"Absence of nausea proves nothing\"],\"key\":\"no morning sickness early pregnancy\"},{\"id\":70,\"title\":\"PMS Feels Different This Month?\",\"head\":[\"PMS FEELS\",\"DIFFERENT?\"],\"eyebrow\":\"CYCLE CHANGES\",\"bullets\":[\"Cycle symptoms can naturally shift\",\"Stress and sleep can play a role\",\"A test is better than symptom guessing\"],\"key\":\"PMS different than usual\"},{\"id\":71,\"title\":\"Late Period but No Symptoms?\",\"head\":[\"LATE PERIOD\",\"NO SIGNS?\"],\"eyebrow\":\"MISSED PERIOD\",\"bullets\":[\"Some people notice no early symptoms\",\"A late period can have many causes\",\"Testing provides clearer information\"],\"key\":\"late period no symptoms\"},{\"id\":72,\"title\":\"An Early Negative: How Long to Wait?\",\"head\":[\"NEGATIVE NOW?\",\"WHAT NEXT?\"],\"eyebrow\":\"RETEST PLANNING\",\"bullets\":[\"Always follow your test leaflet\",\"An early test may need repeating\",\"Speak to a clinician if you remain unsure\"],\"key\":\"retest after early negative\"},{\"id\":73,\"title\":\"Does Morning Urine Really Matter?\",\"head\":[\"MORNING URINE\",\"MATTERS?\"],\"eyebrow\":\"PREGNANCY TESTS\",\"bullets\":[\"Concentrated urine may help very early\",\"Some tests work at any time of day\",\"Your test instructions come first\"],\"key\":\"first morning urine pregnancy test\"},{\"id\":74,\"title\":\"What Pregnancy Tests Cannot Tell You\",\"head\":[\"A TEST CAN'T\",\"TELL YOU THIS\"],\"eyebrow\":\"TESTING FACTS\",\"bullets\":[\"A test does not date a pregnancy\",\"Symptoms still need clinical assessment\",\"Contact a clinician about concerns\"],\"key\":\"what pregnancy tests cannot tell\"},{\"id\":75,\"title\":\"Can Period Apps Predict Pregnancy?\",\"head\":[\"CAN AN APP\",\"PREDICT IT?\"],\"eyebrow\":\"CYCLE TRACKING\",\"bullets\":[\"Cycle apps estimate fertile timing\",\"Predictions can be inaccurate\",\"Only a test confirms pregnancy\"],\"key\":\"period tracking app accuracy\"},{\"id\":76,\"title\":\"Not Ready to Test? Save This Checklist\",\"head\":[\"NOT READY\",\"TO TEST?\"],\"eyebrow\":\"SAVE FOR LATER\",\"bullets\":[\"Note your expected period date\",\"Read when your test recommends testing\",\"Give yourself a practical next step\"],\"key\":\"before pregnancy test checklist\"},{\"id\":77,\"title\":\"5 Questions About a Late Period\",\"head\":[\"LATE PERIOD?\",\"5 QUESTIONS\"],\"eyebrow\":\"QUICK SELF CHECK\",\"bullets\":[\"When did your last cycle begin?\",\"Has your routine changed recently?\",\"Is it time for a home test?\"],\"key\":\"late period questions\"},{\"id\":78,\"title\":\"Pregnancy Test Symbols, Explained\",\"head\":[\"WHAT DOES\",\"THIS SYMBOL MEAN?\"],\"eyebrow\":\"TEST LABELS\",\"bullets\":[\"Check the expiration information\",\"Locate the result and control sections\",\"Use the manufacturer's guide\"],\"key\":\"pregnancy test control symbols\"},{\"id\":79,\"title\":\"Is Your Period Actually Late?\",\"head\":[\"IS IT REALLY\",\"LATE?\"],\"eyebrow\":\"CYCLE MATH\",\"bullets\":[\"Compare with your typical cycle length\",\"Allow for normal monthly variation\",\"Test if pregnancy is possible\"],\"key\":\"am I late period tracker\"},{\"id\":80,\"title\":\"Might Be Pregnant? A Calm 3-Step Plan\",\"head\":[\"MIGHT BE\",\"PREGNANT?\"],\"eyebrow\":\"3 NEXT STEPS\",\"bullets\":[\"Check your cycle dates\",\"Take a pregnancy test at the right time\",\"Seek advice if you need support\"],\"key\":\"what to do if pregnant possible\"}]")
ROOT=Path('pregnancy/new-40')
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
    ident=d['id']; n=i+3
    svg=layout(d,n,palette[(i*9+4)%len(palette)])
    dest=ROOT/f'pregnancy-pin-{ident:02}.png'
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(dest))
    desc=(f"{d['title']}. {'. '.join(d['bullets'])}. "
          f"Explore the Am I Pregnant? Pregnancy Quiz app to understand possible signs and plan your next steps. "
          f"A quiz cannot diagnose pregnancy; confirm with a home pregnancy test or clinician. "
          f"#AmIPregnant #PregnancyQuiz #PregnancySymptoms")
    rows.append({'Title':d['title'],'Media URL':f"https://raw.githubusercontent.com/{REPO}/main/pregnancy/new-40/pregnancy-pin-{ident:02}.png",
         'Pinterest board':BOARD,'Thumbnail':'','Description':desc[:497],
         'Link':f"{APP}?utm_content=pinterest_pin_{ident:02}",'Publish date':'','Keywords':d['key']+', pregnancy quiz, pregnancy symptoms'})
    print('generated',dest)
with open('pinterest_40_more_pins.csv','w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
print('COMPLETE',len(rows),'ADDITIONAL PIN DESIGNS AND CSV')
