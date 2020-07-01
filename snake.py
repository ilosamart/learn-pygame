import pygame, random
from pygame.locals import *


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
screen_point_size = 20
screen_limits = (800,800)
screen_center = (screen_limits[0]//2, screen_limits[1]//2)
game_paused = False

pygame.init()
screen = pygame.display.set_mode(screen_limits)
pygame.display.set_caption('Snake')

movement_directions = {
    K_UP: (0, -1 * screen_point_size),
    K_DOWN: (0, screen_point_size),
    K_LEFT: (-1 * screen_point_size, 0),
    K_RIGHT: (screen_point_size, 0),
}
horizontal_movement = (K_LEFT, K_RIGHT)
vertical_movement = (K_UP, K_DOWN)

#  objetos do jogo
snake = initial_snake((200, 200), 20)
snake_skin = pygame.Surface((screen_point_size,screen_point_size))
snake_skin.fill((0,200,0))

apple = on_grid_random()
apple_skin = pygame.Surface((screen_point_size,screen_point_size))
apple_skin.fill((255,0,0))

my_direction = K_LEFT

clock = pygame.time.Clock()

while True:
    clock.tick(10)

    # trata colisão
    if collision(snake[0], apple):
        apple = on_grid_random()
        snake.append((0,0))

    # trata inputs do usuário
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            # se estou indo para a esquerda não posso ir para a direita (e vice-versa)
            # se estou indo para cima não posso ir para baixo (e vice-versa)
            if event.key in movement_directions.keys() and \
                (
                    (event.key in horizontal_movement and my_direction not in horizontal_movement) or \
                    (event.key in vertical_movement and my_direction not in vertical_movement)
                ):
                my_direction = event.key

            if event.key == K_ESCAPE:
                game_paused = True

    # pause
    while game_paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            
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

    pygame.display.update()

    


# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()