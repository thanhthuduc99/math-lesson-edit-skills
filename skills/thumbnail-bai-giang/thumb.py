# Usage: python thumb.py config.json
# Thumbnail 1280x720 theo style kênh thầy Đức: thanh tiêu đề màu + badge trắng, 2 hình cắt từ PDF đề
# hai bên, ảnh thầy ở giữa (PNG nền trong). Không có ảnh thầy thì để khung chờ.
import json, sys
from pathlib import Path
import pymupdf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).parent
W, H = 1280, 720
BAR = (43, 165)
BARS = {"pink": "#DF1279", "red": "#B63E3D", "blue": "#0000FE", "purple": "#62256B"}
PINK = (205, 38, 116)
FONT = str(HERE / "fonts" / "Montserrat-ExtraBold.ttf")
CONDENSED = "C:/Windows/Fonts/bahnschrift.ttf"
LEFT_BOX = (50, 215, 470, 690)
RIGHT_BOX = (805, 225, 1230, 680)
TEACHER_BOX = (490, 205, 790, 720)


def font(size, kind="wide"):
    if kind == "condensed":
        f = ImageFont.truetype(CONDENSED, size)
        f.set_variation_by_name("Bold Condensed")
        return f
    return ImageFont.truetype(FONT, size)


def bar_fill(canvas, colors):
    """1 màu hoặc [trái, phải] chuyển màu ngang."""
    y0, y1 = BAR
    if isinstance(colors, str):
        ImageDraw.Draw(canvas).rectangle((0, y0, W, y1), fill=BARS.get(colors, colors))
        return BARS.get(colors, colors)
    a, b = (Image.new("RGB", (1, 1), BARS.get(c, c)).getpixel((0, 0)) for c in colors)
    grad = Image.new("RGB", (W, 1))
    for x in range(W):
        t = x / (W - 1)
        grad.putpixel((x, 0), tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3)))
    canvas.paste(grad.resize((W, y1 - y0)), (0, y0))
    return BARS.get(colors[-1], colors[-1])


def crop_pdf(pdf, page, bbox, dpi=400):
    doc = pymupdf.open(pdf)
    pix = doc[page].get_pixmap(dpi=dpi, clip=pymupdf.Rect(*bbox), alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def to_pink(im):
    """Nét đen/xám -> hồng, giữ nguyên chỗ đã có màu."""
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = px[x, y]
            if max(r, g, b) - min(r, g, b) > 40:
                continue
            k = 1 - (r + g + b) / 765
            px[x, y] = tuple(round(255 * (1 - k) + c * k) for c in PINK)
    return im


def trim(im, pad=6):
    box = Image.eval(im.convert("L"), lambda v: 255 if v < 240 else 0).getbbox()
    if not box:
        return im
    x0, y0, x1, y1 = box
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def place(canvas, im, box):
    bw, bh = box[2] - box[0], box[3] - box[1]
    s = min(bw / im.width, bh / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    canvas.paste(im, (box[0] + (bw - im.width) // 2, box[1] + (bh - im.height) // 2))


def figure(cfg, f):
    if "image" in f:
        im = Image.open(f["image"]).convert("RGB")
    else:
        im = crop_pdf(cfg["pdf"], f["page"], f["bbox"])
    im = trim(im)
    if f.get("clear_bg"):
        # nền hồng nhạt của khung lời giải -> trắng
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                if min(px[x, y]) > 205:
                    px[x, y] = (255, 255, 255)
        im = trim(im)
    if f.get("bold", 3) > 1:
        im = im.filter(ImageFilter.MinFilter(f.get("bold", 3)))
    return to_pink(im) if f.get("pink", True) else im


def header(canvas, cfg):
    color = bar_fill(canvas, cfg.get("bar", "pink"))
    d = ImageDraw.Draw(canvas)
    kind = cfg.get("font", "wide")
    right = 1245
    badge = cfg.get("badge")
    if badge:
        bf = font(cfg.get("badge_size", (56 if len(badge) <= 6 else 38) if kind == "wide" else 56), kind)
        tw = d.textlength(badge, font=bf)
        bx0 = right - tw - 50
        d.rounded_rectangle((bx0, 52, right, 157), radius=24 if kind == "wide" else 6, fill=cfg.get("badge_bg", "white"))
        d.text(((bx0 + right) / 2, 104), badge, font=bf, fill=cfg.get("badge_color", color), anchor="mm")
        right = bx0 - 18
    size = cfg.get("title_size", 66 if kind == "wide" else 106)
    # co tới khi vừa ngang và phần có dấu cao không quá thanh (chừa 8px trên dưới)
    def ink(sz):
        return d.textbbox((0, 0), cfg["title"], font=font(sz, kind), anchor="ls")
    while size > 30 and (d.textlength(cfg["title"], font=font(size, kind)) > right - 40
                         or ink(size)[3] - ink(size)[1] > BAR[1] - BAR[0] - 16):
        size -= 2
    tw = d.textlength(cfg["title"], font=font(size, kind))
    x = 40 + (right - 40 - tw) / 2 if badge else (W - tw) / 2
    if kind == "wide":
        d.text((x, 104), cfg["title"], font=font(size, kind), fill="white", anchor="lm")
    else:
        top, bottom = ink(size)[1], ink(size)[3]
        d.text((x, (BAR[0] + BAR[1]) / 2 - (top + bottom) / 2), cfg["title"], font=font(size, kind), fill="white", anchor="ls")


def teacher(canvas, cfg):
    x0, y0, x1, y1 = TEACHER_BOX
    if cfg.get("teacher"):
        path = Path(cfg["teacher"])
        t = Image.open(path).convert("RGBA")
        t = t.crop(t.getbbox())
        # teacher/keep.json: phần trên của ảnh được giữ (ảnh toàn thân cắt tới đùi cho cỡ người đều nhau)
        keep_file = path.parent / "keep.json"
        keep = json.load(open(keep_file)).get(path.name, 1.0) if keep_file.exists() else 1.0
        t = t.crop((0, 0, t.width, round(t.height * keep)))
        s = (y1 - y0) / t.height
        t = t.resize((round(t.width * s), y1 - y0), Image.LANCZOS)
        canvas.paste(t, ((x0 + x1 - t.width) // 2, y0), t)
    elif cfg.get("placeholder", True):
        d = ImageDraw.Draw(canvas)
        d.rounded_rectangle((x0 + 20, y0, x1 - 20, y1 - 6), radius=18, outline="#C9CCD3", width=3)
        d.text(((x0 + x1) / 2, (y0 + y1) / 2), "ẢNH THẦY", font=font(30), fill="#B0B4BC", anchor="mm")


def main():
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    canvas = Image.new("RGB", (W, H), "white")
    header(canvas, cfg)
    figs = cfg["figures"]
    place(canvas, figure(cfg, figs[0]), LEFT_BOX)
    if len(figs) > 1:
        place(canvas, figure(cfg, figs[1]), RIGHT_BOX)
    teacher(canvas, cfg)
    Path(cfg["out"]).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(cfg["out"], quality=95)
    print(cfg["out"])


if __name__ == "__main__":
    main()
