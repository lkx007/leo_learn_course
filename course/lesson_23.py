import os

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = str(text).replace("🔍 ", "").replace("🤔 ", "").replace("🤖 ", "").replace("╔", "").replace("║", "").replace("╚", "").replace("═", "").replace("╗", "").replace("╝", "")
    os.system(f"say -r 150 '{clean_text}'")

# --- 1. 秘密笔记本 (Knowledge Base) ---
# 这是 AI 的长期记忆
notebook = {
    "小鱼": "7岁的大帅哥，喜欢乐高和编程。",
    "爸爸": "可以把电脑变听话的魔法师。",
    "妈妈": "做饭超好吃，虽然有时候会凶巴巴。",
    "Python": "一种像英语一样的魔法语言。",
    "Turtle": "一只会画画的小海龟。"
}

# --- 2. 搜索工具 (Search Tool) ---

def search_notebook(keyword):
    speak(f"🔍 正在翻阅笔记本，查找 '{keyword}' ...")
    
    # 在字典里找 key
    if keyword in notebook:
        return notebook[keyword]
    else:
        return "不知道... 笔记本里没写这个。"

# --- 3. AI 的大脑 (The Brain) ---

speak("╔════════════════════════════╗")
speak("║    🔍  我是超级搜索助手    ║")
speak("╚════════════════════════════╝")
speak("你想知道什么秘密？(输入 'exit' 退出)")
speak("试试问：小鱼, 爸爸, Python")

while True:
    question = input("\n🤔 请提问: ")
    
    if question == "exit":
        break
        
    # 直接调用搜索工具
    answer = search_notebook(question)
    
    speak("🤖 回答：" + answer)

