from pathlib import Path
import csv, json, math, random
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
META = json.loads((ROOT / "ideas.json").read_text(encoding="utf-8"))
assert len(META) == 20
SRC, OUT = ROOT / "sources", ROOT / "images"
OUT.mkdir(parents=True, exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
assert Path(FONT).is_file()

def text_font(d, txt, width, max_h, size):
    for s in range(size, 22, -1):
        f = ImageFont.truetype(FONT, s)
        b = d.textbbox((0,0), txt, font=f, stroke_width=4)
        if b[2]-b[0] <= width and b[3]-b[1] <= max_h:
            return f
    raise ValueError(f"Text cannot fit: {txt}")

def raised(d, text, y, main):
    f=text_font(d,text,805,102,94)
    for shift in (13,11,9,7,5):
        d.text((500,y+shift),text,anchor="mm",font=f,fill="#38111a",
               stroke_width=7,stroke_fill="#30101a")
    d.text((500,y+2),text,anchor="mm",font=f,fill="#fff6e2",
           stroke_width=6,stroke_fill="#fff5d7")
    d.text((500,y),text,anchor="mm",font=f,fill=main,
           stroke_width=3,stroke_fill="#7f1723")

def apple_silhouette(d,x,y):
    d.ellipse((x-37,y-25,x+15,y+31),fill="white")
    d.ellipse((x-4,y-28,x+41,y+31),fill="white")
    d.ellipse((x+22,y-13,x+50,y+16),fill="#b70725")
    d.ellipse((x-5,y-48,x+28,y-20),fill="white")
    d.line((x+5,y-28,x+23,y-52),fill="white",width=8)

for i,info in enumerate(META,1):
    srcpath=SRC/f"scene-{i:02}.png"
    assert srcpath.is_file(), srcpath
    with Image.open(srcpath) as src:
        src.load()
        assert src.width>=1000 and src.height>=1500, (i,src.size)
        source=src.convert("RGB")
    # Avoid cropping children's faces or Santa's device to force the 2:3 canvas.
    background=ImageOps.fit(source,(1000,1500),Image.Resampling.LANCZOS)
    background=background.filter(ImageFilter.GaussianBlur(26)).convert("RGBA")
    full=ImageOps.contain(source,(1000,1500),Image.Resampling.LANCZOS).convert("RGBA")
    assert full.width<=1000 and full.height<=1500
    background.alpha_composite(full,((1000-full.width)//2,(1500-full.height)//2))
    overlay=Image.new("RGBA",(1000,1500),(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    # Legible headline panel, completely within Pinterest safe margins.
    d.rounded_rectangle((39,39,961,381),radius=47,
                        fill=(31,53,40,233),outline=(255,211,117,255),width=7)
    d.rounded_rectangle((54,54,946,366),radius=39,
                        outline=(255,249,231,245),width=3)
    # Decorative gold lights at margins, never interfering with copy.
    rng=random.Random(20261022+i*11)
    for j in range(38):
        x=rng.choice((rng.randint(76,115),rng.randint(885,924)))
        y=rng.randint(77,333)
        rad=rng.choice((2,3,4,5))
        col=rng.choice(("#ffe3a5","#fff8d4","#f5b76e"))
        d.ellipse((x-rad,y-rad,x+rad,y+rad),fill=col)
    raised(d,info["top"],145,"#ff4135")
    raised(d,info["bottom"],269,"#ffd246")
    # Distinct real-English prompt in cream plaque.
    d.rounded_rectangle((48,1133,952,1253),radius=53,
                        fill=(255,247,224,251),outline="#ffca77",width=7)
    d.rounded_rectangle((63,1146,937,1240),radius=43,
                        outline="#e7a55e",width=2)
    sf=text_font(d,info["subtitle"],832,69,46)
    d.text((500,1192),info["subtitle"],font=sf,anchor="mm",
           fill="#a6092b")
    # Matching glossy Christmas-red iPhone call-to-action.
    d.rounded_rectangle((46,1289,954,1455),radius=77,
                        fill="#f7ca6a")
    d.rounded_rectangle((57,1300,943,1445),radius=70,
                        fill="#c30029",outline="#fff9ec",width=6)
    d.rounded_rectangle((68,1312,931,1433),radius=60,
                        outline="#ff8d68",width=3)
    for yy in range(1312,1355):
        alpha=int(38*(1-(yy-1312)/43))
        d.line((155,yy,873,yy),fill=(255,255,255,alpha),width=1)
    apple_silhouette(d,167,1370)
    d.text((590,1350),"Try Call Santa",anchor="mm",
           font=text_font(d,"Try Call Santa",620,59,60),fill="white")
    d.text((590,1401),"on iPhone",anchor="mm",
           font=text_font(d,"on iPhone",560,53,52),fill="white")
    result=Image.alpha_composite(background,overlay).convert("RGB")
    outfile=OUT/f"call-santa-20261022-{i:02}.png"
    result.save(outfile,"PNG",optimize=True)
    with Image.open(outfile) as verified:
        assert verified.size==(1000,1500),(outfile,verified.size)
        verified.verify()
    assert outfile.stat().st_size>100000
    print("VALID PIN",i,outfile.stat().st_size,info["top"],info["bottom"])

header=["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"]
base="https://raw.githubusercontent.com/shsweb/pinterest-pregnancy-pins/main/santa/fun-calls-new-20261022-20/images/"
app="https://apps.apple.com/us/app/call-santa-talk-video/id6808839679"
rows=[]
for i,info in enumerate(META,1):
    rows.append([info["title"],
                 base+f"call-santa-20261022-{i:02}.png",
                 "Christmas Activities for Kids","",
                 info["description"]+" Try Call Santa: Talk & Video on iPhone.",
                 app+f"?ct=pinterest-oct22-new20-{i:02}","",
                 "Santa video call,Christmas activities for kids,Call Santa on iPhone,holiday fun"])
csvpath=ROOT/"pinterest_santa_20_BULK_READY.csv"
with csvpath.open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.writer(f,lineterminator="\r\n",quoting=csv.QUOTE_ALL)
    w.writerow(header)
    w.writerows(rows)
with csvpath.open(encoding="utf-8-sig",newline="") as f:
    r=list(csv.DictReader(f))
assert len(r)==20
for i,row in enumerate(r,1):
    assert row["Media URL"].endswith(f"/call-santa-20261022-{i:02}.png")
    assert row["Link"].startswith(app)
    assert (OUT/f"call-santa-20261022-{i:02}.png").is_file()

# A CONTACT SHEET FOR REVIEW ONLY, NOT A PIN IMAGE.
w,h,gap=228,342,12
sheet=Image.new("RGB",(5*(w+gap)+gap,4*(h+gap)+gap),(255,249,240))
for j in range(20):
    with Image.open(OUT/f"call-santa-20261022-{j+1:02}.png") as im:
        im=im.resize((w,h),Image.Resampling.LANCZOS)
    sheet.paste(im,(gap+(j%5)*(w+gap),gap+(j//5)*(h+gap)))
sheet.save(ROOT/"preview_20.jpg",quality=90,optimize=True)
print("COMPLETE: 20 UNIQUE ORIGINAL PINS + VERIFIED PINTEREST CSV")
