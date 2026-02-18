import sys
import tty
import termios
import random
import time
import os
import glob

# --- Mac 专用按键读取函数 ---
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# --- 魔法地图绘制 ---
def draw_keyboard(highlight_char=None):
    # ANSI 颜色代码
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED_BG = "\033[41m" # 红色背景，高亮目标
    GREEN = "\033[92m"  # 绿色文字

    # 键盘布局数据 (为了方便查找)
    # 每一行是一个字符串
    rows = [
        "  [q] [w] [e] [r] [t]   [y] [u] [i] [o] [p] ",
        "   [a] [s] [d] [f] [g]   [h] [j] [k] [l] [;] ",
        "    [z] [x] [c] [v] [b]   [n] [m] [,] [.]     ",
        "               [     SPACE     ]              "
    ]

    # 清屏 (使用 ANSI 原地刷新会更好，但简单起见用 clear)
    os.system('cls' if os.name == 'nt' else 'clear')

    print("╔════════════════════════════╗")
    print("║    🖐️  魔法指法特训游戏  🖐️    ║")
    print("╚════════════════════════════╝")
    print("\n👀 小提示：请按红色高亮的键！(按 'Ctrl+C' 退出)")
    
    print("\n")
    for row in rows:
        line_str = ""
        # 简单的字符串替换来高亮 (注意：这只处理简单字母，不做复杂定位)
        if highlight_char:
            # 处理特殊按键空格
            if highlight_char == " " and "SPACE" in row:
                line_str = row.replace("[     SPACE     ]", f"{RED_BG}[     SPACE     ]{RESET}")
            # 处理普通字母 (加中括号匹配，防止误伤)
            elif f"[{highlight_char}]" in row:
                line_str = row.replace(f"[{highlight_char}]", f"{RED_BG}[{highlight_char}]{RESET}")
            # 处理符号 ; , . (它们在布局里)
            elif f"[{highlight_char}]" in row:
                line_str = row.replace(f"[{highlight_char}]", f"{RED_BG}[{highlight_char}]{RESET}")
            else:
                line_str = row
        else:
            line_str = row
        print(line_str)
    print("\n")

# --- 题库加载逻辑 ---
def load_code_bank():
    """从当前目录的所有 .py 文件加载代码行作为题库"""
    code_lines = []
    # 获取当前脚本所在目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 查找所有 .py 文件
    py_files = glob.glob(os.path.join(base_dir, "*.py"))

    for file_path in py_files:
        # 跳过自身，避免剧透代码或者读到奇怪的东西（虽然也可以读自己作为练习）
        # 这里还是读所有的吧，练习打自己的代码也挺好
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    # 过滤掉空行、注释、太短的行
                    if not line:
                        continue
                    if line.startswith("#"):
                        continue
                    if len(line) < 4: # 太短的没意义
                        continue
                    # 过滤掉包含非ASCII字符的行（如中文、中文标点等），以免无法输入
                    if not all(ord(c) < 128 for c in line):
                        continue
                    code_lines.append(line)
        except Exception as e:
            # 忽略读取错误
            continue
            
    # 去重
    unique_lines = list(set(code_lines))
    
    # 如果没有找到足够多的行，就用默认的补充一下
    if len(unique_lines) < 10:
        defaults = [
            "print('Hello World')", "import random", "def my_func():", 
            "return True", "if __name__ == '__main__':", "class MyClass:",
            "for i in range(10):", "while True:", "try: except:", "with open() as f:"
        ]
        unique_lines.extend(defaults)
        
    return unique_lines

# --- 游戏主逻辑 ---

# 每一局的轮数，可以根据需要调整，但题目池很大
ROUNDS = 10 

# --- 语音播报函数 ---
def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 过滤掉一些字符以获得更好的语音效果
    clean_text = text.replace("📚 ", "").replace("🎮 ", "").replace("⏱️  ", "").replace("⌨️  ", "").replace("💯 ", "").replace("📝 ", "").replace("🐢 ", "").replace("🐇 ", "").replace("🏎️ ", "").replace("🚀 ", "").replace("🏆 ", "").replace("💪 ", "").replace("✨ ", "").replace("🖐️  ", "")
    os.system(f"say -r 150 '{clean_text}'")

def play_game():
    score = 0
    
    # 加载动态题库
    all_questions = load_code_bank()
    
    # 按照长度分类（难度分级）
    easy_pool = [q for q in all_questions if 4 <= len(q) <= 12]
    medium_pool = [q for q in all_questions if 13 <= len(q) <= 25]
    hard_pool = [q for q in all_questions if len(q) > 25]

    speak(f"📚 已加载题库，共有 {len(all_questions)} 条代码练习！")
    speak("准备好了吗？我们将由浅入深开始练习。")
    
    print("按任意键开始...")
    getch()

    game_start_time = time.time()
    total_chars_typed = 0

    for i in range(ROUNDS):
        # 难度分段逻辑
        if i < 3: # 1-3 轮：入门级
            pool = easy_pool if easy_pool else all_questions
            level_msg = "🌟 入门级 (短小精悍)"
            if i == 0: speak("🎮 开始 入门级 练习，代码很短哦，加油！")
        elif i < 7: # 4-7 轮：进阶级
            pool = medium_pool if medium_pool else all_questions
            level_msg = "🚀 进阶级 (渐入佳境)"
            if i == 3: speak("🚀 难度升级！进入 进阶级，代码变长了一点点，你可以的！")
        else: # 8-10 轮：挑战级
            pool = hard_pool if hard_pool else all_questions
            level_msg = "🔥 挑战级 (终极挑战)"
            if i == 7: speak("🔥 英雄请留步！终极挑战已经开启，展示你真实实力的时候到了！")

        target_word = random.choice(pool)
        typed_word = ""
        
        start_time = time.time()
        
        # 语音提示第几轮
        os.system(f"say -r 150 '第 {i+1} 轮'")
        
        # 逐个字符练习
        for char in target_word:
            # 1. 绘制键盘，高亮当前需要的字符
            draw_keyboard(char.lower())
            
            # 2. 显示当前进度
            print(f"------------------------------")
            print(f"{level_msg} | 第 {i+1}/{ROUNDS} 轮")
            print(f"目标: {target_word}")
            print(f"输入: {typed_word}", end="", flush=True) # 不换行
            
            # 3. 等待输入
            while True:
                # 获取按键 (不回显)
                key = getch()
                
                # 如果按对了
                if key == char:
                    typed_word += key
                    break # 进入下一个字符
                
                # 如果是 Ctrl+C
                elif ord(key) == 3: 
                    sys.exit()
                
                # 如果是回车
                elif char == '\n' and key in ['\r', '\n']:
                     typed_word += '\n'
                     break

        # 单词/句子完成！
        end_time = time.time()
        time_taken = round(end_time - start_time, 2)
        score += 10 # 每完成一个给 10 分
        total_chars_typed += len(target_word)
        
        draw_keyboard(None) # 清除高亮
        speak(f"\n✨ 完成！ 本句用时 {time_taken} 秒")
        time.sleep(0.5)

    # 游戏结束总结
    game_end_time = time.time()
    total_duration = round(game_end_time - game_start_time, 2)
    
    # 计算每分钟字符数 (CPM)
    cpm = 0
    if total_duration > 0:
        cpm = int((total_chars_typed / total_duration) * 60)

    draw_keyboard(None)
    speak(f"\n🎮 游戏结束！")
    speak(f"⏱️  总耗时: {total_duration} 秒")
    speak(f"⌨️  平均速度: {cpm} 字符每分钟")
    speak(f"💯 总得分: {score} 分")

    # 根据时长/速度展示不同结束语
    # 这里我们主要用 CPM 来衡量水平，用“时长”也可以但 CPM 更公平
    # 如果用户特别强调“根据打字时长”，可以理解为“坚持了多久”或者“用时由快到慢”
    # 我们还是结合一下吧
    
    speak("\n📝 评语：")
    if cpm < 60:
         speak("🐢 慢慢来，比较快！还需要多多练习哦~")
    elif cpm < 120:
         speak("🐇 不错不错，已经有一点程序员的感觉了！")
    elif cpm < 200:
         speak("🏎️ 速度很快！你的手指在键盘上飞舞！")
    else:
         speak("🚀 太强了！你是传说中的键盘侠客吗？！")
         
    if total_duration > 60:
        speak(f"坚持练习了 {total_duration} 秒，毅力可嘉！")

    if score == ROUNDS*10:
        speak("\n🏆 完美通关！")
    else:
        speak("\n💪 继续加油！")

if __name__ == "__main__":
    play_game()
