import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)

font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 40)

clock = pygame.time.Clock()


#  Reset function (ВАЖНО ДЛЯ RESTART)
def reset_game():
    global snake, dx, dy, score, level, foods_eaten, FPS, game_over, food

    snake = [(100, 100), (80, 100), (60, 100)]
    dx, dy = CELL, 0

    score = 0
    level = 1
    foods_eaten = 0
    FPS = 8

    game_over = False
    food = random_free_cell()


#  Check borders
def out_of_bounds(x, y):
    return x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT


#  Generate food
def random_free_cell():
    while True:
        cell = (
            random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL)
        )
        if cell not in snake:
            return cell


# Start game first time
reset_game()

running = True

while running:

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #  Controls (only if game not over)
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -CELL
            elif event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, CELL
            elif event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -CELL, 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = CELL, 0

        # Restart button click
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if restart_button.collidepoint(mouse_pos):
                    reset_game()

    if not game_over:
        new_head = (snake[0][0] + dx, snake[0][1] + dy)

        if out_of_bounds(*new_head) or new_head in snake[1:]:
            game_over = True

        else:
            snake.insert(0, new_head)

            if new_head == food:
                foods_eaten += 1
                score += 1

                if foods_eaten % 4 == 0:
                    level += 1
                    FPS += 2

                food = random_free_cell()
            else:
                snake.pop()

    #  Draw
    screen.fill(BLACK)

    # Snake
    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], CELL, CELL))

    # Food
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL))

    # Score + Level
    hud = font.render(f"Score: {score}   Level: {level}", True, WHITE)
    screen.blit(hud, (10, 10))

    # 🔹 Game Over Screen
    if game_over:
        text = big_font.render("GAME OVER", True, WHITE)
        screen.blit(text, (180, 200))

        # Restart button
        restart_button = pygame.Rect(220, 300, 160, 50)
        pygame.draw.rect(screen, GRAY, restart_button)
        pygame.draw.rect(screen, WHITE, restart_button, 2)

        restart_text = font.render("RESTART", True, BLACK)
        screen.blit(restart_text, (250, 315))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()