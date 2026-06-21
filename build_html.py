#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把全部课程（Markdown + Python 源码）打包成一个自包含的 HTML 文件。

用法：
    python3 build_html.py

输出：
    课程合集.html   —— 双击用浏览器打开即可，离线可用，内容已全部预渲染。

依赖：
    pip install markdown
"""

import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(ROOT, "课程合集.html")

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
    """提取文件名里第一个数字，用于自然排序；没有则返回大数。"""
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
    """把文档里的相对 img/href 路径，改成相对仓库根目录，
    这样把多个目录下的文档内联进根目录 HTML 时，图片仍能正确显示。"""
    if not base_rel_dir:
        return html_body

    def repl(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r"^(https?:|data:|mailto:|#|/)", url):
            return m.group(0)
        return '%s="%s/%s"' % (attr, base_rel_dir.rstrip("/"), url)

    return re.sub(r'(src|href)="([^"]+)"', repl, html_body)


# ---------------------------------------------------------------------------
# 收集文件
# ---------------------------------------------------------------------------

def list_md(folder: str):
    if not os.path.isdir(folder):
        return []
    return [f for f in os.listdir(folder) if f.endswith(".md")]


def list_py(folder: str):
    if not os.path.isdir(folder):
        return []
    return [f for f in os.listdir(folder) if f.endswith(".py")]


course_dir = os.path.join(ROOT, "course")
ai_dir = os.path.join(ROOT, "AI训练师课程")

# --- 总览（根目录） ---
overview_order = ["README.md", "课程分析报告.md", "暑假教学日程表.md", "需求.md"]
overview_files = [
    os.path.join(ROOT, f) for f in overview_order if os.path.exists(os.path.join(ROOT, f))
]

# --- Python / Scratch 课程（course/） ---
py_course_files = []
scratch_files = []
for f in list_md(course_dir):
    full = os.path.join(course_dir, f)
    if f.endswith("_Scratch.md") or f.startswith("Scratch"):
        scratch_files.append(full)
    else:
        py_course_files.append(full)


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
    if name.startswith("Scratch进阶"):
        return (3, first_number(name), name)
    return (2, first_number(name), name)  # 第NN课_..._Scratch.md


py_course_files.sort(key=py_course_key)
scratch_files.sort(key=scratch_key)

# --- AI 训练师课程 ---
ai_files = []
for f in list_md(ai_dir):
    ai_files.append(os.path.join(ai_dir, f))


def ai_key(path):
    name = os.path.basename(path)
    if name.startswith("AI训练师课程大纲"):
        return (0, 0, name)
    return (1, first_number(name), name)


ai_files.sort(key=ai_key)

# --- Python 源码 ---
py_src = [
    os.path.join(course_dir, f)
    for f in list_py(course_dir)
    if f not in ("a.py",)
]
py_src.sort(key=lambda p: (first_number(os.path.basename(p)), os.path.basename(p)))

GROUPS = [
    ("📚 开始这里", "总览、分析与学习计划", overview_files, "md"),
    ("🐍 Python 课程", "课程大纲与每课讲解", py_course_files, "md"),
    ("🐱 Scratch 课程", "图形化课程 · 基础 + 进阶（数学/游戏）", scratch_files, "md"),
    ("🧑‍🚀 AI 训练师课程", "提示词 · Skills · Tools · MCP · 把点子变软件", ai_files, "md"),
    ("💻 Python 源码", "可运行的课程代码", py_src, "py"),
]

# ---------------------------------------------------------------------------
# 生成 HTML
# ---------------------------------------------------------------------------

nav_parts = []
article_parts = []
total_docs = 0

for group_title, group_desc, files, kind in GROUPS:
    if not files:
        continue
    nav_items = []
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
        else:
            title = name
            body = "<pre><code class=\"language-python\">%s</code></pre>" % html.escape(raw)
        anchor = slugify(name)
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

nav_html = "\n".join(nav_parts)
articles_html = "\n".join(article_parts)

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

/* layout */
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

/* content */
.content{flex:1;min-width:0;padding:34px clamp(18px,5vw,64px) 80px;max-width:980px;margin:0 auto}
#top{height:1px}
.intro{background:linear-gradient(135deg,#eef2ff,#f7f0ff);border:1px solid var(--line);border-radius:16px;padding:22px 24px;margin-bottom:26px}
.intro h2{margin:.1em 0 .3em}
.intro .stats{color:var(--muted);font-size:14px}
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

JS = """
const links=[...document.querySelectorAll('.nav-group li a')];
const arts=[...document.querySelectorAll('article.doc')];
// scroll spy
const obs=new IntersectionObserver((es)=>{
  es.forEach(e=>{ if(e.isIntersecting){
    const id=e.target.id;
    links.forEach(a=>a.classList.toggle('active',a.dataset.target===id));
  }});
},{rootMargin:'-10% 0px -80% 0px',threshold:0});
arts.forEach(a=>obs.observe(a));
// search filter
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
// mobile menu
const sb=document.querySelector('.sidebar');
document.getElementById('menu').addEventListener('click',()=>sb.classList.toggle('open'));
links.forEach(a=>a.addEventListener('click',()=>{ if(window.innerWidth<=880) sb.classList.remove('open'); }));
"""

PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>小鱼编程课程合集 · Leo's Coding Courses</title>
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
      <div class="stats">📦 全部内容已离线打包，双击本文件即可阅读，无需联网。</div>
    </div>
    {articles}
  </main>
</div>
<button class="menu-btn" id="menu" aria-label="目录">☰</button>
<script>{js}</script>
</body>
</html>
"""

out = PAGE.format(css=CSS, js=JS, nav=nav_html, articles=articles_html, count=total_docs)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(out)

print("✅ 已生成：%s（共 %d 篇课程）" % (OUTPUT, total_docs))
