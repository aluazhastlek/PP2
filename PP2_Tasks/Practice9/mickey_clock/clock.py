import pygame
from datetime import datetime
import os


def run_clock():
    pygame.init()

    WIDTH, HEIGHT = 1000, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey Clock")

    bg_color = (236, 236, 236)
    center = (WIDTH // 2, HEIGHT // 2 + 40)
    fps_clock = pygame.time.Clock()

    base_path = os.path.dirname(__file__)
    images_path = os.path.join(base_path, "images")

    clock_img = pygame.image.load(os.path.join(images_path, "clock.png")).convert_alpha()
    mickey_img = pygame.image.load(os.path.join(images_path, "mickey.png")).convert_alpha()
    right_hand_img = pygame.image.load(os.path.join(images_path, "righthand.png")).convert_alpha()
    left_hand_img = pygame.image.load(os.path.join(images_path, "lefthand.png")).convert_alpha()

    clock_img = pygame.transform.scale(clock_img, (650, 650))
    mickey_img = pygame.transform.scale(mickey_img, (300, 360))
    right_hand_img = pygame.transform.scale(right_hand_img, (90, 190))
    left_hand_img = pygame.transform.scale(left_hand_img, (120, 300))

    title_font = pygame.font.SysFont("Calibri", 44, bold=True)

    RIGHT_PIVOT = (45, 170)
    LEFT_PIVOT = (60, 245)

    def make_rotatable_hand(hand_img, pivot_point):
        w, h = hand_img.get_size()
        canvas_size = 700
        surface = pygame.Surface((canvas_size, canvas_size), pygame.SRCALPHA)

        cx = canvas_size // 2
        cy = canvas_size // 2

        blit_x = cx - pivot_point[0]
        blit_y = cy - pivot_point[1]

        surface.blit(hand_img, (blit_x, blit_y))
        return surface

    right_hand_surface = make_rotatable_hand(right_hand_img, RIGHT_PIVOT)
    left_hand_surface = make_rotatable_hand(left_hand_img, LEFT_PIVOT)

    def draw_rotated(surface, angle, draw_center):
        rotated = pygame.transform.rotate(surface, -angle)
        rect = rotated.get_rect(center=draw_center)
        screen.blit(rotated, rect)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = datetime.now()

        minute = now.minute
        second = now.second
        microsecond = now.microsecond

        second_fraction = second + microsecond / 1_000_000
        minute_fraction = minute + second_fraction / 60

        second_angle = second_fraction * 6
        minute_angle = minute_fraction * 6

        screen.fill(bg_color)

        clock_rect = clock_img.get_rect(center=center)
        screen.blit(clock_img, clock_rect)
        mickey_rect = mickey_img.get_rect(center=center)
        screen.blit(mickey_img, mickey_rect)

        draw_rotated(right_hand_surface, minute_angle, center)
        draw_rotated(left_hand_surface, second_angle, center)

        pygame.draw.circle(screen, (40, 40, 40), center, 6)

        time_text = f"{minute:02d}:{second:02d}"
        text_surface = title_font.render(time_text, True, (55, 55, 55))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 70))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()
        fps_clock.tick(60)

    pygame.quit()