import os

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = text.replace("🎨 ", "").replace("✨ ", "").replace("🍌🍎 ", "").replace("🧃", "")
    os.system(f"say -r 150 '{clean_text}'")

# 定义一个能画出任何东西的 AI 函数
def create_art(thing, style):
    speak("----- AI 绘画中 -----")
    speak("正在接收指令：画一个 " + thing)
    speak("正在应用风格：" + style)
    speak("🎨 唰唰唰...")
    speak("✨ 一幅 [" + style + " 的 " + thing + "] 画好了！")
    speak("--------------------")

# 第一次测试
create_art("猫", "卡通风格")

# 第二次测试
create_art("城堡", "乐高风格")

# 每日挑战：榨果汁
def make_juice(fruit):
    speak("\n🍌🍎 榨汁机启动！")
    speak("正在把 " + fruit + " 变成美味的果汁！🧃")
    speak("请慢用！")

make_juice("草莓")
make_juice("西瓜")
