from common import *

# White cards over free areas of the live screen. Times are in cut.mp4 seconds.
CARD_FILL = "#FFFFFF"
EDGE = "#E3E5EA"


def px(x, y):
    return np.array([(x - 960) / 135, (540 - y) / 135, 0])


def card(x0, y0, x1, y1, n, title):
    w, h = (x1 - x0) / 135, (y1 - y0) / 135
    c = (px(x0, y0) + px(x1, y1)) / 2
    shadow = RoundedRectangle(width=w, height=h, corner_radius=0.16, fill_color="#000000", fill_opacity=0.13,
                              stroke_width=0).move_to(c + [0.05, -0.07, 0])
    body = RoundedRectangle(width=w, height=h, corner_radius=0.16, fill_color=CARD_FILL, fill_opacity=1,
                            stroke_color=EDGE, stroke_width=1.5).move_to(c)
    bar = RoundedRectangle(width=0.08, height=h - 0.5, corner_radius=0.04, fill_color=C2, fill_opacity=1,
                           stroke_width=0).move_to(body.get_left() + [0.22, 0, 0])
    chip = RoundedRectangle(width=1.2, height=0.38, corner_radius=0.1, fill_color=C2, fill_opacity=1, stroke_width=0)
    chip = VGroup(chip, U(f"Câu {n}", WHITE, 20, BOLD).move_to(chip))
    head = VGroup(chip, U(title, INK, 22, BOLD)).arrange(RIGHT, buff=0.2)
    head.move_to(body.get_corner(UL) + [0.45, -0.38, 0], aligned_edge=LEFT)
    return VGroup(shadow, body, bar, head), body


def chip_pick(letter, near, direction=RIGHT):
    box = RoundedRectangle(width=1.3, height=0.44, corner_radius=0.1, fill_color=C_OK, fill_opacity=1, stroke_width=0)
    return VGroup(box, U(f"Chọn {letter}", WHITE, 20, BOLD).move_to(box)).next_to(near, direction, buff=0.22)


def okbox(m):
    return SurroundingRectangle(m, color=C_OK, buff=0.1, corner_radius=0.08, stroke_width=3.5)


class CardScene(Scene):
    T0 = 0.0
    END = 0.0

    def at(self, t):
        dt = t - self.T0 - self.time
        if dt > 0:
            self.wait(dt)

    def enter(self, base):
        self.play(FadeIn(base, shift=UP * 0.15, scale=0.97), run_time=0.45)

    def leave(self):
        if os.environ.get("STILL") == "1":
            return
        self.at(self.END - 0.4)
        self.play(FadeOut(Group(*self.mobjects), shift=DOWN * 0.1), run_time=0.4)


class Card1(CardScene):
    T0, END = 3.4, 37.3

    def construct(self):
        base, body = card(180, 466, 1262, 1000, 1, "Min trên đoạn [0; 3]")
        ax = Axes(x_range=[-0.5, 3.5, 1], y_range=[-1.4, 1.0, 0.5], x_length=2.7, y_length=2.6,
                  axis_config={"color": MUTED, "stroke_width": 2, "include_tip": True, "tip_length": 0.13})
        ax.move_to(body.get_left() + [1.95, -0.3, 0])
        f = lambda x: (x - 1) / (x + 1)
        curve = ax.plot(f, x_range=[0, 3], color=INK, stroke_width=4)
        span = Line(ax.c2p(0, 0), ax.c2p(3, 0), color=C5, stroke_width=7, stroke_opacity=0.35)
        d0 = Dot(ax.c2p(0, -1), color=C2, radius=0.08)
        d3 = Dot(ax.c2p(3, 0.5), color=C5, radius=0.08)
        l0 = T("(0; −1)", C2, 24).next_to(d0, RIGHT, buff=0.12)
        l3 = T("(3; ½)", C5, 24).next_to(d3, UP, buff=0.12)

        s1 = U("Bậc nhất / bậc nhất", INK, 22)
        s2 = U("⇒ đơn điệu trên [0; 3]", C5, 22, BOLD)
        s3 = row(T("y(0) = −1", C2, 28), T(";", INK, 28), T("y(3) = ½", C5, 28), buff=0.15)
        res = T("−1", C_OK, 34, MATH, BOLD)
        s4 = row(T("min y =", INK, 30), res, buff=0.15)
        col = VGroup(s1, s2, s3, s4).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        col.next_to(ax, RIGHT, buff=0.55).shift(UP * 0.05)
        box = okbox(res)
        pk = chip_pick("B", box)

        self.enter(base)
        self.play(Create(ax), FadeIn(s1, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(span), Create(curve), run_time=1.0)
        self.at(12.08)
        self.play(FadeIn(s2, shift=UP * 0.1), run_time=0.5)
        self.at(16.12)
        self.play(Write(s3[0]), FadeIn(d0, scale=1.5), FadeIn(l0), run_time=0.8)
        self.at(19.92)
        self.play(Write(s3[1:]), FadeIn(d3, scale=1.5), FadeIn(l3), run_time=0.8)
        self.at(31.35)
        self.play(Write(s4), Indicate(d0, color=C_OK, scale_factor=1.8), run_time=0.9)
        self.play(Create(box), run_time=0.35)
        self.at(34.57)
        self.play(FadeIn(pk, shift=LEFT * 0.1), run_time=0.4)
        self.leave()


class Card2(CardScene):
    T0, END = 43.9, 61.6

    def construct(self):
        base, body = card(160, 600, 1262, 1040, 2, "Phương trình mũ")
        ax = Axes(x_range=[-3, 2, 1], y_range=[0, 4, 1], x_length=3.0, y_length=2.2,
                  axis_config={"color": MUTED, "stroke_width": 2, "include_tip": True, "tip_length": 0.13})
        ax.move_to(body.get_left() + [2.05, -0.3, 0])
        curve = ax.plot(lambda x: 2 ** x, x_range=[-3, 2], color=INK, stroke_width=4)
        cl = sup(T("y = 2", INK, 26), "x", INK, 26).move_to(ax.c2p(-1.6, 2.9))
        hline = DashedLine(ax.c2p(-3, 0.25), ax.c2p(2, 0.25), color=C2, stroke_width=3, dash_length=0.08)
        hl = T("y = 0,25", C2, 22).next_to(ax.c2p(2, 0.25), UP, buff=0.08).shift(LEFT * 0.35)
        dot = Dot(ax.c2p(-2, 0.25), color=C_OK, radius=0.09)
        tick = VGroup(*[T(str(k), MUTED, 20).next_to(ax.c2p(k, 0), DOWN, buff=0.1) for k in (-2, -1, 1)])

        q = row(T("0,25 =", INK, 34), frac(T("1", INK, 28), T("4", INK, 28)), T("=", INK, 34),
                sup(T("2", C5, 34), "−2", C5, 34), buff=0.15)
        e = row(sup(T("2", INK, 34), "x", INK, 34), T("=", INK, 34), sup(T("2", C5, 34), "−2", C5, 34), buff=0.15)
        res = T("x = −2", C_OK, 36, MATH, BOLD)
        e2 = row(T("⇒", MUTED, 34), res, buff=0.2)
        col = VGroup(q, e, e2).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        col.next_to(ax, RIGHT, buff=0.55).shift(UP * 0.05)
        box = okbox(res)
        pk = chip_pick("C", box)

        self.enter(base)
        self.play(Create(ax), FadeIn(tick), run_time=0.6)
        self.play(Create(curve), FadeIn(cl), run_time=0.9)
        self.at(48.0)
        self.play(Write(q[:3]), Create(hline), FadeIn(hl), run_time=0.9)
        self.at(50.62)
        self.play(Write(q[3:]), run_time=0.6)
        self.play(Write(e), run_time=0.7)
        self.at(55.42)
        self.play(Write(e2), FadeIn(dot, scale=1.6), run_time=0.7)
        self.play(Create(box), run_time=0.35)
        self.at(59.06)
        self.play(FadeIn(pk, shift=LEFT * 0.1), run_time=0.4)
        self.leave()


class Card3(CardScene):
    T0, END = 71.6, 107.6

    def construct(self):
        base, body = card(160, 605, 1490, 1055, 3, "Tổng hai vectơ")
        L, Y = body.get_left()[0], body.get_bottom()[1]
        S = np.array([L + 1.6, Y + 2.0, 0])
        B = np.array([L + 0.6, Y + 0.4, 0])
        D = np.array([L + 2.6, Y + 0.4, 0])
        O = (B + D) / 2
        tri = VGroup(Line(S, B, color=INK, stroke_width=2.5), Line(S, D, color=INK, stroke_width=2.5),
                     DashedLine(B, D, color=INK, stroke_width=2.5, dash_length=0.08))
        lab = VGroup(T("S", INK, 24).next_to(S, UP, buff=0.06), T("B", INK, 24).next_to(B, LEFT, buff=0.08),
                     T("D", INK, 24).next_to(D, RIGHT, buff=0.08), T("O", INK, 22).next_to(O, DOWN, buff=0.08))
        vSB = Arrow(S, B, buff=0, color=C5, stroke_width=5, tip_length=0.18)
        vSD = Arrow(S, D, buff=0, color=C5, stroke_width=5, tip_length=0.18)
        vSO = Arrow(S, O, buff=0, color=C2, stroke_width=6, tip_length=0.2)
        dO = Dot(O, color=C2, radius=0.06)
        mid = U("O là trung điểm BD", MUTED, 16).next_to(B, DOWN, buff=0.12).align_to(B, LEFT)

        A2, C2p = np.array([L + 3.5, Y + 0.4, 0]), np.array([L + 5.3, Y + 0.4, 0])
        S3 = np.array([L + 4.4, Y + 0.4 + 1.56, 0])
        O3 = (A2 + C2p) / 2
        eq = Polygon(S3, A2, C2p, color=INK, stroke_width=2.5, fill_color=C2, fill_opacity=0.1)
        med = Line(S3, O3, color=C2, stroke_width=4)
        lab2 = VGroup(T("S", INK, 24).next_to(S3, UP, buff=0.06), T("A", INK, 24).next_to(A2, LEFT, buff=0.08),
                      T("C", INK, 24).next_to(C2p, RIGHT, buff=0.08), T("O", INK, 22).next_to(O3, DOWN, buff=0.08),
                      T("a", MUTED, 24).next_to(Line(S3, C2p).get_center(), UR, buff=0.04))
        eqn = U("tam giác SAC đều", MUTED, 16).next_to(A2, DOWN, buff=0.12).align_to(A2, LEFT)

        F = 28
        l1 = row(vec("SB", C5, F), T("+", INK, F), vec("SD", C5, F), T("=", INK, F), T("2", C2, F), vec("SO", C2, F), buff=0.1)
        l2 = row(T("SO =", INK, F), frac(T("a√3", INK, 24), T("2", INK, 24)), U("(SAC đều)", MUTED, 18), buff=0.12)
        res = T("a√3", C_OK, 34, MATH, BOLD)
        l3 = row(T("⇒ |", INK, F), vec("SB", INK, F), T("+", INK, F), vec("SD", INK, F), T("| =", INK, F), res, buff=0.08)
        col = VGroup(l1, l2, l3).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        col.move_to([L + 5.95, Y + 1.25, 0], aligned_edge=LEFT)
        box = okbox(res)
        pk = chip_pick("D", box)
        pk.move_to(body.get_corner(UR) + [-1.0, -0.38, 0])

        self.enter(base)
        self.play(Create(tri), FadeIn(lab), run_time=0.7)
        self.play(GrowArrow(vSB), GrowArrow(vSD), run_time=0.7)
        self.at(82.27)
        self.play(FadeIn(dO), run_time=0.3)
        self.play(GrowArrow(vSO), Write(l1), run_time=1.0)
        self.at(88.37)
        self.play(Create(eq), FadeIn(lab2), run_time=0.8)
        self.at(97.41)
        self.play(Create(med), Write(l2), run_time=0.9)
        self.at(100.61)
        self.play(Write(l3), run_time=1.0)
        self.play(Create(box), run_time=0.35)
        self.at(104.43)
        self.play(FadeIn(pk, shift=DOWN * 0.1), run_time=0.4)
        self.leave()


class Card4(CardScene):
    T0, END = 114.6, 181.0

    def construct(self):
        base, body = card(1348, 110, 1906, 630, 4, "Tiệm cận")
        L, Y = body.get_left()[0], body.get_bottom()[1]
        ax = Axes(x_range=[-3.5, 2.5, 1], y_range=[-2.5, 2.5, 1], x_length=2.0, y_length=2.0,
                  axis_config={"color": MUTED, "stroke_width": 1.6, "include_tip": True, "tip_length": 0.1})
        ax.move_to([L + 1.35, Y + 1.95, 0])
        f = lambda x: -1 / (x + 2) - 1 / x
        curve = ax.plot(f, x_range=[-1.72, -0.28], color=INK, stroke_width=3.5)
        ya = DashedLine(ax.c2p(-3.5, 0), ax.c2p(2.5, 0), color=C5, stroke_width=4, dash_length=0.08)
        xa1 = DashedLine(ax.c2p(-2, -2.5), ax.c2p(-2, 2.5), color=C2, stroke_width=4, dash_length=0.08)
        xa2 = DashedLine(ax.c2p(0, -2.5), ax.c2p(0, 2.5), color=C2, stroke_width=4, dash_length=0.08)

        F = 24
        r1 = VGroup(U("Ngang", C5, 15, BOLD), T("y = 0", C5, F)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        r2 = VGroup(U("Đứng", C2, 15, BOLD), T("x = −2", C2, F)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        r3 = VGroup(U("Đứng", C2, 15, BOLD), T("x = 0", C2, F)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        col = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        col.move_to([L + 2.65, ax.get_center()[1], 0], aligned_edge=LEFT)
        n = T("3", C_OK, 32, MATH, BOLD)
        r4 = row(T("⇒", MUTED, F), n, U("tiệm cận", INK, 20), buff=0.2)
        box = okbox(n)
        pk = chip_pick("C", r4)
        VGroup(r4, box, pk).move_to([L + 2.15, Y + 0.45, 0])

        self.enter(base)
        self.play(Create(ax), run_time=0.6)
        self.play(Create(ya), FadeIn(r1, shift=LEFT * 0.1), run_time=0.7)
        self.at(139.21)
        self.play(Create(xa1), FadeIn(r2, shift=LEFT * 0.1), run_time=0.7)
        self.at(150.04)
        self.play(Create(xa2), FadeIn(r3, shift=LEFT * 0.1), run_time=0.7)
        self.play(Create(curve), run_time=0.8)
        self.at(168.88)
        self.play(FadeIn(r4, shift=UP * 0.1), run_time=0.45)
        self.play(Create(box), run_time=0.35)
        self.at(170.02)
        self.play(FadeIn(pk, shift=UP * 0.1), run_time=0.4)
        self.leave()
