import os
import turtle
import time

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = str(text).replace("🎨 ", "").replace("✅ ", "").replace("🔍 ", "").replace("🔵 ", "").replace("💁‍♂️ ", "").replace("🧮 ", "").replace("📄 ", "").replace("💬 ", "")
    os.system(f"say -r 150 '{clean_text}'")

# ==========================================
# 🧠 1. 定义大脑的知识库 (Knowledge Base)
# ==========================================
memory = {
    "小鱼": "7岁的天才程序员",
    "JARVIS": "我是你的超级管家，全名 Just A Rather Very Intelligent System",
    "钢铁侠": "我的创造者 Tony Stark (其实是你！)",
    "大象": "陆地上最大的动物"
}

# ==========================================
# 🛠️ 2. 定义工具 (Tools)
# ==========================================

# --- 工具 A: 画笔 (Turtle) ---
def tool_draw(shape):
    t = turtle.Turtle()
    t.speed(5)
    t.pensize(3)
    
    speak(f"🎨 JARVIS: 正在为您绘制 {shape} ...")
    
    if "圆" in shape:
        t.color("red")
        t.circle(50)
    elif "方" in shape:
        t.color("blue")
        for i in range(4):
            t.forward(100)
            t.right(90)
    elif "三角" in shape:
        t.color("green")
        for i in range(3):
            t.forward(100)
            t.left(120)
    else:
        speak("🎨 JARVIS: 抱歉，我只会画简单的图形")
        
    speak("✅ 绘制完成")

# --- 工具 B: 计算器 (Math) ---
def tool_calculate(expression):
    # 简单的加法解析器
    if "+" in expression:
        parts = expression.split("+")
        a = int(parts[0])
        b = int(parts[1])
        return a + b
    elif "-" in expression:
        parts = expression.split("-")
        a = int(parts[0])
        b = int(parts[1])
        return a - b
    else:
        return "未知算式"

# --- 工具 C: 搜索 (Search) ---
def tool_search(keyword):
    speak(f"🔍 JARVIS: 正在搜索记忆库关于 '{keyword}' 的信息...")
    time.sleep(1) # 假装在思考
    if keyword in memory:
        return memory[keyword]
    else:
        return "没有找到相关记录"

# ==========================================
# 🤖 3. 启动主程序 (Main Loop)
# ==========================================

speak("🔵 系统启动中...")
time.sleep(1)
speak("🔵 连接网络...")
time.sleep(1)
speak("✅ JARVIS 在线！")
speak("-----------------------------------")
speak("你好，主人。我是 JARVIS。")
speak("我可以：画画、算数、查资料、聊天。")
speak("-----------------------------------")

while True:
    command = input("\n💁‍♂️ 请下令: ")
    
    if command == "exit":
        speak("🔵 JARVIS 关机。晚安，先生。")
        break
        
    # --- 核心智能：意图识别 (Intent Recognition) ---
    
    # 1. 识别画画意图
    if "画" in command:
        tool_draw(command)
        
    # 2. 识别计算意图
    elif "+" in command or "-" in command or "算" in command:
        try:
            # 简单的取巧，把 "算一下" 去掉
            clean_cmd = command.replace("算一下", "").replace("算", "").strip()
            result = tool_calculate(clean_cmd)
            speak("🧮 JARVIS: 结果是 " + str(result))
        except:
            speak("🧮 JARVIS: 请输入简单的算式，例如 '10+20'")

    # 3. 识别搜索意图
    elif "是谁" in command or "是什么" in command:
        # 提取关键词，比如 "小鱼是谁" -> "小鱼"
        keyword = command.replace("是谁", "").replace("是什么", "").replace("?", "").strip()
        info = tool_search(keyword)
        speak("📄 JARVIS: " + info)
        
    # 4. 默认聊天模式
    else:
        speak("💬 JARVIS: 我在听。")

turtle.done()
