import pygame

pygame.init()

WIDTH, HEIGHT = 900, 600
TOOLBAR = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0)
]

tools = ["brush", "rect", "circle", "eraser", "clear"]

current_color = BLACK
current_tool = "brush"

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR))
canvas.fill(WHITE)

font = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()

drawing = False
start_pos = None
last_pos = None

running = True

while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, TOOLBAR))

    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR))

    x = 10
    for tool in tools:
        button = pygame.Rect(x, 20, 90, 40)

        if tool == current_tool:
            pygame.draw.rect(screen, (160, 160, 160), button)
        else:
            pygame.draw.rect(screen, WHITE, button)

        pygame.draw.rect(screen, BLACK, button, 2)

        text = font.render(tool, True, BLACK)
        screen.blit(text, (x + 10, 30))

        x += 100

    x = 530
    for color in colors:
        color_button = pygame.Rect(x, 25, 35, 35)
        pygame.draw.rect(screen, color, color_button)
        pygame.draw.rect(screen, BLACK, color_button, 2)
        x += 45

    mouse_x, mouse_y = pygame.mouse.get_pos()
    canvas_pos = (mouse_x, mouse_y - TOOLBAR)

    if drawing and current_tool in ["rect", "circle"]:
        preview = canvas.copy()

        x1, y1 = start_pos
        x2, y2 = canvas_pos

        shape_rect = pygame.Rect(
            min(x1, x2),
            min(y1, y2),
            abs(x2 - x1),
            abs(y2 - y1)
        )

        if current_tool == "rect":
            pygame.draw.rect(preview, current_color, shape_rect, 3)

        if current_tool == "circle":
            pygame.draw.ellipse(preview, current_color, shape_rect, 3)

        screen.blit(preview, (0, TOOLBAR))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                mouse_x, mouse_y = event.pos

                if mouse_y < TOOLBAR:

                    x = 10
                    for tool in tools:
                        button = pygame.Rect(x, 20, 90, 40)

                        if button.collidepoint(event.pos):
                            if tool == "clear":
                                canvas.fill(WHITE)
                            else:
                                current_tool = tool

                        x += 100

                    x = 530
                    for color in colors:
                        color_button = pygame.Rect(x, 25, 35, 35)

                        if color_button.collidepoint(event.pos):
                            current_color = color

                        x += 45

                else:
                    drawing = True
                    start_pos = (mouse_x, mouse_y - TOOLBAR)
                    last_pos = start_pos

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                mouse_x, mouse_y = event.pos

                if mouse_y > TOOLBAR:
                    new_pos = (mouse_x, mouse_y - TOOLBAR)

                    if current_tool == "brush":
                        pygame.draw.line(canvas, current_color, last_pos, new_pos, 5)

                    if current_tool == "eraser":
                        pygame.draw.line(canvas, WHITE, last_pos, new_pos, 25)

                    last_pos = new_pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                mouse_x, mouse_y = event.pos
                end_pos = (mouse_x, mouse_y - TOOLBAR)

                x1, y1 = start_pos
                x2, y2 = end_pos

                shape_rect = pygame.Rect(
                    min(x1, x2),
                    min(y1, y2),
                    abs(x2 - x1),
                    abs(y2 - y1)
                )

                if current_tool == "rect":
                    pygame.draw.rect(canvas, current_color, shape_rect, 3)

                if current_tool == "circle":
                    pygame.draw.ellipse(canvas, current_color, shape_rect, 3)

                drawing = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()