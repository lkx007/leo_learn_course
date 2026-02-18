# 第05课 - 真真假假
# 目标：理解 True (真) 和 False (假)

import os
import time

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报（过滤掉表情符号，语速设为匀速）
    clean_text = text.replace("⚖️  ", "").replace("❓ ", "").replace("🤔 ", "").replace("👉 ", "")
    os.system(f"say -r 150 '{clean_text}'")

speak("⚖️  大法官电脑开庭啦！")
time.sleep(1)

# 1. 数字大比拼
speak("--- 第一回合：数字大比拼 ---")
speak("❓ 10 比 5 大吗？")
speak(str(10 > 5))

speak("❓ 3 比 100 大吗？")
speak(str(3 > 100))

speak("❓ 1 加 1 等于 2 吗？")
speak(str(1 + 1 == 2))
time.sleep(2)

# 2. 猜猜我是谁
speak("\n--- 第二回合：身份大揭秘 ---")
input_name = input("👉 请输入你的名字: ")

# 判断输入的名字是不是 "小鱼"
# 结果会存到 is_master (是不是主人) 这个盒子里
is_master = (input_name == "小鱼")

speak("🤔 让我通过数据分析一下...")
time.sleep(1)
speak("你是我的主人小鱼吗？")
speak(str(is_master))

# 3. 简单的数学题
speak("\n--- 第三回合：数学小测试 ---")
user_ans = input("👉 10 + 10 = ? 请输入答案: ")

# 比较用户的答案是不是 "20"
is_right = (user_ans == "20")

speak("你的答案正确吗？")
speak(str(is_right))
