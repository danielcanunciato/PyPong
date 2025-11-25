from idlelib.autocomplete import FORCE
from idlelib.configdialog import changes

import pygame as pg
import random as rnd

pg.init()

# CONFIGURAÇÃO DE TELA
scr_width = 800
scr_height = 500
scr = pg.display.set_mode((scr_width, scr_height))
pg.display.set_caption("PyPong Cassino")

# MENUS
screens = {"MENU": 0, "GAME": 1}
current_screen_state = screens["MENU"]

# CORES E FONTES
WHITE = (255, 255, 255)
GOLD = (245, 200, 39)
BLACK = (0, 0, 0)
game_font = pg.font.Font("pixelate.ttf", 40)
fps_font = pg.font.Font("pixelate.ttf", 16)

run = True
menu_option = 0
play_colour = GOLD
quit_colour = WHITE

clock = pg.time.Clock()
fps = 60

## GAME
game_score = [0,0]

# IMAGENS
image_resources = {}
try:
    image_resources.update({
        'ball': pg.image.load("images/ball2.png"),
        'player': pg.image.load("images/bar.png"),
    })
except pg.error as e:
    print("An error occurred while trying to load image:", e)
    pg.quit()
    exit()

# BALL
ball_angle = 25
ball_force = 5
ball_force_max = 20
force_x = ball_force
force_y = ball_force

ball_original = image_resources['ball'].convert_alpha()
ball_original = pg.transform.scale(ball_original, (24, 24))
ball = ball_original.copy()
ball_rect = ball.get_rect(center=(scr_width // 2, scr_height // 2))

# PLAYER
player = image_resources['player'].convert_alpha()
player_rect1 = player.get_rect(topleft=(10, scr_height // 2))
player_rect2 = player.get_rect(topleft=(scr_width - 40, scr_height // 2))

PLAYERS_CONFIG = {"Player1": {"speed": 8}, "Player2": {"speed": 8}}
PLAYERS_CAN_MOVE = False

def display_fps(screen, c, font, position):
    fps_text = font.render(f"FPS: {int(c.get_fps())}", True, WHITE)
    screen.blit(fps_text, position)

def get_collision_side(ballRect, plrRect):
    dx = (ballRect.centerx - plrRect.centerx) / plrRect.width
    dy = (ballRect.centery - plrRect.centery) / plrRect.height

    abs_dx = abs(dx)
    abs_dy = abs(dy)

    if abs_dx > abs_dy:
        return "left" if dx < 0 else "right"
    else:
        return "top" if dy < 0 else "bottom"

def new_score(player_that_won):
    global game_score
    global ON_COUNTDOWN
    global PREPARE_COUNTDOWN
    global LAST_WON

    if player_that_won == "P1":
        game_score[0] += 1

        if not ON_COUNTDOWN:
            ON_COUNTDOWN = True
            PREPARE_COUNTDOWN = 3
            LAST_WON = "PLAYER 1"

    else:
        game_score[1] += 1

        if not ON_COUNTDOWN:
            ON_COUNTDOWN = True
            PREPARE_COUNTDOWN = 3
            LAST_WON = "PLAYER 2"

ON_COUNTDOWN = False
PREPARE_COUNTDOWN = 0
LAST_WON = ""

# LOOP PRINCIPAL
while run:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run = False

        if i.type == pg.KEYDOWN:
            if current_screen_state == screens["MENU"]:
                if i.key == pg.K_UP:
                    menu_option = 0
                elif i.key == pg.K_DOWN:
                    menu_option = 1
                elif i.key == pg.K_RETURN:
                    if menu_option == 0:
                        current_screen_state = screens["GAME"]
                    else:
                        run = False

    # MENU
    if current_screen_state == screens["MENU"]:
        scr.fill(BLACK)
        play_text = game_font.render("Jogar", True, play_colour)
        quit_text = game_font.render("Sair", True, quit_colour)
        play_rect = play_text.get_rect(center=(scr_width // 2, scr_height // 2 - 20))
        quit_rect = quit_text.get_rect(center=(scr_width // 2, scr_height // 2 + 40))
        scr.blit(play_text, play_rect)
        scr.blit(quit_text, quit_rect)

        if menu_option == 0:
            play_colour = GOLD
            quit_colour = WHITE
        else:
            play_colour = WHITE
            quit_colour = GOLD

    # GAME
    elif current_screen_state == screens["GAME"]:

        # UPDATE & SHOW FPS
        scr.fill(BLACK)
        display_fps(scr, clock, fps_font, (10, 10))

        # BALL FORCE & ANGLE
        ball_rect.x += force_x
        ball_rect.y += force_y
        ball_angle += ball_force
        ball_force += .005
        
        if (ball_force > ball_force_max):
            ball_force = ball_force_max

        if ball_angle >= 360:
            ball_angle = 0

        if ball_rect.top <= 0 or ball_rect.bottom >= scr_height:
            force_y *= -1

        rotated_ball = pg.transform.rotate(ball_original, ball_angle)
        rotated_rect = rotated_ball.get_rect(center=ball_rect.center)

        # BALL COLLISION
        if ball_rect.colliderect(player_rect1) or ball_rect.colliderect(player_rect2):
            side = get_collision_side(ball_rect, player_rect1) if ball_rect.colliderect(
                player_rect1) else get_collision_side(ball_rect, player_rect2)
            who = "P1" if ball_rect.colliderect(player_rect1) else "P2"

            if side in ("left", "right", "top", "bottom"):
                if who == "P1":
                    force_x = ball_force
                else:
                    force_x = -ball_force

        ## PLAYERS COLLISION
        #PLAYER 1
        if player_rect1.y < 10:
            player_rect1.y = 10
        elif player_rect1.y > (scr_height-90):
            player_rect1.y = (scr_height-90)

        #PLAYER 2
        if player_rect2.y < 10:
            player_rect2.y = 10
        elif player_rect2.y > (scr_height-90):
            player_rect2.y = (scr_height-90)

        # CHECK PLAYERS KEY PRESSES
        gKeys = pg.key.get_pressed()

        if gKeys[pg.K_w]:
            player_rect1.y -= PLAYERS_CONFIG["Player1"]["speed"]
        if gKeys[pg.K_s]:
            player_rect1.y += PLAYERS_CONFIG["Player1"]["speed"]

        if gKeys[pg.K_UP]:
            player_rect2.y -= PLAYERS_CONFIG["Player2"]["speed"]
        if gKeys[pg.K_DOWN]:
            player_rect2.y += PLAYERS_CONFIG["Player2"]["speed"]

        # SCORING
        if ball_rect.left <= -80:  # PLAYER 2 WON
            new_score("P2")
            ball_force = 5
            ball_rect.x = scr_width / 2
            ball_rect.y = scr_height / 2
            force_x = -ball_force
            force_y = ball_force

        elif ball_rect.right >= scr_width + 80:  # PLAYER 1 WON
            new_score("P1")
            ball_force = 5
            ball_rect.x = scr_width // 2
            ball_rect.y = scr_height // 2
            force_x = ball_force
            force_y = ball_force

        # DRAW TEXT SCORES
        score_text = game_font.render(f"{game_score[0]} - {game_score[1]}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(scr_width // 2, 45))

        scr.blit(score_text, score_rect)
        
        print(ball_force)

        # DRAW SPRITES ON SCREEN
        scr.blit(rotated_ball, rotated_rect)
        scr.blit(player, player_rect1)
        scr.blit(player, player_rect2)

    pg.display.flip()
    clock.tick(fps)

pg.quit()
