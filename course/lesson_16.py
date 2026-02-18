import os

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = str(text).replace("🐶", "").replace("🐱", "").replace("🐰", "").replace("🐼", "").replace("🦁", "")
    os.system(f"say -r 150 '{clean_text}'")

# 这里有一群小动物
animals = ["🐶", "🐱", "🐰", "🐼", "🦁"]

speak("动物园点名开始！")

# 使用 for 循环一个一个点名
for animal in animals:
    speak("发现了一只：" + animal)
    # 你甚至可以在循环里做更多事
    if animal == "🐼":
        speak("哇！是大熊猫！国宝！")

speak("点名结束！")
