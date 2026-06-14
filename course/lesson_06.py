# 第06课 - 魔法门卫 (If Statement)
# 目标：学会使用 if (如果) 来做决定

import os
import time

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报（过滤掉表情符号，语速设为匀速）
    clean_text = text.replace("🏰 ", "").replace("⚔️  ", "").replace("✨ ", "").replace("🔑 ", "")
    os.system(f"say -r 150 '{clean_text}'")

speak("🏰 站住！这里是魔法城堡！")
time.sleep(1)

# 1. 询问口令
speak("⚔️  门卫：想要进去吗？")
password = input("🔑 请说出通关口令: ")

# 2. 判断口令
if password == "芝麻开门":
    speak("✨ (门缓缓打开的声音...)")
    time.sleep(1)
    speak("⚔️  门卫：口令正确！请进！")
    speak("🏰 欢迎来到魔法城堡大厅！")

# 3. 无论进没进去，最后都会说的话
speak("\n--- 游戏结束 ---")
