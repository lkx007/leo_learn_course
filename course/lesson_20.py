import os
import turtle

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = text.replace("🎨 ", "").replace("🔴 ", "").replace("🟢 ", "").replace("🔵 ", "").replace("⚫️ ", "").replace("⚪️ ", "").replace("✨ ", "").replace("✈️ ", "").replace("➖ ", "").replace("➕ ", "")
    os.system(f"say -r 150 '{clean_text}'")

# --- 1. 初始化魔法画板 ---
t = turtle.Turtle()
screen = turtle.Screen()

t.speed(0)     # 最快速度
t.pensize(2)   # 默认粗细
t.shape("circle") # 笔头是个小圆点
t.shapesize(0.5)

speak("🎨 魔法画板启动！")
speak("按 R/G/B/K 换颜色")
speak("按 1-9 换粗细")
speak("按 C 清空")
speak("用鼠标拖动来画画！")

# --- 2. 定义魔法能力 (函数) ---

def set_red():
    t.pencolor("red")
    speak("🔴 笔变成红色了")

def set_green():
    t.pencolor("green")
    speak("🟢 笔变成绿色了")

def set_blue():
    t.pencolor("blue")
    speak("🔵 笔变成蓝色了")

def set_black():
    t.pencolor("black")
    speak("⚫️ 笔变成黑色了")

def set_white():  # 相当于橡皮擦！
    t.pencolor("white")
    t.pensize(20)
    speak("⚪️ 橡皮擦模式")

def clear_screen():
    t.clear()
    speak("✨ 画布清空！")

# 瞬移魔法：点击哪里，笔就飞到哪里（不画线）
def jump_to(x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()
    speak("✈️ 笔飞到了 (" + str(x) + ", " + str(y) + ")")

# 改变粗细的函数
def width_small():
    t.pensize(2)
    speak("➖ 变细")

def width_big():
    t.pensize(10)
    speak("➕ 变粗")

# 让他能听到键盘事件
def exit_app():
    screen.bye()

# --- 3. 绑定魔法按键 (Events) ---

# 颜色控制
screen.onkey(set_red, "r")
screen.onkey(set_green, "g")
screen.onkey(set_blue, "b")
screen.onkey(set_black, "k")
screen.onkey(set_white, "e") # E for Eraser

# 粗细控制
screen.onkey(width_small, "1")
screen.onkey(width_big, "9")

# 功能控制
screen.onkey(clear_screen, "c")
screen.onkey(exit_app, "q") # Quit

# 核心魔法：鼠标拖动 -> 乌龟跟随
t.ondrag(t.goto)

# 瞬移魔法：鼠标点击 -> 笔飞过去
screen.onclick(jump_to)

# --- 4. 开启监听 ---
screen.listen() # 开始听
turtle.done()   # 保持窗口打开
