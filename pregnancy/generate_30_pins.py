from pathlib import Path
import os, random, csv, math, base64, html, textwrap
from PIL import Image
from io import BytesIO
import cairosvg
import json

DATA=json.loads("[{\"id\":11,\"title\":\"7 Early Signs Worth Knowing\",\"head\":[\"COULD THESE BE\",\"EARLY SIGNS?\"],\"eyebrow\":\"EARLY PREGNANCY\",\"bullets\":[\"A missed period can be one clue\",\"Fatigue and breast tenderness can overlap with PMS\",\"Only a test can help confirm\"],\"key\":\"early pregnancy signs\"},{\"id\":12,\"title\":\"5 Things to Check if Your Period Is Late\",\"head\":[\"LATE PERIOD?\",\"CHECK THESE 5\"],\"eyebrow\":\"CYCLE CLARITY\",\"bullets\":[\"Cycle dates and natural variation\",\"Stress, illness or lifestyle changes\",\"When to take a pregnancy test\"],\"key\":\"late period\"},{\"id\":13,\"title\":\"Negative Test but No Period?\",\"head\":[\"NEGATIVE TEST...\",\"STILL NO PERIOD?\"],\"eyebrow\":\"TESTING QUESTIONS\",\"bullets\":[\"A test may be too early\",\"Read the test instructions closely\",\"Retest later or ask a clinician\"],\"key\":\"negative pregnancy test\"},{\"id\":14,\"title\":\"PMS or Pregnancy? Know the Overlap\",\"head\":[\"PMS OR\",\"PREGNANCY?\"],\"eyebrow\":\"SYMPTOM CHECK\",\"bullets\":[\"Tender breasts can happen with either\",\"Bloating and tiredness overlap\",\"Symptoms alone cannot confirm pregnancy\"],\"key\":\"PMS versus pregnancy\"},{\"id\":15,\"title\":\"When Is a Pregnancy Test Most Reliable?\",\"head\":[\"WHEN SHOULD\",\"YOU TEST?\"],\"eyebrow\":\"PREGNANCY TEST TIPS\",\"bullets\":[\"Usually more reliable after a missed period\",\"Timing can affect a result\",\"Follow the instructions on your test\"],\"key\":\"pregnancy test timing\"},{\"id\":16,\"title\":\"Feeling Extra Tired?\",\"head\":[\"SO TIRED\",\"LATELY?\"],\"eyebrow\":\"SYMPTOMS EXPLAINED\",\"bullets\":[\"Fatigue has many possible causes\",\"Notice your cycle timing\",\"Test if pregnancy is possible\"],\"key\":\"fatigue early pregnancy\"},{\"id\":17,\"title\":\"Cramps Without a Period?\",\"head\":[\"CRAMPS...\",\"NO PERIOD?\"],\"eyebrow\":\"BODY SIGNALS\",\"bullets\":[\"Cramping can have many causes\",\"Symptoms do not give an answer alone\",\"Check the timing and consider testing\"],\"key\":\"cramps no period\"},{\"id\":18,\"title\":\"Early Spotting: What It Can Mean\",\"head\":[\"SPOTTING?\",\"WHAT TO KNOW\"],\"eyebrow\":\"CYCLE & SPOTTING\",\"bullets\":[\"Light spotting has many possible causes\",\"Note timing and how much bleeding\",\"Seek care for severe pain or heavy bleeding\"],\"key\":\"spotting early pregnancy\"},{\"id\":19,\"title\":\"Does Nausea Mean Pregnancy?\",\"head\":[\"NAUSEOUS?\",\"IS IT A SIGN?\"],\"eyebrow\":\"SYMPTOM GUIDE\",\"bullets\":[\"Nausea is not specific to pregnancy\",\"Timing and other symptoms matter\",\"A test is needed to confirm\"],\"key\":\"nausea pregnancy sign\"},{\"id\":20,\"title\":\"Breast Tenderness and Pregnancy\",\"head\":[\"SORE BREASTS?\",\"HERE'S WHY\"],\"eyebrow\":\"COMMON SYMPTOMS\",\"bullets\":[\"Tender breasts are common before a period\",\"They can also occur in early pregnancy\",\"Track timing rather than guessing\"],\"key\":\"breast tenderness pregnancy\"},{\"id\":21,\"title\":\"How Late Is a Late Period?\",\"head\":[\"PERIOD LATE?\",\"START HERE\"],\"eyebrow\":\"MENSTRUAL CYCLE\",\"bullets\":[\"Cycles vary from month to month\",\"Record the first day of your last period\",\"Test if pregnancy is possible\"],\"key\":\"how late period\"},{\"id\":22,\"title\":\"Pregnancy Symptoms vs Period Symptoms\",\"head\":[\"THE SYMPTOMS\",\"OVERLAP\"],\"eyebrow\":\"PMS VS PREGNANCY\",\"bullets\":[\"Cramps, bloating and tiredness can occur in both\",\"Symptoms may change cycle to cycle\",\"A home test can give more clarity\"],\"key\":\"period symptoms versus pregnancy\"},{\"id\":23,\"title\":\"What to Do After a Missed Period\",\"head\":[\"MISSED YOUR\",\"PERIOD?\"],\"eyebrow\":\"3 SIMPLE STEPS\",\"bullets\":[\"Check your usual cycle dates\",\"Take a home test at the right time\",\"Ask a clinician if you're unsure\"],\"key\":\"missed period next steps\"},{\"id\":24,\"title\":\"Is Testing Too Early a Mistake?\",\"head\":[\"TOO EARLY\",\"TO TEST?\"],\"eyebrow\":\"TEST SMARTER\",\"bullets\":[\"Hormone levels rise over time\",\"Testing before a missed period may miss pregnancy\",\"Retest as directed if still unsure\"],\"key\":\"testing too early pregnancy\"},{\"id\":25,\"title\":\"Bloating: PMS or Early Pregnancy?\",\"head\":[\"BLOATING?\",\"PMS OR MORE?\"],\"eyebrow\":\"BODY CHANGES\",\"bullets\":[\"Bloating is common in the menstrual cycle\",\"Digestive changes have many causes\",\"Avoid reading too much into one symptom\"],\"key\":\"bloating PMS pregnancy\"},{\"id\":26,\"title\":\"What Your Last Period Date Tells You\",\"head\":[\"YOUR LAST\",\"PERIOD DATE\"],\"eyebrow\":\"CYCLE TIMELINE\",\"bullets\":[\"First day of your last period matters\",\"Cycle length affects timing\",\"Dates alone cannot confirm pregnancy\"],\"key\":\"last menstrual period pregnancy\"},{\"id\":27,\"title\":\"3 Questions Before You Take a Test\",\"head\":[\"BEFORE YOU\",\"TAKE A TEST\"],\"eyebrow\":\"TESTING CHECKLIST\",\"bullets\":[\"When was your expected period?\",\"Are you following test directions?\",\"Do you need to retest later?\"],\"key\":\"pregnancy test checklist\"},{\"id\":28,\"title\":\"Could Mood Changes Be a Sign?\",\"head\":[\"MOOD SWINGS?\",\"LET'S TALK\"],\"eyebrow\":\"PREGNANCY & PMS\",\"bullets\":[\"Hormone shifts can affect mood\",\"Stress and sleep can also play a role\",\"Mood alone is not a pregnancy sign\"],\"key\":\"mood swings pregnancy\"},{\"id\":29,\"title\":\"No Symptoms: Could You Still Be Pregnant?\",\"head\":[\"NO SYMPTOMS?\",\"STILL UNSURE?\"],\"eyebrow\":\"PREGNANCY FACTS\",\"bullets\":[\"Not everyone notices early symptoms\",\"Many signs overlap with PMS\",\"Testing gives a better answer\"],\"key\":\"no pregnancy symptoms\"},{\"id\":30,\"title\":\"A Quick Guide to Pregnancy Test Lines\",\"head\":[\"FAINT LINE?\",\"WHAT NEXT?\"],\"eyebrow\":\"READING RESULTS\",\"bullets\":[\"Follow the test's reading window\",\"Evaporation lines can confuse results\",\"Retest or check with a clinician if unsure\"],\"key\":\"faint pregnancy test line\"},{\"id\":31,\"title\":\"Why Your Period Timing Can Change\",\"head\":[\"CYCLE SHIFT?\",\"IT HAPPENS\"],\"eyebrow\":\"PERIOD FACTS\",\"bullets\":[\"Illness or stress may shift a cycle\",\"Natural variation is common\",\"Use a pregnancy test if needed\"],\"key\":\"irregular period reasons\"},{\"id\":32,\"title\":\"What to Know About Food Cravings\",\"head\":[\"CRAVING\",\"SOMETHING?\"],\"eyebrow\":\"SYMPTOM EXPLAINED\",\"bullets\":[\"Cravings can have many explanations\",\"They are not a reliable sign alone\",\"Look at timing, not a single symptom\"],\"key\":\"food cravings pregnancy\"},{\"id\":33,\"title\":\"Early Pregnancy Discharge: Basics\",\"head\":[\"DISCHARGE?\",\"WHAT'S NORMAL?\"],\"eyebrow\":\"BODY BASICS\",\"bullets\":[\"Discharge changes across the cycle\",\"Color, odor and irritation can matter\",\"Seek medical advice for concerning changes\"],\"key\":\"early pregnancy discharge\"},{\"id\":34,\"title\":\"Do Smells Suddenly Feel Stronger?\",\"head\":[\"SMELLS FEEL\",\"STRONGER?\"],\"eyebrow\":\"SENSORY CHANGES\",\"bullets\":[\"Sensitivity to smells has many causes\",\"Some people notice it in pregnancy\",\"A test is needed for confirmation\"],\"key\":\"sensitive smell pregnancy\"},{\"id\":35,\"title\":\"When to Take a Second Pregnancy Test\",\"head\":[\"TEST AGAIN?\",\"WHEN?\"],\"eyebrow\":\"RETESTING GUIDE\",\"bullets\":[\"Read the instructions on your test\",\"Wait and retest if the first was too early\",\"Speak with a clinician if uncertainty continues\"],\"key\":\"when to retest pregnancy\"},{\"id\":36,\"title\":\"20-Second Pregnancy Symptom Quiz\",\"head\":[\"CURIOUS?\",\"TAKE THE QUIZ\"],\"eyebrow\":\"INTERACTIVE QUIZ\",\"bullets\":[\"Explore common early symptoms\",\"Reflect on cycle timing\",\"Get ideas for next steps, not a diagnosis\"],\"key\":\"pregnancy symptoms quiz\"},{\"id\":37,\"title\":\"A Simple Late-Period Checklist\",\"head\":[\"YOUR LATE\",\"PERIOD PLAN\"],\"eyebrow\":\"SAVE THIS CHECKLIST\",\"bullets\":[\"Note your expected start date\",\"Think about recent cycle changes\",\"Use a home test for clarity\"],\"key\":\"late period checklist\"},{\"id\":38,\"title\":\"The Difference Between a Quiz and a Test\",\"head\":[\"QUIZ OR TEST?\",\"KNOW THE DIFFERENCE\"],\"eyebrow\":\"IMPORTANT TO KNOW\",\"bullets\":[\"A quiz helps explore possible signs\",\"A home test checks for pregnancy hormones\",\"Only testing or clinical care can confirm\"],\"key\":\"pregnancy quiz versus test\"},{\"id\":39,\"title\":\"When Should You Contact a Clinician?\",\"head\":[\"WHEN TO\",\"GET CARE\"],\"eyebrow\":\"HEALTH FIRST\",\"bullets\":[\"Heavy bleeding or severe pain needs care\",\"Seek help for worrying symptoms\",\"Do not rely on a quiz for diagnosis\"],\"key\":\"pregnancy when to see doctor\"},{\"id\":40,\"title\":\"Wondering If You're Pregnant? Start Here\",\"head\":[\"COULD I BE\",\"PREGNANT?\"],\"eyebrow\":\"YOUR NEXT STEP\",\"bullets\":[\"Understand common early signs\",\"Review when to take a home test\",\"Explore the free pregnancy quiz\"],\"key\":\"am I pregnant quiz\"}]")
ROOT=Path('pregnancy/new-30')
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
    ident=d['id']; n=i
    svg=layout(d,n,palette[(i*7)%len(palette)])
    dest=ROOT/f'pregnancy-pin-{ident:02}.png'
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(dest))
    desc=(f"{d['title']}. {'. '.join(d['bullets'])}. "
          f"Explore the Am I Pregnant? Pregnancy Quiz app to understand possible signs and plan your next steps. "
          f"A quiz cannot diagnose pregnancy; confirm with a home pregnancy test or clinician. "
          f"#AmIPregnant #PregnancyQuiz #PregnancySymptoms")
    rows.append({'Title':d['title'],'Media URL':f"https://raw.githubusercontent.com/{REPO}/main/pregnancy/new-30/pregnancy-pin-{ident:02}.png",
         'Pinterest board':BOARD,'Thumbnail':'','Description':desc[:497],
         'Link':f"{APP}?utm_content=pinterest_pin_{ident:02}",'Publish date':'','Keywords':d['key']+', pregnancy quiz, pregnancy symptoms'})
    print('generated',dest)
with open('pinterest_30_new_pins.csv','w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
print('COMPLETE',len(rows),'NEW PIN DESIGNS AND CSV')
