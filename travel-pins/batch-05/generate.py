from PIL import Image,ImageDraw,ImageFont,ImageEnhance
from pathlib import Path
out=Path('travel-pins/batch-05');out.mkdir(parents=True,exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
items=[
('51-first-trip-abroad','FIRST TRIP','ABROAD?','20 things to know before you go','travel-pins/batch-04/pin-44-greek-islands.jpg'),
('52-tourist-traps','AVOID TOURIST','TRAPS','Travel smarter like a local','travel-pins/batch-04/pin-43-amalfi-coast.jpg'),
('53-cheap-hotels','FIND CHEAP','HOTELS','Great stays without bad surprises','travel-pins/batch-02/pin-21-spain-best-time.jpg'),
('54-airport-security','AIRPORT SECURITY','MADE EASY','Simple tips for a smoother trip','travel-pins/batch-02/pin-26-dubai-best-time.jpg'),
('55-winter-sun','BEST WINTER','SUN ESCAPES','Warm getaways close to Europe','travel-pins/batch-04/pin-44-greek-islands.jpg'),
('56-flying-with-kids','FLYING WITH','KIDS','A stress-free family checklist','travel-pins/batch-02/pin-23-bali-best-time.jpg'),
('57-direct-connecting-flights','DIRECT OR','CONNECTING?','Which flight is worth the savings?','travel-pins/batch-04/pin-46-switzerland-train.jpg'),
('58-last-minute-flights','LAST-MINUTE','FLIGHT DEALS','How to find better fares','travel-pins/batch-02/pin-22-thailand-best-time.jpg'),
('59-hotel-hostel-apartment','HOTEL, HOSTEL','OR APARTMENT?','Choose the stay that fits your trip','travel-pins/batch-04/pin-49-vienna.jpg'),
('60-multi-city-trips','PLAN A','MULTI-CITY TRIP','More exploring. Less backtracking.','travel-pins/batch-04/pin-50-turkey.jpg')]
for name,top,main,sub,src in items:
 orig=Image.open(src).convert('RGB');W,H=orig.size
 crop=orig.crop((0,int(H*.38),W,int(H*.87)))
 r=max(1000/crop.width,1500/crop.height)
 b=crop.resize((round(crop.width*r),round(crop.height*r)),Image.Resampling.LANCZOS)
 bg=Image.new('RGB',(1000,1500),(20,84,117));bg.paste(b,((1000-b.width)//2,(1500-b.height)//2))
 bg=ImageEnhance.Color(bg).enhance(1.25).convert('RGBA');d=ImageDraw.Draw(bg)
 d.rounded_rectangle((56,52,944,535),radius=58,fill=(255,251,235,245))
 d.rounded_rectangle((190,1305,810,1420),radius=57,fill=(244,77,64,255),outline=(255,250,235,255),width=5)
 d.rounded_rectangle((220,1431,780,1491),radius=28,fill=(255,251,236,242))
 def fit(s,w,sz):
  f=ImageFont.truetype(font,sz)
  while d.textbbox((0,0),s,font=f)[2]>w and sz>25:
   sz-=2;f=ImageFont.truetype(font,sz)
  return f
 def line(s,y,f,c):d.text((500,y),s,font=f,anchor='mt',fill=c)
 line(top,90,fit(top,815,77),(10,45,80))
 line(main,217,fit(main,815,104),(245,78,62))
 line(sub,390,fit(sub,790,37),(12,46,76))
 line('READ THE GUIDE  →',1331,fit('READ THE GUIDE  →',565,53),'white')
 line('asktrippilot.com',1440,fit('asktrippilot.com',510,34),(12,42,80))
 bg.convert('RGB').save(out/(name+'.jpg'),quality=93,optimize=True,subsampling=0)
