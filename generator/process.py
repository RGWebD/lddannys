"""Photo processing for L&D Danny's demo (RGWebD). Source: /workspace/lead-ll1f/photos (Google Business Profile photos)."""
from PIL import Image, ImageFilter, ImageDraw, ImageOps
from pathlib import Path
SRC=Path('/workspace/lead-ll1f/photos'); A=Path(__file__).parent/'assets'/'img'; A.mkdir(parents=True,exist_ok=True)
KEEP=['g01','g03','g04','g05','g06','g07','g08','g09','g10','g11','g12','g14','g15','g16','g17','g18','g19','g20','g22','g23','g24','g25']
def blur(im,box,r=26,feather=18):
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).ellipse(box,fill=255); m=m.filter(ImageFilter.GaussianBlur(feather))
    return Image.composite(im.filter(ImageFilter.GaussianBlur(r)),im,m)
for k in KEEP:
    im=ImageOps.exif_transpose(Image.open(SRC/f'{k}.jpg')).convert('RGB')
    if k=='g17':
        im=blur(im,(700,540,850,740))   # photographer reflected in the mirror
        im=im.crop((0,0,2000,1230))      # cut off the paperwork on the counter
    if k=='g12': im=im.crop((0,470,1500,2000))  # focus on the star inlay, drop the backyard
    for w in (800,1600):
        x=im.copy()
        if x.width>w: x=x.resize((w,round(x.height*w/x.width)),Image.LANCZOS)
        x.save(A/f'{k}-{w}.webp',quality=80,method=6)
# blueprint line drawing of g16 (same room) for the compare slider
im=ImageOps.equalize(ImageOps.exif_transpose(Image.open(SRC/'g16.jpg')).convert('L').resize((1600,1200),Image.LANCZOS))
ed=im.filter(ImageFilter.GaussianBlur(2.0)).filter(ImageFilter.FIND_EDGES)
ed=ed.point(lambda v:255 if v>16 else 0)
bg=Image.new('RGB',im.size,(27,35,40)); d=ImageDraw.Draw(bg)
for x in range(0,1600,40): d.line([(x,0),(x,1200)],fill=(38,50,57) if x%200 else (48,63,72),width=1)
for y in range(0,1200,40): d.line([(0,y),(1600,y)],fill=(38,50,57) if y%200 else (48,63,72),width=1)
line=Image.new('RGB',im.size,(232,222,204)); bg.paste(line,(0,0),ed.point(lambda v:int(v*.85)))
for w in (800,1600): bg.resize((w,w*3//4),Image.LANCZOS).save(A/f'bp16-{w}.webp',quality=82,method=6)
print('ok')
