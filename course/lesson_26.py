import os
import turtle
import random
import time

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = text.replace("✨ ", "").replace("🎆", "")
    os.system(f"say -r 150 '{clean_text}'")

# --- 1. 环境准备 ---
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("魔法烟花秀 🎆")
# 禁用自动刷新，开启手动刷新以获得流畅动画
turtle.tracer(0)

# 隐藏画笔，只看结果
t = turtle.Turtle()
t.hideturtle()

# 存储所有活动粒子的列表
particles = []

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        # 赋予一个随机的初始速度 (爆炸效果)
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-2, 8)
        # 生命值：粒子能存活多久
        self.life = random.randint(30, 60)
        # 重力大小
        self.gravity = 0.2

    def move(self):
        """更新粒子位置并模拟重力"""
        self.x += self.vx
        self.y += self.vy
        self.vy -= self.gravity # 模拟重力往下拉
        self.life -= 1

    def draw(self):
        """在屏幕上画出粒子"""
        if self.life > 0:
            t.penup()
            t.goto(self.x, self.y)
            t.dot(random.randint(2, 5), self.color)

def create_firework(x, y):
    """在指定位置创建一个烟花（包含几十个粒子）"""
    colors = ["#FF5E5E", "#FFD700", "#00FF7F", "#00BFFF", "#FF00FF", "#FFFFFF"]
    firework_color = random.choice(colors)
    for _ in range(30):
        particles.append(Particle(x, y, firework_color))

# 监听鼠标点击，点击哪里就在哪里放烟花
screen.onclick(create_firework)

speak("✨ 准备好了！点击黑色屏幕，释放魔法烟花吧！")

# --- 2. 动画主循环 ---
while True:
    try:
        t.clear() # 清空画板

        # 遍历每一个粒子，更新并绘制
        # 我们使用切片 [:] 来遍历，这样在循环中删除元素才安全
        for p in particles[:]:
            p.move()
            p.draw()
            # 如果粒子生命结束，从列表中移除
            if p.life <= 0:
                particles.remove(p)

        # 刷新屏幕显示最终结果
        turtle.update()
        
        # 维持大约 60 FPS 的速度
        time.sleep(1/60)
        
        # 为了防止画面太空，偶尔自动放一个烟花
        if random.random() < 0.02:
            create_firework(random.randint(-200, 200), random.randint(-100, 200))

    except turtle.Terminator:
        # 捕获窗口关闭异常，防止报错
        break
    except Exception as e:
        print(f"哎呀，出错了: {e}")
        break

turtle.done()
