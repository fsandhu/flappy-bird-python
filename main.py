import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, int(900 / 2)))
    screen.blit(floor_surface, (floor_x_pos + int(576 / 2), int(900 / 2)))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(int(700 / 2), random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(int(700 / 2), random_pipe_pos - 150))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= int(1024 / 2):
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -50 or bird_rect.bottom >= int(900 / 2):
        return False

    return True


pygame.init()

screen = pygame.display.set_mode((int(576 / 2), int(1024 / 2)))
clock = pygame.time.Clock()  # sets frame rate

# game variables
gravity = 0.2
bird_movement = 0
game_active = True

# surfaces
bg_surface = pygame.image.load('assets/background-day.png').convert()
floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0

bird_surface = pygame.image.load('assets/redbird-midflap.png').convert()
bird_rect = bird_surface.get_rect(center=(int(100 / 2), int(512 / 2)))  # rects detect collisions

pipe_surface = pygame.image.load('assets/pipe-red.png').convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 300, 400]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 4
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                pipe_height.clear()
                bird_rect.center = (int(100 / 2), int(512 / 2))
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface, (0, 0))

    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement

        screen.blit(bird_surface, bird_rect)

        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -int(576 / 2):
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)  # running at 120fps
