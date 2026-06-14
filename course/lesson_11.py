# 第11课 - 复制魔法 (Loops)
# 目标：使用 for 循环简化重复代码

import os
import turtle
import time

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = text.replace("🌀 ", "").replace("🎨 ", "")
    os.system(f"say -r 150 '{clean_text}'")

speak("🌀 启动无限循环魔法！")

t = turtle.Turtle()
t.shape("turtle")
t.color("purple")
t.pensize(3)

# 1. 简单的正方形循环
speak("--- 任务1：画正方形 ---")
for i in range(4):
    speak("画第" + str(i+1) + "条边")
    t.forward(100)
    t.left(90)
    time.sleep(0.5)

time.sleep(1)
t.clear() # 清空屏幕

# 2. 画个更复杂的：六边形
# 六边形转角是 360 / 6 = 60 度
speak("--- 任务2：画六边形 ---")
t.color("orange")

for i in range(6):
    t.forward(80)
    t.left(60)

time.sleep(1)
t.clear()

# 3. 疯狂的艺术 (花朵)
speak("--- 任务3：画一朵花 ---")
t.color("red")
t.speed(10) # 全速前进！

# 重复 36 次
for i in range(36):
    t.circle(50) # 画一个圆
    t.left(10)   # 每次歪一点点

speak("🎨 这是一个甜甜圈吗？")
turtle.done()
