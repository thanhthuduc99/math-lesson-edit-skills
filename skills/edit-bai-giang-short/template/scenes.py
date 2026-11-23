import json
from common import *

PTS = [(1, 6), (2, 16), (3, 26)]


def v(t):
    return -2 / 3 * t ** 3 + 4 * t ** 2 + 8 / 3 * t


def s(t):
    return -t ** 4 / 6 + 4 * t ** 3 / 3 + 4 * t ** 2 / 3


def make_axes():
    ax = Axes(x_range=[0, 5.6, 1], y_range=[0, 36, 10], x_length=6.9, y_length=3.55,
              axis_config={"color": INK, "stroke_width": 3, "include_tip": True, "tip_length": 0.2, "tip_width": 0.18})
    ax.shift([-3.25, 0.15, 0] - ax.c2p(0, 0))
    lab = VGroup(
        *[M(str(i), 26, GREY).next_to(ax.c2p(i, 0), DOWN, 0.12) for i in range(1, 6)],
        *[M(str(j), 26, GREY).next_to(ax.c2p(0, j), LEFT, 0.12) for j in (10, 20, 30)],
        M("O", 26, GREY).next_to(ax.c2p(0, 0), DL, 0.06),
        M("t (s)", 28, INK).next_to(ax.x_axis.get_end(), DOWN, 0.15).shift(LEFT * 0.15),
        M("v (m/s)", 28, INK).next_to(ax.y_axis.get_end(), RIGHT, 0.15),
    )
    ticks = VGroup(*[Line(ax.c2p(i, 0) + DOWN * 0.06, ax.c2p(i, 0) + UP * 0.06, color=INK, stroke_width=3) for i in range(1, 6)],
                   *[Line(ax.c2p(0, j) + LEFT * 0.06, ax.c2p(0, j) + RIGHT * 0.06, color=INK, stroke_width=3) for j in (10, 20, 30)])
    return ax, VGroup(ticks, lab)


def pdot(ax, x, y, color=PINK):
    return Dot(ax.c2p(x, y), radius=0.1, color=color, stroke_color=INK, stroke_width=2.5).set_z_index(5)


def plabel(ax, x, y, color=PINK):
    return M(f"({x}; {y})", 26, color).next_to(ax.c2p(x, y), RIGHT, 0.14).shift(DOWN * 0.16).set_z_index(5)


def car(x, y_road, ang=0.0):
    lower = RoundedRectangle(width=1.5, height=0.3, corner_radius=0.1, fill_color=PINK, fill_opacity=1,
                             stroke_color=INK, stroke_width=3).move_to([0, 0.27, 0])
    cabin = Polygon([-0.5, 0.41, 0], [-0.28, 0.68, 0], [0.3, 0.68, 0], [0.6, 0.41, 0], fill_color=PINK, fill_opacity=1,
                    stroke_color=INK, stroke_width=3)
    win = Polygon([-0.38, 0.45, 0], [-0.23, 0.62, 0], [0.24, 0.62, 0], [0.46, 0.45, 0], fill_color="#DDEAF6",
                  fill_opacity=1, stroke_color=INK, stroke_width=2)
    pillar = Line([0.02, 0.45, 0], [0.02, 0.62, 0], color=INK, stroke_width=2.5)
    light = Dot([0.7, 0.3, 0], radius=0.04, color="#FFD166")
    wheels = VGroup()
    for wx in (-0.45, 0.45):
        c = Circle(radius=0.15, fill_color=INK, fill_opacity=1, stroke_color=INK).move_to([wx, 0.15, 0])
        hub = Circle(radius=0.07, fill_color="#CFCFCF", fill_opacity=1, stroke_width=0).move_to(c)
        sp = Line(c.get_center() + 0.12 * np.array([np.cos(ang), np.sin(ang), 0]),
                  c.get_center() - 0.12 * np.array([np.cos(ang), np.sin(ang), 0]), color="#CFCFCF", stroke_width=3)
        wheels.add(VGroup(c, hub, sp))
    g = VGroup(lower, cabin, win, pillar, light, wheels)
    g.shift([x, y_road, 0])
    return g


ROAD_Y = 2.3
XS = lambda tau: -3.45 + 6.95 * s(tau) / s(3)


def road():
    base = Line([-4.3, ROAD_Y, 0], [4.3, ROAD_Y, 0], color=INK, stroke_width=4)
    dash = DashedLine([-4.3, ROAD_Y - 0.14, 0], [4.3, ROAD_Y - 0.14, 0], color=LINE, stroke_width=3, dash_length=0.18)
    return VGroup(base, dash)


def flag(k):
    x = XS(k)
    tick = Line([x, ROAD_Y + 0.08, 0], [x, ROAD_Y - 0.25, 0], color=PINK, stroke_width=5)
    lab = M(f"{k}s", 26, PINK if k else GREY).next_to(tick, DOWN, 0.06)
    return VGroup(tick, lab)


def table():
    w0, w, h = 2.75, 1.25, 0.72
    cells = VGroup()
    heads = [M("t (giây)", 30), M("v(t) (m/s)", 30)]
    nums = [["1", "2", "3"], ["6", "16", "26"]]
    x0 = -(w0 + 3 * w) / 2
    grid = VGroup()
    bgs = VGroup()
    vals = [VGroup(), VGroup()]
    for r in range(2):
        y = h / 2 - r * h
        bg = Rectangle(width=w0, height=h, fill_color=PINK_L, fill_opacity=1, stroke_width=0).move_to([x0 + w0 / 2, y, 0])
        bgs.add(bg)
        heads[r].move_to(bg)
        for c in range(3):
            cx = x0 + w0 + w * c + w / 2
            vals[r].add(M(nums[r][c], 36, INK if r == 0 else PINK).move_to([cx, y, 0]))
    W, H = w0 + 3 * w, 2 * h
    frame = Rectangle(width=W, height=H, stroke_color=INK, stroke_width=3)
    grid.add(Line([x0, 0, 0], [x0 + W, 0, 0], color=INK, stroke_width=2.5))
    for c in range(3):
        xx = x0 + w0 + w * c
        grid.add(Line([xx, H / 2, 0], [xx, -H / 2, 0], color=INK, stroke_width=2.5))
    sh = Rectangle(width=W, height=H, fill_color=INK, fill_opacity=1, stroke_width=0).shift(SH)
    body = VGroup(sh, Rectangle(width=W, height=H, fill_color=WHITE, fill_opacity=1, stroke_width=0), bgs, grid, frame,
                  heads[0], heads[1])
    return body, vals


def formula():
    f = M("v(t) = at³ + bt² + ct + d", 46)
    return shadow_box(f, stroke=PINK, shadow=INK, pad=(0.3, 0.16)), f


class S1Intro(CueScene):
    T0 = 0.0

    def construct(self):
        self.base()
        top = VGroup(pill("ĐỀ GIỮA HỌC KÌ 1 · TOÁN 12").move_to([0, 5.8, 0]),
                     title_text("TÌM HÀM BẬC BA TỪ BẢNG SỐ").move_to([0, 5.02, 0]),
                     VGroup(chip("THPT Nguyễn Khuyến", "pink"), chip("Phần III · Câu 1")).arrange(RIGHT, buff=0.2).move_to([0, 4.17, 0]))
        ax = Axes(x_range=[0, 5.3, 1], y_range=[0, 36, 10], x_length=4.6, y_length=2.5,
                  axis_config={"color": INK, "stroke_width": 3, "include_tip": True, "tip_length": 0.18, "tip_width": 0.16})
        ax.shift([-1.9, 1.05, 0] - ax.c2p(0, 0))
        curve = ax.plot(v, x_range=[0, 5], color=PINK, stroke_width=6)
        dts = VGroup(*[pdot(ax, x, y) for x, y in [(0, 0)] + PTS])
        q = pdot(ax, 5, 30, WHITE)
        ql = M("v(5) = ?", 32, PINK).next_to(q, UP, 0.15).shift(LEFT * 0.2)
        cr = car(0, 0).scale(0.75).next_to(ax.c2p(0.2, 30), RIGHT, 0)
        bd = badge().scale(0.85).move_to([0, -1.5, 0])
        self.swap_top(top, 0.6)
        self.set_caption("Ô tô tăng tốc, đo tốc độ ở giây 1, 2, 3.\nHỏi tốc độ ở giây thứ 5 là bao nhiêu?", 0.3)
        self.play(Create(ax), FadeIn(cr, shift=RIGHT * 0.3), run_time=0.6)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dts], lag_ratio=0.25), run_time=0.7)
        self.play(Create(curve), FadeIn(q), FadeIn(ql), FadeIn(bd, shift=UP * 0.2), run_time=1.0)
        self.at(4.9)


class S2DeBai(CueScene):
    T0 = 4.9

    def construct(self):
        self.base()
        top = top_block(chip("ĐỀ BÀI", "dark"), title_text("Ô TÔ TĂNG TỐC"),
                        VGroup(chip("t = 0: đứng yên", "pink"), chip("Đo tại giây 1, 2, 3")))
        self.swap_top(top, 0.45)
        self.set_caption("Lúc t = 0, chiếc xe đứng yên.", 0.25)
        rd = road()
        tau = ValueTracker(0)
        c = always_redraw(lambda: car(XS(tau.get_value()), ROAD_Y, -(XS(tau.get_value()) - XS(0)) / 0.15))
        f0 = flag(0)
        self.play(Create(rd), FadeIn(c, shift=RIGHT * 0.2), FadeIn(f0), run_time=0.6)
        clock = always_redraw(lambda: M(f"t = {tau.get_value():.1f} s", 30, GREY).move_to([3.25, 3.55, 0]))
        self.at(7.3)
        self.set_caption("Sau đó xe nổ máy và tăng tốc rất nhanh.")
        self.play(FadeIn(clock), run_time=0.3)
        flags = VGroup()
        for k, rt in zip((1, 2, 3), (1.7, 1.5, 1.4)):
            self.play(tau.animate.set_value(k), run_time=rt, rate_func=linear)
            fk = flag(k)
            flags.add(fk)
            self.add(fk)
            if k == 1:
                self.set_caption("Máy bắn tốc độ đo tốc độ tức thời\ntại giây thứ 1, 2 và 3.", 0.2)
        self.at(14.3)
        for k, t in zip(range(3), (14.3, 14.8, 15.1)):
            self.at(t)
            self.play(Indicate(flags[k], color=PINK, scale_factor=1.4), run_time=0.3)
        tb, vals = table()
        tb.move_to([0, 0.75, 0])
        for r in vals:
            r.shift([0, 0.75, 0])
        self.at(15.6)
        self.set_caption("Kết quả đo cho trong bảng.", 0.2)
        self.play(FadeIn(tb, shift=UP * 0.2), FadeOut(clock), run_time=0.45)
        for k, t in enumerate((16.85, 17.25, 17.5)):
            self.at(t)
            self.play(FadeIn(vals[0][k], scale=1.4), run_time=0.2)
        for k, t in enumerate((18.4, 19.15, 19.5)):
            self.at(t)
            sp = M(["6", "16", "26"][k] + " m/s", 28, PINK).move_to([XS(k + 1) - (0.2 if k == 2 else 0), 3.5, 0])
            self.play(FadeIn(vals[1][k], scale=1.4), FadeIn(sp, shift=UP * 0.1), run_time=0.25)
        self.at(19.8)
        self.set_caption("Trong 5 giây đầu, tốc độ tức thời v(t)\nlà một hàm số bậc ba.")
        fb, f = formula()
        fb.move_to([0, -1.05, 0])
        self.at(25.7)
        self.play(FadeIn(fb, shift=UP * 0.2), run_time=0.5)
        self.at(27.7)
        top2 = top_block(chip("CÂU HỎI", "dark"), title_text("TỐC ĐỘ Ở GIÂY THỨ 5?"),
                         VGroup(chip("v(t) bậc ba", "pink"), chip("Tìm v(5)")))
        self.swap_top(top2, 0.4)
        self.set_caption("Hỏi: tại thời điểm 5 giây,\nxe chạy bao nhiêu mét/giây?", 0.2)
        qlab = chip("CẦN TÌM", "pink", 22)
        qv = M("v(5) = ?", 44, INK)
        qb = shadow_box(qv, stroke=INK, shadow=PINK, pad=(0.3, 0.14))
        qg = VGroup(qlab, qb).arrange(RIGHT, buff=0.25).move_to([0, -2.25, 0])
        self.at(28.85)
        self.play(FadeIn(qg, shift=UP * 0.2), run_time=0.45)
        self.at(34.5)
        self.set_caption("Tốc độ xe đo bởi v(t),\nchính là tốc độ tức thời.")
        self.at(37.4)
        self.play(Circumscribe(f[0:4], color=PINK, buff=0.08), run_time=0.9)
        self.at(38.9)
        self.set_caption("Vậy đề bài yêu cầu tìm v(5).")
        self.at(43.1)
        self.play(Indicate(qv, color=PINK, scale_factor=1.15), run_time=0.8)
        self.at(44.7)


def eq_rows():
    left = [M("v(0) = 0", 34), M("v(1) = 6", 34), M("v(2) = 16", 34), M("v(3) = 26", 34)]
    right = [M("d = 0", 34), M("a + b + c = 6", 34), M("8a + 4b + 2c = 16", 34), M("27a + 9b + 3c = 26", 34)]
    arrows = VGroup()
    ys = [-0.68, -1.25, -1.82, -2.39]
    for i, y in enumerate(ys):
        left[i].move_to([-1.25, y, 0], aligned_edge=RIGHT)
        arrows.add(M("⇒", 34, PINK).move_to([-0.8, y, 0]))
        right[i].move_to([-0.35, y, 0], aligned_edge=LEFT)
    return VGroup(*left), arrows, VGroup(*right)


class S3Buoc1(CueScene):
    T0 = 44.7

    def construct(self):
        self.base()
        top = top_block(chip("BƯỚC 1", "dark"), title_text("LẬP HỆ PHƯƠNG TRÌNH"),
                        VGroup(chip("3 điểm từ bảng", "pink"), chip("+ điểm gốc O")))
        self.swap_top(top, 0.45)
        self.set_caption("Muốn tính v(5), cần tìm ra a, b, c, d.", 0.25)
        ax, deco = make_axes()
        self.play(Create(ax), FadeIn(deco), run_time=0.8)
        self.at(47.6)
        self.set_caption("Đề bài đã cho sẵn giá trị của v(t)\ntại t = 1, 2, 3.")
        dots, labs = VGroup(), VGroup()
        for (x, y), t in zip(PTS, (50.1, 50.9, 52.4)):
            self.at(t)
            d, l = pdot(ax, x, y), plabel(ax, x, y)
            guide = DashedLine(ax.c2p(x, 0), ax.c2p(x, y), color=LINE, stroke_width=2.5, dash_length=0.1)
            dots.add(d)
            labs.add(l)
            self.play(Create(guide), GrowFromCenter(d), FadeIn(l), run_time=0.35)
        self.at(53.0)
        self.set_caption("Có 4 ẩn a, b, c, d\nnhưng mới có 3 phương trình.")
        c4 = chip("4 ẩn: a, b, c, d", "outline", 26)
        c3 = chip("3 phương trình", "outline", 26)
        cmp = VGroup(c4, c3).arrange(RIGHT, buff=0.35).move_to([0, -1.2, 0])
        self.at(53.3)
        self.play(FadeIn(c4, shift=UP * 0.15), run_time=0.3)
        self.at(55.2)
        self.play(FadeIn(c3, shift=UP * 0.15), run_time=0.3)
        self.at(56.4)
        self.set_caption("Vẫn còn thiếu 1 dữ kiện nữa?", 0.2)
        qm = T("?", 60, PINK, HEAD, BOLD).next_to(cmp, DOWN, 0.2)
        self.play(FadeIn(qm, scale=1.5), run_time=0.3)
        self.at(59.7)
        self.set_caption("Lúc đầu t = 0 xe đứng yên,\nnghĩa là v(0) = 0.")
        self.at(60.6)
        o = pdot(ax, 0, 0)
        ring = Circle(radius=0.22, color=PINK, stroke_width=4).move_to(o)
        ol = M("(0; 0)", 26, PINK).next_to(ax.c2p(0, 0), LEFT, 0.14).shift(UP * 0.12)
        self.play(GrowFromCenter(o), Create(ring), FadeIn(ol), FadeOut(deco[1][8]), run_time=0.4)
        self.play(FadeOut(ring, scale=1.8), run_time=0.4)
        self.at(65.7)
        c4b = chip("4 phương trình", "pink", 26).move_to(c3)
        self.set_caption("Đủ 4 phương trình cho 4 ẩn,\ntìm được a, b, c, d.")
        self.play(FadeOut(qm), FadeOut(c3), FadeIn(c4b, scale=1.2), run_time=0.4)
        L, A, R = eq_rows()
        self.at(69.4)
        self.set_caption("v(0) = 0 cho ta d = 0.")
        self.play(FadeOut(VGroup(c4, c4b)), FadeIn(L[0]), Indicate(o, color=PINK, scale_factor=1.6), run_time=0.45)
        self.at(70.8)
        self.play(FadeIn(A[0]), FadeIn(R[0], shift=RIGHT * 0.15), run_time=0.35)
        cues = [(71.3, 72.2), (74.6, 76.1), (83.6, 84.3)]
        caps = ["v(1) = 6: thay t = 1 vào v(t).", "v(2) = 16: thay t = 2 vào v(t).", "v(3) = 26: thay t = 3 vào v(t)."]
        for i, (t1, t2) in enumerate(cues):
            self.at(t1)
            self.set_caption(caps[i], 0.2)
            self.play(FadeIn(L[i + 1]), Indicate(dots[i], color=PINK, scale_factor=1.6), run_time=0.4)
            self.at(t2)
            self.play(FadeIn(A[i + 1]), Write(R[i + 1]), run_time=1.0 if i else 0.8)
        self.at(89.7)


class S4Giai(CueScene):
    T0 = 89.7

    def construct(self):
        self.base()
        old_top = top_block(chip("BƯỚC 1", "dark"), title_text("LẬP HỆ PHƯƠNG TRÌNH"),
                            VGroup(chip("3 điểm từ bảng", "pink"), chip("+ điểm gốc O")))
        self.add(old_top)
        self.top = old_top
        self.cap = caption_box("v(3) = 26: thay t = 3 vào v(t).")
        self.add(self.cap)
        ax, deco = make_axes()
        dots = VGroup(*[pdot(ax, x, y) for x, y in [(0, 0)] + PTS])
        labs = VGroup(*[plabel(ax, x, y) for x, y in PTS], M("(0; 0)", 26, PINK).next_to(ax.c2p(0, 0), LEFT, 0.14).shift(UP * 0.12))
        guides = VGroup(*[DashedLine(ax.c2p(x, 0), ax.c2p(x, y), color=LINE, stroke_width=2.5, dash_length=0.1) for x, y in PTS])
        L, A, R = eq_rows()
        deco[1][8].set_opacity(0)
        self.add(ax, deco, guides, dots, labs, L, A, R)

        top = top_block(chip("BƯỚC 2", "dark"), title_text("GIẢI HỆ 3 ẨN"),
                        VGroup(chip("d = 0", "pink"), chip("Bấm máy tính")))
        self.swap_top(top, 0.4)
        self.set_caption("Giải hệ là tìm được a, b, c ngay.", 0.2)
        sysg = VGroup(*[R[i].copy() for i in (1, 2, 3)])
        targets = VGroup(*[R[i].copy() for i in (1, 2, 3)]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-3.45, -1.45, 0], aligned_edge=LEFT)
        brace = M("{", 120, INK).stretch_to_fit_height(targets.height + 0.25).next_to(targets, LEFT, 0.08)
        self.play(FadeOut(L), FadeOut(A), FadeOut(R[0]), *[Transform(R[i], targets[i - 1]) for i in (1, 2, 3)], run_time=0.6)
        self.play(FadeIn(brace), run_time=0.3)
        eqv = M("⇔", 40, PINK).next_to(targets, RIGHT, 0.3)
        res = VGroup(row(M("a =", 36), frac("2", "3", 36, PINK, "−")),
                     row(M("b =", 36), M("4", 36, PINK)),
                     row(M("c =", 36), frac("8", "3", 36, PINK))).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        res.next_to(eqv, RIGHT, 0.3)
        res_box = shadow_box(res, stroke=PINK, shadow=INK, pad=(0.22, 0.12))
        self.play(FadeIn(eqv), FadeIn(res_box[0:2]), run_time=0.3)
        for k, t in enumerate((92.6, 93.8, 94.8)):
            self.at(t)
            if k == 0:
                self.set_caption("a = −2/3,  b = 4,  c = 8/3.", 0.2)
            self.play(FadeIn(res[k], shift=RIGHT * 0.15), run_time=0.35)

        self.at(96.0)
        top3 = top_block(chip("BƯỚC 3", "dark"), title_text("THAY t = 5 VÀO v(t)"),
                         VGroup(chip("v(t) đã biết", "pink"), chip("Dóng t = 5")))
        self.swap_top(top3, 0.4)
        self.set_caption("Do đó ta có hàm vận tốc v(t).", 0.2)
        self.play(FadeOut(VGroup(R[1], R[2], R[3], brace, eqv)), FadeOut(res_box[0:2]), FadeOut(res), run_time=0.4)
        p0 = M("v(t) =", 42)
        p1 = row(frac("2", "3", 42, INK, "−"), M("t³", 42), buff=0.06)
        p2 = M("+ 4t²", 42)
        p3 = row(M("+", 42), frac("8", "3", 42), M("t", 42), buff=0.08)
        vt = row(p0, p1, p2, p3, buff=0.16).move_to([0, -1.05, 0])
        vbox = shadow_box(vt, stroke=PINK, shadow=INK, pad=(0.3, 0.12))
        self.play(FadeIn(vbox[0:2]), FadeIn(p0), run_time=0.35)
        curve = ax.plot(v, x_range=[0, 5], color=PINK, stroke_width=6).set_z_index(3)
        self.at(98.4)
        self.play(FadeIn(p1, shift=RIGHT * 0.1), Create(curve, rate_func=linear), run_time=2.9)
        self.add(curve)
        self.at(101.3)
        self.play(FadeIn(p2, shift=RIGHT * 0.1), run_time=0.4)
        self.at(102.3)
        self.play(FadeIn(p3, shift=RIGHT * 0.1), run_time=0.4)
        self.at(104.5)
        self.set_caption("Cần tìm v(5): thay t = 5 vào là xong.")
        vline = DashedLine(ax.c2p(5, 0), ax.c2p(5, 30), color=PINK, stroke_width=4, dash_length=0.12)
        self.at(106.2)
        self.play(Create(vline), Indicate(deco[1][4], color=PINK, scale_factor=1.6), run_time=0.6)
        self.at(108.3)
        hl = DashedLine(ax.c2p(5, 30), ax.c2p(0, 30), color=PINK, stroke_width=4, dash_length=0.12)
        p5 = pdot(ax, 5, 30)
        self.play(GrowFromCenter(p5), Create(hl), run_time=0.6)
        ans = M("v(5) = 30", 44, INK)
        ab = shadow_box(ans, stroke=INK, shadow=PINK, pad=(0.3, 0.14)).move_to([0, -2.4, 0])
        l30 = M("(5; 30)", 26, PINK).next_to(p5, UP, 0.18).shift(LEFT * 0.25)
        self.at(109.1)
        self.set_caption("v(5) = 30 mét/giây.", 0.2)
        self.play(FadeIn(ab, shift=UP * 0.2), FadeIn(l30), Indicate(deco[1][7], color=PINK, scale_factor=1.6), run_time=0.5)
        self.at(111.2)


class S5Ket(CueScene):
    T0 = 111.2

    def construct(self):
        self.base()
        top = top_block(chip("ĐÁP SỐ", "pink"), title_text("30 m/s"))
        self.swap_top(top, 0.4)
        l1 = row(M("v(5)", 44), M("=", 44), frac("250", "3", 44, INK, "−"), M("+ 100 +", 44), frac("40", "3", 44))
        l2 = row(M("=", 44), M("−70 + 100", 44))
        l3 = row(M("=", 44), M("30", 56, PINK), T("(m/s)", 30, GREY))
        lines = VGroup(l1, l2, l3).arrange(DOWN, buff=0.35)
        for l in (l2, l3):
            l.shift(RIGHT * (l1[1].get_center()[0] - l[0].get_center()[0]))
        box = shadow_box(lines, stroke=PINK, shadow=INK, pad=(0.4, 0.3)).move_to([0, 1.6, 0])
        self.set_caption("Đáp số: 30 m/s.", 0.25)
        self.play(FadeIn(box[0:2], shift=UP * 0.2), run_time=0.35)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15) for l in lines], lag_ratio=0.45), run_time=1.2)
        self.at(113.9)
        top2 = top_block(pill("GHI NHỚ"), title_text("TÓM TẮT"))
        self.play(FadeOut(box), run_time=0.3)
        self.swap_top(top2, 0.35)
        rows = [
            ("Bước 1", [M("v(0) = 0  ⇒  d = 0", 32)]),
            ("Bước 2", [M("v(1), v(2), v(3)  ⇒  hệ 3 ẩn", 32)]),
            ("", [row(M("a =", 32), frac("2", "3", 32, PINK, "−"), M(", b = 4, c =", 32), frac("8", "3", 32, PINK), buff=0.08)]),
            ("Bước 3", [M("v(5) = 30", 32)]),
            ("Đáp số", [M("30 m/s", 40, PINK)]),
        ]
        grid = VGroup()
        for lab, items in rows:
            l = T(lab, 22, GREY, UI, BOLD) if lab else T("Bước 2", 22, WHITE, UI, BOLD).set_opacity(0)
            r = VGroup(l, *items).arrange(RIGHT, buff=0.35)
            grid.add(r)
        grid.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        for r in grid:
            r[1].move_to([grid.get_left()[0] + 1.25, r[1].get_center()[1], 0], aligned_edge=LEFT)
        head = row(Square(0.22, fill_color=PINK, fill_opacity=1, stroke_width=0), T("TÓM TẮT LỜI GIẢI", 26, INK, UI, BOLD), buff=0.15)
        body = VGroup(head, grid).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        card = shadow_box(body, stroke=PINK, shadow=INK, pad=(0.35, 0.3), w=7.6).move_to([0, 1.55, 0])
        bd = badge().move_to([0, -1.75, 0])
        self.set_caption("Mấu chốt: xe đứng yên lúc đầu\nnên v(0) = 0.", 0.2)
        self.play(FadeIn(card, shift=UP * 0.2), FadeIn(bd, shift=UP * 0.2), run_time=0.5)
        self.at(json.load(open(HERE / "cuts.json"))["total"])
