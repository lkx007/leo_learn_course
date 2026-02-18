# 第10课 - 画个房子
# 目标：顺序执行，组合图形

import os
import turtle
import time

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = text.replace("🏗️  ", "").replace("🧱 ", "").replace("🏠 ", "").replace("✨ ", "")
    os.system(f"say -r 150 '{clean_text}'")

speak("🏗️  开始施工！")

t = turtle.Turtle()
t.shape("turtle")
t.speed(1) # 速度慢一点，看清楚

# --- 第一步：画墙体 (蓝色正方形) ---
t.color("blue")
t.pensize(5)

speak("🧱 正在砌墙...")
# 1
t.forward(100)
t.left(90)
# 2
t.forward(100)
t.left(90)
# 3
t.forward(100)
t.left(90)
# 4
t.forward(100)
t.left(90)

# --- 第二步：移动到屋顶位置 ---
# 此时海龟回到了原点，头朝右
t.left(90)      # 头朝上
t.forward(100)  # 爬上去
t.right(90)     # 头朝右，准备画屋顶

# --- 第三步：画屋顶 (红色三角形) ---
t.color("red")
speak("🏠 正在盖屋顶...")

# 三角形三条边
t.forward(100)  # 底边
t.left(120)     # 转120度
t.forward(100)  # 斜边
t.left(120)     # 转120度
t.forward(100)  # 斜边

speak("✨ 房子盖好啦！")
turtle.done()
