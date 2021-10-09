import pygame
import sys


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, int(900 / 2)))
    screen.blit(floor_surface, (floor_x_pos + int(576 / 2), int(900 / 2)))


pygame.init()

screen = pygame.display.set_mode((int(576 / 2), int(1024 / 2)))
clock = pygame.time.Clock()  # sets frame rate

# game variables
gravity = 0.25
bird_movement = 0

# surfaces
bg_surface = pygame.image.load('assets/background-day.png').convert()
floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_rect = bird_surface.get_rect(center=(int(100 / 2), int(512 / 2)))  # rects detect collisions

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 6

    screen.blit(bg_surface, (0, 0))

    bird_movement += gravity
    bird_rect.centery += bird_movement

    screen.blit(bird_surface, bird_rect)
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -int(576 / 2):
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)  # running at 120fps
