from pathlib import Path
import os, random, csv, math, base64, html, textwrap
from PIL import Image
from io import BytesIO
import cairosvg
import json

DATA=json.loads("[{\"id\":131,\"title\":\"Only 5 DPO? Here's Why Waiting Matters\",\"head\":[\"5 DPO?\",\"TOO EARLY?\"],\"eyebrow\":\"THE TWO-WEEK WAIT\",\"bullets\":[\"Five days past ovulation is very early\",\"Symptoms cannot confirm pregnancy\",\"Wait until the advised testing time\"],\"key\":\"5 dpo symptoms\"},{\"id\":132,\"title\":\"7 DPO and Noticing Changes?\",\"head\":[\"7 DPO\",\"FEELING DIFFERENT?\"],\"eyebrow\":\"EARLY SYMPTOMS\",\"bullets\":[\"Body changes can have many causes\",\"Seven DPO can be too early to test\",\"Use a real pregnancy test when due\"],\"key\":\"7 dpo pregnancy symptoms\"},{\"id\":133,\"title\":\"8 DPO: Can a Test Work Yet?\",\"head\":[\"8 DPO\",\"TEST OR WAIT?\"],\"eyebrow\":\"TEST TIMING\",\"bullets\":[\"Ovulation dates are often estimates\",\"An early negative may not be final\",\"Follow your test's timing instructions\"],\"key\":\"8 dpo pregnancy test\"},{\"id\":134,\"title\":\"9 DPO: The Waiting Game\",\"head\":[\"9 DPO\",\"WHAT NOW?\"],\"eyebrow\":\"TWO-WEEK WAIT\",\"bullets\":[\"It is easy to overread symptoms\",\"Period dates and ovulation can shift\",\"Plan a reliable day to test\"],\"key\":\"9 dpo symptoms\"},{\"id\":135,\"title\":\"11 DPO: What Does a Negative Mean?\",\"head\":[\"11 DPO\",\"NEGATIVE?\"],\"eyebrow\":\"TEST RESULTS\",\"bullets\":[\"An early negative is not always conclusive\",\"Results depend on timing and test use\",\"Retest if your period is missed\"],\"key\":\"11 dpo negative pregnancy test\"},{\"id\":136,\"title\":\"13 DPO: Your Period Is Almost Due\",\"head\":[\"13 DPO\",\"PERIOD DUE?\"],\"eyebrow\":\"PERIOD COUNTDOWN\",\"bullets\":[\"Hormones and symptoms can overlap\",\"A home test can help with clarity\",\"Check the result in the correct window\"],\"key\":\"13 dpo testing\"},{\"id\":137,\"title\":\"16 DPO With No Period?\",\"head\":[\"16 DPO\",\"NO PERIOD?\"],\"eyebrow\":\"LATE PERIOD CLUES\",\"bullets\":[\"Ovulation may have happened later\",\"A missed period is a reason to test\",\"Talk to a clinician if you're unsure\"],\"key\":\"16 dpo no period\"},{\"id\":138,\"title\":\"Period Started Earlier Than Expected?\",\"head\":[\"PERIOD EARLY?\",\"HERE'S WHY\"],\"eyebrow\":\"CYCLE CHANGES\",\"bullets\":[\"Cycle length can shift month to month\",\"Bleeding alone cannot confirm pregnancy\",\"Get advice if changes keep happening\"],\"key\":\"period early pregnancy question\"},{\"id\":139,\"title\":\"Period Arrived Then Stopped?\",\"head\":[\"PERIOD STOPPED\",\"SO FAST?\"],\"eyebrow\":\"SHORT PERIOD\",\"bullets\":[\"Light or short bleeding has many causes\",\"Flow length alone does not diagnose pregnancy\",\"Test if pregnancy is possible\"],\"key\":\"period stopped after one day\"},{\"id\":140,\"title\":\"Spotting Just Before Your Period?\",\"head\":[\"SPOTTING\",\"BEFORE PERIOD?\"],\"eyebrow\":\"BLEEDING CLUES\",\"bullets\":[\"Spotting may happen for several reasons\",\"Color alone is not a reliable clue\",\"Test when pregnancy is possible\"],\"key\":\"spotting before period\"},{\"id\":141,\"title\":\"Your Ovulation App Might Be Wrong\",\"head\":[\"APP SAYS\",\"OVULATING?\"],\"eyebrow\":\"FERTILITY TIMING\",\"bullets\":[\"Apps predict rather than confirm ovulation\",\"Real cycle timing can change\",\"Use appropriate testing if uncertain\"],\"key\":\"ovulation predictor app accuracy\"},{\"id\":142,\"title\":\"Two Periods Close Together?\",\"head\":[\"TWO PERIODS\",\"SO CLOSE?\"],\"eyebrow\":\"CYCLE QUESTIONS\",\"bullets\":[\"Bleeding patterns can vary\",\"Unusual bleeding needs proper assessment\",\"Speak with a clinician if it recurs\"],\"key\":\"two periods in one month\"},{\"id\":143,\"title\":\"Could Stress Explain Your Late Period?\",\"head\":[\"STRESS +\",\"LATE PERIOD?\"],\"eyebrow\":\"CYCLE & STRESS\",\"bullets\":[\"Stress can affect menstrual timing\",\"Other causes also need considering\",\"A test can help if pregnancy is possible\"],\"key\":\"stress delay period\"},{\"id\":144,\"title\":\"Sleeping Less and Period Late?\",\"head\":[\"SLEEP CHANGED?\",\"PERIOD LATE?\"],\"eyebrow\":\"CYCLE HABITS\",\"bullets\":[\"Major routine changes can affect cycles\",\"A late period has multiple possible causes\",\"Use a home test when appropriate\"],\"key\":\"sleep disruption menstrual cycle\"},{\"id\":145,\"title\":\"Your Period Is Different This Month\",\"head\":[\"CYCLE CHANGED?\",\"WHAT NOW?\"],\"eyebrow\":\"KNOW YOUR CYCLE\",\"bullets\":[\"Flow and timing can differ by month\",\"Tracking patterns may help\",\"Consult a clinician for persistent changes\"],\"key\":\"period different this month\"},{\"id\":146,\"title\":\"PMS or an Upset Stomach?\",\"head\":[\"NAUSEA?\",\"PMS OR MORE?\"],\"eyebrow\":\"SYMPTOM OVERLAP\",\"bullets\":[\"Nausea is not unique to pregnancy\",\"Illness and stress can cause similar feelings\",\"Check timing before drawing conclusions\"],\"key\":\"PMS nausea versus pregnancy\"},{\"id\":147,\"title\":\"Morning Nausea but a Negative Test?\",\"head\":[\"NAUSEOUS\",\"BUT NEGATIVE?\"],\"eyebrow\":\"UNSURE OF SIGNS\",\"bullets\":[\"Nausea alone does not confirm pregnancy\",\"A test taken early can be unclear\",\"Retest as directed if your period is late\"],\"key\":\"nausea negative pregnancy test\"},{\"id\":148,\"title\":\"Breasts Were Sore, Then Stopped?\",\"head\":[\"SORE THEN\",\"NOT SORE?\"],\"eyebrow\":\"HORMONE CHANGES\",\"bullets\":[\"Breast tenderness can shift during cycles\",\"One symptom cannot rule pregnancy in or out\",\"Test if you have missed a period\"],\"key\":\"breast soreness disappeared\"},{\"id\":149,\"title\":\"Bloating and Cramps Together?\",\"head\":[\"BLOATING +\",\"CRAMPS?\"],\"eyebrow\":\"PMS OR PREGNANCY\",\"bullets\":[\"These feelings overlap across conditions\",\"They cannot confirm pregnancy alone\",\"A home test offers better clarity\"],\"key\":\"bloating cramps pregnancy\"},{\"id\":150,\"title\":\"Peeing More at Night?\",\"head\":[\"UP ALL NIGHT\",\"TO PEE?\"],\"eyebrow\":\"SYMPTOM CHECK\",\"bullets\":[\"Urinary changes have many causes\",\"Burning or fever needs medical attention\",\"Pregnancy requires confirmation with a test\"],\"key\":\"frequent urination at night pregnancy\"},{\"id\":151,\"title\":\"Feeling More Emotional This Cycle?\",\"head\":[\"MOOD CHANGED?\",\"READ THIS\"],\"eyebrow\":\"EMOTIONAL CHANGES\",\"bullets\":[\"Stress and hormones can affect mood\",\"Mood is not a pregnancy diagnosis\",\"Focus on cycle and test timing\"],\"key\":\"mood swings menstrual cycle\"},{\"id\":152,\"title\":\"Cramps but Still No Bleeding?\",\"head\":[\"CRAMPING\",\"NO BLEEDING?\"],\"eyebrow\":\"BODY QUESTIONS\",\"bullets\":[\"Cramps can happen for many reasons\",\"Do not rely on cramping alone\",\"Seek urgent care for severe pain\"],\"key\":\"cramps no bleeding pregnancy\"},{\"id\":153,\"title\":\"Nipple Changes: An Early Clue?\",\"head\":[\"NIPPLE CHANGES?\",\"WHAT'S NORMAL?\"],\"eyebrow\":\"BODY CHANGES\",\"bullets\":[\"Breast and nipple changes have many causes\",\"They do not identify pregnancy on their own\",\"Use testing for confirmation\"],\"key\":\"nipple changes pregnancy\"},{\"id\":154,\"title\":\"Hungry All the Time Before Your Period?\",\"head\":[\"EXTRA HUNGRY?\",\"PMS OR MORE?\"],\"eyebrow\":\"FOOD & HORMONES\",\"bullets\":[\"Appetite may shift across the cycle\",\"Cravings alone cannot confirm pregnancy\",\"Check your expected period date\"],\"key\":\"increased appetite pregnancy signs\"},{\"id\":155,\"title\":\"When a Pregnancy Test Shows No Lines\",\"head\":[\"NO LINES?\",\"TEST INVALID?\"],\"eyebrow\":\"READ YOUR TEST\",\"bullets\":[\"No control line can mean an invalid test\",\"Read the instructions before interpreting\",\"Use a new test if the result is invalid\"],\"key\":\"pregnancy test no lines\"},{\"id\":156,\"title\":\"What Is the Control Line For?\",\"head\":[\"CONTROL LINE?\",\"WHAT IT MEANS\"],\"eyebrow\":\"TEST EDUCATION\",\"bullets\":[\"Control indicators help validate the test\",\"Instructions vary between brands\",\"Do not read results outside the time window\"],\"key\":\"pregnancy test control line\"},{\"id\":157,\"title\":\"Smudged Pregnancy Test: What Next?\",\"head\":[\"TEST SMUDGED?\",\"DO THIS\"],\"eyebrow\":\"UNCLEAR RESULTS\",\"bullets\":[\"A dye run can make a test unreadable\",\"Do not guess from an unclear result\",\"Follow directions and try a new test\"],\"key\":\"pregnancy test dye run\"},{\"id\":158,\"title\":\"Faint Positive, Then Negative?\",\"head\":[\"POSITIVE THEN\",\"NEGATIVE?\"],\"eyebrow\":\"CONFLICTING RESULTS\",\"bullets\":[\"Different timings can produce different readings\",\"Follow your test's instructions\",\"Contact a clinician if uncertainty remains\"],\"key\":\"positive then negative pregnancy test\"},{\"id\":159,\"title\":\"When to Test After Ovulation\",\"head\":[\"AFTER OVULATION\",\"WHEN TO TEST?\"],\"eyebrow\":\"TESTING GUIDE\",\"bullets\":[\"Early tests can miss a pregnancy\",\"Testing after a missed period is more reliable\",\"Follow the instructions for your test\"],\"key\":\"days past ovulation test\"},{\"id\":160,\"title\":\"PCOS and a Late Pregnancy Test?\",\"head\":[\"PCOS +\",\"LATE PERIOD?\"],\"eyebrow\":\"IRREGULAR CYCLES\",\"bullets\":[\"Irregular ovulation can complicate timing\",\"Cycle predictions may be less reliable\",\"Ask a clinician about persistent concerns\"],\"key\":\"PCOS pregnancy test timing\"},{\"id\":161,\"title\":\"Long Cycles and Pregnancy Testing\",\"head\":[\"LONG CYCLE?\",\"WHEN TO TEST?\"],\"eyebrow\":\"CYCLE LENGTH\",\"bullets\":[\"Long cycles can shift expected dates\",\"Guessing ovulation can be difficult\",\"For uncertainty ask a health professional\"],\"key\":\"long menstrual cycle pregnancy test\"},{\"id\":162,\"title\":\"Your Last Period Date Is Unknown\",\"head\":[\"DON'T KNOW\",\"LAST PERIOD?\"],\"eyebrow\":\"PERIOD DATES\",\"bullets\":[\"You can still plan an appropriate test\",\"Timing since possible exposure may help\",\"Ask a clinician if dates are unclear\"],\"key\":\"unknown last period pregnancy\"},{\"id\":163,\"title\":\"3 Questions Before Retesting\",\"head\":[\"TEST AGAIN?\",\"ASK THESE 3\"],\"eyebrow\":\"RETEST CHECKLIST\",\"bullets\":[\"Did you test before your missed period?\",\"Did you follow the reading window?\",\"Is it time to repeat as instructed?\"],\"key\":\"pregnancy retest checklist\"},{\"id\":164,\"title\":\"Can Late Bedtimes Affect Your Period?\",\"head\":[\"LATE NIGHTS\",\"LATE PERIOD?\"],\"eyebrow\":\"SLEEP & CYCLE\",\"bullets\":[\"Sleep and routine changes can matter\",\"A late period is not proof of pregnancy\",\"Check with a test when appropriate\"],\"key\":\"late bedtime cycle timing\"},{\"id\":165,\"title\":\"Pregnancy Test Confusing? Save This\",\"head\":[\"CONFUSING TEST?\",\"SAVE THIS\"],\"eyebrow\":\"RESULT CHECKLIST\",\"bullets\":[\"Check the control indicator first\",\"Read only in the stated time window\",\"Retest or ask a clinician if unsure\"],\"key\":\"confusing pregnancy test result\"},{\"id\":166,\"title\":\"Early Pregnancy Signs That Mislead\",\"head\":[\"THESE SIGNS\",\"AREN'T PROOF\"],\"eyebrow\":\"SYMPTOM MYTHS\",\"bullets\":[\"Fatigue and bloating are non-specific\",\"PMS can feel surprisingly similar\",\"Only a test or clinician can confirm\"],\"key\":\"unreliable pregnancy symptoms\"},{\"id\":167,\"title\":\"What Exactly Counts as a Missed Period?\",\"head\":[\"MISSED PERIOD?\",\"EXPLAINED\"],\"eyebrow\":\"PERIOD TRACKING\",\"bullets\":[\"Expected dates depend on cycle patterns\",\"An app can estimate but not guarantee\",\"Test if your period is late\"],\"key\":\"what counts as missed period\"},{\"id\":168,\"title\":\"When an Ovulation App Doesn't Match\",\"head\":[\"APP VS\",\"YOUR BODY?\"],\"eyebrow\":\"FERTILITY CLUES\",\"bullets\":[\"Algorithms estimate fertile dates\",\"Cycles can vary naturally\",\"Consider proper testing rather than guesses\"],\"key\":\"ovulation app inaccurate\"},{\"id\":169,\"title\":\"False Negative: What Is It?\",\"head\":[\"FALSE NEGATIVE?\",\"LET'S EXPLAIN\"],\"eyebrow\":\"TEST RESULTS\",\"bullets\":[\"Testing too soon can give a negative result\",\"Usage errors can affect reliability\",\"Repeat as directed if your period is late\"],\"key\":\"false negative pregnancy test\"},{\"id\":170,\"title\":\"Nervous About Taking a Pregnancy Test?\",\"head\":[\"NERVOUS\",\"TO TEST?\"],\"eyebrow\":\"YOU HAVE OPTIONS\",\"bullets\":[\"It is okay to plan when and where to test\",\"Read the directions in advance\",\"Seek support if you need it\"],\"key\":\"nervous pregnancy test\"},{\"id\":171,\"title\":\"Is It Period Blood or Spotting?\",\"head\":[\"PERIOD OR\",\"SPOTTING?\"],\"eyebrow\":\"BLEEDING QUESTIONS\",\"bullets\":[\"Flow patterns can vary\",\"Appearance alone cannot confirm pregnancy\",\"Seek advice for unusual bleeding\"],\"key\":\"period blood versus spotting\"},{\"id\":172,\"title\":\"First Pregnancy Test? Know These Tips\",\"head\":[\"FIRST EVER\",\"PREGNANCY TEST?\"],\"eyebrow\":\"BEGINNER GUIDE\",\"bullets\":[\"Check the expiration date\",\"Follow collection and timing instructions\",\"Read results only when directed\"],\"key\":\"first pregnancy test tips\"},{\"id\":173,\"title\":\"Trying to Conceive? Track Wisely\",\"head\":[\"TRYING FOR\",\"A BABY?\"],\"eyebrow\":\"FERTILITY BASICS\",\"bullets\":[\"Cycle tracking can provide useful context\",\"Ovulation predictions are estimates\",\"Use a test to check for pregnancy\"],\"key\":\"trying to conceive cycle tracking\"},{\"id\":174,\"title\":\"Your Cycle Never Matches the App\",\"head\":[\"CYCLE DOESN'T\",\"MATCH THE APP?\"],\"eyebrow\":\"PERIOD APPS\",\"bullets\":[\"Different cycle lengths are common\",\"Prediction errors do not diagnose a problem\",\"Track real dates and ask for advice\"],\"key\":\"period app cycle different\"},{\"id\":175,\"title\":\"Reading Into Every Tiny Symptom?\",\"head\":[\"GOOGLING EVERY\",\"SYMPTOM?\"],\"eyebrow\":\"TWO-WEEK WAIT\",\"bullets\":[\"Many early signs overlap with PMS\",\"Looking for patterns can be stressful\",\"Set a testing date for clarity\"],\"key\":\"overthinking pregnancy symptoms\"},{\"id\":176,\"title\":\"No Pregnancy Symptoms Yet?\",\"head\":[\"NO SYMPTOMS?\",\"DON'T GUESS\"],\"eyebrow\":\"EARLY PREGNANCY\",\"bullets\":[\"Not everyone experiences obvious symptoms\",\"Timing differs between people\",\"A home test is more informative\"],\"key\":\"no early pregnancy symptoms\"},{\"id\":177,\"title\":\"Why You Feel 'Pregnant' Before Your Period\",\"head\":[\"FEEL PREGNANT?\",\"BUT NO TEST?\"],\"eyebrow\":\"PMS VS PREGNANCY\",\"bullets\":[\"PMS and pregnancy can feel similar\",\"Feelings alone are not reliable evidence\",\"Test when your period is missed\"],\"key\":\"feel pregnant before period\"},{\"id\":178,\"title\":\"What Pregnancy Apps Can and Can't Do\",\"head\":[\"CAN AN APP\",\"CONFIRM IT?\"],\"eyebrow\":\"QUIZ VS TEST\",\"bullets\":[\"An app can organize your questions\",\"A quiz is not a pregnancy test\",\"Home testing or clinical care confirms\"],\"key\":\"can pregnancy app diagnose\"},{\"id\":179,\"title\":\"Your Pregnancy-Test Morning Checklist\",\"head\":[\"TEST DAY?\",\"3 THINGS\"],\"eyebrow\":\"PLAN YOUR TEST\",\"bullets\":[\"Read your specific test instructions\",\"Have a timer and clean space ready\",\"Know when to check the result\"],\"key\":\"pregnancy test morning checklist\"},{\"id\":180,\"title\":\"Your 2-Minute Pregnancy Quiz\",\"head\":[\"AM I PREGNANT?\",\"TRY THE QUIZ\"],\"eyebrow\":\"START HERE\",\"bullets\":[\"Explore symptoms and menstrual timing\",\"Learn when to consider a home test\",\"Remember a quiz cannot diagnose pregnancy\"],\"key\":\"free pregnancy quiz iphone\"}]")
ROOT=Path('pregnancy/women-25-a')
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
    p=Path(f'pin-{[1,4,5,6,9,1,4,5,6,10][i%10]:02d}.png')
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
    mode=[0,1,4][n%3]
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
    svg=layout(d,n,palette[(i*7+4)%len(palette)])
    folder=Path('pregnancy/women-25-a' if ident<=155 else 'pregnancy/women-25-b')
    folder.mkdir(parents=True,exist_ok=True)
    dest=folder/f'woman-pin-{ident:03}.png'
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(dest))
    desc=(f"{d['title']}. {'. '.join(d['bullets'])}. "
          f"Explore the Am I Pregnant? Pregnancy Quiz app to understand possible signs and plan your next steps. "
          f"This quiz is informational and cannot diagnose pregnancy; confirm with a test or clinician. "
          f"#AmIPregnant #PregnancyQuiz #PregnancySymptoms")
    rows.append({'Title':d['title'],'Media URL':f"https://raw.githubusercontent.com/{REPO}/main/pregnancy/{'women-25-a' if ident<=155 else 'women-25-b'}/woman-pin-{ident:03}.png",
         'Pinterest board':BOARD,'Thumbnail':'','Description':desc[:497],
         'Link':f"{APP}?utm_content=pinterest_women_pin_{ident:03}",'Publish date':'','Keywords':d['key']+', pregnancy quiz, pregnancy symptoms'})
    print('generated',dest)
with open('pinterest_50_women_pins_ALL.csv','w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
for filename, subset in [('pinterest_women_batch_1_25.csv',rows[:25]),('pinterest_women_batch_2_25.csv',rows[25:])]:
    with open(filename,'w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        writer.writerows(subset)
print('COMPLETE',len(rows),'WOMEN-CENTERED PIN IMAGES AND CSVs')
