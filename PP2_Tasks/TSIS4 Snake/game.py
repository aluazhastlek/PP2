import pygame
import random
import json
import os

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = 20
FPS_START = 8

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (60, 60, 60)
RED = (255, 0, 0)
DARK_RED = (120, 0, 0)
ORANGE = (255, 140, 0)
PURPLE = (160, 32, 240)
BLUE = (50, 130, 255)
CYAN = (0, 220, 220)
YELLOW = (255, 230, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 4 Snake")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 16)
big_font = pygame.font.SysFont("Arial", 42)

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "snake_color": [0, 200, 0],
    "grid": True,
    "sound": True
}


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as file:
                return json.load(file)
        except Exception:
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        label = font.render(self.text, True, BLACK)
        screen.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class SnakeGame:
    def __init__(self, username, personal_best, settings):
        self.username = username if username.strip() else "Player"
        self.personal_best = personal_best
        self.settings = settings
        self.snake_color = tuple(settings["snake_color"])
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.dx, self.dy = CELL, 0
        self.score = 0
        self.level = 1
        self.foods_eaten = 0
        self.fps = FPS_START
        self.game_over = False
        self.saved = False
        self.obstacles = set()
        self.food = None
        self.poison = None
        self.powerup = None
        self.active_power = None
        self.power_end = 0
        self.shield = False
        self.last_power_spawn = pygame.time.get_ticks()
        self.food = self.create_food()
        self.poison = self.create_poison()

    def out_of_bounds(self, x, y):
        return x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT

    def random_free_cell(self):
        while True:
            cell = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
            occupied = set(self.snake) | self.obstacles
            if self.food:
                occupied.add(self.food["pos"])
            if self.poison:
                occupied.add(self.poison["pos"])
            if self.powerup:
                occupied.add(self.powerup["pos"])
            if cell not in occupied:
                return cell

    def create_food(self):
        return {
            "pos": self.random_free_cell(),
            "weight": random.choice([1, 2, 3]),
            "ttl": random.choice([4000, 6000, 8000]),
            "spawn_time": pygame.time.get_ticks()
        }

    def create_poison(self):
        return {
            "pos": self.random_free_cell(),
            "ttl": random.choice([6000, 9000, 12000]),
            "spawn_time": pygame.time.get_ticks()
        }

    def create_powerup(self):
        return {
            "pos": self.random_free_cell(),
            "type": random.choice(["speed", "slow", "shield"]),
            "spawn_time": pygame.time.get_ticks(),
            "ttl": 8000
        }

    def add_obstacles_for_level(self):
        if self.level < 3:
            return
        head = self.snake[0]
        safe_zone = {
            head,
            (head[0] + CELL, head[1]),
            (head[0] - CELL, head[1]),
            (head[0], head[1] + CELL),
            (head[0], head[1] - CELL)
        }
        target_count = min(4 + self.level, 20)
        attempts = 0
        while len(self.obstacles) < target_count and attempts < 300:
            attempts += 1
            block = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
            if block not in self.snake and block not in safe_zone:
                self.obstacles.add(block)

    def handle_direction(self, key):
        if key == pygame.K_UP and self.dy == 0:
            self.dx, self.dy = 0, -CELL
        elif key == pygame.K_DOWN and self.dy == 0:
            self.dx, self.dy = 0, CELL
        elif key == pygame.K_LEFT and self.dx == 0:
            self.dx, self.dy = -CELL, 0
        elif key == pygame.K_RIGHT and self.dx == 0:
            self.dx, self.dy = CELL, 0

    def current_fps(self):
        if self.active_power == "speed":
            return self.fps + 5
        if self.active_power == "slow":
            return max(4, self.fps - 4)
        return self.fps

    def use_shield_or_die(self):
        if self.shield:
            self.shield = False
            self.active_power = None
            self.dx, self.dy = -self.dx, -self.dy
            return False
        return True

    def update_timers(self):
        now = pygame.time.get_ticks()
        if now - self.food["spawn_time"] > self.food["ttl"]:
            self.food = self.create_food()
        if now - self.poison["spawn_time"] > self.poison["ttl"]:
            self.poison = self.create_poison()
        if self.powerup is None and self.active_power is None and now - self.last_power_spawn > 7000:
            self.powerup = self.create_powerup()
            self.last_power_spawn = now
        if self.powerup is not None and now - self.powerup["spawn_time"] > self.powerup["ttl"]:
            self.powerup = None
        if self.active_power in ["speed", "slow"] and now > self.power_end:
            self.active_power = None

    def update(self):
        if self.game_over:
            return
        self.update_timers()
        new_head = (self.snake[0][0] + self.dx, self.snake[0][1] + self.dy)
        collision = self.out_of_bounds(*new_head) or new_head in self.snake[1:] or new_head in self.obstacles
        if collision:
            if self.use_shield_or_die():
                self.game_over = True
            return
        self.snake.insert(0, new_head)
        if new_head == self.food["pos"]:
            self.foods_eaten += 1
            self.score += self.food["weight"]
            if self.foods_eaten % 4 == 0:
                self.level += 1
                self.fps += 2
                self.add_obstacles_for_level()
            self.food = self.create_food()
        elif new_head == self.poison["pos"]:
            for _ in range(2):
                if len(self.snake) > 0:
                    self.snake.pop()
            if len(self.snake) <= 1:
                self.game_over = True
            self.poison = self.create_poison()
        elif self.powerup and new_head == self.powerup["pos"]:
            kind = self.powerup["type"]
            if kind == "speed":
                self.active_power = "speed"
                self.power_end = pygame.time.get_ticks() + 5000
            elif kind == "slow":
                self.active_power = "slow"
                self.power_end = pygame.time.get_ticks() + 5000
            else:
                self.active_power = "shield"
                self.shield = True
            self.powerup = None
            self.snake.pop()
        else:
            self.snake.pop()

    def draw_grid(self):
        if not self.settings.get("grid", True):
            return
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, DARK_GRAY, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(screen, DARK_GRAY, (0, y), (WIDTH, y), 1)

    def draw(self):
        screen.fill(BLACK)
        self.draw_grid()
        for block in self.obstacles:
            pygame.draw.rect(screen, GRAY, (block[0], block[1], CELL, CELL))
        for part in self.snake:
            pygame.draw.rect(screen, self.snake_color, (part[0], part[1], CELL, CELL))
        if self.shield:
            head = self.snake[0]
            pygame.draw.rect(screen, BLUE, (head[0] - 2, head[1] - 2, CELL + 4, CELL + 4), 2)
        food_color = RED if self.food["weight"] == 1 else ORANGE if self.food["weight"] == 2 else PURPLE
        pygame.draw.rect(screen, food_color, (self.food["pos"][0], self.food["pos"][1], CELL, CELL))
        weight_text = small_font.render(str(self.food["weight"]), True, WHITE)
        screen.blit(weight_text, (self.food["pos"][0] + 5, self.food["pos"][1] + 1))
        pygame.draw.rect(screen, DARK_RED, (self.poison["pos"][0], self.poison["pos"][1], CELL, CELL))
        poison_text = small_font.render("P", True, WHITE)
        screen.blit(poison_text, (self.poison["pos"][0] + 5, self.poison["pos"][1] + 1))
        if self.powerup:
            if self.powerup["type"] == "speed":
                color, label = CYAN, "F"
            elif self.powerup["type"] == "slow":
                color, label = BLUE, "S"
            else:
                color, label = YELLOW, "H"
            pygame.draw.rect(screen, color, (self.powerup["pos"][0], self.powerup["pos"][1], CELL, CELL))
            text = small_font.render(label, True, BLACK)
            screen.blit(text, (self.powerup["pos"][0] + 5, self.powerup["pos"][1] + 1))
        food_left = max(0, (self.food["ttl"] - (pygame.time.get_ticks() - self.food["spawn_time"])) // 1000)
        power_info = self.active_power or "none"
        if self.active_power in ["speed", "slow"]:
            power_left = max(0, (self.power_end - pygame.time.get_ticks()) // 1000)
            power_info += f" ({power_left}s)"
        hud_lines = [
            f"User: {self.username}",
            f"Score: {self.score}   Level: {self.level}",
            f"Best: {self.personal_best}",
            f"Food time: {food_left}s",
            f"Power: {power_info}"
        ]
        y = 8
        for line in hud_lines:
            img = small_font.render(line, True, WHITE)
            screen.blit(img, (10, y))
            y += 21
