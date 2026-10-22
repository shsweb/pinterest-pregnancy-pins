from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import math, random

ROOT=Path(__file__).resolve().parent
SRC=ROOT/"sources"
OUT=ROOT/"images"
OUT.mkdir(parents=True,exist_ok=True)

PINS=[
 ("SANTA'S TOY TRAIN","ADVENTURE!","Show Santa Your Christmas Train!"),
 ("SNOW GLOBE","MAGIC!","Show Santa a Sparkling Snow Globe!"),
 ("CHRISTMAS SWEATER","FASHION SHOW!","Make Santa Laugh at Your Sweater!"),
 ("MAKE A WREATH","WITH SANTA!","Show Santa Your Christmas Wreath!"),
 ("CANDY CANE","CRAFT TIME!","Create Sweet Decorations with Santa!"),
 ("JINGLE BELL","MUSIC PARTY!","Play a Christmas Tune for Santa!"),
 ("ROCKET TO THE","NORTH POLE!","Call Santa on a Space Adventure!"),
 ("BUILD A TOY","CASTLE!","Show Santa Your Magical Castle!"),
 ("PINECONE ELF","FRIENDS!","Meet Santa's Tiny Craft Helpers!"),
 ("DRAW A SNOWMAN","FOR SANTA!","Show Santa Your Snowman Art!"),
 ("REINDEER TOY","CHECKUP!","Show Santa Your Reindeer Friend!"),
 ("CHRISTMAS","CUPCAKE PARTY!","Show Santa Your Sweet Cupcakes!"),
 ("RAINBOW LIGHTS","FOR SANTA!","Share Your Colorful Christmas Lights!"),
 ("FUNNY SHADOW","PUPPETS!","Make Santa Laugh with Silly Shadows!"),
 ("BUILD SANTA'S","MINI SLEIGH!","Show Santa Your Handmade Sleigh!"),
 ("SANTA'S CANDY","SHOP!","Open a Pretend Candy Shop for Santa!"),
 ("CHRISTMAS TOY","ORCHESTRA!","Put on a Music Show for Santa!"),
 ("MINI STOCKINGS","FOR SANTA!","Show Santa Your Stocking Creations!"),
 ("SNOWFLAKE CAPE","FASHION SHOW!","Show Santa Your Snowflake Costume!"),
 ("SANTA'S GIFT","DELIVERY GAME!","Play a Christmas Delivery Game!")
]
assert len(PINS)==20
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
assert Path(FONT).is_file()

def fontfit(draw,text,width,height,initial=90):
    for size in range(initial,23,-1):
        f=ImageFont.truetype(FONT,size)
        a=draw.textbbox((0,0),text,font=f,stroke_width=5)
        if a[2]-a[0]<=width and a[3]-a[1]<=height:
            return f
    raise ValueError(f"Cannot fit {text!r}")

def textline(draw, text, cy, color):
    font=fontfit(draw,text,837,103,94)
    x=500
    # A visible dark bevel and raised three-dimensional shadow.
    for offset in (13,11,9,7):
        draw.text((x,cy+offset),text,anchor="mm",font=font,
                  fill="#3c1520",stroke_width=6,stroke_fill="#321018")
    draw.text((x,cy+1),text,anchor="mm",font=font,
              fill=color,stroke_width=5,stroke_fill="#fff2d1")

def apple_mark(draw,cx,cy):
    draw.ellipse((cx-34,cy-24,cx+12,cy+30),fill="white")
    draw.ellipse((cx-5,cy-26,cx+39,cy+31),fill="white")
    draw.ellipse((cx+21,cy-9,cx+49,cy+13),fill="#bb0624")
    draw.ellipse((cx-3,cy-48,cx+29,cy-21),fill="white")
    draw.line((cx+6,cy-29,cx+20,cy-53),fill="white",width=8)

for i, (top,bottom,subtitle) in enumerate(PINS,1):
    path=SRC/f"scene-{i:02}.png"
    assert path.exists(), f"Missing generated scene: {path}"
    with Image.open(path) as src:
        src.load()
        assert src.width>=1000 and src.height>=1500,(path,src.size)
        image=ImageOps.fit(src.convert("RGBA"),(1000,1500),
                            method=Image.Resampling.LANCZOS,centering=(0.5,0.5))
    overlay=Image.new("RGBA",(1000,1500),(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    # Gradient protects legibility without stretching a tiny collage.
    for y in range(0,450):
        alpha=max(0,int(185*(1-y/480)))
        d.line((0,y,999,y),fill=(35,13,22,alpha),width=1)
    for y in range(1060,1500):
        alpha=max(0,int(200*(y-1060)/440))
        d.line((0,y,999,y),fill=(43,6,15,alpha),width=1)
    d.rounded_rectangle((48,48,952,389),radius=44,
                        fill=(42,42,34,220),outline=(248,199,103,255),width=7)
    d.rounded_rectangle((59,59,941,378),radius=37,
                        outline=(255,245,214,255),width=2)
    for side in (99,902):
        for yy in (112,185,275,341):
            rad=4+(yy%3)
            d.ellipse((side-rad,yy-rad,side+rad,yy+rad),fill="#ffe8a7")
    textline(d,top,147,"#fc3128")
    textline(d,bottom,273,"#ffd53e")
    d.rounded_rectangle((53,1141,947,1250),radius=49,
                        fill=(255,249,229,253),outline="#efb65f",width=6)
    font=fontfit(d,subtitle,820,66,47)
    d.text((500,1194),subtitle,anchor="mm",font=font,fill="#b40b25")
    # Standardized red call-to-action with comfortable Pinterest safe area.
    d.rounded_rectangle((51,1288,949,1452),radius=74,fill="#f7cf81")
    d.rounded_rectangle((61,1298,939,1443),radius=69,
                        fill="#b90424",outline="#fff7e3",width=5)
    d.rounded_rectangle((72,1309,929,1432),radius=57,
                        outline="#ff956d",width=3)
    apple_mark(d,175,1373)
    d.text((586,1351),"Try Call Santa",anchor="mm",
           font=fontfit(d,"Try Call Santa",620,54,58),fill="white")
    d.text((586,1402),"on iPhone",anchor="mm",
           font=fontfit(d,"on iPhone",520,50,50),fill="white")
    result=Image.alpha_composite(image,overlay).convert("RGB")
    out=OUT/f"santa-call-20-{i:02}.png"
    result.save(out,"PNG",optimize=True)
    with Image.open(out) as check:
        assert check.size==(1000,1500),check.size
        check.verify()
    assert out.stat().st_size>100000, (out,out.stat().st_size)
    print(f"VERIFIED {out.name} 1000x1500")
# A preview of the campaign, never used as actual Pin images.
sheet=Image.new("RGB",(1220,1545),"#fff8ed")
for i in range(20):
    im=Image.open(OUT/f"santa-call-20-{i+1:02}.png").convert("RGB")
    im.thumbnail((225,337),Image.Resampling.LANCZOS)
    x=20+(i%5)*244
    y=20+(i//5)*381
    sheet.paste(im,(x,y))
sheet.save(ROOT/"preview_20.jpg",quality=91,optimize=True)
print("SUCCESS: 20 unique full-resolution Pins")
