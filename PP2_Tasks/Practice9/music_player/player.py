import pygame
import os

def run_player():
    pygame.init()
    pygame.mixer.init()

    width, height=800, 400
    screen=pygame.display.set_mode((width, height))
    pygame.display.set_caption("Music Player")

    background=(77,198,198)
    black=(0,0,0)
    textcolor=(128,0,0)

    font=pygame.font.SysFont("Calibri", 28)
    small_font=pygame.font.SysFont("Calibri", 22)
    
    title_font = pygame.font.SysFont("Calibri", 36)
    title_font.set_bold(True)
    
    music_folder="music"
    playlist=[
        os.path.join(music_folder, "bvlbrown.wav"), 
        os.path.join(music_folder, "zanovo.wav"), 
        os.path.join(music_folder, "romance.wav"),
    ]

    current_track=0
    is_playing=False
    is_paused = False
    paused_position_sec = 0

    def load_track(index):
        pygame.mixer.music.load(playlist[index])

    def play_track():
        nonlocal is_playing, is_paused

        if is_paused:
            pygame.mixer.music.unpause()
            is_playing = True
            is_paused = False
        else:
            load_track(current_track)
            pygame.mixer.music.play()
            is_playing = True
            is_paused = False

    def pause_track():
        nonlocal is_playing, is_paused, paused_position_sec

        if is_playing:
            position_ms = pygame.mixer.music.get_pos()
            if position_ms < 0:
                position_ms = 0
            paused_position_sec = position_ms // 1000

            pygame.mixer.music.pause()
            is_playing = False
            is_paused = True
    
    def stop_track():
        nonlocal is_playing, is_paused, paused_position_sec

        pygame.mixer.music.stop()
        is_playing = False
        is_paused = False
        paused_position_sec = 0
    
    def next_track():
        nonlocal current_track, is_playing, is_paused, paused_position_sec
        current_track = (current_track + 1) % len(playlist)
        load_track(current_track)
        pygame.mixer.music.play()
        is_playing = True
        is_paused = False
        paused_position_sec = 0
    
    def previous_track():
        nonlocal current_track, is_playing, is_paused, paused_position_sec
        current_track = (current_track - 1) % len(playlist)
        load_track(current_track)
        pygame.mixer.music.play()
        is_playing = True
        is_paused = False
        paused_position_sec = 0

    load_track(current_track)
    clock=pygame.time.Clock()
    running=True

    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    play_track()

                if event.key == pygame.K_SPACE:
                    pause_track()

                if event.key == pygame.K_s:
                    stop_track()

                if event.key == pygame.K_n:
                    next_track()

                if event.key == pygame.K_b:
                    previous_track()

                if event.key == pygame.K_q:
                    running = False

        screen.fill(background)

        title_text = title_font.render("MUSIC PLAYER", True, textcolor)
        screen.blit(title_text, (320,30))

        lines = [
            "P = Play / Resume",
            "SPACE = Pause",
            "S = Stop",
            "N = Next",
            "B = Back",
            "Q = Quit"
        ]
        y = 10
        for line in lines:
            text = small_font.render(line, True, textcolor)
            screen.blit(text, (600, y))
            y += 30

        track_name=os.path.basename(playlist[current_track])
        track_text=font.render(f"Current track: {track_name}", True, textcolor)
        screen.blit(track_text, (160,100))

        if is_playing:
            status = "Playing"
        elif is_paused:
            status = "Paused"
        else:
            status = "Stopped"
        track_text=font.render(f"Status: {status}", True, textcolor)
        screen.blit(track_text, (160,150))

        if is_playing:
            position_ms = pygame.mixer.music.get_pos()
            if position_ms < 0:
                position_ms = 0
            position_sec = position_ms // 1000

        elif is_paused:
            position_sec = paused_position_sec

        else:
            position_sec = 0

        progress_text=font.render(f"Position: {position_sec} sec", True, textcolor)
        screen.blit(progress_text, (160,220))

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()