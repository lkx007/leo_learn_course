# 90坦克大战 🎮
# 经典红白机坦克游戏的 Python 复刻版
# 操作：方向键或 WASD 移动，空格发射，R 重新开始

import os
import random
import subprocess
import sys
import threading

# 减少 macOS 上 pygame 的 IMK / mach port 控制台报错
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
os.environ.setdefault("SDL_IM_MODULE", "dummy")

import pygame

# --- 像素风渲染（经典红白机 16x16 精灵，2倍放大）---
PT = 16
SCALE = 2
TILE = PT * SCALE
COLS = 13
ROWS = 13
HUD = 48
GAME_W = COLS * PT
GAME_H = ROWS * PT
WIDTH = COLS * TILE
HEIGHT = ROWS * TILE + HUD
FPS = 60

# 方向
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
DIR_DELTA = {
    UP: (0, -1),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    RIGHT: (1, 0),
}

MOVE_KEY_CODES = {
    pygame.K_UP,
    pygame.K_DOWN,
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_w,
    pygame.K_a,
    pygame.K_s,
    pygame.K_d,
}


def get_move_keys_down(keys_down):
    """方向键与 WASD 任意一组按下即可（或关系）"""
    if pygame.K_UP in keys_down or pygame.K_w in keys_down:
        return UP
    if pygame.K_DOWN in keys_down or pygame.K_s in keys_down:
        return DOWN
    if pygame.K_LEFT in keys_down or pygame.K_a in keys_down:
        return LEFT
    if pygame.K_RIGHT in keys_down or pygame.K_d in keys_down:
        return RIGHT
    return None


# NES 坦克大战配色（贴近原版 Battle City）
PAL = {
    "O": (216, 96, 0),
    "o": (136, 56, 0),
    "S": (192, 192, 192),
    "s": (112, 112, 112),
    "W": (252, 252, 252),
    "G": (0, 184, 0),
    "g": (0, 112, 0),
    "V": (32, 88, 216),
    "v": (248, 248, 248),
    "Y": (248, 216, 0),
    "y": (184, 152, 0),
    "R": (248, 88, 0),
    "r": (168, 56, 0),
    "E": (216, 216, 216),
    "e": (136, 136, 136),
    "L": (0, 168, 72),
    "l": (0, 104, 48),
    "K": (0, 0, 0),
    "A": (192, 192, 192),
    "a": (112, 112, 112),
    "X": (248, 56, 0),
    "x": (128, 32, 0),
    "P": (252, 252, 252),
    "M": (248, 216, 0),
    "m": (168, 136, 0),
    "C": (0, 168, 0),
    "c": (0, 104, 0),
    "F": (248, 88, 0),
    "f": (168, 56, 0),
    "H": (248, 216, 0),
    "h": (168, 136, 0),
    "1": (248, 216, 0),
    "2": (248, 88, 0),
    "3": (216, 216, 216),
    "4": (0, 168, 72),
}

C_BG = (0, 0, 0)
C_BULLET = (252, 252, 252)
C_HUD = (0, 0, 0)
C_HUD_BORDER = (116, 116, 116)
C_TEXT = (252, 252, 252)
C_TEXT_DIM = (188, 188, 188)
C_GREEN = (0, 168, 0)
C_RED = (248, 56, 0)

ENEMY_PALS = [
    {"Y": "R", "y": "r"},
    {"Y": "E", "y": "e"},
    {"Y": "L", "y": "l"},
]

# --- 地图块（16x16 经典贴图）---
SPR_BRICK = (
    "OOOOooooOOOOoooo",
    "OOOOooooOOOOoooo",
    "ooOOOOooooOOOOoo",
    "ooOOOOooooOOOOoo",
    "OOOOooooOOOOoooo",
    "OOOOooooOOOOoooo",
    "ooOOOOooooOOOOoo",
    "ooOOOOooooOOOOoo",
    "OOOOooooOOOOoooo",
    "OOOOooooOOOOoooo",
    "ooOOOOooooOOOOoo",
    "ooOOOOooooOOOOoo",
    "OOOOooooOOOOoooo",
    "OOOOooooOOOOoooo",
    "ooOOOOooooOOOOoo",
    "ooOOOOooooOOOOoo",
)

SPR_STEEL = (
    "WWSSSSSSSSSSSSWW",
    "WssSSSSSSSSSSssW",
    "SsWWSSSSSSSSWWsS",
    "SSssSSSSSSSSssSS",
    "SSSSWWSSSSWWSSSS",
    "SSSSssSSSSssSSSS",
    "SSSSSSWWSSWWSSSS",
    "SSSSSSssSSssSSSS",
    "SSSSSSWWSSWWSSSS",
    "SSSSSSssSSssSSSS",
    "SSSSWWSSSSWWSSSS",
    "SSSSssSSSSssSSSS",
    "SsWWSSSSSSSSWWsS",
    "SSssSSSSSSSSssSS",
    "WssSSSSSSSSSSssW",
    "WWSSSSSSSSSSSSWW",
)

SPR_GRASS = (
    "...gGGg.........",
    "..gGGGGg........",
    ".gGGGGGGg.......",
    "..gGGGGg........",
    "....gGGg........",
    ".....gGGg.......",
    "....gGGGGg......",
    "...gGGGGGGg.....",
    "...gGGGGGGg.....",
    "....gGGGGg......",
    ".....gGGg.......",
    ".......gGGg.....",
    "......gGGGGg....",
    ".....gGGGGGGg...",
    "......gGGGGg....",
    ".......gGGg.....",
)

SPR_WATER = (
    "VVVVVVVVVVVVVVVV",
    "vvvvvvvvvvvvvvvv",
    "VVVVVVVVVVVVVVVV",
    "..vvvv....vvvv..",
    "VVVVVVVVVVVVVVVV",
    "vvvvvvvvvvvvvvvv",
    "VVVVVVVVVVVVVVVV",
    "..vvvv....vvvv..",
    "VVVVVVVVVVVVVVVV",
    "vvvvvvvvvvvvvvvv",
    "VVVVVVVVVVVVVVVV",
    "..vvvv....vvvv..",
    "VVVVVVVVVVVVVVVV",
    "vvvvvvvvvvvvvvvv",
    "VVVVVVVVVVVVVVVV",
    "..vvvv....vvvv..",
)

SPR_EAGLE = (
    ".......aa.......",
    "......aAAa......",
    ".....aAAAAa.....",
    "....aAaAAaAa....",
    "...aAAAAAAAAa...",
    "..aAaAAAAAAaAa..",
    "..aAAAAAAAAAAa..",
    ".aAaAAaAAaAAaAa.",
    ".aAAAAAAAAAAAAa.",
    "..aAAAAAAAAAAa..",
    "..aAaAAAAAAaAa..",
    "...aAAAAAAAAa...",
    "....aAaAAaAa....",
    ".....aAAAAa.....",
    "......aAAa......",
    ".......aa.......",
)

SPR_EAGLE_DEAD = (
    ".......XX.......",
    "......XxxX......",
    ".....XxxxxX.....",
    "....XxXxxXxX....",
    "...Xxxxxxxxxx...",
    "..XxXxxxxxxXx..",
    "..XxxxxxxxxxxX..",
    ".XxXxxXxxXxxXxX.",
    ".XxxxxxxxxxxxxX.",
    "..XxxxxxxxxxxX..",
    "..XxXxxxxxxXx..",
    "...Xxxxxxxxxx...",
    "....XxXxxXxX....",
    ".....XxxxxX.....",
    "......XxxX......",
    ".......XX.......",
)

# --- 坦克（带履带 + 白色炮管，四方向）---
SPR_TANK_UP = (
    "......PP........",
    "......PP........",
    "...yyYYYYyy.....",
    "..yyYYYYYYyy....",
    ".yyYYYYYYYYyy...",
    ".yyYYYYYYYYyy...",
    "yyYYYYYYYYYYyy..",
    "yyYYYYYYYYYYyy..",
    "yyYYYYYYYYYYyy..",
    "yyYYYYYYYYYYyy..",
    ".yyYYYYYYYYyy...",
    ".yyYYYYYYYYyy...",
    "..yyYYYYYYyy....",
    "...yyYYYYyy.....",
    "...yyYYYYyy.....",
    "...yyYYYYyy.....",
)

SPR_TANK_DOWN = (
    "...yyYYYYyy.....",
    "...yyYYYYyy.....",
    "..yyYYYYYYyy....",
    ".yyYYYYYYYYyy...",
    ".yyYYYYYYYYyy...",
    "yyYYYYYYYYYYyy..",
    "yyYYYYYYYYYYyy..",
    "yyYYYYYYYYYYyy..",
    "yyYYYYYYYYYYyy..",
    ".yyYYYYYYYYyy...",
    ".yyYYYYYYYYyy...",
    "..yyYYYYYYyy....",
    "...yyYYYYyy.....",
    "......PP........",
    "......PP........",
    "......PP........",
)

SPR_TANK_LEFT = (
    "................",
    "PP..............",
    "PP..............",
    "...yyYYYYyy.....",
    "..yyYYYYYYyy....",
    ".yyYYYYYYYYyy...",
    ".yyYYYYYYYYyy...",
    "yyYYYYYYYYYYyy..",
    "yyYYYYYYYYYYyy..",
    "yyYYYYYYYYYYyy..",
    "yyYYYYYYYYYYyy..",
    ".yyYYYYYYYYyy...",
    ".yyYYYYYYYYyy...",
    "..yyYYYYYYyy....",
    "...yyYYYYyy.....",
    "................",
)

SPR_TANK_RIGHT = (
    "................",
    "..............PP",
    "..............PP",
    "...yyYYYYyy.....",
    "..yyYYYYYYyy....",
    ".yyYYYYYYYYyy...",
    ".yyYYYYYYYYyy...",
    "yyYYYYYYYYYYyy..",
    "yyYYYYYYYYYYyy..",
    "yyYYYYYYYYYYyy..",
    "yyYYYYYYYYYYyy..",
    ".yyYYYYYYYYyy...",
    ".yyYYYYYYYYyy...",
    "..yyYYYYYYyy....",
    "...yyYYYYyy.....",
    "................",
)

TANK_SPRITES = {
    UP: SPR_TANK_UP,
    DOWN: SPR_TANK_DOWN,
    LEFT: SPR_TANK_LEFT,
    RIGHT: SPR_TANK_RIGHT,
}

# --- 道具（原版闪烁奖励）---
SPR_POWER_STEEL = (
    "......hh........",
    ".....hHHh.......",
    "....hHmHh.......",
    "...hHmhHh.......",
    "....hHmHh.......",
    ".....hHHh.......",
    "......hh........",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
)

SPR_POWER_ARMOR = (
    ".....cccc.......",
    "....cCCCCc......",
    "...cCCWWCc......",
    "..cCCWWCCc......",
    "...cCCWWCc......",
    "....cCCCCc......",
    ".....cccc.......",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
)

SPR_POWER_LIFE = (
    "................",
    "......ff........",
    ".....FFFF.......",
    "...yyFFFFyy.....",
    "..yyFFFFFFyy....",
    "..yyFFFFFFyy....",
    "...yyFFFFyy.....",
    ".....FFFF.......",
    "......ff........",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
)

POWER_STEEL = "steel"
POWER_ARMOR = "armor"
POWER_LIFE = "life"
POWER_TYPES = [POWER_STEEL, POWER_ARMOR, POWER_LIFE]
POWER_SPRITES = {
    POWER_STEEL: SPR_POWER_STEEL,
    POWER_ARMOR: SPR_POWER_ARMOR,
    POWER_LIFE: SPR_POWER_LIFE,
}
POWER_WEIGHTS = [0.38, 0.35, 0.27]
POWER_BLINK_FRAMES = 10

SPR_BULLET = (
    "..",
    "WW",
)

# 地图图块
EMPTY = 0
BRICK = 1
STEEL = 2
WATER = 3
BASE = 4
GRASS = 5

# 颜色（逻辑层保留，渲染走像素精灵）
C_ENEMY_COLORS = [(248, 56, 0), (180, 180, 180), (0, 168, 0)]

TOTAL_ENEMIES = 6
MAX_LIVES = 3
ENEMY_SPAWN_POINTS = [(1, 1), (6, 1), (11, 1)]
PLAYER_SPAWN = (6, 10)
BASE_POS = (6, 12)

# 老家固定保护圈（每局随机地图也保留）
BASE_WALLS = [
    (5, 11, BRICK), (6, 11, BRICK), (7, 11, BRICK),
    (4, 12, STEEL), (5, 12, BRICK), (6, 12, BASE), (7, 12, BRICK), (8, 12, STEEL),
    (5, 10, STEEL), (7, 10, STEEL),
]


def load_chinese_font(size):
    """加载支持中文的字体（macOS 系统字体路径）"""
    candidates = [
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return pygame.font.Font(path, size)
    return pygame.font.SysFont("arial", size)


def speak(text):
    """屏幕打印 + macOS 语音播报（不阻塞游戏）"""
    print(text)
    clean = text
    for emoji in "🎮 🏆 💥 🛡️ ⭐ 🔫 ":
        clean = clean.replace(emoji, "")

    def _say():
        try:
            subprocess.run(
                ["say", "-r", "160", clean],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        except (OSError, FileNotFoundError):
            pass

    threading.Thread(target=_say, daemon=True).start()


def _protected_cells():
    """出生点、老家附近不参与随机生成"""
    cells = set()
    px, py = PLAYER_SPAWN
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            cells.add((px + dx, py + dy))
    for sx, sy in ENEMY_SPAWN_POINTS:
        for dx in range(-1, 2):
            for dy in range(0, 3):
                cells.add((sx + dx, sy + dy))
    for tx, ty, _ in BASE_WALLS:
        cells.add((tx, ty))
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                cells.add((tx + dx, ty + dy))
    return cells


def generate_random_map():
    """每局随机生成地图，老家保护圈固定"""
    grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
    protected = _protected_cells()

    # 外圈砖墙
    for tx in range(COLS):
        grid[0][tx] = BRICK
        grid[ROWS - 1][tx] = BRICK
    for ty in range(ROWS):
        grid[ty][0] = BRICK
        grid[ty][COLS - 1] = BRICK

    # 老家保护（固定）
    for tx, ty, cell in BASE_WALLS:
        grid[ty][tx] = cell

    # 中间区域随机：草垛 / 砖块 / 铁块
    weights = [
        (EMPTY, 0.52),
        (GRASS, 0.22),
        (BRICK, 0.18),
        (STEEL, 0.08),
    ]

    def pick_cell():
        roll = random.random()
        total = 0.0
        for cell, weight in weights:
            total += weight
            if roll < total:
                return cell
        return EMPTY

    for ty in range(1, ROWS - 1):
        for tx in range(1, COLS - 1):
            if (tx, ty) in protected:
                continue
            if grid[ty][tx] != EMPTY:
                continue
            grid[ty][tx] = pick_cell()

    # 随机撒几簇草垛和砖块掩体，让每局更有变化
    for _ in range(random.randint(3, 6)):
        cx, cy = random.randint(2, COLS - 3), random.randint(2, ROWS - 6)
        cluster = random.choice([GRASS, GRASS, BRICK])
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            tx, ty = cx + dx, cy + dy
            if (tx, ty) not in protected and grid[ty][tx] == EMPTY:
                grid[ty][tx] = cluster

    return grid


def rotate_sprite(sprite, turns):
    """顺时针旋转精灵（0=上 1=右 2=下 3=左）"""
    grid = [list(row.ljust(PT)[:PT]) for row in sprite]
    for _ in range(turns % 4):
        grid = [list(row) for row in zip(*grid[::-1])]
    return ["".join(row) for row in grid]


def map_sprite_chars(sprite, mapping):
    """把精灵里的字符映射到调色板键"""
    out = []
    for row in sprite:
        line = ""
        for ch in row.ljust(PT)[:PT]:
            if ch == ".":
                line += "."
            else:
                line += mapping.get(ch, ch)
        out.append(line)
    return tuple(out)


def blit_sprite(canvas, sprite, px, py, extra_map=None):
    """在像素画布上绘制精灵"""
    for row_i, row in enumerate(sprite):
        for col_i, ch in enumerate(row.ljust(PT)[:PT]):
            if ch == ".":
                continue
            key = ch
            if extra_map and ch in extra_map:
                key = extra_map[ch]
            color = PAL.get(key)
            if color:
                x, y = px + col_i, py + row_i
                if 0 <= x < canvas.get_width() and 0 <= y < canvas.get_height():
                    canvas.set_at((x, y), color)


def screen_to_pixel(x, y):
    """屏幕坐标 -> 像素画布坐标"""
    return int(x // SCALE), int((y - HUD) // SCALE)


def draw_pixel_scene(canvas, grid, tanks, bullets, powerups, base_destroyed, frame, grass_on_top=True):
    """绘制一帧像素场景"""
    canvas.fill(C_BG)

    for ty in range(ROWS):
        for tx in range(COLS):
            cell = grid[ty][tx]
            px, py = tx * PT, ty * PT
            if cell == BRICK:
                blit_sprite(canvas, SPR_BRICK, px, py)
            elif cell == STEEL:
                blit_sprite(canvas, SPR_STEEL, px, py)
            elif cell == WATER:
                blit_sprite(canvas, SPR_WATER, px, py)
            elif cell == BASE:
                if base_destroyed[0]:
                    blit_sprite(canvas, SPR_EAGLE_DEAD, px, py)
                else:
                    blit_sprite(canvas, SPR_EAGLE, px, py)
            elif cell == GRASS and not grass_on_top:
                blit_sprite(canvas, SPR_GRASS, px, py)

    for power in powerups:
        power.draw_pixel(canvas, frame)

    for tank in tanks:
        tank.draw_pixel(canvas)

    for bullet in bullets:
        if bullet.alive:
            bullet.draw_pixel(canvas)

    if grass_on_top:
        for ty in range(ROWS):
            for tx in range(COLS):
                if grid[ty][tx] == GRASS:
                    blit_sprite(canvas, SPR_GRASS, tx * PT, ty * PT)


def pick_power_type():
    roll = random.random()
    total = 0.0
    for kind, weight in zip(POWER_TYPES, POWER_WEIGHTS):
        total += weight
        if roll < total:
            return kind
    return POWER_STEEL


def spawn_powerup(grid, tx, ty):
    """在格子位置生成道具（需要可通行）"""
    if not (0 <= tx < COLS and 0 <= ty < ROWS):
        return None
    if grid[ty][tx] not in (EMPTY, GRASS):
        return None
    return PowerUp(tx, ty, pick_power_type())


def apply_powerup(kind, state):
    player = state["player"]
    if kind == POWER_STEEL:
        player.steel_shot = True
        speak("穿甲弹！现在可以打碎铁块了！")
    elif kind == POWER_ARMOR:
        player.armor += 1
        speak("防弹衣！可以多挡一炮！")
    elif kind == POWER_LIFE:
        state["lives"] += 1
        speak("加命！又多一条命！")


class PowerUp:
    """击毁敌军后掉落的奖励道具"""

    def __init__(self, tx, ty, kind):
        self.tx = tx
        self.ty = ty
        self.kind = kind
        self.alive = True

    def rect(self):
        x = self.tx * TILE + 4
        y = self.ty * TILE + HUD + 4
        return pygame.Rect(x, y, TILE - 8, TILE - 8)

    def draw_pixel(self, canvas, frame):
        if not self.alive:
            return
        if (frame // POWER_BLINK_FRAMES) % 2 == 1:
            return
        sprite = POWER_SPRITES[self.kind]
        blit_sprite(canvas, sprite, self.tx * PT + 2, self.ty * PT + 2)


class Bullet:
    """子弹：直线飞行，碰到墙或坦克就消失"""

    def __init__(self, x, y, direction, owner, pierce_steel=False):
        self.x = x
        self.y = y
        self.direction = direction
        self.owner = owner  # "player" 或 "enemy"
        self.pierce_steel = pierce_steel
        self.speed = 6
        self.alive = True
        self.w = 4
        self.h = 4

    def rect(self):
        sx = int(self.x)
        sy = int(self.y)
        return pygame.Rect(sx, sy, self.w, self.h)

    def draw_pixel(self, canvas):
        px, py = screen_to_pixel(self.x, self.y)
        blit_sprite(canvas, SPR_BULLET, px, py)

    def update(self, grid, tanks, base_destroyed):
        if not self.alive:
            return

        dx, dy = DIR_DELTA[self.direction]
        self.x += dx * self.speed
        self.y += dy * self.speed

        r = self.rect()
        if r.left < 0 or r.right > WIDTH or r.top < HUD or r.bottom > HEIGHT:
            self.alive = False
            return

        # 打中地图
        for ty in range(ROWS):
            for tx in range(COLS):
                cell = grid[ty][tx]
                if cell in (EMPTY, WATER, GRASS):
                    continue
                cell_rect = pygame.Rect(tx * TILE, ty * TILE + HUD, TILE, TILE)
                if not r.colliderect(cell_rect):
                    continue
                if cell == BRICK:
                    grid[ty][tx] = EMPTY
                elif cell == STEEL:
                    if self.pierce_steel:
                        grid[ty][tx] = EMPTY
                    self.alive = False
                    return
                elif cell == BASE:
                    grid[ty][tx] = EMPTY
                    base_destroyed[0] = True
                self.alive = False
                return

        # 打中坦克
        for tank in tanks:
            if not tank.alive:
                continue
            if tank.is_player and self.owner == "player":
                continue
            if not tank.is_player and self.owner == "enemy":
                continue
            if tank.is_player and tank.invincible > 0:
                self.alive = False
                return
            if r.colliderect(tank.rect()):
                if tank.is_player and tank.armor > 0:
                    tank.armor -= 1
                    self.alive = False
                    return
                tank.hit()
                self.alive = False
                return


class Tank:
    """坦克：可以移动、转向、发射"""

    def __init__(self, x, y, direction, is_player=False, enemy_type=0):
        self.x = float(x)
        self.y = float(y)
        self.direction = direction
        self.is_player = is_player
        self.enemy_type = enemy_type
        self.alive = True
        self.speed = 2 if is_player else 1.5
        self.size = TILE - 4
        self.shoot_cooldown = 0
        self.move_timer = 0
        self.move_dir = random.choice([UP, DOWN, LEFT, RIGHT])
        self.steel_shot = False
        self.armor = 0
        self.invincible = 0

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def center(self):
        r = self.rect()
        return r.centerx, r.centery

    def hit(self):
        self.alive = False

    def can_pass(self, grid, nx, ny):
        """检查新位置能否通过"""
        test = pygame.Rect(int(nx), int(ny), self.size, self.size)
        for ty in range(ROWS):
            for tx in range(COLS):
                cell = grid[ty][tx]
                if cell in (EMPTY, GRASS):
                    continue
                if cell == WATER:
                    block = pygame.Rect(tx * TILE, ty * TILE + HUD, TILE, TILE)
                    if test.colliderect(block):
                        return False
                elif cell in (BRICK, STEEL, BASE):
                    block = pygame.Rect(tx * TILE, ty * TILE + HUD, TILE, TILE)
                    if test.colliderect(block):
                        return False
        if test.left < 0 or test.right > WIDTH or test.top < HUD or test.bottom > HEIGHT:
            return False
        return True

    def move(self, grid, direction):
        self.direction = direction
        dx, dy = DIR_DELTA[direction]
        nx = self.x + dx * self.speed
        ny = self.y + dy * self.speed
        if self.can_pass(grid, nx, ny):
            self.x, self.y = nx, ny

    def try_shoot(self, bullets):
        if self.shoot_cooldown > 0:
            return
        cx, cy = self.center()
        bx = cx - 3
        by = cy - 3
        owner = "player" if self.is_player else "enemy"
        pierce = self.is_player and self.steel_shot
        bullets.append(Bullet(bx, by, self.direction, owner, pierce_steel=pierce))
        self.shoot_cooldown = 25 if self.is_player else 30

    def update_enemy_ai(self, grid, bullets, player):
        if not self.alive:
            return
        self.shoot_cooldown = max(0, self.shoot_cooldown - 1)
        self.move_timer -= 1

        if self.move_timer <= 0:
            self.move_timer = random.randint(20, 50)
            if player.alive and random.random() < 0.4:
                px, py = player.center()
                cx, cy = self.center()
                if abs(px - cx) > abs(py - cy):
                    self.move_dir = RIGHT if px > cx else LEFT
                else:
                    self.move_dir = DOWN if py > cy else UP
            else:
                self.move_dir = random.choice([UP, DOWN, LEFT, RIGHT])

        old_x, old_y = self.x, self.y
        self.move(grid, self.move_dir)
        if self.x == old_x and self.y == old_y:
            self.move_dir = random.choice([UP, DOWN, LEFT, RIGHT])

        if random.random() < 0.02:
            self.try_shoot(bullets)

    def draw_pixel(self, canvas):
        if not self.alive:
            return
        px, py = screen_to_pixel(self.x, self.y)
        sprite = TANK_SPRITES[self.direction]
        if self.is_player:
            blit_sprite(canvas, sprite, px, py)
        else:
            pal = ENEMY_PALS[self.enemy_type % len(ENEMY_PALS)]
            mapped = map_sprite_chars(sprite, {"Y": pal["Y"], "y": pal["y"], "P": "P"})
            blit_sprite(canvas, mapped, px, py)


def draw_hud(screen, font, lives, score, enemies_left, player, paused):
    pygame.draw.rect(screen, C_HUD, (0, 0, WIDTH, HUD))
    pygame.draw.rect(screen, C_HUD_BORDER, (0, HUD - 2, WIDTH, 2))
    # 像素风装饰条
    for x in range(0, WIDTH, 8):
        pygame.draw.rect(screen, C_HUD_BORDER, (x, 4, 4, 4))
    text = f"生命 {lives}  得分 {score}  敌军 {enemies_left}"
    if player.steel_shot:
        text += "  [穿甲]"
    if player.armor > 0:
        text += f"  [盾{player.armor}]"
    if paused:
        text += "  [P暂停]"
    screen.blit(font.render(text, True, C_TEXT), (8, 8))
    hint = font.render("黄坦=你 红/白/绿=敌  白炮管=方向  R换地图", True, C_TEXT_DIM)
    screen.blit(hint, (8, 28))


def spawn_enemy(grid, tanks, spawn_index):
    sx, sy = ENEMY_SPAWN_POINTS[spawn_index % len(ENEMY_SPAWN_POINTS)]
    x = sx * TILE + 2
    y = sy * TILE + HUD + 2
    test = pygame.Rect(x, y, TILE - 4, TILE - 4)
    for t in tanks:
        if t.alive and test.colliderect(t.rect()):
            return None
    return Tank(x, y, DOWN, is_player=False, enemy_type=spawn_index % len(C_ENEMY_COLORS))


def reset_game():
    grid = generate_random_map()
    base_destroyed = [False]
    px, py = PLAYER_SPAWN
    player = Tank(px * TILE + 2, py * TILE + HUD + 2, UP, is_player=True)
    tanks = [player]
    bullets = []
    powerups = []
    lives = MAX_LIVES
    score = 0
    enemies_spawned = 0
    enemies_left = TOTAL_ENEMIES
    spawn_timer = 120
    spawn_index = 0
    return {
        "grid": grid,
        "base_destroyed": base_destroyed,
        "player": player,
        "tanks": tanks,
        "bullets": bullets,
        "powerups": powerups,
        "lives": lives,
        "score": score,
        "enemies_spawned": enemies_spawned,
        "enemies_left": enemies_left,
        "spawn_timer": spawn_timer,
        "spawn_index": spawn_index,
        "game_over": False,
        "win": False,
        "paused": False,
        "spoken_end": False,
        "frame": 0,
    }


def run_game():
    pygame.init()
    pygame.display.set_caption("90坦克大战 🎮")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = load_chinese_font(14)
    big_font = load_chinese_font(28)
    pixel_canvas = pygame.Surface((GAME_W, GAME_H))

    state = reset_game()
    intro_spoken = False

    keys_down = set()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in MOVE_KEY_CODES:
                    keys_down.add(event.key)
                elif event.key == pygame.K_SPACE:
                    if not state["game_over"] and not state["paused"] and state["player"].alive:
                        state["player"].try_shoot(state["bullets"])
                elif event.key == pygame.K_p:
                    if not state["game_over"]:
                        state["paused"] = not state["paused"]
                elif event.key == pygame.K_r:
                    state = reset_game()
                    speak("🎮 新地图！保护基地，消灭所有敌军！")
            elif event.type == pygame.KEYUP:
                if event.key in MOVE_KEY_CODES:
                    keys_down.discard(event.key)

        if not intro_spoken:
            speak("90坦克大战开始！击毁敌军会掉落道具，星星可以打铁块！")
            intro_spoken = True

        state["frame"] += 1

        if not state["game_over"] and not state["paused"]:
            player = state["player"]
            if player.invincible > 0:
                player.invincible -= 1
            if player.alive:
                player.shoot_cooldown = max(0, player.shoot_cooldown - 1)
                direction = get_move_keys_down(keys_down)
                if direction is not None:
                    player.move(state["grid"], direction)
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    player.try_shoot(state["bullets"])

            for tank in state["tanks"]:
                if not tank.is_player and tank.alive:
                    tank.update_enemy_ai(state["grid"], state["bullets"], player)

            for bullet in state["bullets"]:
                bullet.update(state["grid"], state["tanks"], state["base_destroyed"])

            state["bullets"] = [b for b in state["bullets"] if b.alive]

            # 敌军被消灭 -> 概率掉落道具
            for tank in [t for t in state["tanks"] if not t.is_player and not t.alive]:
                state["score"] += 100
                state["enemies_left"] -= 1
                etx = int(tank.x // TILE)
                ety = int((tank.y - HUD) // TILE)
                if random.random() < 0.45:
                    power = spawn_powerup(state["grid"], etx, ety)
                    if power:
                        state["powerups"].append(power)
                state["tanks"].remove(tank)

            # 拾取道具
            for power in state["powerups"]:
                if not power.alive or not player.alive:
                    continue
                if player.rect().colliderect(power.rect()):
                    apply_powerup(power.kind, state)
                    power.alive = False
            state["powerups"] = [p for p in state["powerups"] if p.alive]

            # 补充敌军
            state["spawn_timer"] -= 1
            alive_enemies = sum(1 for t in state["tanks"] if not t.is_player and t.alive)
            if (
                state["spawn_timer"] <= 0
                and state["enemies_spawned"] < TOTAL_ENEMIES
                and alive_enemies < 3
            ):
                enemy = spawn_enemy(state["grid"], state["tanks"], state["spawn_index"])
                if enemy:
                    state["tanks"].append(enemy)
                    state["enemies_spawned"] += 1
                    state["spawn_index"] += 1
                state["spawn_timer"] = 180

            # 玩家被击中
            if player.alive is False:
                player.steel_shot = False
                player.armor = 0
                state["lives"] -= 1
                if state["lives"] > 0:
                    speak(f"💥 坦克被击中！还剩 {state['lives']} 条命")
                    player.alive = True
                    player.x = PLAYER_SPAWN[0] * TILE + 2
                    player.y = PLAYER_SPAWN[1] * TILE + HUD + 2
                    player.direction = UP
                    player.invincible = 90
                else:
                    state["game_over"] = True

            # 胜负判定（语音只播一次）
            if not state["spoken_end"]:
                if state["base_destroyed"][0]:
                    state["game_over"] = True
                    state["spoken_end"] = True
                    speak("💥 基地被摧毁了！按 R 键再来一次")
                elif state["lives"] <= 0 and not player.alive:
                    state["spoken_end"] = True
                    speak("💥 游戏结束！按 R 键重新开始")
                elif state["enemies_left"] <= 0 and alive_enemies == 0:
                    state["game_over"] = True
                    state["win"] = True
                    state["spoken_end"] = True
                    speak(f"🏆 胜利！你得了 {state['score']} 分！按 R 键继续挑战")

        # --- 绘制（低分辨率像素画布 -> 整数倍放大）---
        screen.fill(C_BG)
        draw_pixel_scene(
            pixel_canvas,
            state["grid"],
            state["tanks"],
            state["bullets"],
            state["powerups"],
            state["base_destroyed"],
            state["frame"],
        )
        scaled = pygame.transform.scale(pixel_canvas, (WIDTH, ROWS * TILE))
        screen.blit(scaled, (0, HUD))
        # 游戏区像素边框
        pygame.draw.rect(screen, C_HUD_BORDER, (0, HUD, WIDTH, ROWS * TILE), 2)
        draw_hud(
            screen,
            font,
            state["lives"],
            state["score"],
            state["enemies_left"],
            state["player"],
            state["paused"],
        )

        if state["game_over"]:
            msg = "胜利!" if state["win"] else "游戏结束"
            color = C_GREEN if state["win"] else C_RED
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            title = big_font.render(msg, True, color)
            sub = font.render("按 R 键重新开始", True, C_TEXT)
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
            screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
        elif state["paused"]:
            pause_text = big_font.render("暂停", True, C_TEXT)
            screen.blit(pause_text, pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_game()
