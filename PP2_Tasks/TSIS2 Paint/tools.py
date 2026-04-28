import pygame
import math
from collections import deque

def normalize_rect(start, end):
    x1, y1 = start
    x2, y2 = end
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))


def draw_shape(surface, tool, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    rect = normalize_rect(start, end)

    if tool == "line":
        pygame.draw.line(surface, color, start, end, width)

    elif tool == "rect":
        pygame.draw.rect(surface, color, rect, width)

    elif tool == "circle":
        pygame.draw.ellipse(surface, color, rect, width)

    elif tool == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))
        square_rect = pygame.Rect(x1, y1, side, side)
        square_rect.normalize()
        pygame.draw.rect(surface, color, square_rect, width)

    elif tool == "right tri":
        points = [(x1, y1), (x2, y1), (x1, y2)]
        pygame.draw.polygon(surface, color, points, width)

    elif tool == "eq tri":
        side = abs(x2 - x1)
        height = side * math.sqrt(3) / 2
        p1 = (x1, y1)
        p2 = (x1 + side, y1)
        p3 = (x1 + side / 2, y1 - height)
        pygame.draw.polygon(surface, color, [p1, p2, p3], width)

    elif tool == "rhombus":
        points = [
            (rect.centerx, rect.top),
            (rect.right, rect.centery),
            (rect.centerx, rect.bottom),
            (rect.left, rect.centery)
        ]
        pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface, start, fill_color):
    width, height = surface.get_size()
    x, y = start

    target_color = surface.get_at((x, y))
    replacement_color = pygame.Color(*fill_color)

    if target_color == replacement_color:
        return

    queue = deque([(x, y)])

    while queue:
        cx, cy = queue.popleft()

        if not (0 <= cx < width and 0 <= cy < height):
            continue

        if surface.get_at((cx, cy)) != target_color:
            continue

        surface.set_at((cx, cy), replacement_color)

        queue.append((cx + 1, cy))
        queue.append((cx - 1, cy))
        queue.append((cx, cy + 1))
        queue.append((cx, cy - 1))