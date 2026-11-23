import os
from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30

MATH = "Cambria Math"
UI = "Segoe UI"
INK = "#1F2A44"
PAPER = "#FBFAF6"
C5 = "#2563EB"
C2 = "#D6246E"
C_OK = "#16A34A"
MUTED = "#6B7280"
TILE = "#EEF0F4"

config.background_color = PAPER

def T(s, color=INK, size=40, font=MATH, weight=NORMAL):
    return Text(s, font=font, font_size=size, color=color, weight=weight)


def U(s, color=INK, size=28, weight=NORMAL):
    return T(s, color, size, UI, weight)


def row(*items, buff=0.15):
    return VGroup(*items).arrange(RIGHT, buff=buff)


def frac(num, den, color=INK):
    bar = Line(LEFT, RIGHT, stroke_width=3, color=color).set_width(max(num.width, den.width) + 0.15)
    return VGroup(num, bar, den).arrange(DOWN, buff=0.1)


def sup(base, exp, color=INK, size=40):
    b = base if isinstance(base, Mobject) else T(base, color, size)
    e = T(exp, color, size * 0.6).next_to(b, RIGHT, buff=0.04).align_to(b, UP).shift(UP * 0.12)
    return VGroup(b, e)


def sub(base, s, color=INK, size=40):
    b = base if isinstance(base, Mobject) else T(base, color, size)
    e = T(s, color, size * 0.6).next_to(b, RIGHT, buff=0.04).align_to(b, DOWN).shift(DOWN * 0.1)
    return VGroup(b, e)


def vec(s, color=INK, size=40):
    t = T(s, color, size)
    a = Arrow(LEFT, RIGHT, buff=0, stroke_width=2.5, color=color, tip_length=0.1,
              max_tip_length_to_length_ratio=0.5).set_width(t.width + 0.05).next_to(t, UP, buff=0.04)
    return VGroup(t, a)

