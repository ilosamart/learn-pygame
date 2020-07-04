import random
import time
import pygame
from pygame.locals import *


def sair():
    pygame.quit()
    quit()

def message(text, color):
    global screen
    global font_style
    text_box = font_style.render(text, True, color)
    text_rect = text_box.get_rect()
    text_rect.center = screen_limits[0]//2, screen_limits[1]//2
    pos_x = ( - text_box.get_height()//2)
    pos_y = (screen_limits[1] - text_box.get_width()) // 2
    screen.blit(text_box, text_rect)

def on_grid_random():
    global screen_point_size
    global screen_limits
    x = random.randint(0,screen_limits[0]-screen_point_size)
    y = random.randint(0,screen_limits[1]-screen_point_size)
    return (x//screen_point_size * screen_point_size, y//screen_point_size * screen_point_size)

def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

def initial_snake(starting_point, size):
    global screen_point_size
    snake = []
    for i in range(size-1):
        snake.append((starting_point[0] + (i*screen_point_size), starting_point[1]))
    return snake

# dimensões da tela
screen_point_size = 10
screen_limits = (800,800)
screen_center = (screen_limits[0]//2, screen_limits[1]//2)
game_paused = False
game_over = False
pontos = 0
speed = 10+10/(screen_point_size*10)

pygame.init()
screen = pygame.display.set_mode(screen_limits)
pygame.display.set_caption('Snake')
font_style = pygame.font.SysFont('Ubuntu', 50)

movement_directions = {
    K_UP: (0, -1 * screen_point_size),
    K_DOWN: (0, screen_point_size),
    K_LEFT: (-1 * screen_point_size, 0),
    K_RIGHT: (screen_point_size, 0),
}
horizontal_movement = (K_LEFT, K_RIGHT)
vertical_movement = (K_UP, K_DOWN)

#  objetos do jogo
snake = initial_snake((200, 200), 5)
snake_skin = pygame.Surface((screen_point_size,screen_point_size))
snake_skin.fill((0,200,0))

apple = on_grid_random()
apple_skin = pygame.Surface((screen_point_size,screen_point_size))
apple_skin.fill((255,0,0))

my_direction = K_LEFT

clock = pygame.time.Clock()

while not game_over:
    clock.tick(speed)

    # trata inputs do usuário
    for event in pygame.event.get():
        if event.type == QUIT:
            game_over = True

        if event.type == KEYDOWN:
            # se estou indo para a esquerda não posso ir para a direita (e vice-versa)
            # se estou indo para cima não posso ir para baixo (e vice-versa)
            if event.key in movement_directions.keys() and \
                (
                    (event.key in horizontal_movement and my_direction not in horizontal_movement) or \
                    (event.key in vertical_movement and my_direction not in vertical_movement)
                ):
                my_direction = event.key

            # se foi ESC, pause
            if event.key == K_ESCAPE:
                game_paused = True
                message(f'JOGO PAUSADO ({pontos} pontos)', (255,255,255))
                pygame.display.update()

    # jogo pausado
    while game_paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = True
                game_paused = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                game_paused = False
                        
    # atualiza a rodada
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])

    snake_diff = movement_directions[my_direction]
    snake_head_x = (snake[0][0] + snake_diff[0]) % screen_limits[0]
    snake_head_y = (snake[0][1] + snake_diff[1]) % screen_limits[1]
    snake[0] = (snake_head_x, snake_head_y)
    screen.fill((0,0,0))
    screen.blit(apple_skin, apple)
    for pos in snake:
        screen.blit(snake_skin,pos)

    

    # trata colisão
    for pedaco_corpo in snake[1:]:
        game_over = game_over or collision(snake[0], pedaco_corpo)

    # trata comer maçã
    if collision(snake[0], apple):
        apple = on_grid_random()
        snake.append((0,0))
        pontos += 10
        speed += 10/(screen_point_size*10)
        print(f'velocidade ({speed})')

    if not game_over:
        pygame.display.update()

    
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
message(f'GAME OVER: {pontos} pontos!',(255, 0, 0))
pygame.display.update()
time.sleep(2)
sair()