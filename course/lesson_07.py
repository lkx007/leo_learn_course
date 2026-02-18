# 第07课 - 左转还是右转 (If/Else)
# 目标：学会使用 else (否则) 来处理另外一种情况

import os
import time

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = text.replace("🦁 ", "").replace("🚪 ", "").replace("👉 ", "").replace("🐰 ", "").replace("✅ ", "").replace("🚫 ", "").replace("🐕", "")
    os.system(f"say -r 150 '{clean_text}'")

speak("🦁 欢迎来到动物园！")
time.sleep(1)

# 1. 简单的二选一
speak("🚪 面前有两扇门...")
choice = input("👉 你想进 左边的门 还是 右边的门？(输入 左 或 右): ")

# 2. If/Else 结构
if choice == "左":
    speak("🦁 吼！！！你遇到了一只大狮子！")
    speak("快跑啊！")
else:
    speak("🐰 哇！你遇到了一群可爱的小兔子！")
    speak("可以摸摸它们哦。")

time.sleep(2)

# 3. 密码门升级版
speak("\n--- 城堡大门 ---")
password = input("🔑 请再次输入口令 (芝麻开门): ")

if password == "芝麻开门":
    speak("✅ 欢迎回家，主人！")
else:
    speak("🚫 警报！警报！坏人想闯入！")
    speak("放狗！汪汪汪！🐕")
