#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Scratch 3 reference answer .sb3 files for all lessons.

Usage:
    python3 build_scratch_sb3.py
    python3 build_scratch_sb3.py --copy-docs
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

from scratch.sb3_builder import APPLE_SVG, DOT_SVG, PLANE_SVG, SB3Builder, Script

ROOT = Path(__file__).parent
OUT = ROOT / "course" / "scratch_answers"
DOCS_OUT = ROOT / "docs" / "scratch_answers"
MANIFEST = OUT / "manifest.json"


def sb3_name_for_md(md_filename: str) -> str | None:
    m = re.match(r"第(\d+)课_(.+)_Scratch\.md", md_filename)
    if m:
        return f"S{int(m.group(1)):02d}_{m.group(2)}_参考答案.sb3"
    m = re.match(r"Scratch进阶第(\d+)课_(.+)\.md", md_filename)
    if m:
        title = m.group(2).split("（")[0].split("(")[0].strip()
        return f"A{int(m.group(1)):02d}_{title}_参考答案.sb3"
    return None


def _set_var_from_answer(s: Script, var: str) -> Script:
    ans = s._block("sensing_answer")
    s._link(s._block(
        "data_setvariableto",
        inputs={"VALUE": [2, ans]},
        fields={"VARIABLE": s._var_field(var)},
    ))
    return s


def lesson_01(b: SB3Builder):
    b.script("Sprite1").flag().say("你好，我是小猫！", 2).say("今年我 7 岁了！", 2)


def lesson_02(b: SB3Builder):
    b.script("Sprite1").flag().set_var("my_age", 7).say_join("我今年 ", "my_age", 2)


def lesson_03(b: SB3Builder):
    b.script("Sprite1").flag().say_math("3", "+", "5", secs=2).set_var("a", 12).set_var("b", 8).say_var_expr("水果总数：", "a", "+", "b", 2)


def lesson_04(b: SB3Builder):
    s = b.script("Sprite1").flag().ask("你叫什么名字？")
    jid = s._block("operator_join", inputs={"STRING1": s._lit_str("你好，"), "STRING2": s._answer()})
    s._link(s._block("looks_sayforsecs", inputs={"MESSAGE": [2, jid], "SECS": s._lit_num(2)}))


def lesson_05(b: SB3Builder):
    s = b.script("Sprite1").flag().ask("你几岁了？")
    s.if_eq_answer("7", Script(b, "Sprite1").say("哇，我们同岁！", 2),
                   Script(b, "Sprite1").say("你不是 7 岁！", 2))


def lesson_06(b: SB3Builder):
    s = b.script("Sprite1").flag().ask("请输入开门密码：")
    s.if_eq_answer("1234", Script(b, "Sprite1").say("🔓 咔嚓！门打开了！", 2).say("欢迎回家，主人！", 2))


def lesson_07(b: SB3Builder):
    s = b.script("Sprite1").flag().ask("苹果好吃吗？（好吃/不好吃）")
    s.if_eq_answer("好吃", Script(b, "Sprite1").say("我也觉得超好吃！🍎", 2),
                   Script(b, "Sprite1").say("啊？你是不是味觉有问题？🤔", 2))


def lesson_08(b: SB3Builder):
    s = b.script("Sprite1").flag().say("石头剪刀布！", 1).ask("你出什么？（1=石头 2=剪刀 3=布）")
    _set_var_from_answer(s, "player")
    s.random_var("computer", 1, 3).say_join("电脑出了：", "computer", 2)


def lesson_09(b: SB3Builder):
    b.script("Sprite1").flag().say("我要开始散步啦！", 1).move(100).turn_right(90).move(100)


def lesson_10(b: SB3Builder):
    body = Script(b, "Sprite1").move(100).turn_right(90)
    b.script("Sprite1").flag().pen_clear().pen_down().repeat(4, body).pen_up()


def lesson_11(b: SB3Builder):
    body = Script(b, "Sprite1").move(20).turn_right(90)
    b.script("Sprite1").flag().pen_clear().pen_down().repeat(36, body).pen_up()


def lesson_12(b: SB3Builder):
    body = Script(b, "Sprite1").move(10).turn_right(15)
    b.script("Sprite1").flag().pen_clear().pen_down().repeat(24, body).pen_up()


def lesson_13(b: SB3Builder):
    b.script("Sprite1").flag().add_to_list("小汽车", "我的玩具").add_to_list("机器人", "我的玩具").say("我的玩具有：小汽车、机器人…", 2)


def lesson_14(b: SB3Builder):
    b.script("Sprite1").flag().add_to_list("第一节", "小火车").add_to_list("第二节", "小火车").say("又加了一节车厢！", 2)


def lesson_15(b: SB3Builder):
    b.script("Sprite1").flag().add_to_list("苹果", "零食").add_to_list("饼干", "零食").say_list("第 1 个零食是：", "零食", 2)


def lesson_16(b: SB3Builder):
    b.script("Sprite1").flag().add_to_list("红", "颜色").add_to_list("蓝", "颜色").add_to_list("绿", "颜色").say("开始检阅：红、蓝、绿！", 2)


def lesson_17(b: SB3Builder):
    s = b.script("Sprite1")
    body = Script(b, "Sprite1").change_y(10).wait(0.1).change_y(-10).wait(0.1)
    _, call = s.define_block("跳一跳", body)
    b.script("Sprite1").flag().call(call).call(call)


def lesson_18(b: SB3Builder):
    s = b.script("Sprite1")
    body = Script(b, "Sprite1").turn_right(36)
    _, call = s.define_block("转一圈", body)
    b.script("Sprite1").flag().repeat(10, Script(b, "Sprite1").call(call))


def lesson_19(b: SB3Builder):
    b.script("Sprite1").flag().say("这个积木会思考…", 1).wait(0.5).say("答案是：42！", 2)


def lesson_20(b: SB3Builder):
    s = b.script("Sprite1")
    body = Script(b, "Sprite1").move(30).turn_right(90)
    _, call = s.define_block("画一边", body)
    b.script("Sprite1").flag().pen_clear().pen_down().repeat(4, Script(b, "Sprite1").call(call)).pen_up()


def lesson_21(b: SB3Builder):
    b.add_sprite("Sprite1")
    b.add_sprite("Apple", APPLE_SVG)
    loop = Script(b, "Sprite1")
    loop.if_key("left arrow", Script(b, "Sprite1").change_x(-15))
    loop.if_key("right arrow", Script(b, "Sprite1").change_x(15))
    b.script("Sprite1").flag().go_xy(0, -120).forever(loop)

    fall = Script(b, "Apple").change_y(-8)
    apple_loop = Script(b, "Apple").set_random_x(-200, 200, 180).repeat_until_touch("Sprite1", fall).go_xy(0, 180)
    b.script("Apple").flag().show().forever(apple_loop)


def lesson_22(b: SB3Builder):
    pop = Script(b, "Sprite1").show().wait(0.8).hide().wait(0.5)
    b.script("Sprite1").flag().say("打地鼠！看到小猫就点它！", 2).hide().forever(pop)


def lesson_23(b: SB3Builder):
    loop = Script(b, "Sprite1")
    loop.if_key("up arrow", Script(b, "Sprite1").change_y(10))
    loop.if_key("down arrow", Script(b, "Sprite1").change_y(-10))
    loop.if_key("left arrow", Script(b, "Sprite1").change_x(-10))
    loop.if_key("right arrow", Script(b, "Sprite1").change_x(10))
    b.script("Sprite1").flag().go_xy(-180, 0).say("用方向键走出迷宫！", 2).forever(loop)


def lesson_24(b: SB3Builder):
    s = b.script("Sprite1").flag().say("欢迎来到我的毕业大作！", 2).ask("你的名字？")
    jid = s._block("operator_join", inputs={"STRING1": s._lit_str("谢谢 "), "STRING2": s._answer()})
    s._link(s._block("looks_sayforsecs", inputs={"MESSAGE": [2, jid], "SECS": s._lit_num(2)}))
    body = Script(b, "Sprite1").turn_right(30).move(20)
    s.pen_clear().pen_down().repeat(12, body).pen_up()


def adv_01_snail(b: SB3Builder):
    for v in ("高度", "天数", "井深"):
        b.ensure_var("Sprite1", v)
    b.script("Sprite1").flag().set_var("井深", 10).set_var("高度", 0).set_var("天数", 0).say("蜗牛开始爬井！看变量变化", 2)


def adv_02_buyer(b: SB3Builder):
    b.ensure_var("Sprite1", "件数")
    s = b.script("Sprite1").flag().ask("买了几件？每件 3 元")
    _set_var_from_answer(s, "件数")
    s.say("付 20 元，用 减法 算找零！", 2)


def adv_03_candy(b: SB3Builder):
    b.script("Sprite1").flag().ask("有多少颗糖？").ask("分给几个人？").say("用 除法 和 余数 算每人几颗！", 3)


def adv_04_multiply(b: SB3Builder):
    body = Script(b, "Sprite1").say("3 x 3 = 9", 0.5)
    b.script("Sprite1").flag().say("九九乘法表：用 重复执行 练！", 2).repeat(3, body)


def adv_05_plane(b: SB3Builder):
    b.add_sprite("Plane", PLANE_SVG)
    b.add_sprite("Bullet", DOT_SVG)
    move = Script(b, "Plane")
    move.if_key("left arrow", Script(b, "Plane").change_x(-10))
    move.if_key("right arrow", Script(b, "Plane").change_x(10))
    b.script("Plane").flag().go_xy(0, -150).forever(move)
    b.script("Bullet").flag().hide()
    b.script("Bullet").key_flag_script("space").create_clone("_myself_")
    b.script("Bullet").clone_start().show().go_xy(0, -150).repeat(20, Script(b, "Bullet").change_y(12)).delete_clone()


def adv_06_plane2(b: SB3Builder):
    adv_05_plane(b)
    b.ensure_var("Plane", "得分")
    b.script("Plane").flag().set_var("得分", 0).say("得分：碰到敌人 +1", 1)


def adv_07_tank(b: SB3Builder):
    loop = Script(b, "Sprite1")
    loop.if_key("up arrow", Script(b, "Sprite1").change_y(8))
    loop.if_key("down arrow", Script(b, "Sprite1").change_y(-8))
    loop.if_key("left arrow", Script(b, "Sprite1").change_x(-8))
    loop.if_key("right arrow", Script(b, "Sprite1").change_x(8))
    b.script("Sprite1").flag().say("坦克大战：方向键移动，空格发射", 2).forever(loop)


LESSONS = [
    ("S01_你好小猫_参考答案.sb3", lesson_01),
    ("S02_神奇的盒子_参考答案.sb3", lesson_02),
    ("S03_数学魔法_参考答案.sb3", lesson_03),
    ("S04_会聊天的小猫_参考答案.sb3", lesson_04),
    ("S05_真真假假_参考答案.sb3", lesson_05),
    ("S06_魔法门卫_参考答案.sb3", lesson_06),
    ("S07_左转还是右转_参考答案.sb3", lesson_07),
    ("S08_石头剪刀布_参考答案.sb3", lesson_08),
    ("S09_遇见小猫_参考答案.sb3", lesson_09),
    ("S10_画个正方形_参考答案.sb3", lesson_10),
    ("S11_复制魔法_参考答案.sb3", lesson_11),
    ("S12_绚丽的烟花_参考答案.sb3", lesson_12),
    ("S13_搭建小火车_参考答案.sb3", lesson_13),
    ("S14_添加车厢_参考答案.sb3", lesson_14),
    ("S15_车厢里有什么_参考答案.sb3", lesson_15),
    ("S16_检阅火车_参考答案.sb3", lesson_16),
    ("S17_召唤自制积木_参考答案.sb3", lesson_17),
    ("S18_积木的秘密_参考答案.sb3", lesson_18),
    ("S19_给积木加脑袋_参考答案.sb3", lesson_19),
    ("S20_超级积木_参考答案.sb3", lesson_20),
    ("S21_接苹果游戏_参考答案.sb3", lesson_21),
    ("S22_打地鼠_参考答案.sb3", lesson_22),
    ("S23_迷宫大冒险_参考答案.sb3", lesson_23),
    ("S24_我的第一个大作_参考答案.sb3", lesson_24),
    ("A01_蜗牛爬井_参考答案.sb3", adv_01_snail),
    ("A02_聪明小买手_参考答案.sb3", adv_02_buyer),
    ("A03_公平分糖果_参考答案.sb3", adv_03_candy),
    ("A04_乘法魔方_参考答案.sb3", adv_04_multiply),
    ("A05_飞机大战①起飞与开火_参考答案.sb3", adv_05_plane),
    ("A06_飞机大战②敌机来袭_参考答案.sb3", adv_06_plane2),
    ("A07_坦克大战_参考答案.sb3", adv_07_tank),
]


def build_all():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.sb3"):
        old.unlink()
    manifest = []
    for fname, fn in LESSONS:
        b = SB3Builder()
        b.add_sprite("Sprite1")
        fn(b)
        b.save(OUT / fname)
        manifest.append({"file": fname, "md": _md_for_sb3(fname)})
        print(f"  ✅ {fname}")
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ 共生成 {len(manifest)} 个 sb3 → {OUT}/")
    return manifest


def _md_for_sb3(fname: str) -> str | None:
    for p in Path(ROOT / "course").glob("*.md"):
        if sb3_name_for_md(p.name) == fname:
            return p.name
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy-docs", action="store_true")
    args = parser.parse_args()
    build_all()
    if args.copy_docs:
        if DOCS_OUT.exists():
            shutil.rmtree(DOCS_OUT)
        shutil.copytree(OUT, DOCS_OUT)
        print(f"✅ 已复制到 {DOCS_OUT}/")


if __name__ == "__main__":
    main()
