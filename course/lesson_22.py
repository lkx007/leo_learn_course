import os

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = str(text).replace("🧮 ", "").replace("✅ ", "").replace("🤔 ", "").replace("🤯 ", "").replace("╔", "").replace("║", "").replace("╚", "").replace("═", "").replace("╗", "").replace("╝", "")
    os.system(f"say -r 150 '{clean_text}'")

# --- 1. 定义数学工具 (Math Tools) ---

def add(a, b):
    speak(f"🧮 正在计算 {a} + {b} ...")
    return a + b

def subtract(a, b):
    speak(f"🧮 正在计算 {a} - {b} ...")
    return a - b

def multiply(a, b):
    speak(f"🧮 正在计算 {a} x {b} ...")
    return a * b

# --- 2. AI 的大脑 (The Brain) ---

speak("╔════════════════════════════╗")
speak("║    🧮  我是你的 AI 数学家  ║")
speak("╚════════════════════════════╝")
speak("我会算简单的数学题！(比如: 1 + 1, 10 - 5, 3 * 3)")
speak("输入 'exit' 退出")

while True:
    text = input("\n请出题: ")
    
    if text == "exit":
        speak("Bye!")
        break
    
    # --- 3. 核心逻辑：解析 (Parsing) ---
    # 我们假设用户输入的是 "数字 符号 数字" (用空格分开)
    # 比如 "10 + 20"
    
    parts = text.split(" ") # 把句子切开
    
    # 简单的错误检查：如果切开不是3部分，那就看不懂
    if len(parts) != 3:
        speak("🤔 我没看懂... 请用空格分开，比如 '1 + 1'")
        continue
        
    try:
        num1 = int(parts[0]) # 把第一个变成数字
        op   = parts[1]      # 符号 (+, -, *)
        num2 = int(parts[2]) # 把第三个变成数字 (中间是符号)
    except ValueError:
        speak("🤔 请确保输入的是数字，比如 '1 + 1'")
        continue
    
    # --- 4. 选择工具 (Tool Selection) ---
    
    if op == "+":
        result = add(num1, num2)
        speak("✅ 答案是：" + str(result))
        
    elif op == "-":
        result = subtract(num1, num2)
        speak("✅ 答案是：" + str(result))
        
    elif op == "*":
        result = multiply(num1, num2)
        speak("✅ 答案是：" + str(result))
        
    else:
        speak("🤯 我还不会算这个符号！")

