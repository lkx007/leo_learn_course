# 第08课 - 石头剪刀布
# 目标：制作一个简单的对战游戏

import os
import time
import random

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = text.replace("🎮 ", "").replace("🤖 ", "").replace("👉 ", "").replace("🧑 ", "").replace("🎉 ", "").replace("😭 ", "").replace("🤝 ", "").replace("😵 ", "")
    os.system(f"say -r 150 '{clean_text}'")

speak("🎮 欢迎来到石头剪刀布大赛！")
speak("规则：石头砸剪刀，剪刀剪布，布包石头")
time.sleep(4)

# 1. 电脑准备出拳
choices = ["石头", "剪刀", "布"]
computer_choice = random.choice(choices)

speak("🤖 电脑已经准备好了！")

# 2. 玩家出拳
my_choice = input("👉 请出拳 (输入 石头/剪刀/布): ")

speak("...")
time.sleep(3)
speak("🤖 电脑出的是: " + computer_choice)
speak("🧑 你出的是: " + my_choice)
speak("--- 裁判结果 ---")

# 3. 判断输赢
if my_choice == computer_choice:
    speak("🤝 平局！心有灵犀一点通！")
elif my_choice == "石头":
    if computer_choice == "剪刀":
        speak("🎉 你赢了！石头砸烂了剪刀！")
    else:
        speak("😭 你输了... 布把石头包住了！")
elif my_choice == "剪刀":
    if computer_choice == "布":
        speak("🎉 你赢了！剪刀剪碎了布！")
    else:
        speak("😭 你输了... 剪刀被石头砸坏了！")
elif my_choice == "布":
    if computer_choice == "石头":
        speak("🎉 你赢了！布包住了石头！")
    else:
        speak("😭 你输了... 布被剪刀剪破了！")
else:
    speak("😵 哎呀？你出的是什么拳法？裁判看不懂！(输入错误)")

speak("\n--- 游戏结束 ---")
