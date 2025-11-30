
"""

Nesse início aqui a gente faz as importações principais, sendo a geração aleatória, as funções matemáticas e o próprio Pygame, que é a ferramenta
que utilizaremos na produção do jogo.

"""

import pygame as pg
import random as rnd
import math

# Aqui carregamos o ícone de forma direta.
icon = pg.image.load("images/icon.png")

# Aqui inicializamos o Pygame e a definição do ícone da aplicação.
pg.init()
pg.display.set_icon(icon)

# CONFIGURAÇÃO DE TELA

# Aqui definimos a largura, altura, título da janela e a própria tela do jogo.
scr_width = 1920
scr_height = 1080
scr = pg.display.set_mode((scr_width, scr_height), pg.FULLSCREEN)
pg.display.set_caption("PyPong Casino")

# MENUS

# Aqui é o dicionário que será usado para definir uma identificação para o Menu e para a tela do jogo.
screens = {"MENU": 0, "GAME": 1}
current_screen_state = screens["MENU"]

# CORES E FONTES

# Aqui definimos 3 padrões de cores para evitar repetições e também definimos as fontes que será usada para o FPS (Frames Per Second ou Frames Por Segundo) e para as opções/pontuação.
WHITE = (255, 255, 255)
GOLD = (245, 200, 39)
BLACK = (0, 0, 0)
game_font = pg.font.Font("pixelate.ttf", 40)
fps_font = pg.font.Font("pixelate.ttf", 16)

# Aqui definimos a cor dos textos para poder fazer uma alteração entre a cor Branca e a cor Dourada, para podermos saber qual opção foi selecionada.
# E também definimos a variável "verdadeira" para dizermos se o jogo está rodando ou não, e definimos a variável que dirá qual opção foi selecionada no momento.
run = True
menu_option = 0
play_colour = GOLD
quit_colour = WHITE

# Aqui definimos o Clock, que será utilizado par definir o FPS da janela, juntamente da variável que define quantos de fps teremos no jogo.
clock = pg.time.Clock()
fps = 60

## GAME
# Aqui é a pontuação de ambos os jogadores
game_score = [0,0]

# IMAGENS
# Aqui definimos o dicionário que armazanerará as imagens, e também um try & except para evitar problemas no jogo quando carregamos as imagens.
image_resources = {}
try:
    image_resources.update({
        'ball': pg.image.load("images/ball2.png"),
        'player': pg.image.load("images/bar_hidden.png"),
        'logo' : pg.image.load("images/logo.png"),
        'dindin' : pg.image.load("images/dindin.png"),
        "gmbg" : pg.image.load("images/bg.png"),
        "p1hand" : pg.image.load("images/hand1.png"),
        "p2hand" : pg.image.load("images/hand2.png"),
        "wood" : pg.image.load("images/wood.png"),
    })
except pg.error as e:
    print("An error occurred while trying to load image:", e)
    pg.quit()
    exit()
    
# LOGO
# Aqui é a definição dos sprites com o alpha convertido (para imagens transparentes).
# Primeiro que é o nome da imagem, é a imagem selecionada do dicionário e que tem seu alpha convertido para ficar transparente
# As variáveis que tiverem o nome da imagem juntamente de "_rect" é onde vai pegar o retângulo da imagem para definir sua posição na tela.

game_logo = image_resources['logo'].convert_alpha()
game_logo_rect = game_logo.get_rect(center=(scr_width // 2, (scr_height // 2)-120))

# GAME BACKGROUND
game_bg = image_resources['gmbg'].convert_alpha()
game_bg = pg.transform.scale(game_bg, (scr_width, scr_height-200))
game_bg_rect = game_bg.get_rect(center=(scr_width // 2, scr_height // 2))

""" 
Nessa parte em específico da variável "wood_bg" até o laço de repetição "for", é a geração do fundo, onde pegará a imagem "wood" da lista de sprites
e irá repetir essa imagem em pisos até cobrir a tela toda.
"""
wood_bg = image_resources["wood"].convert_alpha()
wbg_width, wbg_height = wood_bg.get_size()

tile_surf = pg.Surface((scr_width, scr_height))
tile_x = math.ceil(scr_width / wbg_width)
tile_y = math.ceil(scr_height / wbg_height)

for x in range(tile_x):
    print(f"Generate X-#{x}")
    for y in range(tile_y):
        print(f"Generate Y-#{y}")
        tile_surf.blit(wood_bg, (x*wbg_width, y*wbg_height))

# BALL
# Aqui definimos as configurações da bola, no caso seu ângulo (para podermos fazê-la girar enquanto vai de um canto para o outro), sua força mínima e máxima para acelerar
# qualquer tipo de alteração, sua força atual e sua força na direção horizontal (x) e vertical (y).
ball_angle = 25
ball_force_min = 8
ball_force_max = 20
ball_force = ball_force_min
force_x = ball_force
force_y = ball_force

# Aqui definimos sua imagem e transformamos a imagem para alterar suas dimensões.
ball_original = image_resources['ball'].convert_alpha()
ball_original = pg.transform.scale(ball_original, (24, 24))
ball = ball_original.copy()
ball_rect = ball.get_rect(center=(scr_width // 2, scr_height // 2))

# PLAYER
# Aqui teremos as imagens de ambos os jogadores.
player = image_resources['player'].convert_alpha()
player = pg.transform.scale(player, (15, 98))
player_rect1 = player.get_rect(topleft=(80, scr_height // 2))
player_rect2 = player.get_rect(topleft=(scr_width - 80, scr_height // 2))

player1_hand = image_resources["p1hand"].convert_alpha()
player1_hand = pg.transform.scale(player1_hand, (200, 80))
player2_hand = image_resources["p2hand"].convert_alpha()
player2_hand = pg.transform.scale(player2_hand, (200, 80))

# Aqui é as configurações dos jogadores, que ficou obsoleto devido a alterações de último minuto, só o "speed" dos dicionários é usado.
PLAYERS_CONFIG = {"Player1": {"speed": 8}, "Player2": {"speed": 8}}
PLAYERS_CAN_MOVE = False

# Aqui são funções onde:

""" 

display_fps: Mostra o FPS no canto da tela e a atualiza a cada frame.
get_collision_side: Pega a direção que a bola teve contato com um dos jogadores.
new_score: Acrescenta o score ao jogador vencedor, essa função ficou obsoleto.

"""
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
# Aqui é o laço de repetição while que é usado para a lógica do jogo em si
while run:
    # Essa parte é os eventos atuais, que é usado para dizer para o pygame que quando o jogo encerra, o loop while também é quebrado, e também diz ao jogo qual estado atual da tela,
    # se está no Jogo ou no Menu.
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
    # Aqui é a lógica do Menu
    if current_screen_state == screens["MENU"]:
        scr.fill(BLACK) # Deixa a tela preta para reiniciar o frame
        
        # Aqui define os textos de Jogar e Sair, juntamente com suas posições e coloração.
        play_text = game_font.render("Jogar", True, play_colour)
        quit_text = game_font.render("Sair", True, quit_colour)
        play_rect = play_text.get_rect(center=(scr_width // 2, scr_height // 2 + 20))
        quit_rect = quit_text.get_rect(center=(scr_width // 2, scr_height // 2 + 80))
        
        # Desenha os sprites na tela (no caso os textos)
        scr.blit(game_logo, game_logo_rect)
        scr.blit(play_text, play_rect)
        scr.blit(quit_text, quit_rect)

        # Define a coloração dos textos baseado no menu_option        
        if menu_option == 0:
            play_colour = GOLD
            quit_colour = WHITE
        else:
            play_colour = WHITE
            quit_colour = GOLD

    # GAME
    # Aqui é a lógica do jogo
    elif current_screen_state == screens["GAME"]:

        # UPDATE & SHOW FPS
        scr.fill(BLACK)
        display_fps(scr, clock, fps_font, (10, 10)) # Desenha o FPS no canto da tela

        # BALL FORCE & ANGLE
        # Define a posição e ângulo na bola baseado na força x e y, e seu ângulo.
        # Também vai acelerando a bola conforme a pontuação demora.
        ball_rect.x += force_x
        ball_rect.y += force_y
        ball_angle += ball_force
        ball_force += .005
        
        # Aqui define seu ângulo máximo e sua força máxima para evitar problemas.
        if (ball_force > ball_force_max):
            ball_force = ball_force_max

        if ball_angle >= 360:
            ball_angle = 0

        # Aqui define um limite da bola na tela para quando bater no topo ou no chão para fazê-la ir na direção oposta
        if ball_rect.top <= 0 or ball_rect.bottom >= scr_height:
            force_y *= -1

        # Aqui define a posição da bola e sua transformação para poder alterar seu ângulo constantemente sem afetar a colisão da bola ou seu posicionamento
        rotated_ball = pg.transform.rotate(ball_original, ball_angle)
        rotated_rect = rotated_ball.get_rect(center=ball_rect.center)

        # BALL COLLISION
        # Aqui é para alterar o envio de força da bola baseado no jogador que ela colidiu
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
        # Aqui limitamos os jogadores o quão alto ou quão baixo eles conseguem ir
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
        # Aqui verificamos as teclas dos jogadores que foram apertadas para dizer ao jogo se o jogaodor move pra cima ou pra baixo.
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
        # Aqui é a lógica de pontuação, onde dizemos a posição da bola para saber se ultrapassou em alguma das bordas, e dizer qual jogador recebeu a pontuação
        # , onde também resetamos a bola para o centro e enviá-la ao jogador que perdeu.
        if ball_rect.left <= -80:  # PLAYER 2 WON
            new_score("P2")
            ball_force = ball_force_min
            ball_rect.x = scr_width / 2
            ball_rect.y = scr_height / 2
            force_x = -ball_force
            force_y = ball_force

        elif ball_rect.right >= scr_width + 80:  # PLAYER 1 WON
            new_score("P1")
            ball_force = ball_force_min
            ball_rect.x = scr_width // 2
            ball_rect.y = scr_height // 2
            force_x = ball_force
            force_y = ball_force

        # DRAW TEXT SCORES
        # Aqui desenhamos tudo, sendo o texto de pontuação e as imagens (sprites).
        score_text = game_font.render(f"{game_score[0]} - {game_score[1]}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(scr_width // 2, 45))

        scr.blit(tile_surf, (0,0))
        scr.blit(game_bg, game_bg_rect)
        scr.blit(score_text, score_rect)

        # DRAW SPRITES ON SCREEN
        scr.blit(rotated_ball, rotated_rect)
        scr.blit(player, player_rect1)
        scr.blit(player, player_rect2)
        scr.blit(player1_hand, (player_rect1.x-160, player_rect1.y))
        scr.blit(player2_hand, (player_rect2.x-40, player_rect2.y))

    # Aqui refrescamos a tela e damos um "tick" para atualizar o fps (no caso sempre usar o relógio para atualizar a variável do FPS).
    pg.display.flip()
    clock.tick(fps)

# Aqui fechamos o jogo caso o laço while se quebre usando "break" ou deixando a variável "run" falsa.
pg.quit()

