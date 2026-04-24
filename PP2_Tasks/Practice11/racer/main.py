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
SPEED_UP_EVERY = 5   # enemy speed increases every 5 score points

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (70, 70, 70)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
PURPLE = (160, 32, 240)

ROAD_LEFT = 50
ROAD_RIGHT = 350

score = 0
next_speed_score = SPEED_UP_EVERY

font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 40)


# Reset game variables after restart
def reset_game():
    global score, enemy_speed, game_over, next_speed_score

    score = 0
    enemy_speed = 5
    next_speed_score = SPEED_UP_EVERY
    game_over = False

    player.rect.center = (WIDTH // 2, HEIGHT - 80)
    enemy.rect.center = (random.randint(ROAD_LEFT + 30, ROAD_RIGHT - 30), -100)
    coin.create_new_coin()


# Player car
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((50, 90))
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 80)

    def move(self):
        keys = pygame.key.get_pressed()

        # Move left inside road borders
        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.move_ip(-5, 0)

        # Move right inside road borders
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.move_ip(5, 0)


# Enemy car
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((50, 90))
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(ROAD_LEFT + 30, ROAD_RIGHT - 30), -100)

    def move(self):
        # Enemy moves down
        self.rect.move_ip(0, enemy_speed)

        # If enemy leaves screen, return it to the top
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(ROAD_LEFT + 30, ROAD_RIGHT - 30), -100)


# Coin with random weight
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = 1
        self.create_new_coin()

    # Create coin image depending on weight
    def create_image(self):
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)

        if self.weight == 1:
            color = YELLOW
        elif self.weight == 2:
            color = ORANGE
        else:
            color = PURPLE

        pygame.draw.circle(self.image, color, (15, 15), 15)

        # Show coin weight inside coin
        text = font.render(str(self.weight), True, BLACK)
        self.image.blit(text, (9, 3))

    # Generate position only on road and not on enemy
    def random_position(self):
        while True:
            x = random.randint(ROAD_LEFT + 20, ROAD_RIGHT - 20)
            y = random.randint(-300, -50)

            temp_rect = pygame.Rect(x - 15, y - 15, 30, 30)

            if not temp_rect.colliderect(enemy.rect):
                return x, y

    # Create new coin with random weight and position
    def create_new_coin(self):
        self.weight = random.choice([1, 2, 3])
        self.create_image()
        self.rect = self.image.get_rect()
        self.rect.center = self.random_position()

    def move(self):
        # Coin moves down with road objects
        self.rect.move_ip(0, enemy_speed)

        # If coin leaves screen, create new coin
        if self.rect.top > HEIGHT:
            self.create_new_coin()


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

        # Restart button click after game over
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if restart_button.collidepoint(mouse_pos):
                    reset_game()

    if not game_over:
        player.move()
        enemy.move()
        coin.move()

        # If player hits enemy, game ends
        if pygame.sprite.spritecollideany(player, enemies):
            game_over = True

        # If player collects coin
        if pygame.sprite.spritecollideany(player, coins):
            score += coin.weight

            # Increase enemy speed when score reaches N points
            if score >= next_speed_score:
                enemy_speed += 1
                next_speed_score += SPEED_UP_EVERY

            coin.create_new_coin()

    screen.fill(WHITE)

    # Draw road
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 4)

    # Draw sprites
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)

    # Draw score counter in green rectangle
    counter_rect = pygame.Rect(WIDTH - 160, 10, 140, 40)
    pygame.draw.rect(screen, GREEN, counter_rect)
    pygame.draw.rect(screen, BLACK, counter_rect, 2)

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 150, 15))

    # Draw current speed
    speed_text = font.render(f"Speed: {enemy_speed}", True, BLACK)
    screen.blit(speed_text, (10, 10))

    # Game over screen and restart button
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