import pygame
import sys

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, int(900 / 2)))
    screen.blit(floor_surface, (floor_x_pos + int(576/2), int(900 / 2)))

pygame.init()
screen = pygame.display.set_mode((int(576/2), int(1024/2)))
clock = pygame.time.Clock() # sets frame rate

bg_surface = pygame.image.load('assets/background-day.png').convert()
floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(bg_surface, (0, 0))
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -int(576/2):
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)  # running at 120fps
