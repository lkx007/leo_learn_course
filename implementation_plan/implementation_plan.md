# Implementation Plan - Adding Voice Narration to Lessons

This plan describes how to add text-to-speech (TTS) functionality to all existing Python lessons and the typing game, specifically for macOS users.

## User Review Required

> [!IMPORTANT]
> This change depends on the macOS `say` command. It will work natively on Mac but will not provide voice on Windows or Linux unless additional libraries are installed.

## Proposed Changes

### Core Voice Helper
I will define a `speak` function that both prints to the console and speaks the text aloud.

```python
import os

def speak(text):
    print(text)
    # Filter out emojis for smoother speech
    clean_text = text.replace("🖥️ : ", "").replace("👉 ", "").replace("✨ ", "").replace("👋 ", "").replace("🐢 ", "")
    os.system(f"say '{clean_text}'")
```

### 课程 (Lessons)
I will update every `lesson_*.py` file to:
1.  Import `os` (if not already present).
2.  Include the `speak` helper function.
3.  Replace all `print(...)` calls with `speak(...)`.

### Typing Game
#### [MODIFY] [typing_game.py](file:///Users/lkx007/develop/workspace/ai_course/课程/typing_game.py)
- **Difficulty Progression**: Sort the code bank by length.
- **Round-based Scaling**:
    - **Rounds 1-3 (入门级)**: 仅练习 4-12 字符的短代码。
    - **Rounds 4-7 (进阶级)**: 增加到 13-25 字符。
    - **Rounds 8-10 (挑战级)**: 包含更复杂的长代码（25+ 字符）。
- **Feedback**: Add voice and text messages like "进入下一关！" when the difficulty increases.

## Verification Plan

### Automated Tests
- None, requires manual execution.

### Manual Verification
- Run `python3 课程/lesson_04.py` and verify you can hear the computer "speaking" the prompts.
- Run `python3 课程/typing_game.py` and listen for the game overview.
