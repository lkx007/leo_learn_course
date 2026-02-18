# 第04课 - 会聊天的电脑
# 目标：学会使用 input() 函数让电脑听懂我们的话

import os
import time

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报（过滤掉表情符号，语速设为匀速）
    clean_text = text.replace("🖥️ : ", "").replace("👉 ", "").replace("✨ ", "").replace("👋 ", "")
    os.system(f"say -r 150 '{clean_text}'")

# 欢迎语
speak("🖥️ : 哔哔哔... 启动中...")
time.sleep(1)
speak("🖥️ : 你好！我是你的电脑好朋友。")

# 第一步：认识你
# input() 就像是把麦克风递给你，等你说话
speak("🖥️ : 我还不知道你叫什么名字呢。")
name = input("👉 请在大于号后面输入你的名字，然后按回车: ")

# 第二步：打招呼
# 我们用 + 号把你的名字连起来
speak("✨ 哇！原来是 " + name + " 大侠！久仰大名！")
time.sleep(1)

# 第三步：聊聊爱好
speak("🖥️ : " + name + "，你平常最喜欢做什么事情呀？")
hobby = input("👉 请输入（比如画画、玩乐高、看书）: ")

speak("🖥️ : " + hobby + "？听起来太酷了！")
speak("🖥️ : 下次能不能教教我怎么 " + hobby + " 呀？")

# 第四步：告别
speak("👋 今天聊得很开心，再见啦，" + name + "！")
