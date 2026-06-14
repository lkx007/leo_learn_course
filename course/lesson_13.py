import os

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = str(text).replace("🚂", "")
    os.system(f"say -r 150 '{clean_text}'")

# 创建一个玩具列表 (Magic Train)
my_toys = ["乐高", "变形金刚", "遥控车", "奥特曼"]

# 打印整列火车
speak("我的玩具小火车出发啦！🚂")
speak(my_toys)

# 看看火车有多长？
speak("火车一共有多少节车厢？")
speak(len(my_toys))

# 创建一个数字列表
lucky_numbers = [6, 8, 66, 88]
speak("\n我的幸运数字：")
speak(lucky_numbers)
