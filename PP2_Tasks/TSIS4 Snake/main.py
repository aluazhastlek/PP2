import pygame
import sys

from game import (
    screen, clock, WIDTH, FPS_START,
    WHITE, BLACK, GRAY,
    font, small_font, big_font,
    Button, SnakeGame, load_settings, save_settings
)

import db

pygame.init()


def safe_db_call(func, default=None, *args):
    try:
        return func(*args)
    except Exception as error:
        print("Database error:", error)
        return default


def get_name_screen():
    name = ""
    while True:
        screen.fill(BLACK)
        title = big_font.render("Enter username", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 170)))
        box = pygame.Rect(120, 260, 360, 50)
        pygame.draw.rect(screen, GRAY, box)
        pygame.draw.rect(screen, WHITE, box, 2)
        name_img = font.render(name, True, BLACK)
        screen.blit(name_img, (box.x + 10, box.y + 12))
        hint = small_font.render("Press Enter to start", True, WHITE)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 340)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return name if name.strip() else "Player"
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 15 and event.unicode.isprintable():
                    name += event.unicode


def main_menu():
    buttons = [
        Button(200, 210, 200, 50, "Play"),
        Button(200, 280, 200, 50, "Leaderboard"),
        Button(200, 350, 200, 50, "Settings"),
        Button(200, 420, 200, 50, "Instructions"),
        Button(200, 500, 200, 50, "Quit")
    ]
    while True:
        screen.fill(BLACK)
        title = big_font.render("SNAKE", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))
        for button in buttons:
            button.draw()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if buttons[0].clicked(pos):
                    return "play"
                if buttons[1].clicked(pos):
                    leaderboard_screen()
                if buttons[2].clicked(pos):
                    settings_screen()
                if buttons[3].clicked(pos):
                    instructions_screen()

                if buttons[4].clicked(pos):
                    pygame.quit()
                    sys.exit()


def leaderboard_screen():
    back = Button(200, 530, 200, 45, "Back")
    rows = safe_db_call(db.get_top_scores, [], 10)
    while True:
        screen.fill(BLACK)
        title = big_font.render("Leaderboard", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 55)))
        header = small_font.render("Rank | Username | Score | Level | Date", True, WHITE)
        screen.blit(header, (55, 105))
        y = 140
        for i, row in enumerate(rows, start=1):
            username, score, level, date = row
            line = f"{i}. {username} | {score} | L{level} | {date}"
            img = small_font.render(line, True, WHITE)
            screen.blit(img, (55, y))
            y += 35
        back.draw()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and back.clicked(pygame.mouse.get_pos()):
                return


def settings_screen():
    settings = load_settings()
    colors = [[0, 200, 0], [50, 130, 255], [255, 230, 0], [255, 105, 180], [160, 32, 240]]
    save_back = Button(185, 500, 230, 50, "Save & Back")
    while True:
        screen.fill(BLACK)
        title = big_font.render("Settings", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))
        grid_btn = Button(160, 160, 280, 45, f"Grid: {'ON' if settings['grid'] else 'OFF'}")
        sound_btn = Button(160, 230, 280, 45, f"Sound: {'ON' if settings['sound'] else 'OFF'}")
        color_btn = Button(160, 300, 280, 45, "Change Snake Color")
        for button in [grid_btn, sound_btn, color_btn, save_back]:
            button.draw()
        pygame.draw.rect(screen, tuple(settings["snake_color"]), (270, 370, 60, 40))
        pygame.draw.rect(screen, WHITE, (270, 370, 60, 40), 2)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if grid_btn.clicked(pos):
                    settings["grid"] = not settings["grid"]
                elif sound_btn.clicked(pos):
                    settings["sound"] = not settings["sound"]
                elif color_btn.clicked(pos):
                    index = colors.index(settings["snake_color"]) if settings["snake_color"] in colors else 0
                    settings["snake_color"] = colors[(index + 1) % len(colors)]
                elif save_back.clicked(pos):
                    save_settings(settings)
                    return

def instructions_screen():
    while True:
        screen.fill(WHITE)

        lines = [
            "HOW TO PLAY",
            "",
            "Arrow keys — move snake",
            "Eat food to grow",
            "",
            "Food:",
            "Numbers = points",
            "Poison = -2 length",
            "",
            "Power-ups:",
            "F = speed boost",
            "S = slow motion",
            "H = shield",
            "",
            "Avoid walls and obstacles",
            "Press ESC to go back"
        ]

        y = 50
        for line in lines:
            text = small_font.render(line, True, BLACK)
            screen.blit(text, (50, y))
            y += 30

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

def game_over_screen(game):
    retry = Button(130, 430, 150, 50, "Retry")
    menu = Button(320, 430, 150, 50, "Main Menu")
    final_best = max(game.personal_best, game.score)
    while True:
        screen.fill(BLACK)
        title = big_font.render("GAME OVER", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 150)))
        stats = [
            f"Final score: {game.score}",
            f"Level reached: {game.level}",
            f"Personal best: {final_best}",
            "Result saved"
        ]
        y = 230
        for stat in stats:
            img = font.render(stat, True, WHITE)
            screen.blit(img, img.get_rect(center=(WIDTH // 2, y)))
            y += 42
        retry.draw(); menu.draw()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if retry.clicked(pos): return "retry"
                if menu.clicked(pos): return "menu"


def run_game(username):
    settings = load_settings()
    personal_best = safe_db_call(db.get_personal_best, 0, username)
    game = SnakeGame(username, personal_best, settings)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if not game.game_over and event.type == pygame.KEYDOWN:
                game.handle_direction(event.key)
        game.update(); game.draw()
        pygame.display.flip()
        clock.tick(game.current_fps())
        if game.game_over:
            if not game.saved:
                safe_db_call(db.save_session, None, game.username, game.score, game.level)
                game.saved = True
            result = game_over_screen(game)
            if result == "retry":
                personal_best = safe_db_call(db.get_personal_best, 0, username)
                game = SnakeGame(username, personal_best, load_settings())
            else:
                return


def main():
    safe_db_call(db.init_db)
    while True:
        action = main_menu()
        if action == "play":
            username = get_name_screen()
            run_game(username)


if __name__ == "__main__":
    main()
