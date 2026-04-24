import pygame
import random
import sys

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

FPS = 60
clock = pygame.time.Clock()
enemy_speed = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (70, 70, 70)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)

ROAD_LEFT = 50
ROAD_RIGHT = 350

coins_collected = 0

font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 40)


# RESET FUNCTION
def reset_game():
    global coins_collected, enemy_speed, game_over

    coins_collected = 0
    enemy_speed = 5
    game_over = False

    player.rect.center = (WIDTH // 2, HEIGHT - 80)
    enemy.rect.center = (random.randint(ROAD_LEFT + 30, ROAD_RIGHT - 30), -100)
    coin.rect.center = coin.random_position()


# PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 90))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 80)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.move_ip(-5, 0)

        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.move_ip(5, 0)


# ENEMY
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 90))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(ROAD_LEFT + 30, ROAD_RIGHT - 30), -100)

    def move(self):
        global enemy_speed
        self.rect.move_ip(0, enemy_speed)

        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(ROAD_LEFT + 30, ROAD_RIGHT - 30), -100)


# COIN
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (15, 15), 15)
        self.rect = self.image.get_rect()
        self.rect.center = self.random_position()

    def random_position(self):
        while True:
            x = random.randint(ROAD_LEFT + 20, ROAD_RIGHT - 20)
            y = random.randint(-300, -50)

            temp_rect = pygame.Rect(x - 15, y - 15, 30, 30)

            # проверяем, не пересекается ли с enemy
            if not temp_rect.colliderect(enemy.rect):
                return x, y

    def move(self):
        self.rect.move_ip(0, enemy_speed)

        if self.rect.top > HEIGHT:
            self.rect.center = self.random_position()


player = Player()
enemy = Enemy()
coin = Coin()

enemies = pygame.sprite.Group(enemy)
coins = pygame.sprite.Group(coin)

all_sprites = pygame.sprite.Group(player, enemy, coin)

game_over = False
running = True

while running:

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 🔹 RESTART CLICK
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if restart_button.collidepoint(mouse_pos):
                    reset_game()

    if not game_over:
        player.move()
        enemy.move()
        coin.move()

        # Collision with enemy
        if pygame.sprite.spritecollideany(player, enemies):
            game_over = True

        # Collision with coin
        if pygame.sprite.spritecollideany(player, coins):
            coins_collected += 1
            coin.rect.center = coin.random_position()

            if coins_collected % 3 == 0:
                enemy_speed += 1

    screen.fill(WHITE)

    # Road
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 4)

    # Sprites
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)

    #  COUNTER (зелёный прямоугольник)
    counter_rect = pygame.Rect(WIDTH - 150, 10, 130, 40)
    pygame.draw.rect(screen, GREEN, counter_rect)

    coin_text = font.render(f"Coins: {coins_collected}", True, BLACK)
    screen.blit(coin_text, (WIDTH - 140, 15))

    # GAME OVER + BUTTON
    if game_over:
        text = big_font.render("GAME OVER", True, BLACK)
        screen.blit(text, (80, 250))

        restart_button = pygame.Rect(120, 320, 160, 50)
        pygame.draw.rect(screen, GREEN, restart_button)
        pygame.draw.rect(screen, BLACK, restart_button, 2)

        restart_text = font.render("RESTART", True, BLACK)
        screen.blit(restart_text, (145, 335))

    pygame.display.update()
    clock.tick(FPS)