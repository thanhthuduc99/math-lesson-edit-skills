from pathlib import Path

from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30
config.background_color = WHITE

HERE = Path(__file__).parent
BRAND, BRAND_URL, TEACHER = "TENSCHOOL", "tenschool.vn", "Thầy Đỗ Văn Đức"  # đổi theo khách
# assets/badge_photo.png: crop mặt giáo viên từ 1 khung webcam (~320x330)
UI = "Segoe UI"
UIB = "Segoe UI Black"
HEAD = "Bahnschrift"
MATH = "Cambria Math"
INK = "#151515"
GREY = "#4A4A4A"
LINE = "#BDBDBD"
PINK = "#D6246E"
PINK_D = "#8E1247"
PINK_L = "#FBE3EE"
RED = "#9B1B1B"
BLUE = "#2563EB"
SH = np.array([0.07, -0.07, 0])


def T(s, size=36, color=INK, font=UI, weight=NORMAL):
    return Text(s, font=font, font_size=size, color=color, weight=weight)


def M(s, size=40, color=INK):
    return Text(s, font=MATH, font_size=size, color=color)


def frac(n, d, size=40, color=INK, sign=""):
    num, den = M(n, size * 0.8, color), M(d, size * 0.8, color)
    bar = Line(LEFT, RIGHT, stroke_width=2.5, color=color).set_width(max(num.width, den.width) + 0.12)
    f = VGroup(num, bar, den).arrange(DOWN, buff=0.07)
    if sign:
        s = M(sign, size, color)
        return VGroup(s, f).arrange(RIGHT, buff=0.08)
    return f


def row(*items, buff=0.14):
    return VGroup(*items).arrange(RIGHT, buff=buff)


def shadow_box(mob, fill=WHITE, stroke=INK, shadow=INK, sw=3, pad=(0.22, 0.12), r=0.12, w=None, h=None):
    w = w or mob.width + 2 * pad[0]
    h = h or mob.height + 2 * pad[1]
    sh = RoundedRectangle(width=w, height=h, corner_radius=r, fill_color=shadow, fill_opacity=1, stroke_width=0)
    bx = RoundedRectangle(width=w, height=h, corner_radius=r, fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=sw)
    bx.move_to(mob)
    sh.move_to(bx).shift(SH)
    return VGroup(sh, bx, mob)


def chip(s, kind="outline", size=20):
    if kind == "pink":
        return shadow_box(T(s, size, WHITE, UI, BOLD), fill=PINK, stroke=PINK, shadow=PINK_D, sw=2, pad=(0.2, 0.1), r=0.1)
    if kind == "dark":
        return shadow_box(T(s, size, WHITE, UI, BOLD), fill=INK, stroke=INK, shadow=PINK, sw=2, pad=(0.2, 0.1), r=0.1)
    return shadow_box(T(s, size, INK, UI, BOLD), fill=WHITE, stroke=INK, shadow=INK, sw=2.5, pad=(0.2, 0.1), r=0.1)


def pill(s, size=19):
    t = T(s, size, INK, UI, BOLD)
    p = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.24, corner_radius=(t.height + 0.24) / 2,
                         fill_color=WHITE, fill_opacity=1, stroke_color=INK, stroke_width=2.5)
    return VGroup(p, t.move_to(p))


def title_text(s, size=58):
    t = T(s, size, INK, HEAD, BOLD)
    t.stretch(0.86, 0)
    if t.width > 7.7:
        t.scale_to_fit_width(7.7)
    return t


def dots_bg():
    return ImageMobject(str(HERE / "assets" / "dots_bg.png")).set_z_index(-100).scale_to_fit_height(16)


def header():
    icon = VGroup(
        RoundedRectangle(width=0.34, height=0.28, corner_radius=0.04, stroke_color=RED, stroke_width=3.5),
        Line([0, 0.14, 0], [0, -0.14, 0], color=RED, stroke_width=3.5),
        Arc(radius=0.17, start_angle=0, angle=PI, color=RED, stroke_width=3.5).shift(UP * 0.14),
    )
    name = T(BRAND, 27, RED, HEAD, BOLD)
    logo = row(icon, name, buff=0.1).move_to([-3.92, 6.5, 0], aligned_edge=LEFT)
    url = T(BRAND_URL, 21, INK, UI, BOLD).move_to([3.92, 6.5, 0], aligned_edge=RIGHT)
    rule = Line([-3.95, 6.17, 0], [3.95, 6.17, 0], color=INK, stroke_width=3)
    return VGroup(logo, url, rule)


def caption_box(s):
    txt = VGroup(*[T(l, 26, "#3A3A3A", UI, BOLD) for l in s.split("\n")]).arrange(DOWN, buff=0.1)
    if txt.width > 7.2:
        txt.scale_to_fit_width(7.2)
    sh = RoundedRectangle(width=7.6, height=1.0, corner_radius=0.14, fill_color="#D9D9D9", fill_opacity=1, stroke_width=0)
    bx = RoundedRectangle(width=7.6, height=1.0, corner_radius=0.14, fill_color=WHITE, fill_opacity=1,
                          stroke_color="#C8C8C8", stroke_width=3)
    bx.move_to([0, -3.55, 0])
    sh.move_to(bx).shift(np.array([0.05, -0.06, 0]))
    return VGroup(sh, bx, txt.move_to(bx))


def top_block(chip_mob, title, tags=None):
    chip_mob.move_to([0, 5.8, 0])
    title.move_to([0, 5.02, 0])
    g = VGroup(chip_mob, title)
    if tags is not None:
        tags.arrange(RIGHT, buff=0.18).move_to([0, 4.17, 0])
        g.add(tags)
    return g


def badge():
    photo = ImageMobject(str(HERE / "assets" / "badge_photo.png")).scale_to_fit_height(1.27)
    frame = RoundedRectangle(width=1.3, height=1.35, corner_radius=0.1, fill_color=PINK, fill_opacity=1,
                             stroke_color=INK, stroke_width=3)
    sh = frame.copy().set_fill(INK).set_stroke(width=0).shift(SH)
    photo.move_to(frame)
    lab1 = T("GIẢNG BỞI", 16, "#DDDDDD", UI, BOLD)
    lab2 = T(TEACHER, 34, WHITE, UI, BOLD)
    labs = VGroup(lab1, lab2).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
    bar = RoundedRectangle(width=labs.width + 0.4, height=0.95, corner_radius=0.08, fill_color=INK, fill_opacity=1,
                           stroke_width=0)
    bar_sh = bar.copy().set_fill(PINK).shift(SH)
    labs.move_to(bar)
    card = Group(sh, frame, photo)
    side = VGroup(bar_sh, bar, labs).next_to(frame, RIGHT, buff=0.15)
    return Group(card, side)


class CueScene(Scene):
    T0 = 0.0

    def at(self, t):
        dt = t - self.T0 - self.time
        if dt > 1e-3:
            self.wait(dt)

    def base(self):
        self.add(dots_bg(), header())

    def set_caption(self, s, rt=0.35):
        new = caption_box(s)
        old = getattr(self, "cap", None)
        if old is None:
            self.play(FadeIn(new, shift=UP * 0.15), run_time=rt)
        else:
            self.remove(old)
            self.add(new[0], new[1])
            self.play(FadeIn(new[2]), run_time=rt)
            self.remove(new[0], new[1], new[2])
            self.add(new)
        self.cap = new

    def swap_top(self, new, rt=0.45):
        old = getattr(self, "top", None)
        if old is None:
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.15) for m in new], lag_ratio=0.15), run_time=rt + 0.2)
        else:
            self.play(FadeOut(old, shift=UP * 0.15), run_time=rt * 0.6)
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.15) for m in new], lag_ratio=0.15), run_time=rt)
        self.top = new
