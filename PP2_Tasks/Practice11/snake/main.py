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
ORANGE = (255, 140, 0)
PURPLE = (160, 32, 240)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)

font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 40)

clock = pygame.time.Clock()


# Reset game to initial state
def reset_game():
    global snake, dx, dy, score, level, foods_eaten, FPS, game_over, food

    snake = [(100, 100), (80, 100), (60, 100)]
    dx, dy = CELL, 0

    score = 0
    level = 1
    foods_eaten = 0
    FPS = 8

    game_over = False
    food = create_food()


# Check if snake head leaves the screen
def out_of_bounds(x, y):
    return x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT


# Generate random cell which is not occupied by snake
def random_free_cell():
    while True:
        cell = (
            random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL)
        )

        if cell not in snake:
            return cell


# Create food with random weight and timer
def create_food():
    return {
        "pos": random_free_cell(),
        "weight": random.choice([1, 2, 3]),
        "ttl": random.choice([4000, 6000, 8000]),
        "spawn_time": pygame.time.get_ticks()
    }


# Start game
reset_game()

running = True

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Snake controls
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -CELL
            elif event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, CELL
            elif event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -CELL, 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = CELL, 0

        # Restart button
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if restart_button.collidepoint(mouse_pos):
                    reset_game()

    if not game_over:
        # Check food timer
        now = pygame.time.get_ticks()

        if now - food["spawn_time"] > food["ttl"]:
            food = create_food()

        # Calculate new head position
        new_head = (snake[0][0] + dx, snake[0][1] + dy)

        # Check wall collision and self collision
        if out_of_bounds(*new_head) or new_head in snake[1:]:
            game_over = True

        else:
            snake.insert(0, new_head)

            # Check if snake eats food
            if new_head == food["pos"]:
                foods_eaten += 1
                score += food["weight"]

                # Increase level and speed every 4 foods
                if foods_eaten % 4 == 0:
                    level += 1
                    FPS += 2

                food = create_food()

            else:
                snake.pop()

    screen.fill(BLACK)

    # Draw snake
    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], CELL, CELL))

    # Choose food color depending on weight
    if food["weight"] == 1:
        food_color = RED
    elif food["weight"] == 2:
        food_color = ORANGE
    else:
        food_color = PURPLE

    # Draw food
    pygame.draw.rect(screen, food_color, (food["pos"][0], food["pos"][1], CELL, CELL))

    # Draw food weight number
    weight_text = font.render(str(food["weight"]), True, WHITE)
    screen.blit(weight_text, (food["pos"][0] + 4, food["pos"][1] - 2))

    # Show timer
    time_left = max(0, (food["ttl"] - (pygame.time.get_ticks() - food["spawn_time"])) // 1000)

    hud = font.render(
        f"Score: {score}   Level: {level}   Food time: {time_left}",
        True,
        WHITE
    )
    screen.blit(hud, (10, 10))

    # Game over screen
    if game_over:
        text = big_font.render("GAME OVER", True, WHITE)
        screen.blit(text, (180, 200))

        restart_button = pygame.Rect(220, 300, 160, 50)
        pygame.draw.rect(screen, GRAY, restart_button)
        pygame.draw.rect(screen, WHITE, restart_button, 2)

        restart_text = font.render("RESTART", True, BLACK)
        screen.blit(restart_text, (250, 315))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()