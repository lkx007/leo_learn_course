import os

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = text.replace("🧹 ", "").replace("🧽 ", "").replace("✨ ", "").replace("🤖: ", "").replace("⚡️", "")
    os.system(f"say -r 150 '{clean_text}'")

# 1. 定义一个打扫房间的函数 (咒语)
def clean_room():
    speak("----- 开始大扫除 -----")
    speak("🧹 扫扫地...")
    speak("🧽 擦擦窗...")
    speak("✨ 哇！房间变干净了！")
    speak("--------------------")

# 2. 第一次召唤
speak("妈妈说：要把房间打扫干净！")
clean_room()

# 3. 第二次召唤
speak("\n过了一周，房间又乱了...")
clean_room()

# 定义一个简单的 AI 回答函数
def simple_ai():
    speak("🤖: 我是 AI，我喜欢吃电！⚡️")

speak("\n召唤 AI:")
simple_ai()
