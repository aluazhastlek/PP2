def run_game():
    import pygame

    pygame.init()

    height=600
    width=600
    radius=25
    step=20
    red=(255,0,0)
    white=(255,255,255)

    screen=pygame.display.set_mode((width, height))
    pygame.display.set_caption("GAME: Moving Ball")

    x,y=width//2, height//2
    clock = pygame.time.Clock()

    running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x = min(x + step, width - radius)
                if event.key == pygame.K_LEFT:
                    x = max(x - step, radius)
                if event.key == pygame.K_UP:
                    y = max(y - step, radius)
                if event.key == pygame.K_DOWN:
                    y = min(y + step, height - radius)
                    
        screen.fill(white)
        pygame.draw.circle(screen, red, (x,y), radius)

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()