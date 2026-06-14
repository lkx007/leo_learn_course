import os
import turtle

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = text.replace("🤖 ", "").replace("✅ ", "").replace("💁‍♂️ ", "").replace("🤔 ", "").replace("😴 ", "").replace("╔", "").replace("║", "").replace("╚", "").replace("═", "").replace("╗", "").replace("╝", "")
    os.system(f"say -r 150 '{clean_text}'")

# --- 1. 准备工具箱 (Define Tools) ---
# 这些是 AI 的“手”，负责干活

t = turtle.Turtle()
t.speed(5)
t.pensize(3)

def draw_square():
    speak("🤖 收到！正在调用 [方块工具]...")
    t.color("blue")
    for i in range(4):
        t.forward(100)
        t.right(90)
    speak("✅ 画好了！")

def draw_circle():
    speak("🤖 收到！正在调用 [圆圈工具]...")
    t.color("red")
    t.circle(50)
    speak("✅ 画好了！")

def draw_triangle():
    speak("🤖 收到！正在调用 [三角形工具]...")
    t.color("green")
    for i in range(3):
        t.forward(100)
        t.left(120)
    speak("✅ 画好了！")

# --- 2. AI 的大脑 (The Brain) ---
# 这是一个死循环，直到你让它停下

speak("╔════════════════════════════╗")
speak("║    🤖  我是你的 AI 画家    ║")
speak("╚════════════════════════════╝")
speak("我会画：square (方块), circle (圆圈), triangle (三角形)")
speak("输入 'exit' 退出")

while True:
    # 1. 听指令 (Input)
    command = input("\n💁‍♂️ 主人，请下令: ")
    
    # 2. 思考与决策 (Think & Choose Tool)
    if command == "square":
        draw_square() # 调用方块工具
        
    elif command == "circle":
        draw_circle() # 调用圆圈工具
        
    elif command == "triangle":
        draw_triangle() # 调用三角形工具
        
    elif command == "exit":
        speak("😴 好的，我休息了。再见！")
        break # 跳出循环，结束程序
        
    else:
        speak("🤔 呃，我还没学会这个魔法... 请说 square, circle 或 triangle")

turtle.done()
