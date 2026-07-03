import pygame
import random
import os

pygame.init()

# -----------------------------
# SETTINGS
# -----------------------------
WIDTH, HEIGHT = 1100, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Instructors vs Campers")

clock = pygame.time.Clock()
FPS = 60

ROWS = 5
COLS = 9
CELL_SIZE = 90
GRID_X = 180
GRID_Y = 120

# -----------------------------
# THEME COLORS
# mostly dark grey / white / lime, with optional accent colors
# -----------------------------
BACKGROUND = (24, 25, 28)       # main background
PANEL = (36, 38, 43)            # sidebar / cards
PANEL_DARK = (28, 30, 34)
CELL_LIGHT = (54, 57, 63)       # grid tiles
CELL_DARK = (45, 48, 53)
GRID = (82, 86, 94)             # subtle grid borders
TEXT = (245, 247, 250)
TEXT_DIM = (165, 171, 180)
BLACK = (8, 10, 12)
WHITE = (245, 247, 250)

LIME = (147, 255, 66)           # main highlight
LIME_DARK = (94, 205, 55)
LIME_SOFT = (197, 255, 166)

# Accent colors for individual instructors/enemies/projectiles
RED = (255, 88, 88)
YELLOW = (255, 215, 86)
GREEN = (88, 235, 145)
BLUE = (90, 170, 255)
CYAN = (91, 225, 230)
PURPLE = (185, 125, 255)
ORANGE = (255, 165, 80)
PINK = (255, 135, 190)
BROWN = (175, 128, 80)
GRAY = (150, 155, 165)

font = pygame.font.SysFont(None, 32)
small_font = pygame.font.SysFont(None, 23)
tiny_font = pygame.font.SysFont(None, 18)

# -----------------------------
# IMAGE LOADING
# -----------------------------
ASSET_FOLDER = "assets"
INSTRUCTOR_FOLDER = "assets/instructors"
INSTRUCTOR_SPRITE_SIZE = (70, 70)

def load_image_from_folder(folder, filename, size):
    if filename is None:
        return None

    path = os.path.join(folder, filename)

    if os.path.exists(path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)

    print(f"Missing sprite: {path}")
    return None

def load_image(filename, size):
    path = os.path.join("assets", filename)

    if os.path.exists(path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)

    return None

def add_sprites_to_instructors():
    for name in INSTRUCTORS:
        filename = INSTRUCTORS[name]["sprite_file"]
        INSTRUCTORS[name]["sprite"] = load_image(filename, INSTRUCTOR_SPRITE_SIZE)

# -----------------------------
# CUSTOMIZE THESE!
# -----------------------------
INSTRUCTORS = {
    "Blossom": {
        "cost": 50,
        "damage": 20,
        "cooldown": 80,
        "color": RED,
        "sprite_file": "blossom.png",
        "projectile_color": RED
    },
    "Cam": {
        "cost": 100,
        "damage": 45,
        "cooldown": 140,
        "color": RED,
        "sprite_file": "cam.png",
        "projectile_color": RED
    },
    "Ed-E": {
        "cost": 75,
        "damage": 12,
        "cooldown": 40,
        "color": RED,
        "sprite_file": "ed-e.png",
        "projectile_color": RED
    },
    "Gizmo": {
        "cost": 90,
        "damage": 28,
        "cooldown": 95,
        "color": RED,
        "sprite_file": "gizmo.png",
        "projectile_color": RED
    },
    "Hippo": {
        "cost": 80,
        "damage": 18,
        "cooldown": 60,
        "color": RED,
        "sprite_file": "hippo.png",
        "projectile_color": RED
    },
    "Mr-Loop": {
        "cost": 70,
        "damage": 16,
        "cooldown": 55,
        "color": RED,
        "sprite_file": "mr-loop.png",
        "projectile_color": RED
    },
    "Red": {
        "cost": 85,
        "damage": 32,
        "cooldown": 110,
        "color": RED,
        "sprite_file": "red.png",
        "projectile_color": RED
    },
    "Ring": {
        "cost": 60,
        "damage": 10,
        "cooldown": 35,
        "color": RED,
        "sprite_file": "ring.png",
        "projectile_color": RED
    },
    "Wall-E": {
        "cost": 125,
        "damage": 55,
        "cooldown": 155,
        "color": RED,
        "sprite_file": "wall-e.png",
        "projectile_color": RED
    },
    "Zevo": {
        "cost": 40,
        "damage": 8,
        "cooldown": 45,
        "color": RED,
        "sprite_file": "zevo.png",
        "projectile_color": RED
    }
}

def load_instructor_sprites():
    for name in INSTRUCTORS:
        sprite_file = INSTRUCTORS[name]["sprite_file"]
        INSTRUCTORS[name]["sprite"] = load_image_from_folder(
            INSTRUCTOR_FOLDER,
            sprite_file,
            INSTRUCTOR_SPRITE_SIZE
        )

load_instructor_sprites()
INSTRUCTOR_NAMES = list(INSTRUCTORS.keys())

ENEMY_TYPES = [
    {
        "name": "Camper",
        "health": 100,
        "speed": 0.45,
        "color": YELLOW,
        "sprite": load_image("camper.png", (70, 70))
    },
    {
        "name": "Sugar Rush",
        "health": 70,
        "speed": 0.85,
        "color": YELLOW,
        "sprite": load_image("fast_camper.png", (70, 70))
    },
    {
        "name": "Minecraft Kid",
        "health": 220,
        "speed": 0.25,
        "color": YELLOW,
        "sprite": load_image("tank_camper.png", (70, 70))
    },
    {
        "name": "Bug Reporter",
        "health": 130,
        "speed": 0.38,
        "color": YELLOW,
        "sprite": load_image("bug_camper.png", (70, 70))
    }
]

CAFFEINE_ITEMS = [
    {
        "name": "Coffee",
        "value": 25,
        "emoji": "C",
        "color": LIME,
        "sprite": load_image("coffee.png", (42, 42))
    },
    {
        "name": "Monster",
        "value": 40,
        "emoji": "M",
        "color": GREEN,
        "sprite": load_image("monster.png", (42, 42))
    },
    {
        "name": "Red Bull",
        "value": 35,
        "emoji": "R",
        "color": BLUE,
        "sprite": load_image("redbull.png", (42, 42))
    },
    {
        "name": "Diet Coke",
        "value": 20,
        "emoji": "D",
        "color": RED,
        "sprite": load_image("diet_coke.png", (42, 42))
    },
    {
        "name": "Tea",
        "value": 15,
        "emoji": "T",
        "color": CYAN,
        "sprite": load_image("tea.png", (42, 42))
    }
]

# -----------------------------
# GAME STATE
# -----------------------------
caffeine = 100
selected_instructor_index = 0
selected_instructor = INSTRUCTOR_NAMES[selected_instructor_index]

instructors = []
enemies = []
projectiles = []
caffeine_drops = []
floating_texts = []

spawn_timer = 0
caffeine_timer = 0
wave_timer = 0

game_over = False
win = False

game_length_seconds = 180
start_ticks = pygame.time.get_ticks()


# -----------------------------
# FUNCTIONS
# -----------------------------
def draw_text(text, x, y, color=BLACK, use_small=False, use_tiny=False):
    if use_tiny:
        f = tiny_font
    elif use_small:
        f = small_font
    else:
        f = font

    img = f.render(text, True, color)
    screen.blit(img, (x, y))


def cell_to_pixel(row, col):
    x = GRID_X + col * CELL_SIZE + CELL_SIZE // 2
    y = GRID_Y + row * CELL_SIZE + CELL_SIZE // 2
    return x, y


def grid_position_from_mouse(pos):
    mx, my = pos
    col = (mx - GRID_X) // CELL_SIZE
    row = (my - GRID_Y) // CELL_SIZE

    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col

    return None, None


def spot_taken(row, col):
    for plant in instructors:
        if plant["row"] == row and plant["col"] == col:
            return True
    return False


def place_instructor(row, col):
    global caffeine

    data = INSTRUCTORS[selected_instructor]

    if caffeine >= data["cost"] and not spot_taken(row, col):
        x, y = cell_to_pixel(row, col)

        instructors.append({
            "type": selected_instructor,
            "row": row,
            "col": col,
            "x": x,
            "y": y,
            "cooldown_timer": random.randint(0, data["cooldown"])
        })

        caffeine -= data["cost"]


def spawn_enemy():
    enemy_data = random.choice(ENEMY_TYPES)
    row = random.randint(0, ROWS - 1)
    x = WIDTH + 50
    y = GRID_Y + row * CELL_SIZE + CELL_SIZE // 2

    enemies.append({
        "name": enemy_data["name"],
        "row": row,
        "x": x,
        "y": y,
        "health": enemy_data["health"],
        "max_health": enemy_data["health"],
        "speed": enemy_data["speed"],
        "color": enemy_data["color"],
        "sprite": enemy_data["sprite"]
    })


def spawn_caffeine():
    item = random.choice(CAFFEINE_ITEMS)
    row = random.randint(0, ROWS - 1)
    col = random.randint(0, COLS - 1)
    x, y = cell_to_pixel(row, col)

    caffeine_drops.append({
        "x": x,
        "y": y,
        "value": item["value"],
        "name": item["name"],
        "emoji": item["emoji"],
        "color": item["color"],
        "sprite": item["sprite"],
        "life": 500
    })


def enemy_in_row(row, x):
    for enemy in enemies:
        if enemy["row"] == row and enemy["x"] > x:
            return True
    return False


def update_instructors():
    for plant in instructors:
        data = INSTRUCTORS[plant["type"]]
        plant["cooldown_timer"] -= 1

        if plant["cooldown_timer"] <= 0 and enemy_in_row(plant["row"], plant["x"]):
            projectiles.append({
                "x": plant["x"] + 30,
                "y": plant["y"],
                "row": plant["row"],
                "speed": 6,
                "damage": data["damage"],
                "color": data["projectile_color"]
            })

            plant["cooldown_timer"] = data["cooldown"]


def update_projectiles():
    for proj in projectiles[:]:
        proj["x"] += proj["speed"]

        if proj["x"] > WIDTH:
            projectiles.remove(proj)
            continue

        for enemy in enemies[:]:
            if enemy["row"] == proj["row"]:
                if abs(proj["x"] - enemy["x"]) < 30 and abs(proj["y"] - enemy["y"]) < 40:
                    enemy["health"] -= proj["damage"]

                    if proj in projectiles:
                        projectiles.remove(proj)

                    if enemy["health"] <= 0:
                        enemies.remove(enemy)

                    break


def update_enemies():
    global game_over

    for enemy in enemies:
        enemy["x"] -= enemy["speed"]

        if enemy["x"] < GRID_X - 80:
            game_over = True


def update_caffeine_drops():
    for drop in caffeine_drops[:]:
        drop["life"] -= 1

        if drop["life"] <= 0:
            caffeine_drops.remove(drop)


def update_floating_texts():
    for text in floating_texts[:]:
        text["y"] -= 0.6
        text["life"] -= 1

        if text["life"] <= 0:
            floating_texts.remove(text)


def collect_caffeine(pos):
    global caffeine

    mx, my = pos

    for drop in caffeine_drops[:]:
        distance = ((mx - drop["x"]) ** 2 + (my - drop["y"]) ** 2) ** 0.5

        if distance < 35:
            caffeine += drop["value"]

            floating_texts.append({
                "text": f"{drop['name']} +{drop['value']}",
                "x": drop["x"] - 35,
                "y": drop["y"] - 40,
                "life": 60
            })

            caffeine_drops.remove(drop)


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(
                GRID_X + col * CELL_SIZE,
                GRID_Y + row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            color = CELL_LIGHT if (row + col) % 2 == 0 else CELL_DARK
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID, rect, 1)


def draw_sidebar():
    pygame.draw.rect(screen, PANEL, (0, 0, 170, HEIGHT))

    draw_text(f"⚡ CAFFEINE: {caffeine}", 15, 18, LIME)

    y = 60

    for i, name in enumerate(INSTRUCTOR_NAMES):
        data = INSTRUCTORS[name]

        rect = pygame.Rect(12, y, 145, 48)

        if selected_instructor == name:
            pygame.draw.rect(screen, LIME, rect)
            pygame.draw.rect(screen, LIME_SOFT, rect, 2)
            name_color = BLACK
            cost_color = BLACK
        else:
            pygame.draw.rect(screen, PANEL_DARK, rect)
            pygame.draw.rect(screen, GRID, rect, 1)
            name_color = TEXT
            cost_color = TEXT_DIM

        draw_text(f"{i + 1}. {name}", 20, y + 7, name_color, use_tiny=True)
        draw_text(f"{data['cost']} caffeine", 20, y + 25, cost_color, use_tiny=True)

        y += 55

    draw_text("Keys 1-0 select", 18, HEIGHT - 60, TEXT_DIM, use_small=True)
    draw_text("Click grid to place", 18, HEIGHT - 35, TEXT_DIM, use_small=True)


def draw_instructors():
    for plant in instructors:
        data = INSTRUCTORS[plant["type"]]

        if data["sprite"]:
            rect = data["sprite"].get_rect(center=(plant["x"], plant["y"]))
            screen.blit(data["sprite"], rect)
        else:
            pygame.draw.circle(screen, data["color"], (plant["x"], plant["y"]), 32)
            draw_text(plant["type"][0], plant["x"] - 8, plant["y"] - 12, TEXT)


def draw_enemies():
    for enemy in enemies:
        if enemy["sprite"]:
            rect = enemy["sprite"].get_rect(center=(int(enemy["x"]), int(enemy["y"])))
            screen.blit(enemy["sprite"], rect)
        else:
            pygame.draw.circle(screen, enemy["color"], (int(enemy["x"]), int(enemy["y"])), 32)

        bar_width = 60
        health_ratio = max(0, enemy["health"] / enemy["max_health"])

        pygame.draw.rect(screen, PANEL_DARK, (enemy["x"] - 30, enemy["y"] - 48, bar_width, 8))
        pygame.draw.rect(screen, LIME, (enemy["x"] - 30, enemy["y"] - 48, bar_width * health_ratio, 8))
        pygame.draw.rect(screen, GRID, (enemy["x"] - 30, enemy["y"] - 48, bar_width, 8), 1)

        draw_text(enemy["name"], enemy["x"] - 35, enemy["y"] + 35, TEXT, use_tiny=True)


def draw_projectiles():
    for proj in projectiles:
        pygame.draw.circle(screen, proj["color"], (int(proj["x"]), int(proj["y"])), 8)
        pygame.draw.circle(screen, WHITE, (int(proj["x"]), int(proj["y"])), 3)


def draw_caffeine():
    for drop in caffeine_drops:
        if drop["sprite"]:
            rect = drop["sprite"].get_rect(center=(drop["x"], drop["y"]))
            screen.blit(drop["sprite"], rect)
        else:
            pygame.draw.circle(screen, LIME, (drop["x"], drop["y"]), 23)
            pygame.draw.circle(screen, PANEL_DARK, (drop["x"], drop["y"]), 17)
            draw_text(drop["emoji"], drop["x"] - 6, drop["y"] - 8, LIME, use_small=True)


def draw_floating_texts():
    for text in floating_texts:
        draw_text(text["text"], text["x"], text["y"], LIME, use_tiny=True)


def draw_timer():
    elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining = max(0, game_length_seconds - elapsed)

    draw_text(f"TIME: {remaining}", 900, 20, TEXT)

    return remaining


def draw_game_over():
    screen.fill(BACKGROUND)

    if win:
        draw_text("YOU WIN! Parent Showcase survived!", 340, 280, LIME)
    else:
        draw_text("GAME OVER! The campers reached the lab!", 330, 280, TEXT)

    draw_text("Press R to restart", 440, 330, TEXT_DIM)


def restart_game():
    global caffeine, selected_instructor_index, selected_instructor
    global instructors, enemies, projectiles, caffeine_drops, floating_texts
    global spawn_timer, caffeine_timer, wave_timer
    global game_over, win, start_ticks

    caffeine = 100
    selected_instructor_index = 0
    selected_instructor = INSTRUCTOR_NAMES[selected_instructor_index]

    instructors = []
    enemies = []
    projectiles = []
    caffeine_drops = []
    floating_texts = []

    spawn_timer = 0
    caffeine_timer = 0
    wave_timer = 0

    game_over = False
    win = False
    start_ticks = pygame.time.get_ticks()


def select_instructor_by_key(key):
    global selected_instructor_index, selected_instructor

    key_map = {
        pygame.K_1: 0,
        pygame.K_2: 1,
        pygame.K_3: 2,
        pygame.K_4: 3,
        pygame.K_5: 4,
        pygame.K_6: 5,
        pygame.K_7: 6,
        pygame.K_8: 7,
        pygame.K_9: 8,
        pygame.K_0: 9
    }

    if key in key_map:
        selected_instructor_index = key_map[key]
        selected_instructor = INSTRUCTOR_NAMES[selected_instructor_index]


# -----------------------------
# MAIN GAME LOOP
# -----------------------------
running = True

while running:
    clock.tick(FPS)
    screen.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            select_instructor_by_key(event.key)

            if event.key == pygame.K_r and game_over:
                restart_game()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mx, my = pygame.mouse.get_pos()

            # Click sidebar buttons
            y = 60
            for i, name in enumerate(INSTRUCTOR_NAMES):
                button = pygame.Rect(12, y, 145, 48)

                if button.collidepoint(mx, my):
                    selected_instructor_index = i
                    selected_instructor = name

                y += 55

            # Click caffeine pickup
            collect_caffeine((mx, my))

            # Click grid to place instructor
            row, col = grid_position_from_mouse((mx, my))

            if row is not None:
                place_instructor(row, col)

    if not game_over:
        spawn_timer += 1
        caffeine_timer += 1
        wave_timer += 1

        spawn_rate = max(45, 160 - wave_timer // 600)

        if spawn_timer >= spawn_rate:
            spawn_enemy()
            spawn_timer = 0

        if caffeine_timer >= 150:
            spawn_caffeine()
            caffeine_timer = 0

        update_instructors()
        update_projectiles()
        update_enemies()
        update_caffeine_drops()
        update_floating_texts()

        draw_grid()
        draw_sidebar()
        draw_instructors()
        draw_enemies()
        draw_projectiles()
        draw_caffeine()
        draw_floating_texts()

        remaining = draw_timer()

        if remaining <= 0:
            game_over = True
            win = True

    else:
        draw_game_over()

    pygame.display.flip()

pygame.quit()