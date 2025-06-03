import sys
import pygame
import random


def show_image_and_text(image_path, text, screen, result):
    image = pygame.image.load(image_path)
    image_rect = image.get_rect(center=screen.get_rect().center)
    screen.blit(image, image_rect)

    font = pygame.font.Font(None, 40)
    text_surface = font.render(text, True, (170, 0, 0))
    text_rect = text_surface.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 + image.get_height() // 2 + 60))
    screen.blit(text_surface, text_rect)

    font = pygame.font.Font(None, 50)
    result_surface = font.render("Wynik: " + str(result), True, (170, 0, 0))
    result_rect = result_surface.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 + image.get_height() // 2 + 25))
    screen.blit(result_surface, result_rect)

    pygame.display.flip()


def show_lives(screen, hit, max_lives):
    heart_full = pygame.image.load("[Pliki]/Serca.png").convert_alpha()
    heart_empty = pygame.image.load("[Pliki]/Serce_Puste.png").convert_alpha()
    last_heart = pygame.image.load("[Pliki]/Serca_Ostatnie.png").convert_alpha()
    heart_size = heart_full.get_size()

    for i in range(max_lives):
        heart_rect = pygame.Rect(i * heart_size[0] + 10, 10, heart_size[0], heart_size[1])
        if i < hit:
            if i == 0 and hit == 1:
                pulsating = 5 * abs(pygame.time.get_ticks() % 1000 - 500) / 5000
                last_heart.set_alpha(int(255 * (1 - pulsating)))
                screen.blit(last_heart, heart_rect)
            else:
                screen.blit(heart_full, heart_rect)
        else:
            screen.blit(pygame.transform.scale(heart_empty, (int(heart_size[0] * 0.8), int(heart_size[1] * 0.8))),
                        heart_rect)


def gra():
    # inicjowanie Pygame
    pygame.init()

    # Wynik
    result = 0

    # ustawienie rozmiaru ekranu
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    # załadowanie tła
    background = pygame.image.load('[Pliki]/Tło.png')

    # załadowanie grafiki postaci
    player_image = pygame.image.load('[Pliki]/Gracz.png')

    # załadowanie grafiki kul
    ball_image = pygame.image.load('[Pliki]/Kula.png')

    # załadowanie grafiki nowego elementu
    Shoot = pygame.image.load('[Pliki]/Strzal.png')

    # pozycja postaci
    player_x = 80
    player_y = 300

    # prędkość poruszania postaci
    player_speed = 1.0

    # granice obszaru gry
    left_boundary = 0
    right_boundary = screen_width - player_image.get_width()
    top_boundary = 0
    bottom_boundary = screen_height - player_image.get_height()

    # Życie
    max_lives = 3
    hit = max_lives

    # lista kul
    balls = []

    # czas ostatniego wystrzelenia kuli
    last_ball_time = pygame.time.get_ticks()

    # pętla główna gry
    while True:
        # obsługa zdarzeń (klawiatura, mysz, zamknięcie okna)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # strzał
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                ball_x = player_x + player_image.get_width()
                ball_y = player_y + player_image.get_height() / 2
                ball_speed = 3.5
                balls.append({'x': ball_x, 'y': ball_y, 'speed': ball_speed, 'type': 'bullet'})

            # teleport do góry
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    player_y -= 60

            # teleport w dół
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    player_y += 60

        # poruszanie postaci
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= player_speed
            # ograniczenie ruchu w lewo
            if player_x < left_boundary:
                player_x = left_boundary
        if keys[pygame.K_d]:
            player_x += player_speed
            # ograniczenie ruchu w prawo
            if player_x > right_boundary:
                player_x = right_boundary
        if keys[pygame.K_w]:
            player_y -= player_speed
            # ograniczenie ruchu w górę
            if player_y < top_boundary:
                player_y = top_boundary
        if keys[pygame.K_s]:
            player_y += player_speed
            # ograniczenie ruchu w dół
            if player_y > bottom_boundary:
                player_y = bottom_boundary

        # generowanie kuli
        current_time = pygame.time.get_ticks()
        time_since_last_ball = current_time - last_ball_time
        if time_since_last_ball > random.randint(0, 100) and len(balls) < 5:
            ball_x = screen_width
            ball_y = random.randint(0, screen_height - ball_image.get_height())
            ball_speed = random.uniform(1.0, 2.5)
            balls.append({'x': ball_x, 'y': ball_y, 'speed': ball_speed, 'type': 'ball'})
            last_ball_time = current_time

        # poruszanie kul
        for ball in balls:
            if ball['type'] == 'ball':
                ball['x'] -= ball['speed']
            else:
                ball['x'] += ball['speed']

            # usunięcie kul, które wyleciały poza ekran
            if ball['type'] == 'ball' and ball['x'] < -ball_image.get_width() \
                    or ball['type'] == 'bullet' and ball['x'] > screen_width:
                balls.remove(ball)

            # detekcja kolizji z postacią
            if ball['type'] == 'ball' and \
                    player_x < ball['x'] + ball_image.get_width() and \
                    player_x + player_image.get_width() > ball['x'] and \
                    player_y < ball['y'] + ball_image.get_height() and \
                    player_y + player_image.get_height() > ball['y']:
                hit -= 1
                result -= 23
                balls.remove(ball)
                # warunek kończący grę
                if hit == 0:
                    screen.fill((0, 0, 0))
                    for i in range(3, 0, -1):
                        screen.fill((0, 0, 0))
                        show_image_and_text('[Pliki]/Koniec.png', str(i), screen, result)
                        pygame.time.wait(900)
                    return
                # TODO: obsługa kolizji z kulką

            # detekcja kolizji ze strzałem, i zmiana wielkości
            for ball in balls[:]:
                if ball['type'] == 'bullet':
                    ball_rect = pygame.Rect(ball['x'], ball['y'], Shoot.get_width() + 5,
                                            Shoot.get_height() + 10)  # zwiększenie hitboxa
                    ball_rect.x += ball['speed']
                    for ball2 in balls:
                        if ball2['type'] == 'ball':
                            ball2_rect = pygame.Rect(ball2['x'], ball2['y'], ball_image.get_width() + 10,
                                                     ball_image.get_height() + 20)  # zwiększenie hitboxa
                            if ball_rect.colliderect(ball2_rect):
                                balls.remove(ball)
                                balls.remove(ball2)
                                result += random.randint(10, 70)
                                break
                    if ball_rect.x > screen.get_width():
                        balls.remove(ball)
                    else:
                        screen.blit(Shoot, ball_rect)

        # rysowanie obiektów na ekranie
        screen.blit(background, (0, 0))
        screen.blit(player_image, (player_x, player_y))
        for ball in balls:
            if ball['type'] == 'ball':
                screen.blit(ball_image, (ball['x'], ball['y']))
            else:
                screen.blit(Shoot, (ball['x'], ball['y']))

        # rysowanie tekstu
        show_lives(screen, hit, max_lives)

        # aktualizacja ekranu
        pygame.display.update()


if __name__ == "__main__":
    while True:
        gra()
