import pygame
from datetime import datetime
from tools import draw_shape, flood_fill

pygame.init()

WIDTH, HEIGHT = 1000, 600
TOOLBAR = 95
CANVAS_HEIGHT = HEIGHT - TOOLBAR

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2 Paint Application")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
    (255, 192, 203),
]

tools = [
    "pencil", "line", "rect", "circle", "square",
    "right tri", "eq tri", "rhombus", "fill", "text", "eraser", "clear"
]

current_color = BLACK
current_tool = "pencil"
brush_size = 5

canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

font = pygame.font.SysFont("Arial", 15)
small_font = pygame.font.SysFont("Arial", 13)
text_font = pygame.font.SysFont("Arial", 28)
clock = pygame.time.Clock()

drawing = False
start_pos = None
last_pos = None

text_mode = False
text_pos = None
text_value = ""


def to_canvas_pos(pos):
    return pos[0], pos[1] - TOOLBAR


def inside_canvas(pos):
    x, y = pos
    return 0 <= x < WIDTH and TOOLBAR <= y < HEIGHT


def save_canvas():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"paint_{timestamp}.png"
    pygame.image.save(canvas, filename)
    print(f"Saved: {filename}")


def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR))

    x = 8
    y = 10
    button_w = 74
    button_h = 28

    for tool in tools:
        button = pygame.Rect(x, y, button_w, button_h)
        pygame.draw.rect(screen, (160, 160, 160) if tool == current_tool else WHITE, button)
        pygame.draw.rect(screen, BLACK, button, 2)

        label = small_font.render(tool, True, BLACK)
        screen.blit(label, (x + 4, y + 7))

        x += button_w + 5

        if x + button_w > WIDTH - 10:
            x = 8
            y += 35

    color_x = 8
    color_y = 58

    for color in colors:
        color_button = pygame.Rect(color_x, color_y, 26, 26)
        pygame.draw.rect(screen, color, color_button)
        pygame.draw.rect(screen, BLACK, color_button, 2)

        if color == current_color:
            pygame.draw.rect(screen, BLACK, color_button, 4)

        color_x += 32

    size_x = 300
    size_y = 58

    for label, size in [("S small", 2), ("M med", 5), ("L large", 10)]:
        rect = pygame.Rect(size_x, size_y, 75, 26)
        pygame.draw.rect(screen, (160, 160, 160) if brush_size == size else WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        text = small_font.render(label, True, BLACK)
        screen.blit(text, (size_x + 5, size_y + 6))

        size_x += 82

    info = font.render(
        f"Tool: {current_tool} | Size: {brush_size}px | Ctrl+S: save | Text: Enter confirm, Esc cancel",
        True,
        BLACK
    )
    screen.blit(info, (560, 62))


def handle_toolbar_click(pos):
    global current_tool, current_color, brush_size
    global text_mode, text_value, text_pos

    x = 8
    y = 10
    button_w = 74
    button_h = 28

    for tool in tools:
        button = pygame.Rect(x, y, button_w, button_h)

        if button.collidepoint(pos):
            if tool == "clear":
                canvas.fill(WHITE)
            else:
                current_tool = tool
                text_mode = False
                text_value = ""
                text_pos = None
            return

        x += button_w + 5

        if x + button_w > WIDTH - 10:
            x = 8
            y += 35

    color_x = 8
    color_y = 58

    for color in colors:
        color_button = pygame.Rect(color_x, color_y, 26, 26)

        if color_button.collidepoint(pos):
            current_color = color
            return

        color_x += 32

    size_x = 300
    size_y = 58

    for size in [2, 5, 10]:
        size_button = pygame.Rect(size_x, size_y, 75, 26)

        if size_button.collidepoint(pos):
            brush_size = size
            return

        size_x += 82


preview_tools = ["line", "rect", "circle", "square", "right tri", "eq tri", "rhombus"]

running = True

while running:
    screen.fill(WHITE)

    mouse_pos = pygame.mouse.get_pos()
    canvas_pos = to_canvas_pos(mouse_pos)

    if drawing and current_tool in preview_tools and start_pos is not None and inside_canvas(mouse_pos):
        preview = canvas.copy()
        draw_shape(preview, current_tool, current_color, start_pos, canvas_pos, brush_size)
        screen.blit(preview, (0, TOOLBAR))
    else:
        screen.blit(canvas, (0, TOOLBAR))

    if text_mode and text_pos is not None:
        cursor_x, cursor_y = text_pos
        text_surface = text_font.render(text_value, True, current_color)

        screen.blit(text_surface, (cursor_x, cursor_y + TOOLBAR))

        cursor_offset = text_surface.get_width() + 2
        pygame.draw.line(
            screen,
            current_color,
            (cursor_x + cursor_offset, cursor_y + TOOLBAR),
            (cursor_x + cursor_offset, cursor_y + TOOLBAR + 28),
            2
        )

    draw_toolbar()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if event.key == pygame.K_s and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                save_canvas()

            elif text_mode:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    final_text = text_font.render(text_value, True, current_color)
                    canvas.blit(final_text, text_pos)
                    text_mode = False
                    text_value = ""
                    text_pos = None

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_value = ""
                    text_pos = None

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

            elif event.key == pygame.K_s:
                brush_size = 2

            elif event.key == pygame.K_m:
                brush_size = 5

            elif event.key == pygame.K_l:
                brush_size = 10

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[1] < TOOLBAR:
                    handle_toolbar_click(event.pos)

                elif inside_canvas(event.pos):
                    pos = to_canvas_pos(event.pos)

                    if current_tool == "fill":
                        flood_fill(canvas, pos, current_color)

                    elif current_tool == "text":
                        text_mode = True
                        text_pos = pos
                        text_value = ""

                    else:
                        drawing = True
                        start_pos = pos
                        last_pos = pos

        elif event.type == pygame.MOUSEMOTION:
            if drawing and inside_canvas(event.pos):
                new_pos = to_canvas_pos(event.pos)

                if current_tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, new_pos, brush_size)

                elif current_tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, new_pos, brush_size * 3)

                last_pos = new_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                if inside_canvas(event.pos):
                    end_pos = to_canvas_pos(event.pos)

                    if current_tool in preview_tools:
                        draw_shape(canvas, current_tool, current_color, start_pos, end_pos, brush_size)

                drawing = False
                start_pos = None
                last_pos = None

    pygame.display.flip()
    clock.tick(60)

pygame.quit()