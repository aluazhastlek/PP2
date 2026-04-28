import pygame
import sys
from racer import RacerGame, screen, clock, FPS
from ui import main_menu, game_over_screen
from persistence import load_settings, add_score


pygame.mixer.init()
pygame.mixer.music.load("assets/arcade_loop.wav")
pygame.mixer.music.set_volume(0.3)


def start_music():
    settings = load_settings()

    if settings["sound"]:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()


def run_game(name):
    start_music()

    game = RacerGame(name)
    score_saved = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)

        if game.game_over:
            pygame.mixer.music.stop()

            if not score_saved:
                add_score(
                    name,
                    game.score,
                    game.distance,
                    game.coins
                )
                score_saved = True

            result = game_over_screen(game)

            if result == "retry":
                start_music()
                game = RacerGame(name)
                score_saved = False
            else:
                return


def main():
    while True:
        action, player_name = main_menu()

        if action == "play":
            run_game(player_name)


if __name__ == "__main__":
    main()