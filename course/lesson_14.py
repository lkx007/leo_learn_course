import os

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    os.system(f"say -r 150 '{text}'")

# 创建一个空的购物车
cart = []
speak("现在的购物车是空的：" + str(cart))

# 添加苹果
speak("放入苹果...")
cart.append("Apple")
speak(cart)

# 添加香蕉
speak("放入香蕉...")
cart.append("Banana")
speak(cart)

# 添加巧克力
speak("放入巧克力...")
cart.append("Chocolate")
speak(cart)

# 哎呀，不想要香蕉了
speak("把香蕉拿出来...")
cart.remove("Banana")
speak(cart)

speak("购物完成！最终清单：")
speak(cart)
