from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import random

ROOT=Path("santa/santa-fun-calls-20")
IN=ROOT/"sources"
OUT=ROOT/"images"
OUT.mkdir(parents=True,exist_ok=True)
ITEMS=[
 ("DANCE PARTY","WITH SANTA!","Show Santa Your Best Dance!"),
 ("GINGERBREAD","HOUSE FUN!","Build a Gingerbread House on a Santa Call!"),
 ("SING A SONG","FOR SANTA!","Your Christmas Karaoke Call!"),
 ("SHOW SANTA","YOUR TOY TRAIN!","Make Santa Cheer for Your Train!"),
 ("PAPER SNOWFLAKES","WITH SANTA!","Show Santa Your Snowflake Art!"),
 ("SILLY ELF HAT","CONTEST!","Call Santa and Show Your Funny Hat!"),
 ("MEET MY TOY","DINOSAUR, SANTA!","Surprise Santa with Your Dinosaur!"),
 ("CALL SANTA","FROM A FORT!","A Cozy Christmas Blanket Fort Call!"),
 ("PUPPET SHOW","FOR SANTA!","Make Santa Laugh at Your Puppet Show!"),
 ("PAINT A PICTURE","OF SANTA!","Show Santa Your Christmas Artwork!"),
 ("RACE TOY CARS","WITH SANTA!","Let Santa Watch the Big Race!"),
 ("CHRISTMAS CARDS","FOR SANTA!","Share Your Handmade Card with Santa!"),
 ("WRAP PRESENTS","WITH SANTA!","Show Santa Your Gift Wrapping!"),
 ("PLAY CHRISTMAS","CHARADES!","Can Santa Guess Your Silly Moves?"),
 ("TELL SANTA","A FUNNY JOKE!","Make Santa Laugh on Your Video Call!"),
 ("MAGIC TRICK","FOR SANTA!","Show Santa a Magical Surprise!"),
 ("HOT COCOA","WITH SANTA!","Cheers to Christmas with Santa!"),
 ("MAKE REINDEER","ANTLERS!","Show Santa Your Reindeer Craft!"),
 ("CHRISTMAS CROWN","PARTY!","Try on a Crown for Santa!"),
 ("FIND THE HIDDEN","ORNAMENT!","Call Santa and Celebrate Your Discovery!")
]
assert len(ITEMS)==20

FONT="/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
assert Path(FONT).is_file(),FONT
def font_fit(draw, phrase, max_width, max_height, default=88):
    for size in range(default,25,-1):
        f=ImageFont.truetype(FONT,size)
        b=draw.textbbox((0,0),phrase,font=f,stroke_width=3)
        if (b[2]-b[0])<=max_width and (b[3]-b[1])<=max_height:
            return f
    raise ValueError("Cannot fit type: "+phrase)

def apple_icon(d,x,y):
    # Consistent high-contrast white apple silhouette in red CTA.
    d.ellipse((x-41,y-32,x+16,y+35),fill="#ffffff")
    d.ellipse((x-4,y-34,x+49,y+34),fill="#ffffff")
    d.ellipse((x+29,y-14,x+59,y+12),fill="#a50023")
    d.ellipse((x-10,y-47,x+27,y-17),fill="#ffffff")
    d.line((x+0,y-34,x+16,y-58),fill="#ffffff",width=8)

def draw_text(d,center,phrase,font,fill,outline="#451622"):
    d.text(center,phrase,anchor="mm",font=font,fill=fill,
           stroke_width=4,stroke_fill=outline)

for i, (line1,line2,subtitle) in enumerate(ITEMS,1):
    src=IN/f"source-{i:02}.png"
    assert src.is_file(),f"Source missing: {src}"
    with Image.open(src) as im:
        im.load()
        assert im.width>=1000 and im.height>=1500,(src,im.size)
        base=ImageOps.fit(im.convert("RGBA"),(1000,1500),Image.Resampling.LANCZOS,centering=(.5,.5))
    overlay=Image.new("RGBA",(1000,1500),(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    # Subtle gradient for readability without covering the distinct child/Santa scene.
    for y in range(0,390):
        a=int(190*max(0,1-y/390))
        d.line((0,y,999,y),fill=(13,27,33,a),width=1)
    for y in range(1080,1500):
        a=int(170*max(0,(y-1080)/420))
        d.line((0,y,999,y),fill=(41,9,20,a),width=1)
    d.rounded_rectangle((55,43,945,314),radius=40,
                        fill=(9,62,50,232),outline=(255,223,158,255),width=7)
    d.rounded_rectangle((68,54,931,301),radius=33,
                        outline=(255,246,213,255),width=2)
    f1=font_fit(d,line1,822,93,89)
    f2=font_fit(d,line2,822,95,96)
    draw_text(d,(500,133),line1,f1,"#ffffff")
    draw_text(d,(500,230),line2,f2,"#ffda79")
    # Distinct activity message: full, explicitly typeset English.
    d.rounded_rectangle((53,1141,947,1249),radius=49,
                        fill=(255,249,226,250),outline=(247,189,108,255),width=6)
    sf=font_fit(d,subtitle,832,64,43)
    d.text((500,1194),subtitle,anchor="mm",font=sf,fill="#96132c")
    # Call-to-action, inset enough to survive Pinterest feed rounding.
    d.rounded_rectangle((55,1300,945,1445),radius=68,fill="#e3b95b")
    d.rounded_rectangle((64,1308,937,1438),radius=62,fill="#bc0829",
                        outline="#fff5d7",width=5)
    d.rounded_rectangle((74,1320,927,1427),radius=52,outline="#ff8e56",width=3)
    apple_icon(d,169,1373)
    cta="Try Call Santa on iPhone"
    cf=font_fit(d,cta,650,72,52)
    d.text((583,1376),cta,anchor="mm",font=cf,fill="white")
    result=Image.alpha_composite(base,overlay).convert("RGB")
    dst=OUT/f"santa-fun-{i:02}.png"
    result.save(dst,"PNG",optimize=True)
    with Image.open(dst) as x:
        assert x.size==(1000,1500)
        x.verify()
    assert dst.stat().st_size>100_000,dst
    print("PASS",i,dst.stat().st_size,line1,line2)
    
# Contact sheet for preview only, not used by Pinterest links.
w,h,gap=225,337,8
sheet=Image.new("RGB",(5*(w+gap)+gap,4*(h+gap)+gap),(244,241,234))
for i in range(20):
    with Image.open(OUT/f"santa-fun-{i+1:02}.png") as im:
        thumb=im.resize((w,h),Image.Resampling.LANCZOS)
    sheet.paste(thumb,(gap+(i%5)*(w+gap),gap+(i//5)*(h+gap)))
sheet.save(ROOT/"preview_20.jpg",quality=90,optimize=True)
print("COMPLETE: 20 DISTINCT PINTEREST POSTS VERIFIED")
