import pygame
import random
import sys
from persistence import settings, add_score

pygame.init()

WIDTH, HEIGHT = 500, 700
ROAD_LEFT, ROAD_RIGHT = 80, 420
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
LANES = [125, 210, 295, 380]
FPS = 60
FINISH_DISTANCE = 3000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 Racer")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (70, 70, 70)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (40, 40, 40)
GREEN = (0, 180, 0)
RED = (220, 40, 40)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
PURPLE = (160, 32, 240)
BLUE = (30, 120, 255)
CYAN = (0, 220, 220)
PINK = (255, 105, 180)
BROWN = (130, 80, 40)

font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 16)
big_font = pygame.font.SysFont("Arial", 42)

CAR_COLORS = {
    "green": GREEN,
    "blue": BLUE,
    "pink": PINK,
    "yellow": YELLOW
}

DIFFICULTY_DATA = {
    "easy": {"speed": 4, "traffic": 1600, "obstacles": 2200},
    "normal": {"speed": 5, "traffic": 1200, "obstacles": 1700},
    "hard": {"speed": 6, "traffic": 900, "obstacles": 1300}
}


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((45, 80))
        self.update_color()
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 90))
        self.shield = False
        self.crashes = 0

    def update_color(self):
        self.image.fill(CAR_COLORS.get(settings["car_color"], GREEN))
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 3)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.x -= 6
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.x += 6


class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, player, road_speed):
        super().__init__()
        self.image = pygame.Surface((45, 80))
        self.image.fill(RED)
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 3)
        self.rect = self.image.get_rect()
        self.speed = road_speed
        self.safe_spawn(player)

    def safe_spawn(self, player):
        for _ in range(50):
            self.rect.center = (random.choice(LANES), random.randint(-500, -80))
            if abs(self.rect.centerx - player.rect.centerx) > 45 or player.rect.y < HEIGHT - 180:
                return

        self.rect.center = (random.choice(LANES), -300)

    def update(self, road_speed):
        self.rect.y += road_speed + 1

        if self.rect.top > HEIGHT:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, road_speed):
        super().__init__()
        self.weight = random.choice([1, 2, 3])
        self.image = pygame.Surface((28, 28), pygame.SRCALPHA)

        if self.weight == 1:
            color = YELLOW
        elif self.weight == 2:
            color = ORANGE
        else:
            color = PURPLE

        pygame.draw.circle(self.image, color, (14, 14), 14)
        text = small_font.render(str(self.weight), True, BLACK)
        self.image.blit(text, (9, 5))
        self.rect = self.image.get_rect(center=(random.choice(LANES), random.randint(-500, -60)))
        self.speed = road_speed

    def update(self, road_speed):
        self.rect.y += road_speed

        if self.rect.top > HEIGHT:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, kind):
        super().__init__()
        self.kind = kind
        self.image = pygame.Surface((60, 35), pygame.SRCALPHA)

        if kind == "barrier":
            self.image.fill(ORANGE)
            pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 3)
        elif kind == "oil":
            pygame.draw.ellipse(self.image, BLACK, (0, 5, 60, 25))
        elif kind == "pothole":
            pygame.draw.ellipse(self.image, BROWN, (0, 0, 60, 35))
            pygame.draw.ellipse(self.image, BLACK, (8, 5, 44, 25), 2)
        else:
            self.image.fill(YELLOW)
            pygame.draw.line(self.image, BLACK, (0, 17), (60, 17), 4)

        self.rect = self.image.get_rect(center=(random.choice(LANES), random.randint(-600, -80)))

    def update(self, road_speed):
        self.rect.y += road_speed

        if self.rect.top > HEIGHT:
            self.kill()


class MovingBarrier(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.kind = "moving barrier"
        self.image = pygame.Surface((70, 35))
        self.image.fill(PURPLE)
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 3)
        self.rect = self.image.get_rect(center=(random.choice(LANES), -120))
        self.direction = random.choice([-1, 1])

    def update(self, road_speed):
        self.rect.y += road_speed
        self.rect.x += self.direction * 2

        if self.rect.left < ROAD_LEFT or self.rect.right > ROAD_RIGHT:
            self.direction *= -1

        if self.rect.top > HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, kind):
        super().__init__()
        self.kind = kind
        self.spawn_time = pygame.time.get_ticks()
        self.ttl = 6000
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)

        if kind == "nitro":
            color = CYAN
            letter = "N"
        elif kind == "shield":
            color = BLUE
            letter = "S"
        else:
            color = GREEN
            letter = "R"

        pygame.draw.circle(self.image, color, (18, 18), 18)
        text = font.render(letter, True, BLACK)
        self.image.blit(text, text.get_rect(center=(18, 18)))
        self.rect = self.image.get_rect(center=(random.choice(LANES), random.randint(-700, -100)))

    def update(self, road_speed):
        self.rect.y += road_speed
        now = pygame.time.get_ticks()

        if self.rect.top > HEIGHT or now - self.spawn_time > self.ttl:
            self.kill()


class RacerGame:
    def __init__(self, name):
        self.name = name if name.strip() else "Player"
        self.difficulty = DIFFICULTY_DATA[settings["difficulty"]]
        self.base_speed = self.difficulty["speed"]
        self.road_speed = self.base_speed
        self.score = 0
        self.bonus_score = 0
        self.coins = 0
        self.distance = 0
        self.game_over = False
        self.saved = False
        self.active_power = None
        self.power_end = 0
        self.last_traffic = 0
        self.last_coin = 0
        self.last_obstacle = 0
        self.last_power = 0
        self.last_event = 0

        self.player = Player()
        self.traffic = pygame.sprite.Group()
        self.coins_group = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

    def difficulty_multiplier(self):
        return 1 + self.distance / 1200

    def spawn_objects(self):
        now = pygame.time.get_ticks()
        multiplier = self.difficulty_multiplier()

        if now - self.last_traffic > max(450, self.difficulty["traffic"] / multiplier):
            self.traffic.add(TrafficCar(self.player, self.road_speed))
            self.last_traffic = now

        if now - self.last_obstacle > max(550, self.difficulty["obstacles"] / multiplier):
            kind = random.choice(["barrier", "oil", "pothole", "bump"])
            self.obstacles.add(Obstacle(kind))
            self.last_obstacle = now

        if now - self.last_coin > 1000:
            self.coins_group.add(Coin(self.road_speed))
            self.last_coin = now

        if now - self.last_power > 7000 and len(self.powerups) == 0 and self.active_power is None:
            self.powerups.add(PowerUp(random.choice(["nitro", "shield", "repair"])))
            self.last_power = now

        if now - self.last_event > 9000:
            self.obstacles.add(MovingBarrier())
            self.last_event = now

    def apply_power(self, kind):
        # Only one power-up can be active at a time.
        if self.active_power is not None:
            return

        if kind == "nitro":
            self.active_power = "nitro"
            self.power_end = pygame.time.get_ticks() + 4000
            self.bonus_score += 25

        elif kind == "shield":
            self.active_power = "shield"
            self.player.shield = True
            self.power_end = 0
            self.bonus_score += 15

        elif kind == "repair":
            self.bonus_score += 20
            if len(self.obstacles) > 0:
                random.choice(self.obstacles.sprites()).kill()
            else:
                self.player.crashes = max(0, self.player.crashes - 1)

    def handle_collision(self, group):
        hit = pygame.sprite.spritecollideany(self.player, group)

        if hit:
            if self.player.shield:
                self.player.shield = False
                self.active_power = None
                hit.kill()
            else:
                self.game_over = True

    def update(self):
        if self.game_over:
            if not self.saved:
                add_score(self.name, self.score, self.distance, self.coins)
                self.saved = True
            return

        now = pygame.time.get_ticks()
        self.road_speed = self.base_speed + int(self.distance // 900)

        if self.active_power == "nitro":
            self.road_speed += 4
            if now > self.power_end:
                self.active_power = None

        self.player.move()
        self.spawn_objects()
        self.traffic.update(self.road_speed)
        self.coins_group.update(self.road_speed)
        self.obstacles.update(self.road_speed)
        self.powerups.update(self.road_speed)

        self.distance += self.road_speed * 0.08
        self.score = int(self.coins * 10 + self.distance + self.bonus_score)

        collected_coin = pygame.sprite.spritecollideany(self.player, self.coins_group)
        if collected_coin:
            self.coins += collected_coin.weight
            self.score += collected_coin.weight * 10
            collected_coin.kill()

        collected_power = pygame.sprite.spritecollideany(self.player, self.powerups)
        if collected_power:
            self.apply_power(collected_power.kind)
            collected_power.kill()

        self.handle_collision(self.traffic)
        self.handle_collision(self.obstacles)

        if self.distance >= FINISH_DISTANCE:
            self.score += 500
            self.game_over = True

    def draw_road(self):
        pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))
        pygame.draw.rect(screen, DARK_GRAY, (ROAD_LEFT - 5, 0, 5, HEIGHT))
        pygame.draw.rect(screen, DARK_GRAY, (ROAD_RIGHT, 0, 5, HEIGHT))

        for lane_x in [(LANES[i] + LANES[i + 1]) // 2 for i in range(len(LANES) - 1)]:
            for y in range(-40, HEIGHT, 80):
                pygame.draw.line(screen, WHITE, (lane_x, y), (lane_x, y + 40), 3)

    def draw_hud(self):
        remaining = max(0, FINISH_DISTANCE - int(self.distance))
        texts = [
            f"Name: {self.name}",
            f"Score: {self.score}",
            f"Coins: {self.coins}",
            f"Distance: {int(self.distance)} / {FINISH_DISTANCE}",
            f"Remaining: {remaining}",
            f"Power: {self.active_power or 'none'}"
        ]

        if self.active_power == "nitro":
            left = max(0, (self.power_end - pygame.time.get_ticks()) // 1000)
            texts[-1] += f" ({left}s)"
        elif self.player.shield:
            texts[-1] = "Power: shield active"

        y = 10
        for text in texts:
            img = small_font.render(text, True, BLACK)
            screen.blit(img, (10, y))
            y += 22

    def draw(self):
        screen.fill((30, 150, 40))
        self.draw_road()
        self.coins_group.draw(screen)
        self.powerups.draw(screen)
        self.obstacles.draw(screen)
        self.traffic.draw(screen)
        screen.blit(self.player.image, self.player.rect)

        if self.player.shield:
            pygame.draw.circle(screen, BLUE, self.player.rect.center, 55, 3)

        self.draw_hud()
