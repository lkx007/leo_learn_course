# 实施计划：20260218084600

## 目标描述
在 `lesson_25.py` 的电扇旋转动画中，增加一个实时显示的计数器，让学生可以直观看到“当前已转了多少次”以及“准备转多少次”。

## 拟议变更

### [MODIFY] [lesson_25.py](file:///Users/lkx007/develop/workspace/ai_course/course/lesson_25.py)

1. **定义文字显示位置**：在屏幕上方（例如 `(0, 250)`）增加一个专门用于显示状态的 Turtle 对象或在 `draw_fan` 中通过主 Turtle 写入。
2. **逻辑调整**：
   - 计算当前转数：`current_rotations = int(angle // 360)`
   - 在循环中更新文字：使用 `t.write(f"当前旋转：{current_rotations} / 总计：{rotations}", align="center", font=("Arial", 16, "bold"))`。
3. **性能优化**：为了避免文字抖动或重叠，确保在 `turtle.update()` 之前清除旧文字或将文字更新逻辑整合进 `draw_fan` 的 `t.clear()` 范围内。

## 验证计划
1. 运行 `python3 course/lesson_25.py`。
2. 观察动画窗口，确认顶部是否实时显示类似“当前旋转：3 / 总计：10”的字样。
3. 确认数字随风扇转动准确递增，直到 10 / 10。
