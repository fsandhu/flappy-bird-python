#!/usr/bin/env python

__author__ = "Fateh Sandhu"
__email__ = "fatehkaran@huskers.unl.edu"

"""
Flappy Bird created in PyGame
twas' a fun little project
"""

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
            death_sound.play()
            return False

    if bird_rect.top <= -50 or bird_rect.bottom >= int(900 / 2):
        death_sound.play()
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -(bird_movement * 4), 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(int(100 / 2), bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(122, 25))
        screen.blit(high_score_surface, high_score_rect)


pygame.init()

screen = pygame.display.set_mode((int(576 / 2), int(1024 / 2)))
clock = pygame.time.Clock()  # sets frame rate
game_font = pygame.font.Font('04B_19.ttf', 20)

# game variables
gravity = 0.2
bird_movement = 0
game_active = False
gameStart = True
score = 0
f = open('highScore', 'r')
high_score = int(f.read())
f.close()

# surfaces
bg_surface = pygame.image.load('assets/background-night.png').convert()
floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0

bird_up = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_mid = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_down = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_frames = [bird_down, bird_mid, bird_up]  # animates the bird
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(int(100 / 2), int(512 / 2)))  # rects detect collisions

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('assets/pipe-red.png').convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200 - int(score))
pipe_height = [200, 300, 400]

game_over_surface = pygame.image.load('assets/gameover.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144, 230))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            f = open('highScore', 'w')
            f.write(str(int(high_score)))
            f.close()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 4
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                gameStart = False
                pipe_list.clear()
                bird_rect.center = (int(100 / 2), int(512 / 2))
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            bird_index += 1
            bird_index %= len(bird_frames)
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if gameStart and game_active is False:
        game_start_surface = pygame.image.load('assets/message.png').convert_alpha()
        game_start_rect = game_start_surface.get_rect(center=(144, 256))
        screen.blit(game_start_surface, game_start_rect)
    elif game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement

        screen.blit(rotated_bird, bird_rect)

        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display("main_game")
    else:
        screen.blit(game_over_surface, game_over_rect)
        game_over_text = game_font.render("Tap to play again", True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect(center=(144, 270))
        screen.blit(game_over_text, game_over_text_rect)
        if score > high_score:
            high_score = score
        score_display("game_over")

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -int(576 / 2):
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)  # running at 120fps
