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

from scratch.sb3_builder import (
    APPLE_SVG,
    BIG_FISH_SVG,
    CAT_SVG,
    DOT_SVG,
    PLANE_SVG,
    SB3Builder,
    Script,
    SHARK_SVG,
    SMALL_FISH_SVG,
    WELL_BOTTOM_Y,
    WELL_METER_PX,
    well_backdrop_svg,
)

ROOT = Path(__file__).parent
OUT = ROOT / "course" / "scratch_answers"
DOCS_OUT = ROOT / "docs" / "scratch_answers"
MANIFEST = OUT / "manifest.json"


def sb3_name_for_md(md_filename):
    m = re.match(r"Scratch乘法第(\d+)课_(.+)\.md", md_filename)
    if m:
        title = m.group(2).split("（")[0].split("(")[0].strip()
        return f"M{int(m.group(1)):02d}_{title}_参考答案.sb3"
    m = re.match(r"第(\d+)课_(.+)_Scratch\.md", md_filename)
    if m:
        return f"S{int(m.group(1)):02d}_{m.group(2)}_参考答案.sb3"
    m = re.match(r"Scratch进阶第(\d+)课_(.+)\.md", md_filename)
    if m:
        title = m.group(2).split("（")[0].split("(")[0].strip()
        return f"A{int(m.group(1)):02d}_{title}_参考答案.sb3"
    m = re.match(r"AI训练师项目(\d+)课_(.+)\.md", md_filename)
    if m:
        n = int(m.group(1))
        title = m.group(2).split("（")[0].split("(")[0].strip()
        gmap = {2: "G01_大鱼吃小鱼①游起来", 3: "G02_大鱼吃小鱼②小鱼群", 4: "G03_大鱼吃小鱼③吃掉变大", 5: "G04_大鱼吃小鱼④完整版"}
        if n in gmap:
            return f"{gmap[n]}_参考答案.sb3"
        return None
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
    """蜗牛爬井：带刻度井背景 + 小猫沿标尺上下爬"""
    b.set_backdrop(well_backdrop_svg(depth_m=10))
    b.set_sprite_costume("Sprite1", CAT_SVG, name="小猫")
    for v in ("高度", "天数", "井深"):
        b.ensure_var("Sprite1", v)

    loop = Script(b, "Sprite1")
    loop.change_var("天数", 1)
    loop.say_join_vars("第 ", "天数", " 天", 0.8)
    loop.change_var("高度", 3)
    loop.say_join_vars("白天爬到 ", "高度", " 米", 0.8)
    loop.set_y_from_var_scaled("高度", WELL_METER_PX, WELL_BOTTOM_Y)
    loop.if_var_ge(
        "高度",
        "井深",
        Script(b, "Sprite1")
        .say_join_vars("爬出来啦！一共 ", "天数", " 天", 2.5)
        .stop_this_script(),
    )
    loop.change_var("高度", -2)
    loop.say_join_vars("晚上滑到 ", "高度", " 米", 0.8)
    loop.set_y_from_var_scaled("高度", WELL_METER_PX, WELL_BOTTOM_Y)

    s = b.script("Sprite1").flag()
    s.set_size(55)
    s.set_var("井深", 10).set_var("高度", 0).set_var("天数", 0)
    s.go_xy(0, WELL_BOTTOM_Y).set_y_from_var_scaled("高度", WELL_METER_PX, WELL_BOTTOM_Y)
    s.say("看右边黄色刻度尺！小猫爬几米，就对准第几米", 2)
    s.repeat_until_var_ge("高度", "井深", loop)
    s.say_join_vars("一共用了 ", "天数", " 天", 2)


def adv_02_buyer(b: SB3Builder):
    b.ensure_var("Sprite1", "件数")
    s = b.script("Sprite1").flag().ask("买了几件？每件 3 元")
    _set_var_from_answer(s, "件数")
    s.say("付 20 元，用 减法 算找零！", 2)


def adv_03_candy(b: SB3Builder):
    b.script("Sprite1").flag().ask("有多少颗糖？").ask("分给几个人？").say("用 除法 和 余数 算每人几颗！", 3)


def olymp_01_queue(b: SB3Builder):
    for v in ("前面名次", "后面名次", "总人数"):
        b.ensure_var("Sprite1", v)
    s = b.script("Sprite1").flag()
    s.set_var("前面名次", 4).set_var("后面名次", 6)
    s.set_var_sum2("总人数", "前面名次", "后面名次")
    s.change_var("总人数", -1)
    s.say_join("一共 ", "总人数", 2)
    s.say("4+6-1=9，小鱼被数了两次所以要减1！", 3)


def olymp_02_backtrack(b: SB3Builder):
    for v in ("现在", "给妈妈", "给爸爸", "原来"):
        b.ensure_var("Sprite1", v)
    s = b.script("Sprite1").flag()
    s.set_var("现在", 5).set_var("给妈妈", 3).set_var("给爸爸", 2)
    s.say("从结果倒着推回去：先加回来！", 2)
    s.set_var_sum3("原来", "现在", 2, 3)
    s.say_join("原来有 ", "原来", 2)
    s.say("5+2+3=10 颗糖 🍬", 2)


def olymp_03_age(b: SB3Builder):
    for v in ("小红年龄", "年龄差", "小明年龄"):
        b.ensure_var("Sprite1", v)
    s = b.script("Sprite1").flag()
    s.set_var("小红年龄", 5).set_var("年龄差", 2)
    s.set_var_sum2("小明年龄", "小红年龄", "年龄差")
    s.say_join("小明今年 ", "小明年龄", 2)
    s.say("5+2=7，大几岁就加几！🎂", 2)


def olymp_04_saw(b: SB3Builder):
    for v in ("段数", "锯次数"):
        b.ensure_var("Sprite1", v)
    s = b.script("Sprite1").flag()
    s.set_var("段数", 5)
    s.set_var_from_var("锯次数", "段数")
    s.change_var("锯次数", -1)
    s.say_join("锯成 ", "段数", 1)
    s.say_join("段，要锯 ", "锯次数", 2)
    s.say("段数-1=锯次数！🪚", 2)


def olymp_05_balance(b: SB3Builder):
    for v in ("小鱼", "小华", "总数", "平均", "移出"):
        b.ensure_var("Sprite1", v)
    s = b.script("Sprite1").flag()
    s.set_var("小鱼", 10).set_var("小华", 6)
    s.set_var_sum2("总数", "小鱼", "小华")
    s.set_var_divide_by_num("平均", "总数", 2)
    s.set_var_sub2("移出", "小鱼", "平均")
    s.say_join("每人应该 ", "平均", 2)
    s.say_join("小鱼要给出去 ", "移出", 2)
    s.say("移多补少：先加再除2！⚖️", 2)


def olymp_06_grad(b: SB3Builder):
    for v in ("前面", "后面", "总人数", "段数", "锯次数"):
        b.ensure_var("Sprite1", v)
    s = b.script("Sprite1").flag()
    s.say("奥数毕业快问快答！5 种武器", 2)
    s.set_var("前面", 4).set_var("后面", 6)
    s.set_var_sum2("总人数", "前面", "后面").change_var("总人数", -1)
    s.say_join("①排队：共 ", "总人数", 1.5)
    s.set_var("段数", 5)
    s.set_var_from_var("锯次数", "段数").change_var("锯次数", -1)
    s.say_join("②间隔：5段锯 ", "锯次数", 1.5)
    s.say("③倒推④年龄⑤移多补少：见各课 sb3！", 2)
    s.say("🎓 奥数小毕业快乐！", 2)


def adv_04_multiply(b: SB3Builder):
    for v in ("数字", "次数", "总和", "行数", "列数"):
        b.ensure_var("Sprite1", v)
    s = b.script("Sprite1").flag()
    s.say("乘法 = 重复加法！", 2).set_var("数字", 3).set_var("次数", 5).set_var("总和", 0)
    body = Script(b, "Sprite1").change_var_by_var("总和", "数字").say_join("加了一次：", "总和", 0.4)
    s.repeat(5, body)
    s.say_var_multiply("数字", "次数", 2).say("和点点阵行×列是一回事！", 2)


def mult_01_dot_grid(b: SB3Builder):
    b.add_sprite("Dot", DOT_SVG)
    for v in ("行数", "列数", "当前行", "当前列", "x坐标", "y坐标", "总数"):
        b.ensure_var("Dot", v)
    cell = Script(b, "Dot").set_grid_x().set_grid_y().go_xy_vars("x坐标", "y坐标").create_clone("Dot")
    cell.change_var("总数", 1).change_var("当前列", 1)
    row = Script(b, "Dot").set_var("当前列", 1).repeat(4, cell).change_var("当前行", 1)
    s = b.script("Dot").flag().hide()
    s.say("3 行 × 4 列 = ？个点", 2)
    s.set_var("行数", 3).set_var("列数", 4).set_var("总数", 0).set_var("当前行", 1)
    s.repeat(3, row)
    s.say("数完了！", 1).say_var_multiply("行数", "列数", 2)
    b.script("Dot").clone_start().show()


def mult_02_times_table(b: SB3Builder):
    for v in ("被乘数", "乘数", "a", "b"):
        b.ensure_var("Sprite1", v)
    inner = Script(b, "Sprite1").say_var_multiply("被乘数", "乘数", 0.7).change_var("乘数", 1)
    table = Script(b, "Sprite1").set_var("乘数", 1).repeat(9, inner)
    s = b.script("Sprite1").flag().say("背 7 的乘法口诀！", 2)
    s.set_var("被乘数", 7).repeat(9, table)
    s.say("按空格键：随机口算！", 1)
    quiz = b.script("Sprite1").key_flag_script("space")
    quiz.random_var("a", 1, 9).random_var("b", 1, 9).ask("a×b = ？（看变量）")
    quiz.if_answer_eq_product("a", "b",
                             Script(b, "Sprite1").say("答对啦！🎉", 1),
                             Script(b, "Sprite1").say("再想想！", 1))


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


def _fish_clean(b: SB3Builder):
    """Remove default empty Sprite1 from fish game projects."""
    if "Sprite1" in b.sprites and not b.sprites["Sprite1"]["blocks"]:
        b.remove_sprite("Sprite1")


def _fish_move_loop(b: SB3Builder, sprite: str) -> Script:
    loop = Script(b, sprite)
    loop.if_key("up arrow", Script(b, sprite).change_y(10))
    loop.if_key("down arrow", Script(b, sprite).change_y(-10))
    loop.if_key("left arrow", Script(b, sprite).change_x(-10))
    loop.if_key("right arrow", Script(b, sprite).change_x(10))
    return loop


def game_fish_01(b: SB3Builder):
    """G01: 大鱼方向键游动"""
    _fish_clean(b)
    b.add_sprite("BigFish", BIG_FISH_SVG)
    b.script("BigFish").flag().set_size(80).go_xy(0, 0).say("方向键游！大鱼吃小鱼 ①", 2)
    b.script("BigFish").flag().forever(_fish_move_loop(b, "BigFish"))


def game_fish_02(b: SB3Builder):
    """G02: 大鱼 + 克隆小鱼群"""
    game_fish_01(b)
    b.add_sprite("SmallFish", SMALL_FISH_SVG)
    swim = Script(b, "SmallFish").point_towards("_mouse_").move_steps(4)
    b.script("SmallFish").flag().hide()
    b.script("SmallFish").flag().repeat(8, Script(b, "SmallFish").create_clone("SmallFish"))
    b.script("SmallFish").clone_start().show().go_random_xy(-200, 200, -150, 150).forever(swim)


def game_fish_03(b: SB3Builder):
    """G03: 吃掉变大 + 得分"""
    _fish_clean(b)
    b.add_sprite("BigFish", BIG_FISH_SVG)
    b.add_sprite("SmallFish", SMALL_FISH_SVG)
    b.ensure_var("BigFish", "得分")
    body = _fish_move_loop(b, "BigFish")
    body.if_touching(
        "SmallFish",
        Script(b, "BigFish").change_var("得分", 1).change_size(5),
    )
    b.script("BigFish").flag().set_var("得分", 0).set_size(60).go_xy(0, 0).say("吃小鱼变大！得分！", 2)
    b.script("BigFish").flag().forever(body)
    swim = Script(b, "SmallFish")
    swim.if_touching("BigFish", Script(b, "SmallFish").delete_clone())
    swim.point_towards("_mouse_").move_steps(5)
    b.script("SmallFish").flag().hide()
    b.script("SmallFish").flag().repeat(10, Script(b, "SmallFish").create_clone("SmallFish"))
    b.script("SmallFish").clone_start().show().go_random_xy(-220, 220, -160, 160).forever(swim)


def game_fish_04(b: SB3Builder):
    """G04: 完整版 — 吃音效 + 鲨鱼 + Game Over"""
    _fish_clean(b)
    b.add_sprite("BigFish", BIG_FISH_SVG)
    b.add_sprite("SmallFish", SMALL_FISH_SVG)
    b.add_sprite("Shark", SHARK_SVG)
    b.ensure_var("BigFish", "得分")
    b.ensure_sound("BigFish", "Pop")

    eat = Script(b, "BigFish").play_sound("Pop").change_var("得分", 1).change_size(5)
    game_over = Script(b, "BigFish").say_join("游戏结束！得分：", "得分", 2).stop_all()

    body = _fish_move_loop(b, "BigFish")
    body.if_touching("SmallFish", eat)
    body.if_touching("Shark", game_over)

    b.script("BigFish").flag().set_var("得分", 0).set_size(60).go_xy(0, 0).say("躲鲨鱼！吃小鱼！🐟", 2)
    b.script("BigFish").flag().forever(body)

    swim = Script(b, "SmallFish")
    swim.if_touching("BigFish", Script(b, "SmallFish").delete_clone())
    swim.point_towards("_mouse_").move_steps(5)
    b.script("SmallFish").flag().hide()
    b.script("SmallFish").flag().repeat(10, Script(b, "SmallFish").create_clone("SmallFish"))
    b.script("SmallFish").clone_start().show().go_random_xy(-220, 220, -160, 160).forever(swim)

    patrol = Script(b, "Shark").move_steps(8).if_on_edge_bounce()
    b.script("Shark").flag().set_size(130).go_xy(-180, 120).forever(patrol)


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
    ("M01_几行几列点点阵_参考答案.sb3", mult_01_dot_grid),
    ("M02_九九乘法表_参考答案.sb3", mult_02_times_table),
    ("A04_乘法魔方_参考答案.sb3", adv_04_multiply),
    ("A05_飞机大战①起飞与开火_参考答案.sb3", adv_05_plane),
    ("A06_飞机大战②敌机来袭_参考答案.sb3", adv_06_plane2),
    ("A07_坦克大战_参考答案.sb3", adv_07_tank),
    ("O01_排队报数_参考答案.sb3", olymp_01_queue),
    ("O02_倒推法_参考答案.sb3", olymp_02_backtrack),
    ("O03_年龄差_参考答案.sb3", olymp_03_age),
    ("O04_锯木头间隔_参考答案.sb3", olymp_04_saw),
    ("O05_移多补少_参考答案.sb3", olymp_05_balance),
    ("O06_奥数小毕业_参考答案.sb3", olymp_06_grad),
    ("G01_大鱼吃小鱼①游起来_参考答案.sb3", game_fish_01),
    ("G02_大鱼吃小鱼②小鱼群_参考答案.sb3", game_fish_02),
    ("G03_大鱼吃小鱼③吃掉变大_参考答案.sb3", game_fish_03),
    ("G04_大鱼吃小鱼④完整版_参考答案.sb3", game_fish_04),
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
