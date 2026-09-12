#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把图形化编程读程序题的糊图，画成清晰的矢量积木图。"""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "site" / "e2-img"

C = {
    "yellow": "#ffbf00",
    "yellow2": "#cc9900",
    "blue": "#4c97ff",
    "blue2": "#3373cc",
    "purple": "#9966ff",
    "purple2": "#774dcb",
    "orange": "#ffab19",
    "orange2": "#cf8b17",
    "green": "#59c059",
    "green2": "#389438",
    "pink": "#ff6680",
    "pink2": "#ff3355",
    "var": "#ff8c1a",
    "var2": "#db6e00",
    "ink": "#1e293b",
    "white": "#fff",
    "slot": "#fff",
}


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text(x, y, s, size=22, fill=None, anchor="start", weight=800):
    fill = fill or C["ink"]
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
        f'font-family="PingFang SC,Microsoft YaHei,Noto Sans CJK SC,sans-serif" '
        f'fill="{fill}" text-anchor="{anchor}" dominant-baseline="middle">{esc(s)}</text>'
    )


def rrect(x, y, w, h, fill, stroke, rx=14):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" ry="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
    )


def oval(x, y, w, h, fill="#fff", stroke="#389438"):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" ry="{h/2}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    )


def hexslot(x, y, w, h, fill="#fff", stroke="#389438"):
    r = h / 2
    pts = f"{x+r},{y} {x+w-r},{y} {x+w},{y+r} {x+w-r},{y+h} {x+r},{y+h} {x},{y+r}"
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


class Canvas:
    def __init__(self, w, h, bg="#f8fafc"):
        self.w, self.h, self.bg = w, h, bg
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    def block(self, x, y, w, h, fill, stroke, label, size=22, indent=18):
        self.add(rrect(x, y, w, h, fill, stroke))
        self.add(text(x + indent, y + h / 2, label, size=size, fill=C["ink"]))
        return y + h - 4

    def out(self, path):
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}">'
            f'<rect width="100%" height="100%" fill="{self.bg}"/>'
            + "".join(self.parts)
            + "</svg>"
        )
        path.write_text(svg, encoding="utf-8")
        print("wrote", path.name, self.w, "x", self.h)


def q13():
    c = Canvas(1280, 720)
    # left: green flag script
    x, y, w = 40, 40, 420
    c.add(rrect(x, y, w, 56, C["yellow"], C["yellow2"], 18))
    c.add(text(x + 20, y + 28, "当绿旗被点击", 24))
    y = y + 52
    c.add(rrect(x, y, w, 64, C["pink"], C["pink2"]))
    c.add(text(x + 20, y + 32, "比较", 24))
    for i, n in enumerate(("12", "25", "19")):
        ox = x + 110 + i * 90
        c.add(oval(ox, y + 14, 78, 36, C["white"], C["pink2"]))
        c.add(text(ox + 39, y + 32, n, 22, anchor="middle"))
    # right: define
    x, y, w = 500, 40, 740
    c.add(rrect(x, y, w, 56, C["pink"], C["pink2"], 18))
    c.add(text(x + 20, y + 28, "定义  比较", 24))
    for i, n in enumerate("abc"):
        ox = x + 200 + i * 70
        c.add(oval(ox, y + 12, 56, 32, C["white"], C["pink2"]))
        c.add(text(ox + 28, y + 28, n, 22, anchor="middle"))
    y += 52
    # if a>b and a>c
    c.add(rrect(x, y, w, 70, C["orange"], C["orange2"]))
    c.add(text(x + 16, y + 35, "如果", 22))
    c.add(hexslot(x + 80, y + 14, 430, 42))
    c.add(oval(x + 92, y + 20, 70, 30))
    c.add(text(x + 127, y + 35, "a", 20, anchor="middle"))
    c.add(text(x + 175, y + 35, ">", 22, anchor="middle"))
    c.add(oval(x + 190, y + 20, 70, 30))
    c.add(text(x + 225, y + 35, "b", 20, anchor="middle"))
    c.add(text(x + 280, y + 35, "与", 20, anchor="middle"))
    c.add(oval(x + 310, y + 20, 70, 30))
    c.add(text(x + 345, y + 35, "a", 20, anchor="middle"))
    c.add(text(x + 392, y + 35, ">", 22, anchor="middle"))
    c.add(oval(x + 408, y + 20, 70, 30))
    c.add(text(x + 443, y + 35, "c", 20, anchor="middle"))
    c.add(text(x + 530, y + 35, "那么", 22))
    y += 66
    c.add(rrect(x + 36, y, w - 36, 56, C["purple"], C["purple2"]))
    c.add(text(x + 56, y + 28, "说", 22))
    c.add(oval(x + 110, y + 12, 80, 32, C["white"], C["purple2"]))
    c.add(text(x + 150, y + 28, "a", 22, anchor="middle"))
    y += 52
    c.add(rrect(x, y, w, 48, C["orange"], C["orange2"]))
    c.add(text(x + 16, y + 24, "否则", 22))
    y += 44
    c.add(rrect(x, y, w, 70, C["orange"], C["orange2"]))
    c.add(text(x + 16, y + 35, "如果", 22))
    c.add(hexslot(x + 80, y + 14, 430, 42))
    c.add(oval(x + 92, y + 20, 70, 30))
    c.add(text(x + 127, y + 35, "b", 20, anchor="middle"))
    c.add(text(x + 175, y + 35, ">", 22, anchor="middle"))
    c.add(oval(x + 190, y + 20, 70, 30))
    c.add(text(x + 225, y + 35, "a", 20, anchor="middle"))
    c.add(text(x + 280, y + 35, "与", 20, anchor="middle"))
    c.add(oval(x + 310, y + 20, 70, 30))
    c.add(text(x + 345, y + 35, "b", 20, anchor="middle"))
    c.add(text(x + 392, y + 35, ">", 22, anchor="middle"))
    c.add(oval(x + 408, y + 20, 70, 30))
    c.add(text(x + 443, y + 35, "c", 20, anchor="middle"))
    c.add(text(x + 530, y + 35, "那么", 22))
    y += 66
    c.add(rrect(x + 36, y, w - 36, 56, C["purple"], C["purple2"]))
    c.add(text(x + 56, y + 28, "说", 22))
    c.add(oval(x + 110, y + 12, 80, 32, C["white"], C["purple2"]))
    c.add(text(x + 150, y + 28, "b", 22, anchor="middle"))
    y += 52
    c.add(rrect(x, y, w, 48, C["orange"], C["orange2"]))
    c.add(text(x + 16, y + 24, "否则", 22))
    y += 44
    c.add(rrect(x + 36, y, w - 36, 56, C["purple"], C["purple2"]))
    c.add(text(x + 56, y + 28, "说", 22))
    c.add(oval(x + 110, y + 12, 80, 32, C["white"], C["purple2"]))
    c.add(text(x + 150, y + 28, "c", 22, anchor="middle"))
    c.add(text(40, 690, "点图片可以放大。比较 12、25、19，谁最大就说谁。", 20, "#475569"))
    c.out(OUT / "mepsL4r_13_0.svg")


def q14():
    c = Canvas(1280, 520)
    x, y, w = 40, 50, 400
    c.add(rrect(x, y, w, 56, C["yellow"], C["yellow2"], 18))
    c.add(text(x + 20, y + 28, "当绿旗被点击", 24))
    y += 52
    c.add(rrect(x, y, w, 64, C["pink"], C["pink2"]))
    c.add(text(x + 20, y + 32, "计算", 24))
    c.add(oval(x + 110, y + 14, 78, 36, C["white"], C["pink2"]))
    c.add(text(x + 149, y + 32, "5", 22, anchor="middle"))
    c.add(oval(x + 200, y + 14, 78, 36, C["white"], C["pink2"]))
    c.add(text(x + 239, y + 32, "3", 22, anchor="middle"))
    y += 60
    c.add(rrect(x, y, w, 56, C["var"], C["var2"]))
    c.add(text(x + 20, y + 28, "将 结果 增加", 22))
    c.add(oval(x + 200, y + 12, 80, 32, C["white"], C["var2"]))
    c.add(text(x + 240, y + 28, "b", 22, anchor="middle"))

    x, y, w = 500, 50, 740
    c.add(rrect(x, y, w, 56, C["pink"], C["pink2"], 18))
    c.add(text(x + 20, y + 28, "定义  计算", 24))
    c.add(oval(x + 200, y + 12, 56, 32, C["white"], C["pink2"]))
    c.add(text(x + 228, y + 28, "a", 22, anchor="middle"))
    c.add(oval(x + 270, y + 12, 56, 32, C["white"], C["pink2"]))
    c.add(text(x + 298, y + 28, "b", 22, anchor="middle"))
    y += 52
    c.add(rrect(x, y, w, 70, C["orange"], C["orange2"]))
    c.add(text(x + 16, y + 35, "重复执行", 22))
    c.add(oval(x + 140, y + 17, 160, 36, C["white"], C["orange2"]))
    c.add(text(x + 220, y + 35, "a − 1", 22, anchor="middle"))
    c.add(text(x + 320, y + 35, "次", 22))
    y += 66
    c.add(rrect(x + 36, y, w - 36, 64, C["var"], C["var2"]))
    c.add(text(x + 52, y + 32, "将 结果 设为", 22))
    c.add(oval(x + 230, y + 14, 220, 36, C["white"], C["var2"]))
    c.add(text(x + 340, y + 32, "b × a ＋ 1", 22, anchor="middle"))
    c.add(text(40, 490, "点图片可以放大。绿旗：计算 5 和 3，再把结果加上 b。", 20, "#475569"))
    c.out(OUT / "mepsL4r_14_0.svg")


def q15():
    c = Canvas(1280, 700)
    x, y, w = 40, 40, 400
    c.add(rrect(x, y, w, 56, C["yellow"], C["yellow2"], 18))
    c.add(text(x + 20, y + 28, "当绿旗被点击", 24))
    y += 52
    c.add(rrect(x, y, w, 56, C["var"], C["var2"]))
    c.add(text(x + 20, y + 28, "将 s 设为  0", 22))
    y += 52
    c.add(rrect(x, y, w, 56, C["pink"], C["pink2"]))
    c.add(text(x + 20, y + 28, "运算", 22))
    c.add(oval(x + 110, y + 12, 80, 32, C["white"], C["pink2"]))
    c.add(text(x + 150, y + 28, "15", 22, anchor="middle"))
    y += 52
    c.add(rrect(x, y, w, 56, C["purple"], C["purple2"]))
    c.add(text(x + 20, y + 28, "说", 22))
    c.add(oval(x + 90, y + 12, 80, 32, C["white"], C["purple2"]))
    c.add(text(x + 130, y + 28, "s", 22, anchor="middle"))

    x, y, w = 500, 40, 740
    c.add(rrect(x, y, w, 56, C["pink"], C["pink2"], 18))
    c.add(text(x + 20, y + 28, "定义  运算", 24))
    c.add(oval(x + 200, y + 12, 56, 32, C["white"], C["pink2"]))
    c.add(text(x + 228, y + 28, "n", 22, anchor="middle"))
    y += 52
    c.add(rrect(x, y, w, 70, C["orange"], C["orange2"]))
    c.add(text(x + 16, y + 35, "如果", 22))
    c.add(hexslot(x + 80, y + 14, 360, 42))
    c.add(text(x + 260, y + 35, "n ÷ 2  ＞  3", 22, anchor="middle"))
    c.add(text(x + 470, y + 35, "那么", 22))
    y += 66
    c.add(rrect(x + 36, y, w - 36, 56, C["var"], C["var2"]))
    c.add(text(x + 52, y + 28, "将 s 增加  2", 22))
    y += 52
    c.add(rrect(x + 36, y, w - 36, 56, C["pink"], C["pink2"]))
    c.add(text(x + 52, y + 28, "运算", 22))
    c.add(oval(x + 150, y + 12, 120, 32, C["white"], C["pink2"]))
    c.add(text(x + 210, y + 28, "n ÷ 2", 22, anchor="middle"))
    y += 52
    c.add(rrect(x, y, w, 48, C["orange"], C["orange2"]))
    c.add(text(x + 16, y + 24, "否则", 22))
    y += 44
    c.add(rrect(x + 36, y, w - 36, 56, C["orange"], C["orange2"]))
    c.add(text(x + 52, y + 28, "停止这个脚本", 22))
    c.add(text(40, 670, "点图片可以放大。绿旗先把 s 变成 0，再运算 15，最后说 s。", 20, "#475569"))
    c.out(OUT / "mepsL4r_15_0.svg")


def q16():
    c = Canvas(1280, 680)
    x, y, w = 40, 40, 460
    c.add(rrect(x, y, w, 56, C["yellow"], C["yellow2"], 18))
    c.add(text(x + 20, y + 28, "当绿旗被点击", 24))
    y += 52
    c.add(rrect(x, y, w, 56, C["blue"], C["blue2"]))
    c.add(text(x + 20, y + 28, "移到 x：−240    y：0", 22))
    y += 52
    c.add(rrect(x, y, w, 56, C["blue"], C["blue2"]))
    c.add(text(x + 20, y + 28, "面向  90  方向", 22))
    y += 52
    c.add(rrect(x, y, w, 56, C["pink"], C["pink2"]))
    c.add(text(x + 20, y + 28, "移动", 24))
    y += 52
    c.add(rrect(x, y, w, 56, C["purple"], C["purple2"]))
    c.add(text(x + 20, y + 28, "说  「到达」  2 秒", 22))

    x, y, w = 540, 40, 700
    c.add(rrect(x, y, w, 56, C["pink"], C["pink2"], 18))
    c.add(text(x + 20, y + 28, "定义  移动", 24))
    y += 52
    c.add(rrect(x, y, w, 56, C["blue"], C["blue2"]))
    c.add(text(x + 20, y + 28, "移动  10  步", 22))
    y += 52
    c.add(rrect(x, y, w, 70, C["orange"], C["orange2"]))
    c.add(text(x + 16, y + 35, "如果", 22))
    c.add(hexslot(x + 80, y + 14, 360, 42))
    c.add(text(x + 260, y + 35, "x 坐标  ＞  230", 22, anchor="middle"))
    c.add(text(x + 470, y + 35, "那么", 22))
    y += 66
    c.add(rrect(x + 36, y, w - 36, 56, C["orange"], C["orange2"]))
    c.add(text(x + 52, y + 28, "停止这个脚本", 22))
    y += 52
    c.add(rrect(x, y, w, 56, C["pink"], C["pink2"]))
    c.add(text(x + 20, y + 28, "移动", 24))
    c.add(text(40, 650, "点图片可以放大。自制积木「移动」里面又叫了一次「移动」。", 20, "#475569"))
    c.out(OUT / "mepsL4r_16_0.svg")


def q20():
    c = Canvas(1100, 520)
    x, y, w = 40, 40, 1020
    c.add(rrect(x, y, w, 56, C["pink"], C["pink2"], 18))
    c.add(text(x + 20, y + 28, "定义  模拟抽奖", 24))
    y += 52
    c.add(rrect(x, y, w, 64, C["var"], C["var2"]))
    c.add(text(x + 20, y + 32, "将 随机数 设为    在 1 和 10 之间取随机数", 22))
    y += 60
    c.add(rrect(x, y, w, 70, C["orange"], C["orange2"]))
    c.add(text(x + 16, y + 35, "如果", 22))
    c.add(hexslot(x + 80, y + 14, 620, 42))
    c.add(text(x + 390, y + 35, "随机数 ＞ 3    与    随机数 ＜ 9", 22, anchor="middle"))
    c.add(text(x + 730, y + 35, "那么", 22))
    y += 66
    c.add(rrect(x + 36, y, w - 36, 56, C["purple"], C["purple2"]))
    c.add(text(x + 56, y + 28, "说  「中奖啦」", 22))
    y += 52
    c.add(rrect(x, y, w, 48, C["orange"], C["orange2"]))
    c.add(text(x + 16, y + 24, "否则", 22))
    y += 44
    c.add(rrect(x + 36, y, w - 36, 56, C["purple"], C["purple2"]))
    c.add(text(x + 56, y + 28, "说  「没有中奖」", 22))
    c.add(text(40, 490, "点图片可以放大。随机数是 4、5、6、7、8 就说中奖啦。", 20, "#475569"))
    c.out(OUT / "mepsL4r_20_0.svg")


def q21():
    c = Canvas(1100, 320)
    x, y, w = 40, 40, 680
    c.add(rrect(x, y, w, 56, C["pink"], C["pink2"], 18))
    c.add(text(x + 20, y + 28, "定义  运算", 24))
    c.add(oval(x + 200, y + 12, 56, 32, C["white"], C["pink2"]))
    c.add(text(x + 228, y + 28, "a", 22, anchor="middle"))
    c.add(oval(x + 270, y + 12, 56, 32, C["white"], C["pink2"]))
    c.add(text(x + 298, y + 28, "b", 22, anchor="middle"))
    y += 52
    c.add(rrect(x, y, w, 64, C["purple"], C["purple2"]))
    c.add(text(x + 20, y + 32, "说", 24))
    c.add(oval(x + 90, y + 14, 280, 36, C["white"], C["purple2"]))
    c.add(text(x + 230, y + 32, "( a ＞ b )  ＋  a", 22, anchor="middle"))
    # call
    x, y = 760, 80
    c.add(rrect(x, y, 300, 64, C["pink"], C["pink2"]))
    c.add(text(x + 20, y + 32, "运算", 24))
    c.add(oval(x + 110, y + 14, 70, 36, C["white"], C["pink2"]))
    c.add(text(x + 145, y + 32, "1", 22, anchor="middle"))
    c.add(oval(x + 190, y + 14, 70, 36, C["white"], C["pink2"]))
    c.add(text(x + 225, y + 32, "0", 22, anchor="middle"))
    c.add(text(40, 290, "点图片可以放大。右边是：运算 1 和 0。", 20, "#475569"))
    c.out(OUT / "mepsL4r_21_0.svg")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    q13(); q14(); q15(); q16(); q20(); q21()
