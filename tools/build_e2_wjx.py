#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从问卷星 HTML + 答案表生成 site/e2-wjx.js"""
import json, re, sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wjx_answers import ANSWERS

HTML_DIR = Path("/tmp/wjx")
OUT = ROOT / "site" / "e2-wjx.js"

META = {
    "mepsL4r": {"ic": "🐱", "name": "图形化函数", "file": "图形化编程.url / 10-函数定义与调用.url"},
    "wFT7CW7": {"ic": "⬇️", "name": "程序顺序", "file": "5-1程序顺序结构.url"},
    "hVttuQl": {"ic": "❓", "name": "条件分支", "file": "5-条件判断与分支结构.url"},
    "Qve0fU5": {"ic": "🪆", "name": "嵌套判断", "file": "7-嵌套循环结构.url"},
    "Q0Wn0tC": {"ic": "📦", "name": "变量赋值", "file": "4-变量与赋值.url"},
    "h03VuQl": {"ic": "🔗", "name": "逻辑运算", "file": "3-逻辑运算符.url"},
    "wf76hCW": {"ic": "➕", "name": "算术运算", "file": "2-基本算数运算符.url"},
    "rXLL5Y5": {"ic": "🪆", "name": "递归函数", "file": "递归函数.url / 11递归函数.url"},
    "rbLCkY5": {"ic": "🍽️", "name": "栈", "file": "12栈数据结构.url"},
    "Ot1W0t4": {"ic": "📓", "name": "字典", "file": "13字典数据结构.url"},
    "t4S0FMh": {"ic": "📋", "name": "列表", "file": "14列表创建与遍历.url"},
    "exvSViR": {"ic": "💧", "name": "广度优先", "file": "广度优先搜索BFS.url / 15广度优先.url"},
    "Q0Rm0lQ": {"ic": "🌲", "name": "深度优先", "file": "深度优先搜索.url / 16深度优先.url"},
    "topN3MT": {"ic": "👀", "name": "侦测感知", "file": "17侦测与感知.url"},
    "m3sZsJo": {"ic": "🔬", "name": "科学常识", "file": "1-基础科学常识.url"},
    "YhVNsvx": {"ic": "🧪", "name": "科学探究", "file": "18科学探究与建模关联知识.url"},
}

LETTERS = "ABCDEFGH"
TF_YES = {"对", "正确", "是", "√", "T", "true", "TRUE"}
TF_NO = {"错", "错误", "否", "×", "F", "false", "FALSE"}


def strip_tags(s):
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    return unescape(re.sub(r"\s+", " ", s)).replace("\xa0", " ").strip()


def clean_opt(s):
    s = strip_tags(s)
    for _ in range(3):
        s = re.sub(r"^[A-Ha-h][\.、．\)]\s*", "", s)
    s = s.strip()
    if not s or s == "#" or s.startswith("参考答案"):
        return None
    return s


def is_skip(prompt, typ):
    if not prompt:
        return True
    if prompt.startswith("您的") or prompt in {"考生基本信息", "基本信息："}:
        return True
    if typ in ("1", "9") and ("班级" in prompt or "姓名" in prompt):
        return True
    if any(k in prompt for k in ("第一部分", "第二部分", "第三部分")) and len(prompt) < 50:
        return True
    if "单项选择" in prompt and len(prompt) < 40:
        return True
    return False


def parse_html(path):
    t = path.read_text(encoding="utf-8", errors="replace")
    title = strip_tags(re.search(r"<title>(.*?)</title>", t).group(1))
    qs = []
    for m in re.finditer(r"id='div(\d+)'([^>]*)>", t):
        n = int(m.group(1))
        attrs = m.group(2)
        typ_m = re.search(r"type='(\d+)'", attrs) or re.search(r"type='(\d+)'", t[m.start():m.start() + 180])
        typ = typ_m.group(1) if typ_m else "?"
        rest = t[m.end():]
        nxt = re.search(r"id='div\d+'", rest)
        body = rest[: nxt.start()] if nxt else rest[:5000]
        pm = re.search(r"<div class='topichtml'>(.*?)</div>", body)
        prompt = strip_tags(pm.group(1)) if pm else ""
        if is_skip(prompt, typ):
            continue
        raw_opts = [strip_tags(x) for x in re.findall(r"<div class='label'[^>]*>(.*?)</div>", body)]
        opts = []
        for o in raw_opts:
            c = clean_opt(o)
            if c:
                opts.append(c)
        if not opts:
            continue
        imgs = []
        search_in = (pm.group(1) if pm else "") + body
        for src in re.findall(r"<img[^>]+src=[\"']([^\"']+)[\"']", search_in):
            if any(x in src.lower() for x in ("background", "logo", "wlogo")):
                continue
            imgs.append(src)
        qs.append({"id": n, "prompt": prompt, "options": opts, "imgs": imgs})
    return title, qs


def js_str(s):
    return json.dumps(s, ensure_ascii=False)


def is_tf(opts):
    if len(opts) != 2:
        return False
    joined = "".join(opts)
    return any(x in joined for x in ("正确", "错误", "对", "错"))


def mark_ok(opts, key):
    key = key.strip()
    ok = [False] * len(opts)
    if key in ("对", "正确"):
        for i, o in enumerate(opts):
            if o in TF_YES or o.startswith("正确") or o == "对":
                ok[i] = True
        if not any(ok):
            ok[0] = True
        return ok
    if key in ("错", "错误"):
        for i, o in enumerate(opts):
            if o in TF_NO or o.startswith("错误") or o == "错":
                ok[i] = True
        if not any(ok):
            ok[1] = True
        return ok
    # letters
    for ch in key:
        if ch in LETTERS:
            i = LETTERS.index(ch)
            if i < len(opts):
                ok[i] = True
    return ok


EM = ["🅰️", "🅱️", "🅲", "🅳", "🅴", "🅵"]


def main():
    packs = []
    missing = []
    total = 0
    for sid, meta in META.items():
        html = HTML_DIR / f"{sid}.html"
        if not html.exists():
            raise SystemExit("missing html " + sid)
        title, qs = parse_html(html)
        ans = ANSWERS.get(sid) or {}
        out_qs = []
        for q in qs:
            total += 1
            if q["id"] not in ans:
                missing.append(f"{sid}:{q['id']} {q['prompt'][:40]}")
                continue
            key, why = ans[q["id"]]
            ok = mark_ok(q["options"], key)
            if not any(ok):
                missing.append(f"{sid}:{q['id']} no-ok {key} {q['options']}")
                continue
            tf = is_tf(q["options"])
            multi = (not tf) and key.isalpha() and len(key) > 1
            img = ""
            if q["imgs"]:
                img = f"e2-img/{sid}_{q['id']}_0.png"
            options = []
            for i, t in enumerate(q["options"]):
                e = "✅" if (tf and t in TF_YES or (tf and i == 0 and t in ("对", "正确"))) else (
                    "❌" if tf else EM[i] if i < len(EM) else str(i + 1)
                )
                if tf:
                    e = "✅" if (t in TF_YES or t in ("对", "正确")) else "❌"
                options.append({"e": e, "t": t, "ok": bool(ok[i])})
            out_qs.append({
                "type": "quiz",
                "src": "wjx",
                "wid": f"{sid}-{q['id']}",
                "prompt": q["prompt"],
                "speak": q["prompt"],
                "why": why,
                "tf": tf,
                "multi": multi,
                "img": img,
                "options": options,
            })
        packs.append({
            "id": sid,
            "ic": meta["ic"],
            "name": meta["name"],
            "title": title,
            "file": meta["file"],
            "qs": out_qs,
        })

    if missing:
        print("MISSING", len(missing))
        for x in missing:
            print(" ", x)
        raise SystemExit("answers incomplete")

    # emit JS
    def emit_q(q):
        opts = ",".join(
            "{e:%s,t:%s,ok:%s}" % (js_str(o["e"]), js_str(o["t"]), "true" if o["ok"] else "false")
            for o in q["options"]
        )
        parts = [
            "type:\"quiz\"",
            "src:\"wjx\"",
            "wid:%s" % js_str(q["wid"]),
            "speak:%s" % js_str(q["speak"]),
            "prompt:%s" % js_str(q["prompt"]),
            "why:%s" % js_str(q["why"]),
            "options:[%s]" % opts,
        ]
        if q["tf"]:
            parts.append("tf:true")
        if q["multi"]:
            parts.append("multi:true")
        if q["img"]:
            parts.append("img:%s" % js_str(q["img"]))
        return "{" + ",".join(parts) + "}"

    chunks = ["window.E2_WJX = {"]
    for i, p in enumerate(packs):
        qs = ",".join(emit_q(q) for q in p["qs"])
        line = "%s:{id:%s,ic:%s,name:%s,title:%s,file:%s,qs:[%s]}" % (
            js_str(p["id"]), js_str(p["id"]), js_str(p["ic"]), js_str(p["name"]),
            js_str(p["title"]), js_str(p["file"]), qs
        )
        chunks.append(line + ("," if i < len(packs) - 1 else ""))
    chunks.append("};")
    # papers
    chunks.append("window.E2_WJX_PAPERS = [")
    for i, p in enumerate(packs):
        qs = ",".join(emit_q(q) for q in p["qs"])
        chunks.append("{id:%s,ic:%s,name:%s,file:%s,qs:[%s]}%s" % (
            js_str("w-"+p["id"]), js_str(p["ic"]), js_str(p["name"]), js_str(p["file"]),
            qs, "," if i < len(packs) - 1 else ""
        ))
    chunks.append("];")
    OUT.write_text("\n".join(chunks) + "\n", encoding="utf-8")
    nq = sum(len(p["qs"]) for p in packs)
    print("wrote", OUT, "packs", len(packs), "questions", nq)
    assert nq == 320, nq


if __name__ == "__main__":
    main()
