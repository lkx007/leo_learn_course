#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把全部课程（Markdown + Python 源码）打包成 HTML。

用法：
    python3 build_html.py              # 生成本地 课程合集.html
    python3 build_html.py --pages      # 额外生成 docs/（GitHub Pages）

依赖：
    pip install markdown
"""

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
LOCAL_OUTPUT = os.path.join(ROOT, "课程合集.html")
DOCS_DIR = os.path.join(ROOT, "docs")
SCRATCH_ANSWERS = os.path.join(ROOT, "course", "scratch_answers")

try:
    import markdown
except ImportError:
    sys.exit("缺少依赖，请先运行： pip install markdown")


def md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["fenced_code", "tables", "sane_lists", "nl2br"],
        output_format="html5",
    )


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def first_number(name: str) -> int:
    m = re.search(r"(\d+)", name)
    return int(m.group(1)) if m else 10**6


def title_from_md(text: str, fallback: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def slugify(name: str) -> str:
    base = re.sub(r"[^\w\u4e00-\u9fff]+", "-", name).strip("-")
    return "doc-" + base


def fix_relative_links(html_body: str, base_rel_dir: str) -> str:
    if not base_rel_dir:
        return html_body

    def repl(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r"^(https?:|data:|mailto:|#|/)", url):
            return m.group(0)
        return '%s="%s/%s"' % (attr, base_rel_dir.rstrip("/"), url)

    return re.sub(r'(src|href)="([^"]+)"', repl, html_body)


def list_md(folder: str):
    if not os.path.isdir(folder):
        return []
    return [f for f in os.listdir(folder) if f.endswith(".md")]


def list_py(folder: str):
    if not os.path.isdir(folder):
        return []
    return [f for f in os.listdir(folder) if f.endswith(".py")]


def collect_groups():
    course_dir = os.path.join(ROOT, "course")
    ai_dir = os.path.join(ROOT, "AI训练师课程")

    overview_order = ["README.md", "课程分析报告.md", "暑假教学日程表.md", "秋季进阶日程表.md", "需求.md"]
    overview_files = [
        os.path.join(ROOT, f) for f in overview_order if os.path.exists(os.path.join(ROOT, f))
    ]

    py_course_files = []
    scratch_files = []
    for f in list_md(course_dir):
        full = os.path.join(course_dir, f)
        if f.endswith("_Scratch.md") or f.startswith("Scratch"):
            scratch_files.append(full)
        else:
            py_course_files.append(full)
    sx_dir = os.path.join(course_dir, "scratch_exercises")
    if os.path.isdir(sx_dir):
        scratch_files.extend(os.path.join(sx_dir, f) for f in list_md(sx_dir))

    def py_course_key(path):
        name = os.path.basename(path)
        if name == "课程大纲.md":
            return (0, 0, name)
        if name.startswith("第"):
            return (1, first_number(name), name)
        if name.startswith("L"):
            return (2, first_number(name), name)
        if name.startswith("番外"):
            return (3, 0, name)
        return (4, first_number(name), name)

    def scratch_key(path):
        name = os.path.basename(path)
        if name == "Scratch课程大纲.md":
            return (0, 0, name)
        if name == "Scratch课程评审.md":
            return (1, 0, name)
        if "家长指南" in name:
            return (1, 1, name)
        if "课后练习索引" in name:
            return (1, 2, name)
        if "毕业测验" in name:
            return (1, 3, name)
        if name.startswith("O") and name[1:3].isdigit():
            return (4, first_number(name), name)
        if name.startswith("Scratch奥数"):
            return (2, 50 + first_number(name), name)
        if name.startswith("Scratch乘法"):
            return (2, 100 + first_number(name), name)
        if name.startswith("Scratch进阶"):
            return (3, first_number(name), name)
        return (2, first_number(name), name)

    py_course_files.sort(key=py_course_key)
    scratch_files.sort(key=scratch_key)

    ai_files = [os.path.join(ai_dir, f) for f in list_md(ai_dir)]
    ex_dir = os.path.join(ai_dir, "exercises")
    if os.path.isdir(ex_dir):
        ai_files.extend(os.path.join(ex_dir, f) for f in list_md(ex_dir))

    def ai_key(path):
        name = os.path.basename(path)
        if name.startswith("AI训练师课程大纲"):
            return (0, 0, name)
        if name.startswith("课后练习"):
            return (0, 1, name)
        if name.startswith("AI训练师项目大纲"):
            return (3, 0, name)
        if name.startswith("项目练习"):
            return (3, 1, name)
        if name.startswith("G") and name[1:3].isdigit():
            return (4, 50 + first_number(name), name)
        if name.startswith("AI训练师项目"):
            return (4, first_number(name), name)
        if name.startswith("AI训练师进阶"):
            return (2, first_number(name), name)
        if name.startswith("T") and name[1:3].isdigit():
            return (1, 500 + first_number(name), name)
        return (1, first_number(name), name)

    ai_files.sort(key=ai_key)

    py_src = [
        os.path.join(course_dir, f)
        for f in list_py(course_dir)
        if f not in ("a.py",)
    ]
    py_src.sort(key=lambda p: (first_number(os.path.basename(p)), os.path.basename(p)))

    return [
        ("📚 开始这里", "总览、分析与学习计划", overview_files, "md", "guide"),
        ("🐍 Python 课程", "课程大纲与每课讲解", py_course_files, "md", "python"),
        ("🐱 Scratch 课程", "图形化课程 · 基础 + 进阶（数学/游戏）", scratch_files, "md", "scratch"),
        ("🧑‍🚀 AI 训练师课程", "基础 + 进阶 + 🐟大鱼吃小鱼项目 · 语音指挥", ai_files, "md", "ai"),
        ("💻 Python 源码", "可运行的课程代码", py_src, "py", "code"),
    ]


def webify_python(source: str) -> tuple[str, bool]:
    """Prepare lesson code for browser (Pyodide). Returns (code, web_ready)."""
    web_ready = "turtle" not in source.lower() and "pygame" not in source.lower()

    # Drop speak() definition — runtime shim provides speak()
    source = re.sub(
        r"def speak\([^)]*\):.*?(?=\n(?:def |class |# -|\w|\Z))",
        "",
        source,
        flags=re.DOTALL,
    )
    # Drop standalone os.system say calls
    source = re.sub(r"^\s*os\.system\(.*?\)\s*$", "", source, flags=re.MULTILINE)

    preamble = "# 网页实验室 · speak() 会打印文字（无语音）\n"
    return preamble + source.strip() + "\n", web_ready


def lesson_title_from_source(source: str, filename: str) -> tuple[int, str]:
    m = re.search(r"#\s*第(\d+)课\s*[-–—]?\s*(.*)", source)
    if m:
        return int(m.group(1)), m.group(2).strip() or filename
    return first_number(filename), re.sub(r"^lesson_|\.py$", "", filename)


def build_python_lessons_json():
    course_dir = os.path.join(ROOT, "course")
    items = []
    for name in sorted(os.listdir(course_dir)):
        if not re.match(r"lesson_\d+\.py$", name):
            continue
        path = os.path.join(course_dir, name)
        raw = read(path)
        num, title = lesson_title_from_source(raw, name)
        web_code, web_ready = webify_python(raw)
        items.append({
            "id": num,
            "file": name,
            "title": title,
            "webReady": web_ready,
            "code": raw,
            "webCode": web_code,
        })
    items.sort(key=lambda x: x["id"])
    data = {"defaultId": items[0]["id"] if items else 2, "lessons": items}
    out = os.path.join(DOCS_DIR, "python-lessons.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return len(items)


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
        gmap = {2: "G01_大鱼吃小鱼①游起来", 3: "G02_大鱼吃小鱼②小鱼群", 4: "G03_大鱼吃小鱼③吃掉变大", 5: "G04_大鱼吃小鱼④完整版"}
        n = int(m.group(1))
        if n in gmap:
            return f"{gmap[n]}_参考答案.sb3"
    return None


def sb3_download_link(md_filename: str) -> str:
    sb3 = sb3_name_for_md(md_filename)
    if not sb3:
        return ""
    path = os.path.join(SCRATCH_ANSWERS, sb3)
    if not os.path.isfile(path):
        return ""
    return (
        '<p class="sb3-dl"><a class="run-web" href="scratch_answers/%s" download>'
        "📥 下载参考答案 .sb3</a>"
        '<span class="sb3-hint"> · Scratch 桌面版 → 文件 → 从电脑中上传</span></p>'
    ) % html.escape(sb3)


def build_course_html(*, online: bool = False):
    groups = collect_groups()
    nav_parts = []
    article_parts = []
    total_docs = 0
    group_meta = []

    for group_title, group_desc, files, kind, key in groups:
        if not files:
            continue
        nav_items = []
        first_anchor = ""
        for path in files:
            name = os.path.basename(path)
            raw = read(path)
            if kind == "md":
                title = title_from_md(raw, name)
                body = md_to_html(raw)
                rel_dir = os.path.relpath(os.path.dirname(path), ROOT)
                if rel_dir == ".":
                    rel_dir = ""
                body = fix_relative_links(body, rel_dir)
                if online:
                    body += sb3_download_link(name)
            else:
                title = name
                body = "<pre><code class=\"language-python\">%s</code></pre>" % html.escape(raw)
                if online and name.startswith("lesson_") and re.match(r"lesson_(\d+)\.py", name):
                    num = int(re.search(r"(\d+)", name).group(1))
                    body += (
                        '<p class="run-web-wrap"><a class="run-web" href="python.html?lesson=%d">'
                        "▶ 在浏览器里运行这节课</a></p>" % num
                    )
            anchor = slugify(name)
            if not first_anchor:
                first_anchor = anchor
            total_docs += 1
            nav_items.append(
                '<li><a href="#%s" data-target="%s">%s</a></li>'
                % (anchor, anchor, html.escape(title))
            )
            article_parts.append(
                '<article id="%s" class="doc">\n'
                '<div class="doc-file">%s</div>\n'
                '%s\n'
                '<a class="back-top" href="#top">↑ 回到顶部</a>\n'
                "</article>" % (anchor, html.escape(name), body)
            )
        nav_parts.append(
            '<details open class="nav-group">\n'
            "<summary>%s <span class=\"count\">%d</span></summary>\n"
            '<div class="nav-desc">%s</div>\n'
            "<ul>%s</ul>\n"
            "</details>" % (html.escape(group_title), len(files), html.escape(group_desc), "".join(nav_items))
        )
        group_meta.append({
            "key": key,
            "title": group_title,
            "desc": group_desc,
            "count": len(files),
            "anchor": first_anchor,
        })

    intro_stats = (
        "🌐 在线课程页 · 左侧目录可跳转 · 顶部搜索框可快速查找"
        if online
        else "📦 全部内容已离线打包，双击本文件即可阅读，无需联网。"
    )
    home_link = ""
    if online:
        home_link = '<p class="stats"><a href="index.html">← 返回课程首页</a></p>'

    page = COURSE_PAGE.format(
        css=CSS,
        js=JS,
        nav="\n".join(nav_parts),
        articles="\n".join(article_parts),
        count=total_docs,
        intro_stats=intro_stats,
        home_link=home_link,
    )
    return page, total_docs, group_meta


def build_landing_html(group_meta, total_docs):
    cards = []
    card_styles = {
        "guide": ("#0284c7", "📚"),
        "python": ("#2563eb", "🐍"),
        "scratch": ("#ea580c", "🐱"),
        "ai": ("#7c3aed", "🤖"),
        "code": ("#059669", "💻"),
    }
    for g in group_meta:
        if g["key"] == "guide":
            continue
        color, icon = card_styles.get(g["key"], ("#64748b", "📖"))
        cards.append(
            '<a class="card" href="course.html#%s" style="--accent:%s">'
            '<div class="card-icon">%s</div>'
            "<h3>%s</h3>"
            '<p>%s</p>'
            '<span class="card-meta">%d 篇 · 点击进入</span>'
            "</a>" % (g["anchor"], color, icon, html.escape(g["title"]),
                      html.escape(g["desc"]), g["count"])
        )

    return LANDING_PAGE.format(
        css=LANDING_CSS,
        total=total_docs,
        cards="\n".join(cards),
        python_count=next((g["count"] for g in group_meta if g["key"] == "python"), 0),
        scratch_count=next((g["count"] for g in group_meta if g["key"] == "scratch"), 0),
        ai_count=next((g["count"] for g in group_meta if g["key"] == "ai"), 0),
    )


def copy_assets():
    src = os.path.join(ROOT, "course", "images")
    dst = os.path.join(DOCS_DIR, "course", "images")
    if os.path.isdir(src):
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copytree(src, dst)

    site_dir = os.path.join(ROOT, "site")
    if os.path.isdir(site_dir):
        for name in os.listdir(site_dir):
            if name.endswith(".html"):
                shutil.copy2(os.path.join(site_dir, name), os.path.join(DOCS_DIR, name))


def build_pages():
    os.makedirs(DOCS_DIR, exist_ok=True)
    subprocess.run(
        [sys.executable, os.path.join(ROOT, "build_scratch_sb3.py"), "--copy-docs"],
        cwd=ROOT,
        check=True,
    )
    course_html, total, group_meta = build_course_html(online=True)
    landing_html = build_landing_html(group_meta, total)
    n_py = build_python_lessons_json()

    with open(os.path.join(DOCS_DIR, "course.html"), "w", encoding="utf-8") as f:
        f.write(course_html)
    with open(os.path.join(DOCS_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(landing_html)
    with open(os.path.join(DOCS_DIR, ".nojekyll"), "w", encoding="utf-8") as f:
        f.write("")
    copy_assets()
    return total, n_py


CSS = """
:root{
  --bg:#f6f7fb; --panel:#ffffff; --ink:#22262e; --muted:#6b7280;
  --brand:#5b8def; --brand2:#7c5cff; --line:#e7e9f0; --code-bg:#0f172a; --code-ink:#e2e8f0;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  line-height:1.75;font-size:16px;}
a{color:var(--brand);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{display:flex;min-height:100vh}
.sidebar{width:320px;flex:0 0 320px;background:var(--panel);border-right:1px solid var(--line);
  height:100vh;position:sticky;top:0;overflow-y:auto;padding:0 0 40px}
.brand{padding:20px 20px 14px;background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;position:sticky;top:0;z-index:2}
.brand h1{margin:0;font-size:19px}
.brand p{margin:6px 0 0;font-size:12.5px;opacity:.92}
.search{padding:12px 16px;position:sticky;top:78px;background:var(--panel);z-index:1;border-bottom:1px solid var(--line)}
.search input{width:100%;padding:9px 12px;border:1px solid var(--line);border-radius:10px;font-size:14px;outline:none}
.search input:focus{border-color:var(--brand)}
.nav-group{margin:8px 10px;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff}
.nav-group>summary{cursor:pointer;padding:11px 14px;font-weight:700;font-size:14.5px;list-style:none;display:flex;align-items:center;gap:8px}
.nav-group>summary::-webkit-details-marker{display:none}
.count{margin-left:auto;background:#eef1fb;color:var(--brand);font-size:12px;border-radius:999px;padding:1px 9px;font-weight:700}
.nav-desc{padding:0 14px 6px;color:var(--muted);font-size:12px}
.nav-group ul{list-style:none;margin:0;padding:0 8px 10px}
.nav-group li a{display:block;padding:6px 10px;border-radius:8px;color:var(--ink);font-size:13.5px}
.nav-group li a:hover{background:#f1f4ff;text-decoration:none}
.nav-group li a.active{background:var(--brand);color:#fff}
.content{flex:1;min-width:0;padding:34px clamp(18px,5vw,64px) 80px;max-width:980px;margin:0 auto}
#top{height:1px}
.intro{background:linear-gradient(135deg,#eef2ff,#f7f0ff);border:1px solid var(--line);border-radius:16px;padding:22px 24px;margin-bottom:26px}
.intro h2{margin:.1em 0 .3em}
.intro .stats{color:var(--muted);font-size:14px;margin:.5em 0 0}
.doc{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:26px clamp(16px,3vw,40px);margin:0 0 26px;box-shadow:0 1px 2px rgba(16,24,40,.04)}
.doc-file{font-size:12px;color:var(--muted);margin-bottom:6px;font-family:ui-monospace,Menlo,Consolas,monospace}
.doc h1{margin-top:.1em;font-size:26px;border-bottom:2px solid var(--line);padding-bottom:.3em}
.doc h2{margin-top:1.4em;font-size:21px}
.doc h3{margin-top:1.2em;font-size:17px}
.doc p{margin:.7em 0}
.doc ul,.doc ol{padding-left:1.4em}
.doc li{margin:.25em 0}
.doc blockquote{margin:1em 0;padding:.5em 1em;border-left:4px solid var(--brand);background:#f3f6ff;border-radius:0 10px 10px 0;color:#374151}
.doc code{background:#eef1f6;padding:.12em .4em;border-radius:5px;font-size:.92em;
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Courier New",monospace}
.doc pre{background:var(--code-bg);color:var(--code-ink);padding:16px 18px;border-radius:12px;overflow:auto;line-height:1.55}
.doc pre code{background:transparent;color:inherit;padding:0;font-size:13.5px}
.doc table{border-collapse:collapse;width:100%;margin:1em 0;font-size:14.5px;display:block;overflow:auto}
.doc th,.doc td{border:1px solid var(--line);padding:8px 11px;text-align:left}
.doc th{background:#f1f4ff}
.doc tr:nth-child(even) td{background:#fafbff}
.doc hr{border:none;border-top:1px dashed var(--line);margin:1.6em 0}
.doc img{max-width:100%;border:1px solid var(--line);border-radius:12px;box-shadow:0 2px 10px rgba(16,24,40,.08);margin:.6em 0;background:#fff}
.back-top{display:inline-block;margin-top:14px;font-size:12.5px;color:var(--muted)}
.run-web-wrap{margin:12px 0 0}
.run-web{display:inline-block;background:linear-gradient(135deg,#059669,#10b981);color:#fff !important;
  padding:10px 18px;border-radius:10px;font-weight:700;text-decoration:none;font-size:14px}
.run-web:hover{opacity:.92;text-decoration:none}
.sb3-dl{margin:14px 0 0}
.sb3-hint{font-size:12px;color:var(--muted);margin-left:6px}
.menu-btn{display:none}
@media (max-width:880px){
  .wrap{display:block}
  .sidebar{position:fixed;left:0;top:0;z-index:30;transform:translateX(-100%);transition:.25s;box-shadow:0 0 40px rgba(0,0,0,.2)}
  .sidebar.open{transform:none}
  .menu-btn{display:flex;position:fixed;right:16px;bottom:16px;z-index:40;width:54px;height:54px;border-radius:50%;
    background:var(--brand);color:#fff;border:none;font-size:22px;align-items:center;justify-content:center;box-shadow:0 6px 18px rgba(91,141,239,.5)}
  .content{padding-top:20px}
}
"""

LANDING_CSS = """
:root{--bg:#0f172a;--panel:#1e293b;--ink:#f8fafc;--muted:#94a3b8;--brand:#5b8def;--brand2:#7c5cff;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
  background:radial-gradient(ellipse at top,#1e3a5f 0%,var(--bg) 55%);color:var(--ink);min-height:100vh;line-height:1.6;}
a{color:#93c5fd;text-decoration:none}
a:hover{text-decoration:underline}
.hero{text-align:center;padding:56px 20px 32px;max-width:820px;margin:0 auto}
.hero h1{font-size:clamp(1.8rem,5vw,2.6rem);margin:0 0 12px;background:linear-gradient(90deg,#fff,#93c5fd);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero p{color:var(--muted);font-size:1.05rem;margin:0 0 28px}
.hero-btns{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}
.btn{display:inline-block;padding:14px 28px;border-radius:12px;font-weight:700;font-size:1rem}
.btn-primary{background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;box-shadow:0 8px 24px rgba(91,141,239,.4)}
.btn-secondary{background:var(--panel);color:var(--ink);border:1px solid #334155}
.stats-row{display:flex;flex-wrap:wrap;gap:16px;justify-content:center;margin:36px auto 12px;max-width:720px;padding:0 16px}
.stat{background:var(--panel);border:1px solid #334155;border-radius:14px;padding:16px 24px;text-align:center;min-width:120px}
.stat strong{display:block;font-size:1.8rem;color:#fff}
.stat span{font-size:.85rem;color:var(--muted)}
.section{max-width:960px;margin:0 auto;padding:24px 16px 48px}
.section h2{text-align:center;font-size:1.2rem;color:var(--muted);margin-bottom:20px;font-weight:600}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.card{background:var(--panel);border:1px solid #334155;border-radius:16px;padding:22px;color:inherit;display:block;transition:transform .15s,box-shadow .15s;border-top:4px solid var(--accent,#64748b)}
.card:hover{transform:translateY(-3px);box-shadow:0 12px 32px rgba(0,0,0,.35);text-decoration:none}
.card-icon{font-size:2rem;margin-bottom:8px}
.card h3{margin:0 0 8px;font-size:1.1rem;color:#fff}
.card p{margin:0 0 12px;font-size:.9rem;color:var(--muted);min-height:2.8em}
.card-meta{font-size:.8rem;color:var(--accent);font-weight:600}
.path{background:rgba(30,41,59,.8);border:1px solid #334155;border-radius:16px;padding:24px;max-width:640px;margin:0 auto 40px;text-align:center}
.path p{margin:0;color:var(--muted)}
.path strong{color:#fde68a}
.tools-section .hero-btns{margin-top:0}
footer{text-align:center;padding:32px 16px;color:#64748b;font-size:.85rem;border-top:1px solid #1e293b}
footer a{color:#64748b}
"""

JS = """
const links=[...document.querySelectorAll('.nav-group li a')];
const arts=[...document.querySelectorAll('article.doc')];
const obs=new IntersectionObserver((es)=>{
  es.forEach(e=>{ if(e.isIntersecting){
    const id=e.target.id;
    links.forEach(a=>a.classList.toggle('active',a.dataset.target===id));
  }});
},{rootMargin:'-10% 0px -80% 0px',threshold:0});
arts.forEach(a=>obs.observe(a));
const box=document.getElementById('q');
box.addEventListener('input',()=>{
  const q=box.value.trim().toLowerCase();
  links.forEach(a=>{
    const hit=a.textContent.toLowerCase().includes(q);
    a.parentElement.style.display=hit||!q?'':'none';
  });
  if(q){
    arts.forEach(a=>{
      const t=a.querySelector('h1');
      const hit=(t?t.textContent:'').toLowerCase().includes(q)||a.textContent.toLowerCase().includes(q);
      a.style.display=hit?'':'none';
    });
  }else{ arts.forEach(a=>a.style.display=''); }
});
const sb=document.querySelector('.sidebar');
document.getElementById('menu').addEventListener('click',()=>sb.classList.toggle('open'));
links.forEach(a=>a.addEventListener('click',()=>{ if(window.innerWidth<=880) sb.classList.remove('open'); }));
"""

COURSE_PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="小鱼编程课程合集：Scratch、Python、AI 训练师">
<title>课程合集 · 小鱼编程</title>
<style>{css}</style>
</head>
<body>
<span id="top"></span>
<div class="wrap">
  <aside class="sidebar">
    <div class="brand">
      <h1>🐟 小鱼编程课程合集</h1>
      <p>Scratch · Python · AI 训练师 — 共 {count} 篇</p>
    </div>
    <div class="search"><input id="q" type="search" placeholder="🔍 搜索课程标题…"></div>
    {nav}
  </aside>
  <main class="content">
    <div class="intro">
      <h2>👋 欢迎来到小鱼的编程世界</h2>
      <p>这里汇总了三条学习线的全部课程：<b>Scratch（玩）→ Python（练）→ AI 训练师（创）</b>。左侧目录可点击跳转，顶部搜索框可快速查找。</p>
      <div class="stats">{intro_stats}</div>
      {home_link}
    </div>
    {articles}
  </main>
</div>
<button class="menu-btn" id="menu" aria-label="目录">☰</button>
<script>{js}</script>
</body>
</html>
"""

LANDING_PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="小鱼（Leo）的编程课程：Scratch 图形化、Python 编程、AI 训练师">
<title>小鱼编程 · Leo's Coding Courses</title>
<style>{css}</style>
</head>
<body>
  <header class="hero">
    <h1>🐟 小鱼编程课程</h1>
    <p>为 7 岁孩子设计的编程学习站 · Scratch 玩 · Python 练 · AI 创</p>
    <div class="hero-btns">
      <a class="btn btn-primary" href="course.html">📖 打开全部课程（{total} 篇）</a>
      <a class="btn btn-secondary" href="course.html#doc-Scratch桌面版使用指南-md">🐱 Scratch 新手指南</a>
    </div>
  </header>

  <div class="stats-row">
    <div class="stat"><strong>{scratch_count}</strong><span>Scratch 课时</span></div>
    <div class="stat"><strong>{python_count}</strong><span>Python 课时</span></div>
    <div class="stat"><strong>{ai_count}</strong><span>AI 训练师课</span></div>
    <div class="stat"><strong>{total}</strong><span>总计文档</span></div>
  </div>

  <div class="path">
    <p>推荐学习路径：<strong>Scratch（玩）</strong> → <strong>Python（练）</strong> → <strong>AI 训练师（创）</strong></p>
  </div>

  <section class="section tools-section">
    <h2>快捷入口</h2>
    <div class="hero-btns">
      <a class="btn btn-primary" href="day1.html">⭐ 第一课流程</a>
      <a class="btn btn-primary" href="python.html">🐍 Python 实验室</a>
      <a class="btn btn-primary" href="voice-ai.html">🎤 语音指挥 AI</a>
      <a class="btn btn-primary" href="course.html#doc-AI训练师项目大纲_大鱼吃小鱼-md">🐟 大鱼吃小鱼项目</a>
      <a class="btn btn-secondary" href="typing.html">🖐️ 指法特训</a>
      <a class="btn btn-secondary" href="course.html#doc-Scratch桌面版使用指南-md">🐱 Scratch 指南</a>
    </div>
  </section>

  <section class="section">
    <h2>选择一条学习线</h2>
    <div class="grid">{cards}</div>
  </section>

  <footer>
    <p>Leo's Python Adventure · 课程内容由 Markdown 自动生成</p>
    <p><a href="https://github.com/lkx007/leo_learn_course">GitHub 仓库</a></p>
  </footer>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Build course HTML")
    parser.add_argument("--pages", action="store_true", help="Generate docs/ for GitHub Pages")
    args = parser.parse_args()

    course_html, total, _ = build_course_html(online=False)
    with open(LOCAL_OUTPUT, "w", encoding="utf-8") as f:
        f.write(course_html)
    print("✅ 已生成：%s（共 %d 篇课程）" % (LOCAL_OUTPUT, total))

    if args.pages:
        total, n_py = build_pages()
        print("✅ 已生成 GitHub Pages 站点：%s/" % DOCS_DIR)
        print("   首页：docs/index.html")
        print("   课程：docs/course.html")
        print("   第一课：docs/day1.html")
        print("   指法：docs/typing.html")
        print("   Python 实验室：docs/python.html（%d 课）" % n_py)


if __name__ == "__main__":
    main()
