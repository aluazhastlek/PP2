import pygame
import sys
from persistence import settings, save_settings, leaderboard
from racer import (
    screen, WIDTH, HEIGHT, WHITE, BLACK, LIGHT_GRAY,
    font, small_font, big_font, CAR_COLORS, DIFFICULTY_DATA
)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, LIGHT_GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        label = font.render(self.text, True, BLACK)
        screen.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


def get_name_screen():
    name = ""

    while True:
        screen.fill(WHITE)
        title = big_font.render("Enter your name", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 160)))

        box = pygame.Rect(100, 260, 300, 50)
        pygame.draw.rect(screen, LIGHT_GRAY, box)
        pygame.draw.rect(screen, BLACK, box, 2)

        name_text = font.render(name, True, BLACK)
        screen.blit(name_text, (box.x + 10, box.y + 13))

        hint = small_font.render("Press Enter to start", True, BLACK)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 330)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12:
                    name += event.unicode


def main_menu():
    buttons = [
        Button(150, 220, 200, 50, "Play"),
        Button(150, 290, 200, 50, "Leaderboard"),
        Button(150, 360, 200, 50, "Settings"),
        Button(150, 430, 200, 50, "Quit")
    ]

    while True:
        screen.fill(WHITE)
        title = big_font.render("RACER", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 130)))

        for button in buttons:
            button.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if buttons[0].clicked(pos):
                    name = get_name_screen()
                    return "play", name
                elif buttons[1].clicked(pos):
                    leaderboard_screen()
                elif buttons[2].clicked(pos):
                    settings_screen()
                elif buttons[3].clicked(pos):
                    pygame.quit()
                    sys.exit()


def leaderboard_screen():
    back = Button(150, 620, 200, 45, "Back")

    while True:
        screen.fill(WHITE)
        title = big_font.render("Top 10", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 70)))

        y = 130
        for i, item in enumerate(leaderboard[:10], start=1):
            name_line = f"{i}. {item['name']}"
            stats_line = f"Score: {item['score']}   Dist: {item['distance']}   Coins: {item['coins']}"

            img1 = small_font.render(name_line, True, BLACK)
            img2 = small_font.render(stats_line, True, BLACK)

            screen.blit(img1, (55, y))
            screen.blit(img2, (105, y + 20))

            y += 50

        back.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and back.clicked(pygame.mouse.get_pos()):
                return


def settings_screen():
    back = Button(150, 620, 200, 45, "Back")

    while True:
        screen.fill(WHITE)
        title = big_font.render("Settings", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 70)))

        sound_btn = Button(120, 150, 260, 45, f"Sound: {'ON' if settings['sound'] else 'OFF'}")
        color_btn = Button(120, 230, 260, 45, f"Car color: {settings['car_color']}")
        diff_btn = Button(120, 310, 260, 45, f"Difficulty: {settings['difficulty']}")

        for button in [sound_btn, color_btn, diff_btn, back]:
            button.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if sound_btn.clicked(pos):
                    settings["sound"] = not settings["sound"]
                    save_settings()

                elif color_btn.clicked(pos):
                    keys = list(CAR_COLORS.keys())
                    index = (keys.index(settings["car_color"]) + 1) % len(keys)
                    settings["car_color"] = keys[index]
                    save_settings()

                elif diff_btn.clicked(pos):
                    keys = list(DIFFICULTY_DATA.keys())
                    index = (keys.index(settings["difficulty"]) + 1) % len(keys)
                    settings["difficulty"] = keys[index]
                    save_settings()

                elif back.clicked(pos):
                    return


def game_over_screen(game):
    retry = Button(100, 520, 140, 50, "Retry")
    menu = Button(260, 520, 140, 50, "Main Menu")

    while True:
        game.draw()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 210))
        screen.blit(overlay, (0, 0))

        title = big_font.render("GAME OVER", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 170)))

        stats = [
            f"Score: {game.score}",
            f"Distance: {int(game.distance)}",
            f"Coins: {game.coins}",
            "Result saved to leaderboard"
        ]

        y = 240
        for stat in stats:
            img = font.render(stat, True, BLACK)
            screen.blit(img, img.get_rect(center=(WIDTH // 2, y)))
            y += 45

        retry.draw()
        menu.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if retry.clicked(pos):
                    return "retry"
                elif menu.clicked(pos):
                    return "menu"
