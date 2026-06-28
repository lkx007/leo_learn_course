# Scratch 参考答案 (.sb3)

每课一个参考答案工程，用 **Scratch 桌面版（Mac）** 打开：

1. 打开 Scratch 桌面应用
2. **文件 → 从电脑中上传**（Load from your computer）
3. 选择对应的 `.sb3` 文件

## 重新生成

修改了 `build_scratch_sb3.py` 里的课程逻辑后：

```bash
python3 build_scratch_sb3.py              # 生成到本目录
python3 build_scratch_sb3.py --copy-docs    # 并复制到 docs/scratch_answers/（GitHub Pages）
```

或在构建网站时自动执行：

```bash
python3 build_html.py --pages
```

## 说明

- 文件由 `build_scratch_sb3.py` 自动生成，覆盖每课核心积木逻辑
- 打开后请点 **绿旗** 运行；若舞台左上角有变量监视器（高度/天数/井深），说明加载正常
- 复杂游戏课（第 21–24 课、飞机大战等）为**简化参考版**，可在 Scratch 里继续扩展
- 建议：先让孩子自己做，卡住时再打开参考答案对照
