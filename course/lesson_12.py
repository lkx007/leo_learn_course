import os
import turtle

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    os.system(f"say -r 150 '{text}'")

speak("✨ 欢迎来到魔法烟花秀！🎆")

# 创建画笔
t = turtle.Turtle()
t.speed(0)  # 0 是最快速度，瞬间完成！
t.pensize(2)

# 设置黑色背景，更有烟花的感觉
turtle.bgcolor("black")

# 准备 6 种颜色
colors = ["red", "orange", "yellow", "green", "blue", "purple"]

# 循环 200 次
for i in range(200):
    # 挑选颜色：i % 6 的结果是 0,1,2,3,4,5 循环
    t.pencolor(colors[i % 6])
    
    # 前进距离越来越长
    t.forward(i * 1.5)
    
    # 每次向左转 59 度（你可以改成 90 或 91 试试看！）
    t.left(59)

# 点击窗口关闭
turtle.done()
