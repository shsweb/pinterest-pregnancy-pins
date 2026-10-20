import csv, os, re, time, textwrap, io
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
BASE='https://asktrippilot.com/blog/'
OUT=Path('travel-pins/images'); OUT.mkdir(parents=True,exist_ok=True)
RAW='https://raw.githubusercontent.com/shsweb/pinterest-pregnancy-pins/main/travel-pins/images/'
DATA=[
('best-time-to-visit-portugal','BEST TIME TO VISIT','PORTUGAL','The months locals love','Portugal Travel'),
('best-time-to-visit-greece','BEST TIME TO VISIT','GREECE','Islands, sunshine & fewer crowds','Greece Travel'),
('best-time-to-visit-costa-rica','BEST TIME TO VISIT','COSTA RICA','Rainforest, beach & wildlife seasons','Central America Travel'),
('best-time-to-visit-cancun','BEST TIME TO VISIT','CANCUN','Sun, beaches & fewer crowds','Mexico Travel'),
('best-time-to-visit-puerto-rico','BEST TIME TO VISIT','PUERTO RICO','Beach weather & island life','Caribbean Travel'),
('best-time-to-visit-italy','BEST TIME TO VISIT','ITALY','Rome, Florence & the Amalfi Coast','Italy Travel'),
('best-time-to-visit-iceland','BEST TIME TO VISIT','ICELAND','Northern lights or midnight sun?','Iceland Travel'),
('best-time-to-visit-hawaii','BEST TIME TO VISIT','HAWAII','Island adventures year-round','Hawaii Travel'),
('best-places-to-visit-in-december','BEST PLACES TO VISIT','IN DECEMBER','Sunny escapes & winter wonders','Winter Travel'),
('where-to-travel-in-2026-12-places-worth-the-trip','WHERE TO TRAVEL','IN 2026','12 places worth the journey','Travel Inspiration'),
('when-to-book-flights-to-get-the-lowest-price','WHEN TO BOOK','CHEAP FLIGHTS','Timing tips to save on airfare','Flight Booking Tips'),
('the-cheapest-cities-to-visit-in-europe-this-year','CHEAPEST CITIES','IN EUROPE','Beautiful trips on a budget','Budget Travel'),
('the-best-weekend-trips-in-europe-for-first-timers','BEST EUROPE','WEEKEND TRIPS','Easy escapes for first-timers','Europe Travel'),
('the-best-islands-in-greece-for-every-kind-of-traveler','BEST GREEK','ISLANDS','Which island is right for you?','Greece Travel'),
('solo-travel-safe-fun-destinations-for-a-first-trip-alone','BEST FIRST','SOLO TRIPS','Inspiring places to explore alone','Solo Travel'),
('romantic-weekend-getaways-in-europe','ROMANTIC EUROPE','GETAWAYS','Dreamy destinations for two','Couples Travel'),
('morocco-travel-guide-where-to-go-what-to-know-and-how-much-it-costs','EXPLORE','MOROCCO','Medinas, mountains & the desert','Morocco Travel'),
('marrakech-in-3-days-the-perfect-first-visit','MARRAKECH','IN 3 DAYS','The perfect first-time itinerary','Morocco Travel'),
('japan-for-first-timers-tokyo-kyoto-and-osaka-in-10-days','JAPAN','IN 10 DAYS','Tokyo, Kyoto & Osaka itinerary','Japan Travel'),
('chefchaouen-the-blue-city-a-complete-guide','CHEFCHAOUEN','BLUE CITY','Discover Morocco’s magical blue town','Morocco Travel'),
]
s=requests.Session();s.headers['User-Agent']='Mozilla/5.0 (compatible; TripPilotPinMaker/1.0)'
font_candidates=['/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
font_path=next(p for p in font_candidates if os.path.exists(p))
def ft(sz): return ImageFont.truetype(font_path,sz)
def getimage(url):
    try:
        r=s.get(url,timeout=20)
        if r.status_code!=200: return None
        soup=BeautifulSoup(r.text,'html.parser')
        for prop in ('og:image','twitter:image'):
            tag=soup.find('meta',attrs={'property':prop}) or soup.find('meta',attrs={'name':prop})
            if tag and tag.get('content'):
                u=urljoin(url,tag['content'])
                x=s.get(u,timeout=25);x.raise_for_status()
                img=Image.open(io.BytesIO(x.content)).convert('RGB')
                if min(img.size)>=400:return img
    except Exception as e: print('image lookup:',str(e)[:80])
    return None
def fallback(i):
    im=Image.new('RGB',(1000,1500)); pix=im.load()
    palettes=[((12,100,150),(64,208,186)),((29,60,142),(252,157,100)),((38,116,68),(153,213,118)),((23,82,136),(62,198,231))]
    a,b=palettes[i%len(palettes)]
    for y in range(1500):
        f=y/1499
        c=tuple(int(a[k]*(1-f)+b[k]*f) for k in range(3))
        ImageDraw.Draw(im).line((0,y,1000,y),fill=c)
    return im
def cover(im):
    w,h=im.size
    ratio=max(1000/w,1500/h)
    im=im.resize((round(w*ratio),round(h*ratio)),Image.Resampling.LANCZOS)
    x=(im.width-1000)//2;y=(im.height-1500)//2
    return im.crop((x,y,x+1000,y+1500))
def drawcenter(d,txt,y,font,fill,stroke_width=0,stroke_fill=None):
    d.text((500,y),txt,font=font,fill=fill,anchor='mt',stroke_width=stroke_width,stroke_fill=stroke_fill)
rows=[]
for i,(slug,top,main,sub,board) in enumerate(DATA,1):
    url=BASE+slug
    source_image=getimage(url)
    if source_image is None:
        source_image=fallback(i)
    im=cover(source_image)
    im=ImageEnhance.Color(im).enhance(1.22)
    # dark photo at bottom for easy legibility, bright header at top
    dark=Image.new('RGBA',(1000,1500),(0,0,0,0))
    dd=ImageDraw.Draw(dark)
    for y in range(740,1500):
        a=int(185*(y-740)/760)
        dd.line((0,y,1000,y),fill=(4,26,43,a))
    im=Image.alpha_composite(im.convert('RGBA'),dark)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((48,43,952,535),radius=85,fill=(255,253,239,243))
    fonttop=ft(56 if len(top)<20 else 47)
    drawcenter(d,top,88,fonttop,(16,48,76))
    fs=114 if len(main)<12 else 91 if len(main)<17 else 75
    drawcenter(d,main,192,ft(fs),(244,81,61))
    ysub=355
    for ln in textwrap.wrap(sub,width=31):
        drawcenter(d,ln,ysub,ft(37),(13,48,78));ysub+=52
    d.rounded_rectangle((115,1285,885,1408),radius=59,fill=(246,86,67),outline=(255,246,230),width=5)
    drawcenter(d,'READ THE FULL GUIDE  →',1317,ft(46),(255,255,255))
    drawcenter(d,'asktrippilot.com',1433,ft(33),(255,255,255),stroke_width=2,stroke_fill=(9,44,75))
    fn=f'pin-{i:02d}-{slug[:55]}.jpg'
    im.convert('RGB').save(OUT/fn,'JPEG',quality=93,subsampling=0,optimize=True)
    title=(top+' '+main).title()+': '+sub
    descr=title+'. Discover tips, best months, sights and practical travel planning ideas. Read the full AskTripPilot article!'
    rows.append({'Title':title[:100],'Media URL':RAW+fn,'Pinterest board':board,'Thumbnail':'','Description':descr,'Link':url,'Publish date':'','Keywords':main.title()+', travel guide, vacation planning, travel inspiration'})
    print('Created',fn,flush=True)
with open('travel-pins/pinterest_travel_pins_20.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['Title','Media URL','Pinterest board','Thumbnail','Description','Link','Publish date','Keywords']);w.writeheader();w.writerows(rows)
print('Created CSV with',len(rows),'rows')
