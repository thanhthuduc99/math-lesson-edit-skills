# Usage: python figs.py bai-giang.pdf [figs.jpg]
# Liệt kê mọi hình trong PDF bài giảng (page + bbox để dán vào config) và ghép sheet có đánh số để chọn.
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont

pdf = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "figs.jpg"
doc = pymupdf.open(pdf)
items = []
for i, page in enumerate(doc):
    for info in page.get_image_info():
        r = pymupdf.Rect(info["bbox"]) & page.rect
        if r.width >= 60 and r.height >= 40:
            items.append((i, [round(v) for v in r]))

tiles = []
label = ImageFont.load_default(16)
for k, (i, b) in enumerate(items):
    print(f'{k}: {{"page": {i}, "bbox": {b}}}')
    pix = doc[i].get_pixmap(dpi=96, clip=pymupdf.Rect(*b))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    im.thumbnail((240, 180))
    t = Image.new("RGB", (250, 210), "white")
    t.paste(im, (5, 25))
    ImageDraw.Draw(t).text((5, 3), f"{k}  p{i}", fill="red", font=label)
    tiles.append(t)

cols = 6
sheet = Image.new("RGB", (cols * 250, max(1, -(-len(tiles) // cols)) * 210), "#ddd")
for k, t in enumerate(tiles):
    sheet.paste(t, ((k % cols) * 250, (k // cols) * 210))
sheet.save(out, quality=85)
print(out)
