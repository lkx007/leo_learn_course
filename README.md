# Leo's Python Adventure 🚀

欢迎来到 **Leo 的 Python 编程大冒险**！这是一个专门为 7 岁孩子（Leo）设计的 Python 入门课程。通过有趣的案例、生动的语音播报和好玩的打字游戏，开启编程的大门。

## 🌟 项目亮点

- **全线语音播报**：所有课程脚本都集成了 macOS `say` 功能，屏幕显示什么，电脑就读什么，学习更轻松！
- **循序渐进打字特训**：
  - **动态题库**：从课程代码中自动提取练习题。
  - **自适应难度**：从入门短句到挑战级长语段，陪伴孩子手感提升。
  - **语音实时激励**：每一关、每一个评价都有生动的语音反馈。
- **趣味化案例**：包含“魔法门卫”、“烟花秀”、“AI 数学家”等多个贴近孩子生活的编程小练习。

## 📖 一键查看全部课程（推荐）

不想一个个打开 Markdown？有两种方式：

**本地离线**：双击 **`课程合集.html`**（全部课程预渲染，带目录和搜索）

**公网在线**：部署到 GitHub Pages 后访问  
👉 **https://lkx007.github.io/leo_learn_course/**

**Python 实验室**：浏览器里直接写代码、运行、调试（基于 Pyodide）  
👉 **https://lkx007.github.io/leo_learn_course/python.html**

重新生成网页：

```bash
pip install markdown   # 仅首次需要
python3 build_html.py              # 本地 课程合集.html
python3 build_html.py --pages      # 额外生成 docs/（GitHub Pages）
```

### 发布到 GitHub Pages

1. 推送代码到 GitHub（仓库 `lkx007/leo_learn_course`）
2. 打开仓库 **Settings → Pages**
3. **Build and deployment → Source** 选 **GitHub Actions**
4. 推送 `main` 分支后，Actions 会自动构建并发布 `docs/` 站点

首次也可手动构建：`python3 build_html.py --pages`，然后把 `docs/` 推上去，Source 选 **Deploy from a branch → main → /docs**。

## 🧭 三条学习线

本课程现在包含三条互补的学习线，建议交替进行（先玩、再练、后创）：

1. **Scratch 图形化课**（玩）：拖拽积木，零打字建立计算思维。→ `course/Scratch课程大纲.md`
   - 使用 **Scratch 桌面版（Mac 应用）**，新手先看带图的 `course/Scratch桌面版使用指南.md`。
   - 含 **进阶篇**：用 Scratch 解决现实数学问题（蜗牛爬井、找零、分糖、乘法）+ 做游戏（飞机大战、坦克大战）。评审见 `course/Scratch课程评审.md`。
2. **Python 编程课**（练）：真正动手写代码，掌握语法。→ `course/课程大纲.md`
3. **AI 训练师课**（创）：学会跟真 AI 聊天、用提示词/技能/工具/MCP，把点子变成软件。→ `AI训练师课程/AI训练师课程大纲.md`
   - **进阶 4 课**：模型 · Harness · OpenClaw（基础毕业后）
   - **实战项目**：🐟 [大鱼吃小鱼](AI训练师课程/AI训练师项目大纲_大鱼吃小鱼.md) — 语音指挥 AI + Scratch 分步做游戏（G01–G04 参考答案 sb3）
   - **语音指挥台**（Chrome）：[voice-ai.html](https://lkx007.github.io/leo_learn_course/voice-ai.html) — 按住说话，复制粘贴给 Cursor

> 想先了解整体情况？请看 `课程分析报告.md`。
> 想要现成的学习计划？请看 `暑假教学日程表.md`（8 周，三条线交替）。

## 📁 目录结构

- `course/`：核心教学资源
  - `lesson_*.py`：可运行的 Python 代码脚本。
  - `*.md`：对应的课程文档，解释编程概念。
  - `scratch_lesson_*.sb3` / `*_Scratch.md`：Scratch 工程文件与配套课件。
  - `课程大纲.md`：Python 主线大纲。
  - `Scratch课程大纲.md`：Scratch 主线大纲。
  - `typing_game.py`：特制的编程打字训练游戏。
- `AI训练师课程/`：**用 AI** 特训营（提示词、Skills、Tools、MCP、进阶、大鱼吃小鱼项目课）。
- `site/`：GitHub Pages 静态页（`voice-ai.html` 语音指挥台、`python.html`、`typing.html` 等）。
- `implementation_plan/`：需求开发记录与计划归档。
- `课程分析报告.md`：对全部课程的分析与新增内容说明。
- `需求.md`：项目的原始需求文档。

## 🚀 快速开始

### 准备工作
- **操作系统**：推荐在 **macOS** 上运行以获得最佳语音体验。
- **Python 版本**：Python 3.12+

### 运行课程
打开终端，进入项目目录，运行任意一课：
```bash
python3 course/lesson_12.py
```

### 开启打字挑战
运行打字游戏，开始指法特训：
```bash
python3 course/typing_game.py
```

## 🛠️ 技术栈
- **语言**：Python 3
- **图形**：Standard `turtle` library
- **系统交互**：`os`, `sys`, `time`, `random`, `tty`, `termios`
- **语音引擎**：macOS `say` command

---
*祝 Leo 在编程的世界里玩得开心！* 🐍✨
