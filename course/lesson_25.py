import os
import turtle
import time

def speak(text):
    """同时在屏幕打印文字并语音播报"""
    print(text)
    # 语音播报
    clean_text = text.replace("🚀 ", "").replace("✅ ", "")
    os.system(f"say -r 150 '{clean_text}'")

# --- 1. 环境准备 ---
# 创建海龟对象
t = turtle.Turtle()
# 关闭海龟本身的形状，直接画扇叶
t.hideturtle()
# 提高绘图速度到最快
t.speed(0)
# 禁用自动刷新，开启手动刷新（重要：实现不闪烁动画的关键）
turtle.tracer(0)

def draw_fan(angle):
    """根据给定的旋转角度绘制风扇"""
    t.clear()  # 清除上一帧
    t.penup()
    t.goto(0, -200) # 把风扇支架画在下面
    t.pendown()
    t.setheading(90)
    t.forward(200)
    
    # 画风扇中心轴
    center_y = 0
    t.penup()
    t.goto(0, center_y)
    t.dot(20, "gray")
    
    # 画三片扇叶
    colors = ["#3498db", "#e74c3c", "#f1c40f"] # 蓝、红、黄
    for i in range(3):
        t.penup()
        t.goto(0, center_y)
        # 每片扇叶间隔 120 度，再加上当前的旋转角 angle
        current_angle = angle + (i * 120)
        t.setheading(current_angle)
        
        # 开始画扇叶
        t.pendown()
        t.color(colors[i])
        t.begin_fill()
        # 画一个水滴形状作为扇叶
        t.circle(80, 60)
        t.left(120)
        t.circle(80, 60)
        t.end_fill()
        
    # --- 新增：显示计数器 ---
    t.penup()
    t.goto(0, 250)
    t.color("black")
    current_rotations = int(angle // 360)
    # 使用总圈数变量 rotations (在外部定义)
    t.write(f"当前旋转：{current_rotations} / 总计：10", align="center", font=("Arial", 20, "bold"))
    # -----------------------
    t.color("black")

# --- 2. 动画循环 ---
speak("🚀 电风扇启动！准备转动 10 圈...")

# 设定总圈数
rotations = 10
angle = 0
# 每一步旋转的角度
step = 5 
# 总共需要旋转的角度 (10 圈 * 360 度)
total_angle = rotations * 360

while angle < total_angle:
    # 1. 绘制当前帧
    draw_fan(angle)
    # 2. 手动刷新屏幕（把画好的图一次性显示出来）
    turtle.update()
    # 3. 增加角度
    angle += step
    # 4. 稍微等一下，控制动画速度
    time.sleep(0.01)

speak("✅ 转动完成！电风扇已停。")
# 保持窗口开启
turtle.done()
