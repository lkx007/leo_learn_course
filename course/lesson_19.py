import os

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = text.replace("🤖 ", "").replace("📖 ", "").replace("💡 ", "").replace("❓ ", "").replace("🎂 ", "").replace("🎉 ", "").replace("🤔 ", "")
    os.system(f"say -r 150 '{clean_text}'")

# 这是一个简单的“知识增强” AI
def super_ai(question, context):
    speak("\n🤖 AI 正在思考: " + question)
    speak("📖 AI 正在翻阅你给的书...")
    
    # 模拟 AI 理解上下文
    if "小鱼" in question:
        if "名字" in context:
            speak("💡 回答：书里说，你的名字叫小鱼！")
        else:
            speak("❓ 书里没提你的名字呀。")
            
    elif "生日" in question:
        if "5月1日" in context:
            speak("🎂 回答：你的生日是 5月1日！祝你生日快乐！")
        else:
            speak("❓ 我不知道你的生日...")
            
    else:
        speak("🤔 这个问题书里找不到答案。")

# --- 让我们来测试一下 ---

# 1. 准备一本“书” (Context)
my_secret_book = "我的名字叫小鱼。我的生日是 5月1日。"

# 2. 问一个简单的问题
super_ai("我的生日是哪天？", my_secret_book)

# 3. 问一个没写的问题
super_ai("我喜欢吃什么？", my_secret_book)

# 4. 假如我不给它书...
super_ai("我的生日是哪天？", "")
