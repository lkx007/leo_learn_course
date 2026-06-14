import os

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    os.system(f"say -r 150 '{text}'")

# 三只小猪的名字
pigs = ["老大", "老二", "老三"]

speak("三只小猪盖房子！")

# 访问第一个元素 (Index 0)
speak("第一只小猪是：" + pigs[0])

# 访问第二个元素 (Index 1)
speak("第二只小猪是：" + pigs[1])

# 访问第三个元素 (Index 2)
speak("第三只小猪是：" + pigs[2])

# 试试倒着数 (Index -1)
speak("最聪明的小猪是最后一个：" + pigs[-1])

# 修改列表里的东西
speak("\n哎呀，老大改名了！")
pigs[0] = "猪大哥"
speak("现在的名单：" + str(pigs))
