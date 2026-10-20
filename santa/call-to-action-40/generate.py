from pathlib import Path
from PIL import Image, ImageFilter
import csv

ROOT = Path("santa/call-to-action-40")
SRC1 = Path("/tmp/santa-cta-src-1.png")
SRC2 = Path("/tmp/santa-cta-src-2.png")
APP = "https://apps.apple.com/us/app/call-santa-talk-video/id6808839679"
BASE = "https://raw.githubusercontent.com/shsweb/pinterest-pregnancy-pins/main/santa/call-to-action-40"
BOARD = "Christmas Activities for Kids"
A = [
 "Santa Heard Your Christmas Wish", "Santa Lost His Cookies",
 "Santa Snowball Fight", "Santa Silly Selfie",
 "Who Wrapped the Reindeer", "Santa Midnight Snack",
 "Explore the North Pole with Santa", "Santa Secret Christmas Map",
 "Find the Hidden Present with Santa", "Build a Snowman with Santa",
 "Santa Christmas Bedtime Story", "Santa Pet Friends",
 "Santa Magic Phone Call", "Sing Christmas Songs with Santa",
 "Meet Santa's Happy Elves", "Santa Nice List Surprise",
 "Visit Santa Toy Workshop", "Fly with Santa in His Sleigh",
 "Send a Letter to Santa", "Open a Surprise Gift with Santa",
 "Santa Good Night Christmas Call"
]
B = [
 "Santa Heard Your Wish Tonight", "Call Santa Right Now",
 "Santa Cookie Hunt", "Santa Snowball Battle",
 "Santa Magic Phone Surprise", "Santa and the Tangled Reindeer",
 "Santa Midnight Cookies and Milk", "Discover the North Pole with Santa",
 "Santa Magical Christmas Stories", "Talk to Santa Live on iPhone",
 "Meet Santa and His Elves", "Snowman Building with Santa",
 "Peek Inside Santa's Workshop", "Sing Christmas Carols with Santa",
 "Countdown to Christmas with Santa", "Help Santa Deliver Presents",
 "Share Your Christmas Wish with Santa", "Meet Santa's Reindeer Family",
 "Santa Bedtime Goodnight Call"
]
assert len(A) == 21 and len(B) == 19
entries = [("A",i,A[i]) for i in range(20)] + [("A",20,A[20])] + [("B",i,B[i]) for i in range(19)]
assert len(entries) == 40
srca = Image.open(SRC1).convert("RGB")
srcb = Image.open(SRC2).convert("RGB")
assert srca.size == (1536,1024) and srcb.size == (1536,1024), (srca.size,srcb.size)

def extract(which,idx):
    if which == "A":
        cc = idx % 7
        rr = idx // 7
        w,h = srca.size
        return srca.crop((int(cc*w/7)+2,int(rr*h/3)+2,
                          int((cc+1)*w/7)-2,int((rr+1)*h/3)-2))
    w,h = srcb.size
    if idx < 9:
        cols = 9
        col = idx
        y0,y1 = 0,h//2
    else:
        cols = 10
        col = idx-9
        y0,y1 = h//2,h
    return srcb.crop((int(col*w/cols)+2,y0+3,
                      int((col+1)*w/cols)-2,y1-3))

columns = ["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"]
all_rows = []
for batch in (1,2):
    folder = ROOT/f"batch-{batch:02}"
    images = folder/"images"
    images.mkdir(parents=True,exist_ok=True)
    rows = []
    for index,(which,source_id,label) in enumerate(entries[(batch-1)*20:batch*20],1):
        name = f"call-santa-b{batch:02}-{index:02}.jpg"
        im = extract(which,source_id).resize((1000,1500),Image.Resampling.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=2.2,percent=95,threshold=3))
        im.save(images/name,format="JPEG",quality=93,subsampling=0,optimize=True)
        assert (images/name).stat().st_size > 25000
        title = f"{label} | Call Santa Christmas Video App"
        description = (
            f"{label}! Give your family a joyful, festive moment with Call Santa: Talk & Video. "
            "Explore Santa-themed calls on iPhone and iPad, and add more Christmas magic "
            "to your holiday traditions. Try the Call Santa app today! "
            "#SantaClaus #ChristmasForKids #CallSanta"
        )
        media = f"{BASE}/batch-{batch:02}/images/{name}"
        link = f"{APP}?ct=santa-cta40-b{batch:02}-{index:02}"
        rows.append([title,media,BOARD,"",description,link,"",
                     "Santa video call,call Santa,Christmas activities for kids,Christmas Santa fun"])
    with (folder/f"pinterest_santa_batch_{batch:02}_20.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w = csv.writer(f); w.writerow(columns); w.writerows(rows)
    all_rows.extend(rows)
    print(f"Rendered batch {batch} with {len(rows)} JPG images and CSV")
with (ROOT/"pinterest_santa_40_ALL.csv").open("w",encoding="utf-8-sig",newline="") as f:
    w = csv.writer(f); w.writerow(columns);w.writerows(all_rows)
assert len(all_rows) == 40
print("All 40 images and CSV files generated successfully")
