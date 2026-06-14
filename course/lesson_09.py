# 第09课 - 遇见小海龟 (Turtle Intro)
# 目标：学会引入 turtle 库，并控制海龟移动

import os
import turtle
import time

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = text.replace("🐢 ", "").replace("⤴️  ", "").replace("⤵️  ", "").replace("🔙 ", "").replace("🎨 ", "")
    os.system(f"say -r 150 '{clean_text}'")

speak("🐢 正在召唤小海龟...")

# 1. 召唤海龟
t = turtle.Turtle()

# 2. 设置海龟的样子
t.shape("turtle")  # 变成海龟形状
t.color("green")   # 变成绿色
t.pensize(5)       # 笔变粗一点

# 3. 开始画画
speak("🐢 海龟开始移动！")

t.forward(100)  # 向前走 100 步
time.sleep(1)

t.left(90)      # 向左转 90 度
speak("⤴️  左转！")

t.forward(100)  # 再向前走 100 步
time.sleep(1)

t.right(90)     # 向右转 90 度
speak("⤵️  右转！")

t.backward(50)  # 倒退 50 步
speak("🔙 倒车请注意！")

# 4. 结束
speak("🎨 作画完成！")
speak("请手动关闭海龟窗口哦。")

# 这一行很重要，能让窗口一直停在屏幕上，不会闪一下就消失
turtle.done()
