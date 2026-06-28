#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build minimal valid Scratch 3 (.sb3) project files."""

from __future__ import annotations

import json
import uuid
import zipfile
from pathlib import Path
from typing import Any


def _bid() -> str:
    return uuid.uuid4().hex[:20]


def _asset_id() -> str:
    return uuid.uuid4().hex


TEMPLATE_SB3 = Path(__file__).resolve().parent.parent / "course" / "scratch_lesson_01.sb3"


# Simple orange cat SVG (opens fine in Scratch Desktop)
CAT_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="52" r="38" fill="#FFAB19" stroke="#CC8B17" stroke-width="2"/>
  <polygon points="20,25 30,5 40,25" fill="#FFAB19" stroke="#CC8B17"/>
  <polygon points="60,25 70,5 80,25" fill="#FFAB19" stroke="#CC8B17"/>
  <circle cx="38" cy="48" r="6" fill="#fff"/><circle cx="38" cy="48" r="3" fill="#000"/>
  <circle cx="62" cy="48" r="6" fill="#fff"/><circle cx="62" cy="48" r="3" fill="#000"/>
  <path d="M35 68 Q50 82 65 68" fill="none" stroke="#000" stroke-width="3" stroke-linecap="round"/>
</svg>"""

APPLE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60">
  <circle cx="30" cy="34" r="22" fill="#e11d48"/>
  <path d="M30 12 Q38 8 34 18" stroke="#16a34a" stroke-width="4" fill="none"/>
</svg>"""

DOT_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
  <circle cx="10" cy="10" r="8" fill="#fbbf24"/>
</svg>"""

PLANE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80">
  <polygon points="40,5 70,70 40,55 10,70" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
</svg>"""

BIG_FISH_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 60">
  <ellipse cx="45" cy="30" rx="38" ry="22" fill="#2563eb" stroke="#1d4ed8" stroke-width="2"/>
  <polygon points="78,30 95,20 95,40" fill="#2563eb"/>
  <circle cx="22" cy="24" r="5" fill="#fff"/><circle cx="22" cy="24" r="2.5" fill="#000"/>
</svg>"""

SMALL_FISH_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 36">
  <ellipse cx="28" cy="18" rx="22" ry="12" fill="#f97316" stroke="#ea580c" stroke-width="2"/>
  <polygon points="48,18 58,12 58,24" fill="#f97316"/>
  <circle cx="14" cy="15" r="3" fill="#fff"/><circle cx="14" cy="15" r="1.5" fill="#000"/>
</svg>"""

SHARK_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 70">
  <ellipse cx="52" cy="35" rx="46" ry="26" fill="#64748b" stroke="#334155" stroke-width="2"/>
  <polygon points="92,35 115,18 115,52" fill="#64748b"/>
  <circle cx="24" cy="28" r="6" fill="#fff"/><circle cx="24" cy="28" r="3" fill="#ef4444"/>
  <path d="M30 48 L55 42 L80 48" fill="none" stroke="#334155" stroke-width="3"/>
</svg>"""

# Snail-well lesson: 1 meter on stage = 12 Scratch y-units; 0 m sits at y = -150
WELL_METER_PX = 12
WELL_BOTTOM_Y = -150

# 5×7 pixel font for ruler labels (Scratch SVG does not render <text>)
_GLYPH_ROWS = {
    "0": ("11111", "10001", "10001", "10001", "10001", "10001", "11111"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("11111", "00001", "00001", "11111", "10000", "10000", "11111"),
    "3": ("11111", "00001", "00001", "11111", "00001", "00001", "11111"),
    "4": ("10001", "10001", "10001", "11111", "00001", "00001", "00001"),
    "5": ("11111", "10000", "10000", "11111", "00001", "00001", "11111"),
    "6": ("11111", "10000", "10000", "11111", "10001", "10001", "11111"),
    "7": ("11111", "00001", "00001", "00010", "00100", "01000", "01000"),
    "8": ("11111", "10001", "10001", "11111", "10001", "10001", "11111"),
    "9": ("11111", "10001", "10001", "11111", "00001", "00001", "11111"),
}


def _scratch_y_to_svg_y(scratch_y: float) -> float:
    return 180 - scratch_y


def _svg_glyph(parts: list[str], text: str, x: float, y: float, *, px: float = 2.2, fill: str = "#0D47A1") -> None:
    """Draw digits using small rects (Scratch-compatible, no <text>)."""
    cursor = x
    for ch in text:
        rows = _GLYPH_ROWS.get(ch)
        if not rows:
            cursor += px * 6
            continue
        for row_i, row in enumerate(rows):
            for col_i, bit in enumerate(row):
                if bit == "1":
                    parts.append(
                        f'<rect x="{cursor + col_i * px}" y="{y + row_i * px}" '
                        f'width="{px - 0.2}" height="{px - 0.2}" fill="{fill}"/>'
                    )
        cursor += px * 6


def well_backdrop_svg(*, depth_m: int = 10, meter_px: int = WELL_METER_PX, bottom_y: int = WELL_BOTTOM_Y) -> str:
    """Stage backdrop: well shaft + vertical ruler (0 … depth_m meters), shapes only."""
    top_y = bottom_y + depth_m * meter_px
    svg_top = _scratch_y_to_svg_y(top_y)
    svg_bottom = _scratch_y_to_svg_y(bottom_y)
    shaft_h = svg_bottom - svg_top
    wall_l = 168
    wall_r = 312
    ruler_x = 368
    panel_l = 338
    panel_r = 472
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360">',
        '<rect width="480" height="360" fill="#87CEEB"/>',
        f'<rect y="{svg_top - 8}" width="480" height="{360 - svg_top + 8}" fill="#66BB6A"/>',
        # ruler panel (high contrast)
        f'<rect x="{panel_l}" y="{svg_top - 14}" width="{panel_r - panel_l}" height="{shaft_h + 28}" '
        f'fill="#FFFDE7" stroke="#F9A825" stroke-width="3" rx="4"/>',
        f'<rect x="{wall_l}" y="{svg_top}" width="{wall_r - wall_l}" height="{shaft_h}" fill="#455A64" opacity="0.18"/>',
        f'<rect x="{wall_l}" y="{svg_top}" width="14" height="{shaft_h}" fill="#6D4C41" rx="2"/>',
        f'<rect x="{wall_r - 14}" y="{svg_top}" width="14" height="{shaft_h}" fill="#6D4C41" rx="2"/>',
        f'<line x1="{ruler_x}" y1="{svg_top - 4}" x2="{ruler_x}" y2="{svg_bottom + 4}" stroke="#D32F2F" stroke-width="6"/>',
        f'<rect x="{panel_l + 6}" y="{svg_top - 12}" width="{panel_r - panel_l - 12}" height="10" fill="#F9A825" rx="2"/>',
    ]
    _svg_glyph(parts, "m", panel_l + 14, svg_top - 11, px=1.8, fill="#FFFFFF")
    for m in range(depth_m + 1):
        sy = bottom_y + m * meter_px
        svg_y = _scratch_y_to_svg_y(sy)
        tick_w = 22 if m % 5 == 0 else 16
        stroke_w = 4 if m % 5 == 0 else 2.5
        parts.append(
            f'<line x1="{ruler_x - tick_w}" y1="{svg_y}" x2="{ruler_x + tick_w}" y2="{svg_y}" '
            f'stroke="#1565C0" stroke-width="{stroke_w}"/>'
        )
        label = str(m)
        _svg_glyph(parts, label, ruler_x + 26, svg_y - 7, px=2.4, fill="#0D47A1" if m < depth_m else "#2E7D32")
        if m == depth_m:
            parts.append(
                f'<polygon points="{ruler_x + 58},{svg_y - 8} {ruler_x + 70},{svg_y} {ruler_x + 58},{svg_y + 8}" fill="#2E7D32"/>'
            )
    parts.append("</svg>")
    return "\n".join(parts)


class Script:
    """Build a linked chain of Scratch blocks."""

    def __init__(self, builder: "SB3Builder", sprite_name: str):
        self.b = builder
        self.sprite_name = sprite_name
        self.sprite = builder.sprites[sprite_name]
        self.blocks: dict[str, Any] = self.sprite["blocks"]
        self._owned: set[str] = set()
        self.head: str | None = None
        self.tail: str | None = None
        self.y = 50

    def _link(self, block_id: str, *, x: int | None = None) -> str:
        blk = self.blocks[block_id]
        if self.tail:
            self.blocks[self.tail]["next"] = block_id
            blk["parent"] = self.tail
            blk["topLevel"] = False
        else:
            self.head = block_id
            blk["topLevel"] = True
            blk["x"] = x if x is not None else 50
            blk["y"] = self.y
        self.tail = block_id
        return block_id

    def _block(self, opcode: str, *, inputs=None, fields=None, mutation=None, shadow=False) -> str:
        bid = _bid()
        self.blocks[bid] = {
            "opcode": opcode,
            "next": None,
            "parent": None,
            "inputs": inputs or {},
            "fields": fields or {},
            "shadow": shadow,
            "topLevel": False,
        }
        if mutation:
            self.blocks[bid]["mutation"] = mutation
        self._owned.add(bid)
        return bid

    def _lit_str(self, text: str) -> list:
        return [1, [10, str(text)]]

    def _lit_num(self, num: float | int) -> list:
        n = str(int(num)) if float(num).is_integer() else str(num)
        return [1, [4, n]]

    def _absorb_body(self, body: "Script") -> str | None:
        """Merge a sub-script into this sprite; clear erroneous topLevel flags."""
        sub_id = body.head
        if not sub_id:
            return None
        self._owned.update(body._owned)
        for bid in body._owned:
            blk = self.blocks[bid]
            blk["topLevel"] = False
            blk.pop("x", None)
            blk.pop("y", None)
        return sub_id

    def _substack(self, bid: str) -> list:
        return [2, bid]

    def _var_field(self, name: str) -> list:
        vid = self.b.ensure_var(self.sprite_name, name)
        return [name, vid]

    def _var_input(self, name: str) -> list:
        rid = self._block("data_variable", fields={"VARIABLE": self._var_field(name)})
        return [2, rid]

    def _list_field(self, name: str) -> list:
        lid = self.b.ensure_list(self.sprite_name, name)
        return [name, lid]

    def _answer(self) -> list:
        rid = self._block("sensing_answer")
        return [2, rid]

    def _ref(self, block_id: str) -> list:
        return [2, block_id]

    def flag(self) -> "Script":
        self._link(self._block("event_whenflagclicked"))
        return self

    def say(self, text: str, secs: float = 2) -> "Script":
        self._link(self._block(
            "looks_sayforsecs",
            inputs={"MESSAGE": self._lit_str(text), "SECS": self._lit_num(secs)},
        ))
        return self

    def ask(self, question: str) -> "Script":
        self._link(self._block("sensing_askandwait", inputs={"QUESTION": self._lit_str(question)}))
        return self

    def set_var(self, name: str, value: str | float | int) -> "Script":
        if isinstance(value, str) and not value.isidentifier():
            val_in = self._lit_str(value)
        elif isinstance(value, str):
            val_in = self._var_input(value)
        else:
            val_in = self._lit_num(value)
        self._link(self._block(
            "data_setvariableto",
            inputs={"VALUE": val_in},
            fields={"VARIABLE": self._var_field(name)},
        ))
        return self

    def change_var(self, name: str, delta: float | int) -> "Script":
        self._link(self._block(
            "data_changevariableby",
            inputs={"VALUE": self._lit_num(delta)},
            fields={"VARIABLE": self._var_field(name)},
        ))
        return self

    def change_var_by_var(self, target: str, source_var: str) -> "Script":
        self._link(self._block(
            "data_changevariableby",
            inputs={"VALUE": self._var_input(source_var)},
            fields={"VARIABLE": self._var_field(target)},
        ))
        return self

    def say_join(self, a: str, b_var: str, secs: float = 2) -> "Script":
        jid = self._block("operator_join", inputs={
            "STRING1": self._lit_str(a),
            "STRING2": self._var_input(b_var),
        })
        self._link(self._block(
            "looks_sayforsecs",
            inputs={"MESSAGE": [2, jid], "SECS": self._lit_num(secs)},
        ))
        return self

    def say_expr(self, text: str, expr_block: str, secs: float = 2) -> "Script":
        jid = self._block("operator_join", inputs={
            "STRING1": self._lit_str(text),
            "STRING2": [2, expr_block],
        })
        self._link(self._block(
            "looks_sayforsecs",
            inputs={"MESSAGE": [2, jid], "SECS": self._lit_num(secs)},
        ))
        return self

    def say_math(self, a: str, op: str, b: str, prefix: str = "", secs: float = 2) -> "Script":
        ops = {"+": "operator_add", "-": "operator_sub", "*": "operator_multiply", "/": "operator_divide"}
        mid = self._block(ops[op], inputs={"NUM1": self._lit_num(a), "NUM2": self._lit_num(b)})
        if prefix:
            return self.say_expr(prefix, mid, secs)
        self._link(self._block(
            "looks_sayforsecs",
            inputs={"MESSAGE": [2, mid], "SECS": self._lit_num(secs)},
        ))
        return self

    def say_var_expr(self, prefix: str, var_a: str, op: str, var_b: str, secs: float = 2) -> "Script":
        ops = {"+": "operator_add", "-": "operator_sub", "*": "operator_multiply", "/": "operator_divide"}
        va = self._block("data_variable", fields={"VARIABLE": self._var_field(var_a)})
        vb = self._block("data_variable", fields={"VARIABLE": self._var_field(var_b)})
        mid = self._block(ops[op], inputs={"NUM1": [2, va], "NUM2": [2, vb]})
        return self.say_expr(prefix, mid, secs)

    def if_eq_answer(self, value: str, then: Script, else_: Script | None = None) -> "Script":
        eq = self._block("operator_equals", inputs={
            "OPERAND1": self._answer(),
            "OPERAND2": self._lit_str(value),
        })
        sub_id = self._absorb_body(then)
        if else_:
            sub2_id = self._absorb_body(else_)
            bid = self._block("control_if_else", inputs={
                "CONDITION": [2, eq],
                "SUBSTACK": self._substack(sub_id) if sub_id else [2, None],
                "SUBSTACK2": self._substack(sub2_id) if sub2_id else [2, None],
            })
            if sub2_id:
                self.blocks[sub2_id]["parent"] = bid
        else:
            bid = self._block("control_if", inputs={
                "CONDITION": [2, eq],
                "SUBSTACK": self._substack(sub_id) if sub_id else [2, None],
            })
        if sub_id:
            self.blocks[sub_id]["parent"] = bid
        self._link(bid)
        return self

    def if_var_eq(self, var: str, value: str | int, then: Script, else_: Script | None = None) -> "Script":
        va = self._block("data_variable", fields={"VARIABLE": self._var_field(var)})
        eq = self._block("operator_equals", inputs={
            "OPERAND1": [2, va],
            "OPERAND2": self._lit_num(value) if isinstance(value, int) else self._lit_str(value),
        })
        sub_id = self._absorb_body(then)
        if else_:
            sub2_id = self._absorb_body(else_)
            bid = self._block("control_if_else", inputs={
                "CONDITION": [2, eq],
                "SUBSTACK": self._substack(sub_id) if sub_id else [2, None],
                "SUBSTACK2": self._substack(sub2_id) if sub2_id else [2, None],
            })
            if sub2_id:
                self.blocks[sub2_id]["parent"] = bid
        else:
            bid = self._block("control_if", inputs={
                "CONDITION": [2, eq],
                "SUBSTACK": self._substack(sub_id) if sub_id else [2, None],
            })
        if sub_id:
            self.blocks[sub_id]["parent"] = bid
        self._link(bid)
        return self

    def wait(self, secs: float) -> "Script":
        self._link(self._block("control_wait", inputs={"DURATION": self._lit_num(secs)}))
        return self

    def repeat(self, times: int, body: Script) -> "Script":
        sub_id = self._absorb_body(body)
        bid = self._block("control_repeat", inputs={
            "TIMES": self._lit_num(times),
            "SUBSTACK": self._substack(sub_id) if sub_id else [2, None],
        })
        if sub_id:
            self.blocks[sub_id]["parent"] = bid
        self._link(bid)
        return self

    def forever(self, body: Script) -> "Script":
        sub_id = self._absorb_body(body)
        bid = self._block("control_forever", inputs={
            "SUBSTACK": self._substack(sub_id) if sub_id else [2, None],
        })
        if sub_id:
            self.blocks[sub_id]["parent"] = bid
        self._link(bid)
        return self

    def move(self, steps: int) -> "Script":
        self._link(self._block("motion_movesteps", inputs={"STEPS": self._lit_num(steps)}))
        return self

    def turn_right(self, deg: int = 90) -> "Script":
        self._link(self._block("motion_turnright", inputs={"DEGREES": self._lit_num(deg)}))
        return self

    def go_xy(self, x: int, y: int) -> "Script":
        self._link(self._block("motion_gotoxy", inputs={"X": self._lit_num(x), "Y": self._lit_num(y)}))
        return self

    def change_y(self, dy: int) -> "Script":
        self._link(self._block("motion_changeyby", inputs={"DY": self._lit_num(dy)}))
        return self

    def change_x(self, dx: int) -> "Script":
        self._link(self._block("motion_changexby", inputs={"DX": self._lit_num(dx)}))
        return self

    def point_towards(self, target: str = "_mouse_") -> "Script":
        self._link(self._block("motion_pointtowards", fields={"TOWARDS": [target, None]}))
        return self

    def move_steps(self, steps: int) -> "Script":
        self._link(self._block("motion_movesteps", inputs={"STEPS": self._lit_num(steps)}))
        return self

    def turn_right(self, deg: int) -> "Script":
        self._link(self._block("motion_turnright", inputs={"DEGREES": self._lit_num(deg)}))
        return self

    def set_size(self, pct: int) -> "Script":
        self._link(self._block("looks_setsizeto", inputs={"SIZE": self._lit_num(pct)}))
        return self

    def change_size(self, delta: int) -> "Script":
        self._link(self._block("looks_changesizeby", inputs={"CHANGE": self._lit_num(delta)}))
        return self

    def if_touching(self, target: str, then: Script) -> "Script":
        cond = self.touching(target)
        sub_id = self._absorb_body(then)
        bid = self._block("control_if", inputs={
            "CONDITION": [2, cond],
            "SUBSTACK": self._substack(sub_id) if sub_id else [2, None],
        })
        if sub_id:
            self.blocks[sub_id]["parent"] = bid
        self._link(bid)
        return self

    def go_random_xy(self, xlo: int, xhi: int, ylo: int, yhi: int) -> "Script":
        self.random_var("随机x", xlo, xhi)
        self.random_var("随机y", ylo, yhi)
        return self.go_xy_vars("随机x", "随机y")

    def play_sound(self, name: str) -> "Script":
        self._link(self._block("sound_play", fields={"SOUND_MENU": [name, None]}))
        return self

    def stop_all(self) -> "Script":
        self._link(self._block("control_stop", fields={"STOP_OPTION": ["all", None]}))
        return self

    def if_on_edge_bounce(self) -> "Script":
        self._link(self._block("motion_ifonedgebounce"))
        return self

    def set_random_x(self, lo: int, hi: int, y: int) -> "Script":
        rnd = self._block("operator_random", inputs={"FROM": self._lit_num(lo), "TO": self._lit_num(hi)})
        self._link(self._block("motion_gotoxy", inputs={"X": [2, rnd], "Y": self._lit_num(y)}))
        return self

    def random_var(self, name: str, lo: int, hi: int) -> "Script":
        rnd = self._block("operator_random", inputs={"FROM": self._lit_num(lo), "TO": self._lit_num(hi)})
        self._link(self._block(
            "data_setvariableto",
            inputs={"VALUE": [2, rnd]},
            fields={"VARIABLE": self._var_field(name)},
        ))
        return self

    def add_to_list(self, item: str, list_name: str) -> "Script":
        self._link(self._block(
            "data_addtolist",
            inputs={"ITEM": self._lit_str(item)},
            fields={"LIST": self._list_field(list_name)},
        ))
        return self

    def add_answer_to_list(self, list_name: str) -> "Script":
        self._link(self._block(
            "data_addtolist",
            inputs={"ITEM": self._answer()},
            fields={"LIST": self._list_field(list_name)},
        ))
        return self

    def say_list(self, prefix: str, list_name: str, secs: float = 2) -> "Script":
        item = self._block("data_itemoflist", inputs={"INDEX": self._lit_num(1)}, fields={"LIST": self._list_field(list_name)})
        return self.say_expr(prefix, item, secs)

    def pen_clear(self) -> "Script":
        self.b.use_extension("pen")
        self._link(self._block("pen_clear"))
        return self

    def pen_down(self) -> "Script":
        self.b.use_extension("pen")
        self._link(self._block("pen_penDown"))
        return self

    def pen_up(self) -> "Script":
        self.b.use_extension("pen")
        self._link(self._block("pen_penUp"))
        return self

    def go_xy_vars(self, x_var: str, y_var: str) -> "Script":
        xv = self._block("data_variable", fields={"VARIABLE": self._var_field(x_var)})
        yv = self._block("data_variable", fields={"VARIABLE": self._var_field(y_var)})
        self._link(self._block("motion_gotoxy", inputs={"X": [2, xv], "Y": [2, yv]}))
        return self

    def set_grid_x(self) -> "Script":
        """x坐标 = -120 + 当前列 × 30"""
        col = self._block("data_variable", fields={"VARIABLE": self._var_field("当前列")})
        mul = self._block("operator_multiply", inputs={"NUM1": self._lit_num(30), "NUM2": [2, col]})
        add = self._block("operator_add", inputs={"NUM1": self._lit_num(-120), "NUM2": [2, mul]})
        self._link(self._block(
            "data_setvariableto",
            inputs={"VALUE": [2, add]},
            fields={"VARIABLE": self._var_field("x坐标")},
        ))
        return self

    def set_grid_y(self) -> "Script":
        """y坐标 = 100 - 当前行 × 30"""
        row = self._block("data_variable", fields={"VARIABLE": self._var_field("当前行")})
        mul = self._block("operator_multiply", inputs={"NUM1": self._lit_num(30), "NUM2": [2, row]})
        sub = self._block("operator_sub", inputs={"NUM1": self._lit_num(100), "NUM2": [2, mul]})
        self._link(self._block(
            "data_setvariableto",
            inputs={"VALUE": [2, sub]},
            fields={"VARIABLE": self._var_field("y坐标")},
        ))
        return self

    def say_var_multiply(self, var_a: str, var_b: str, secs: float = 1.5) -> "Script":
        va = self._block("data_variable", fields={"VARIABLE": self._var_field(var_a)})
        vb = self._block("data_variable", fields={"VARIABLE": self._var_field(var_b)})
        mul = self._block("operator_multiply", inputs={"NUM1": [2, va], "NUM2": [2, vb]})
        j1 = self._block("operator_join", inputs={"STRING1": self._lit_str(""), "STRING2": [2, va]})
        j2 = self._block("operator_join", inputs={"STRING1": [2, j1], "STRING2": self._lit_str(" × ")})
        j3 = self._block("operator_join", inputs={"STRING1": [2, j2], "STRING2": [2, vb]})
        j4 = self._block("operator_join", inputs={"STRING1": [2, j3], "STRING2": self._lit_str(" = ")})
        j5 = self._block("operator_join", inputs={"STRING1": [2, j4], "STRING2": [2, mul]})
        self._link(self._block(
            "looks_sayforsecs",
            inputs={"MESSAGE": [2, j5], "SECS": self._lit_num(secs)},
        ))
        return self

    def if_answer_eq_product(self, var_a: str, var_b: str, then: Script, else_: Script | None = None) -> "Script":
        va = self._block("data_variable", fields={"VARIABLE": self._var_field(var_a)})
        vb = self._block("data_variable", fields={"VARIABLE": self._var_field(var_b)})
        prod = self._block("operator_multiply", inputs={"NUM1": [2, va], "NUM2": [2, vb]})
        eq = self._block("operator_equals", inputs={"OPERAND1": self._answer(), "OPERAND2": [2, prod]})
        sub_id = self._absorb_body(then)
        if else_:
            sub2_id = self._absorb_body(else_)
            bid = self._block("control_if_else", inputs={
                "CONDITION": [2, eq],
                "SUBSTACK": self._substack(sub_id) if sub_id else [2, None],
                "SUBSTACK2": self._substack(sub2_id) if sub2_id else [2, None],
            })
            if sub2_id:
                self.blocks[sub2_id]["parent"] = bid
        else:
            bid = self._block("control_if", inputs={
                "CONDITION": [2, eq],
                "SUBSTACK": self._substack(sub_id) if sub_id else [2, None],
            })
        if sub_id:
            self.blocks[sub_id]["parent"] = bid
        self._link(bid)
        return self

    def hide(self) -> "Script":
        self._link(self._block("looks_hide"))
        return self

    def show(self) -> "Script":
        self._link(self._block("looks_show"))
        return self

    def key_flag_script(self, key: str) -> "Script":
        self.head = self.tail = None
        self._link(self._block("event_whenkeypressed", fields={"KEY_OPTION": [key, None]}))
        return self

    def clone_start(self) -> "Script":
        self.head = self.tail = None
        self._link(self._block("control_start_as_clone"))
        return self

    def create_clone(self, target: str = "_myself_") -> "Script":
        self._link(self._block("control_create_clone_of", fields={"CLONE_OPTION": [target, None]}))
        return self

    def delete_clone(self) -> "Script":
        self._link(self._block("control_delete_this_clone"))
        return self

    def key_pressed(self, key: str) -> str:
        return self._block("sensing_keypressed", fields={"KEY_OPTION": [key, None]})

    def if_key(self, key: str, then: Script) -> "Script":
        cond = self.key_pressed(key)
        sub_id = self._absorb_body(then)
        bid = self._block("control_if", inputs={
            "CONDITION": [2, cond],
            "SUBSTACK": self._substack(sub_id) if sub_id else [2, None],
        })
        if sub_id:
            self.blocks[sub_id]["parent"] = bid
        self._link(bid)
        return self

    def touching(self, target: str) -> str:
        return self._block("sensing_touchingobject", fields={"TOUCHINGOBJECTMENU": [target, None]})

    def repeat_until_touch(self, target: str, body: Script) -> "Script":
        cond = self.touching(target)
        sub_id = self._absorb_body(body)
        bid = self._block("control_repeat_until", inputs={
            "CONDITION": [2, cond],
            "SUBSTACK": self._substack(sub_id) if sub_id else [2, None],
        })
        if sub_id:
            self.blocks[sub_id]["parent"] = bid
        self._link(bid)
        return self

    def _var_ge(self, var_a: str, var_b: str) -> str:
        va = self._block("data_variable", fields={"VARIABLE": self._var_field(var_a)})
        vb = self._block("data_variable", fields={"VARIABLE": self._var_field(var_b)})
        gt = self._block("operator_gt", inputs={"OPERAND1": [2, va], "OPERAND2": [2, vb]})
        eq = self._block("operator_equals", inputs={"OPERAND1": [2, va], "OPERAND2": [2, vb]})
        return self._block("operator_or", inputs={"OPERAND1": [2, gt], "OPERAND2": [2, eq]})

    def repeat_until_var_ge(self, var_a: str, var_b: str, body: Script) -> "Script":
        cond = self._var_ge(var_a, var_b)
        sub_id = self._absorb_body(body)
        bid = self._block("control_repeat_until", inputs={
            "CONDITION": [2, cond],
            "SUBSTACK": self._substack(sub_id) if sub_id else [2, None],
        })
        if sub_id:
            self.blocks[sub_id]["parent"] = bid
        self._link(bid)
        return self

    def if_var_ge(self, var_a: str, var_b: str, then: Script) -> "Script":
        cond = self._var_ge(var_a, var_b)
        sub_id = self._absorb_body(then)
        bid = self._block("control_if", inputs={
            "CONDITION": [2, cond],
            "SUBSTACK": self._substack(sub_id) if sub_id else [2, None],
        })
        if sub_id:
            self.blocks[sub_id]["parent"] = bid
        self._link(bid)
        return self

    def stop_this_script(self) -> "Script":
        self._link(self._block("control_stop", fields={"STOP_OPTION": ["this script", None]}))
        return self

    def set_y_from_var_scaled(self, var_name: str, scale: int, offset: int) -> "Script":
        """y = var * scale + offset"""
        vv = self._block("data_variable", fields={"VARIABLE": self._var_field(var_name)})
        mul = self._block("operator_multiply", inputs={"NUM1": [2, vv], "NUM2": self._lit_num(scale)})
        yv = self._block("operator_add", inputs={"NUM1": [2, mul], "NUM2": self._lit_num(offset)})
        self._link(self._block("motion_sety", inputs={"Y": [2, yv]}))
        return self

    def say_join_vars(self, prefix: str, var_name: str, suffix: str, secs: float = 1) -> "Script":
        j1 = self._block("operator_join", inputs={
            "STRING1": self._lit_str(prefix),
            "STRING2": self._var_input(var_name),
        })
        j2 = self._block("operator_join", inputs={"STRING1": [2, j1], "STRING2": self._lit_str(suffix)})
        self._link(self._block(
            "looks_sayforsecs",
            inputs={"MESSAGE": [2, j2], "SECS": self._lit_num(secs)},
        ))
        return self

    def _var_block(self, name: str) -> str:
        return self._block("data_variable", fields={"VARIABLE": self._var_field(name)})

    def set_var_sum2(self, target: str, var_a: str, var_b: str) -> "Script":
        va = self._var_block(var_a)
        vb = self._var_block(var_b)
        add = self._block("operator_add", inputs={"NUM1": [2, va], "NUM2": [2, vb]})
        self._link(self._block(
            "data_setvariableto",
            inputs={"VALUE": [2, add]},
            fields={"VARIABLE": self._var_field(target)},
        ))
        return self

    def set_var_sub2(self, target: str, var_a: str, var_b: str) -> "Script":
        va = self._var_block(var_a)
        vb = self._var_block(var_b)
        sub = self._block("operator_sub", inputs={"NUM1": [2, va], "NUM2": [2, vb]})
        self._link(self._block(
            "data_setvariableto",
            inputs={"VALUE": [2, sub]},
            fields={"VARIABLE": self._var_field(target)},
        ))
        return self

    def set_var_sum3(self, target: str, var_a: str, num_b: int, num_c: int) -> "Script":
        va = self._var_block(var_a)
        add1 = self._block("operator_add", inputs={"NUM1": [2, va], "NUM2": self._lit_num(num_b)})
        add2 = self._block("operator_add", inputs={"NUM1": [2, add1], "NUM2": self._lit_num(num_c)})
        self._link(self._block(
            "data_setvariableto",
            inputs={"VALUE": [2, add2]},
            fields={"VARIABLE": self._var_field(target)},
        ))
        return self

    def set_var_from_var(self, target: str, source: str) -> "Script":
        self._link(self._block(
            "data_setvariableto",
            inputs={"VALUE": self._var_input(source)},
            fields={"VARIABLE": self._var_field(target)},
        ))
        return self

    def set_var_divide_by_num(self, target: str, source_var: str, divisor: int) -> "Script":
        va = self._var_block(source_var)
        div = self._block("operator_divide", inputs={"NUM1": [2, va], "NUM2": self._lit_num(divisor)})
        floor = self._block("operator_mathop", inputs={"NUM": [2, div]}, fields={"OPERATOR": ["floor", None]})
        self._link(self._block(
            "data_setvariableto",
            inputs={"VALUE": [2, floor]},
            fields={"VARIABLE": self._var_field(target)},
        ))
        return self

    def define_block(self, name: str, body: Script) -> tuple[str, str]:
        proto = _bid()
        self.blocks[proto] = {
            "opcode": "procedures_prototype",
            "next": None,
            "parent": None,
            "inputs": {},
            "fields": {},
            "shadow": True,
            "topLevel": False,
            "mutation": {
                "tagName": "mutation",
                "proccode": name,
                "argumentids": "[]",
                "argumentnames": "[]",
                "argumentdefaults": "[]",
                "warp": "false",
            },
        }
        def_id = _bid()
        sub_id = self._absorb_body(body)
        self.blocks[def_id] = {
            "opcode": "procedures_definition",
            "next": sub_id,
            "parent": None,
            "inputs": {"custom_block": [1, proto]},
            "fields": {},
            "shadow": False,
            "topLevel": True,
            "x": 50,
            "y": self.y,
        }
        if sub_id:
            self.blocks[sub_id]["parent"] = def_id
        call_id = _bid()
        self.blocks[call_id] = {
            "opcode": "procedures_call",
            "next": None,
            "parent": None,
            "inputs": {},
            "fields": {},
            "shadow": False,
            "topLevel": False,
            "mutation": {
                "tagName": "mutation",
                "proccode": name,
                "argumentids": "[]",
                "warp": "false",
            },
        }
        self.y += 200
        return def_id, call_id

    def call(self, call_id: str) -> "Script":
        self._link(call_id)
        return self


class SB3Builder:
    def __init__(self):
        self.extensions: set[str] = set()
        self.assets: dict[str, bytes | str] = {}
        self._template_assets: dict[str, bytes] = {}
        self._tpl_stage: dict | None = None
        self._tpl_sprite: dict | None = None
        self._load_template()
        self.stage = self._empty_target(is_stage=True, name="Stage")
        self.sprites: dict[str, dict] = {"Stage": self.stage}
        self._var_ids: dict[tuple[str, str], str] = {}
        self._list_ids: dict[tuple[str, str], str] = {}

    def _load_template(self) -> None:
        if not TEMPLATE_SB3.exists():
            return
        with zipfile.ZipFile(TEMPLATE_SB3) as zf:
            tpl = json.loads(zf.read("project.json"))
            self._tpl_stage = tpl["targets"][0]
            self._tpl_sprite = tpl["targets"][1]
            for name in zf.namelist():
                if name != "project.json":
                    self._template_assets[name] = zf.read(name)

    def use_extension(self, name: str):
        self.extensions.add(name)

    def ensure_var(self, sprite: str, name: str) -> str:
        key = (sprite, name)
        if key not in self._var_ids:
            vid = _bid()
            self._var_ids[key] = vid
            self.sprites[sprite]["variables"][vid] = [name, 0]
        return self._var_ids[key]

    def ensure_list(self, sprite: str, name: str) -> str:
        key = (sprite, name)
        if key not in self._list_ids:
            lid = _bid()
            self._list_ids[key] = lid
            self.sprites[sprite]["lists"][lid] = [name, []]
        return self._list_ids[key]

    def _costume(self, name: str, svg: str, *, is_stage: bool = False) -> dict:
        aid = _asset_id()
        fname = f"{aid}.svg"
        self.assets[fname] = svg
        return {
            "name": name,
            "dataFormat": "svg",
            "assetId": aid,
            "md5ext": fname,
            "rotationCenterX": 240 if is_stage else 48,
            "rotationCenterY": 180 if is_stage else 50,
        }

    def _empty_target(self, *, is_stage: bool, name: str, svg: str = CAT_SVG) -> dict:
        if is_stage and self._tpl_stage:
            t = {k: v for k, v in self._tpl_stage.items() if k not in ("blocks", "comments", "variables", "lists")}
            t["variables"] = {}
            t["lists"] = {}
            t["blocks"] = {}
            t["comments"] = {}
            t["sounds"] = []
            return t
        if not is_stage and name == "Sprite1" and self._tpl_sprite:
            t = {k: v for k, v in self._tpl_sprite.items() if k not in ("blocks", "comments", "variables", "lists")}
            t["variables"] = {}
            t["lists"] = {}
            t["blocks"] = {}
            t["comments"] = {}
            t["sounds"] = []
            return t
        return {
            "isStage": is_stage,
            "name": name,
            "variables": {},
            "lists": {},
            "broadcasts": {},
            "blocks": {},
            "comments": {},
            "currentCostume": 0,
            "costumes": [self._costume("costume1", svg)],
            "sounds": [],
            "volume": 100,
            "visible": False if is_stage else True,
            "layerOrder": 0 if is_stage else 1,
            "x": 0,
            "y": 0,
            "size": 100,
            "direction": 90,
            "draggable": False,
            "rotationStyle": "all around",
        }

    def add_sprite(self, name: str, svg: str = CAT_SVG) -> dict:
        sp = self._empty_target(is_stage=False, name=name, svg=svg)
        self.sprites[name] = sp
        return sp

    def remove_sprite(self, name: str) -> None:
        self.sprites.pop(name, None)

    def set_backdrop(self, svg: str, name: str = "well") -> None:
        self.stage["costumes"] = [self._costume(name, svg, is_stage=True)]
        self.stage["currentCostume"] = 0

    def set_sprite_costume(self, sprite: str, svg: str, name: str = "小猫") -> None:
        c = self._costume(name, svg)
        c["rotationCenterX"] = 50
        c["rotationCenterY"] = 50
        self.sprites[sprite]["costumes"] = [c]
        self.sprites[sprite]["currentCostume"] = 0

    def _pop_wav_bytes(self) -> tuple[bytes, int, int]:
        import io
        import math
        import struct
        import wave

        rate = 22050
        duration = 0.12
        freq = 880.0
        n = int(rate * duration)
        buf = io.BytesIO()
        with wave.open(buf, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(rate)
            frames = bytearray()
            for i in range(n):
                amp = 16000 * (1.0 - i / n)
                val = int(amp * math.sin(2 * math.pi * freq * i / rate))
                frames.extend(struct.pack("<h", val))
            w.writeframes(bytes(frames))
        data = buf.getvalue()
        return data, rate, n

    def ensure_sound(self, sprite: str, name: str, *, wav: bytes | None = None, sample_rate: int = 22050, sample_count: int | None = None) -> str:
        sp = self.sprites[sprite]
        for snd in sp["sounds"]:
            if snd["name"] == name:
                return snd["assetId"]
        if wav is None:
            wav, sample_rate, sample_count = self._pop_wav_bytes()
        elif sample_count is None:
            sample_count = max(0, (len(wav) - 44) // 2)
        aid = _asset_id()
        fname = f"{aid}.wav"
        self.assets[fname] = wav
        sp["sounds"].append({
            "name": name,
            "assetId": aid,
            "dataFormat": "wav",
            "format": "",
            "rate": sample_rate,
            "sampleCount": sample_count,
            "md5ext": fname,
        })
        return aid

    def script(self, sprite: str = "Sprite1") -> Script:
        if sprite not in self.sprites:
            self.add_sprite(sprite)
        return Script(self, sprite)

    def _build_monitors(self) -> list[dict]:
        monitors = []
        y = 5
        for (sprite_name, var_name), vid in self._var_ids.items():
            value = self.sprites[sprite_name]["variables"][vid][1]
            monitors.append({
                "id": vid,
                "mode": "default",
                "opcode": "data_variable",
                "params": {"VARIABLE": var_name},
                "spriteName": None if sprite_name == "Stage" else sprite_name,
                "value": value,
                "width": 0,
                "height": 0,
                "x": 5,
                "y": y,
                "visible": True,
                "sliderMin": 0,
                "sliderMax": 200,
                "isDiscrete": True,
            })
            y += 30
        return monitors

    def _finalize_targets(self) -> list[dict]:
        targets = list(self.sprites.values())
        layer = 0
        for t in targets:
            if t.get("isStage"):
                t["layerOrder"] = 0
                t["visible"] = False
            else:
                layer += 1
                t["layerOrder"] = layer
                t["visible"] = True
            # Drop legacy SB2 sound entries copied from old templates.
            sounds = []
            for snd in t.get("sounds") or []:
                if isinstance(snd, dict) and snd.get("md5ext") and snd.get("assetId"):
                    sounds.append(snd)
            t["sounds"] = sounds
        return targets

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        project = {
            "targets": self._finalize_targets(),
            "monitors": self._build_monitors(),
            "extensions": sorted(self.extensions),
            "meta": {"semver": "3.0.0", "vm": "5.0.0", "agent": "leo_learn_course sb3_builder"},
        }
        all_assets: dict[str, bytes | str] = dict(self._template_assets)
        all_assets.update(self.assets)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("project.json", json.dumps(project, ensure_ascii=False))
            for fname, content in all_assets.items():
                data = content.encode("utf-8") if isinstance(content, str) else content
                zf.writestr(fname, data)
