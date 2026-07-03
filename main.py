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

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (120, 200, 120)
DARK_GREEN = (70, 150, 70)
BROWN = (160, 110, 60)
RED = (220, 70, 70)
BLUE = (70, 130, 220)
YELLOW = (240, 220, 80)
GRAY = (180, 180, 180)
PURPLE = (160, 90, 220)
ORANGE = (240, 150, 60)
PINK = (240, 130, 180)
CYAN = (80, 210, 220)

font = pygame.font.SysFont(None, 32)
small_font = pygame.font.SysFont(None, 23)
tiny_font = pygame.font.SysFont(None, 18)

# -----------------------------
# IMAGE LOADING
# -----------------------------
def load_image(filename, size):
    path = os.path.join("assets", filename)

    if os.path.exists(path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)

    return None


# -----------------------------
# CUSTOMIZE THESE!
# -----------------------------
INSTRUCTORS = {
    "Python": {
        "cost": 50,
        "damage": 20,
        "cooldown": 80,
        "color": BLUE,
        "sprite": load_image("python_teacher.png", (70, 70)),
        "projectile_color": YELLOW
    },
    "Robotics": {
        "cost": 100,
        "damage": 45,
        "cooldown": 140,
        "color": GRAY,
        "sprite": load_image("robotics_teacher.png", (70, 70)),
        "projectile_color": RED
    },
    "GameDev": {
        "cost": 75,
        "damage": 12,
        "cooldown": 40,
        "color": GREEN,
        "sprite": load_image("gamedev_teacher.png", (70, 70)),
        "projectile_color": WHITE
    },
    "Physics": {
        "cost": 90,
        "damage": 28,
        "cooldown": 95,
        "color": PURPLE,
        "sprite": load_image("physics_teacher.png", (70, 70)),
        "projectile_color": CYAN
    },
    "Minecraft": {
        "cost": 80,
        "damage": 18,
        "cooldown": 60,
        "color": BROWN,
        "sprite": load_image("minecraft_teacher.png", (70, 70)),
        "projectile_color": ORANGE
    },
    "Video": {
        "cost": 70,
        "damage": 16,
        "cooldown": 55,
        "color": PINK,
        "sprite": load_image("video_teacher.png", (70, 70)),
        "projectile_color": WHITE
    },
    "Math": {
        "cost": 85,
        "damage": 32,
        "cooldown": 110,
        "color": CYAN,
        "sprite": load_image("math_teacher.png", (70, 70)),
        "projectile_color": BLUE
    },
    "Art": {
        "cost": 60,
        "damage": 10,
        "cooldown": 35,
        "color": ORANGE,
        "sprite": load_image("art_teacher.png", (70, 70)),
        "projectile_color": PINK
    },
    "Director": {
        "cost": 125,
        "damage": 55,
        "cooldown": 155,
        "color": RED,
        "sprite": load_image("director.png", (70, 70)),
        "projectile_color": PURPLE
    },
    "Counselor": {
        "cost": 40,
        "damage": 8,
        "cooldown": 45,
        "color": YELLOW,
        "sprite": load_image("counselor.png", (70, 70)),
        "projectile_color": GREEN
    }
}

INSTRUCTOR_NAMES = list(INSTRUCTORS.keys())

ENEMY_TYPES = [
    {
        "name": "Camper",
        "health": 100,
        "speed": 0.45,
        "color": RED,
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
        "color": BROWN,
        "sprite": load_image("tank_camper.png", (70, 70))
    },
    {
        "name": "Bug Reporter",
        "health": 130,
        "speed": 0.38,
        "color": PURPLE,
        "sprite": load_image("bug_camper.png", (70, 70))
    }
]

CAFFEINE_ITEMS = [
    {
        "name": "Coffee",
        "value": 25,
        "emoji": "C",
        "color": BROWN,
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

            color = GREEN if (row + col) % 2 == 0 else DARK_GREEN
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)


def draw_sidebar():
    pygame.draw.rect(screen, (230, 230, 210), (0, 0, 170, HEIGHT))

    draw_text(f"Caffeine: {caffeine}", 15, 18)

    y = 60

    for i, name in enumerate(INSTRUCTOR_NAMES):
        data = INSTRUCTORS[name]

        rect = pygame.Rect(12, y, 145, 48)

        if selected_instructor == name:
            pygame.draw.rect(screen, YELLOW, rect)
        else:
            pygame.draw.rect(screen, WHITE, rect)

        pygame.draw.rect(screen, BLACK, rect, 2)

        draw_text(f"{i + 1}. {name}", 20, y + 7, BLACK, use_tiny=True)
        draw_text(f"{data['cost']} caffeine", 20, y + 25, BLACK, use_tiny=True)

        y += 55

    draw_text("Keys 1-0 select", 18, HEIGHT - 60, BLACK, use_small=True)
    draw_text("Click grid to place", 18, HEIGHT - 35, BLACK, use_small=True)


def draw_instructors():
    for plant in instructors:
        data = INSTRUCTORS[plant["type"]]

        if data["sprite"]:
            rect = data["sprite"].get_rect(center=(plant["x"], plant["y"]))
            screen.blit(data["sprite"], rect)
        else:
            pygame.draw.circle(screen, data["color"], (plant["x"], plant["y"]), 32)
            draw_text(plant["type"][0], plant["x"] - 8, plant["y"] - 12, BLACK)


def draw_enemies():
    for enemy in enemies:
        if enemy["sprite"]:
            rect = enemy["sprite"].get_rect(center=(int(enemy["x"]), int(enemy["y"])))
            screen.blit(enemy["sprite"], rect)
        else:
            pygame.draw.circle(screen, enemy["color"], (int(enemy["x"]), int(enemy["y"])), 32)

        bar_width = 60
        health_ratio = max(0, enemy["health"] / enemy["max_health"])

        pygame.draw.rect(screen, RED, (enemy["x"] - 30, enemy["y"] - 48, bar_width, 8))
        pygame.draw.rect(screen, GREEN, (enemy["x"] - 30, enemy["y"] - 48, bar_width * health_ratio, 8))

        draw_text(enemy["name"], enemy["x"] - 35, enemy["y"] + 35, BLACK, use_tiny=True)


def draw_projectiles():
    for proj in projectiles:
        pygame.draw.circle(screen, proj["color"], (int(proj["x"]), int(proj["y"])), 8)


def draw_caffeine():
    for drop in caffeine_drops:
        if drop["sprite"]:
            rect = drop["sprite"].get_rect(center=(drop["x"], drop["y"]))
            screen.blit(drop["sprite"], rect)
        else:
            pygame.draw.circle(screen, drop["color"], (drop["x"], drop["y"]), 22)
            draw_text(drop["emoji"], drop["x"] - 6, drop["y"] - 8, BLACK, use_small=True)


def draw_floating_texts():
    for text in floating_texts:
        draw_text(text["text"], text["x"], text["y"], BLACK, use_tiny=True)


def draw_timer():
    elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining = max(0, game_length_seconds - elapsed)

    draw_text(f"Time: {remaining}", 900, 20)

    return remaining


def draw_game_over():
    screen.fill(BLACK)

    if win:
        draw_text("YOU WIN! Parent Showcase survived!", 340, 280, WHITE)
    else:
        draw_text("GAME OVER! The campers reached the lab!", 330, 280, WHITE)

    draw_text("Press R to restart", 440, 330, WHITE)


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
    screen.fill(WHITE)

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

        if caffeine_timer >= 280:
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