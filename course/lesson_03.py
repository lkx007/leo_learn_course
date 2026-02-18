import os

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报（过滤掉表情符号，语速设为匀速）
    clean_text = text.replace("-", "").replace("\n", "").strip()
    if clean_text:
        os.system(f"say -r 150 '{clean_text}'")

# --------------------------
# 魔法 1：加法 (+)
# --------------------------
speak("--- 魔法 1: 加苹果 ---")
apples_left = 3
apples_right = 2

# 这里的 + 就是把两边的数字加起来
total = apples_left + apples_right

speak("原本有3个，又拿来2个，一共有:")
speak(str(total))

# --------------------------
# 魔法 2：减法 (-)
# --------------------------
speak("\n--- 魔法 2: 吃苹果 ---")
total_apples = 5
ate = 1

# 这里的 - 就是减去
left = total_apples - ate

speak("有5个苹果，吃掉1个，还剩:")
speak(str(left))

# --------------------------
# 练习 1：玩具总动员
# --------------------------
speak("\n--- 练习 1: 玩具 ---")
my_toys = 2
friend_toys = 3

# 算加法
all_toys = my_toys + friend_toys

speak("我的玩具总数:")
speak(str(all_toys))

# --------------------------
# 练习 2：买糖果
# --------------------------
speak("\n--- 练习 2: 买糖果 ---")
money = 10
price = 2

# 算减法
left_money = money - price

speak("剩下的钱:")
speak(str(left_money))

# --------------------------
# 小任务：压岁钱
# --------------------------
speak("\n--- 小任务: 压岁钱 ---")
# 在下面写你的代码
gift_grandma = 5
gift_mom = 5
total_money = gift_grandma + gift_mom

speak("我的压岁钱总共:")
speak(str(total_money))
