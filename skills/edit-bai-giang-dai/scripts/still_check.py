# Usage: python still_check.py cut.mp4 out_dir Card1=36.0 Card2=60.5 ...
# Needs stills rendered first:  STILL=1 manim -s -t -q h cards.py Card1 Card2 ...
# Composites each card's last frame over the live frame at time t, plus a 2x2 sheet.
import sys, os, glob, subprocess
from PIL import Image

video, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
ims = []
for arg in sys.argv[3:]:
    k, t = arg.split("=")
    live = f"{out}/live_{k}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", t, "-i", video, "-frames:v", "1", live], check=True)
    fg = Image.open(sorted(glob.glob(f"media/images/cards/{k}_*.png"))[-1]).convert("RGBA")
    im = Image.alpha_composite(Image.open(live).convert("RGBA"), fg).convert("RGB")
    im.save(f"{out}/still_{k}.jpg", quality=88)
    ims.append(im.resize((960, 540)))
rows = (len(ims) + 1) // 2
sheet = Image.new("RGB", (1920, 540 * rows))
for i, im in enumerate(ims):
    sheet.paste(im, ((i % 2) * 960, (i // 2) * 540))
sheet.save(f"{out}/still_sheet.jpg", quality=88)
