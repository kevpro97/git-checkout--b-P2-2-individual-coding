# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018
@author: zou
"""

import pygame, random
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT

from game import Game
from game import Wall
from game import Settings

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)

game = Game()
rect_len = game.settings.rect_len
snake = game.snake
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))
pygame.display.set_caption('Gluttonous')

crash_sound = pygame.mixer.Sound(f'./sound/crash.wav')
# Kevin
# Settings variables
difficulty = "normal"
map = "normal"
# clicked = [normaldifficulty, easy, hard, normalmap, ice, desert, fire], expands dependent on the number of options in settings
clicked = [False] * 7


# End


def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


# Kevin - altered
# altered to include textsize which allows for different text size displays
def message_display(textsize, text, x, y, color=black):
    large_text = pygame.font.SysFont('comicsansms', textsize)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()


# altered buttons to include button type
def button(textsize, buttontype, msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # used to take user to different pages
    if buttontype == None:
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, active_color, (x, y, w, h))
            if click[0] == 1 and action != None:
                if parameter != None:
                    action(parameter)
                else:
                    action()
        else:
            pygame.draw.rect(screen, inactive_color, (x, y, w, h))
    # used for options buttons which change settings variables
    else:
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, active_color, (x, y, w, h))
            if click[0] == 1 and action != None:
                global clicked
                clicked[buttontype] = True
                if parameter != None:
                    action(parameter)
                else:
                    action()
        elif clicked[buttontype]:
            pygame.draw.rect(screen, red, (x, y, w, h))
        else:
            pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    smallText = pygame.font.SysFont('comicsansms', textsize)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)


# End

def quitgame():
    pygame.quit()
    quit()


def crash():
    pygame.mixer.Sound.play(crash_sound)
    message_display(50, 'crashed', game.settings.width / 2 * 15, game.settings.height / 3 * 15, white)
    time.sleep(1)


def initial_interface():
    pygame.display.set_caption("Menu")
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill(white)
        message_display(50, 'Gluttonous', game.settings.width / 2 * 15, game.settings.height / 4 * 15)

        button(20, None, 'Play Game', 160, 160, 120, 40, green, bright_green, game_loop, 'human')
        button(20, None, 'Instructions', 160, 220, 120, 40, green, bright_green, instructions_page)
        # Kevin - button on initial interface to take the user to the settings page
        button(20, None, 'Settings', 160, 280, 120, 40, green, bright_green, settings_page)
        # End
        button(20, None, 'Quit', 160, 340, 120, 40, red, bright_red, quitgame)
        pygame.display.update()
        pygame.time.Clock().tick(15)

def instructions_page():
    pygame.display.set_caption("How to Play")
    intro = True
    while intro:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill(white)
        message_display(20, 'Instructions',game.settings.width/2 * 15, game.settings.height/4 + 10)
        message_display(10, 'The snake can be moved by the arrow keys. The aim is to eat as much food ',game.settings.width/2 * 15, game.settings.height/4 + 30)
        message_display(10, 'as possible without dying to a wall, the edges or the snake itself.', game.settings.width / 2 * 15, game.settings.height / 4 + 45)
        message_display(15, 'Normal Mode', game.settings.width / 2 * 15, game.settings.height / 4 + 70)
        message_display(10, '1. Snake has medium speed, 2. 2-4 walls are generated, 3. Only apples can be eaten,', game.settings.width / 2 * 15, game.settings.height / 4 + 95)
        message_display(10, '4. Start off with 2 lives', game.settings.width / 2 * 15, game.settings.height / 4 + 110)
        message_display(15, 'Easy Mode', game.settings.width / 2 * 15, game.settings.height / 4 + 135)
        message_display(10, '1. Snake has slow speed, 2. No walls are generated, 3. Buff food (Hearts, cherries and  ', game.settings.width / 2 * 15, game.settings.height / 4 + 160)
        message_display(10, 'peels) alongside apples can also be eaten, 4. Start off with 3 lives', game.settings.width / 2 * 15, game.settings.height / 4 + 175)
        message_display(15, 'Hard Mode', game.settings.width / 2 * 15, game.settings.height / 4 + 200)
        message_display(10, '1. Snake has fast speed, 2. 6-8 walls are generated, 3. Debuff food (Coffee, avocado) ', game.settings.width / 2 * 15, game.settings.height / 4 + 225)
        message_display(10, 'alongside apples can also be eaten, 4. Only 1 life given', game.settings.width / 2 * 15, game.settings.height / 4 + 240)
        message_display(15, 'Food', game.settings.width / 2 * 15, game.settings.height / 4 + 265)
        message_display(10, '1. Heart - gain 1 life, 2. Cherry - gain an additional point (2 instead of 1)', game.settings.width / 2 * 15, game.settings.height / 4 + 290)
        message_display(10, '3. Peels - slow down snake speed, 4. Apple - standard food, 5. Avocado - gain an ', game.settings.width / 2 * 15, game.settings.height / 4 + 305)
        message_display(10, 'additional snake segment (2 instead of 1) and 6. Coffee - speed up snake speed', game.settings.width / 2 * 15, game.settings.height / 4 + 320)
        button(20, None, 'Back', 170, 370, 70, 40, green, bright_green, initial_interface)

        pygame.display.update()
        pygame.time.Clock().tick(15)
# End



# Kevin - settings page
def settings_page():
    pygame.display.set_caption("Settings")
    intro = True
    while intro:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill(white)
        message_display(50, 'Settings', 210, 40)
        message_display(20, 'Difficulty:', 50, 115)
        button(15, 0, 'Normal', 100, 100, 70, 40, green, bright_green, output_difficulty, 'normal')
        button(15, 1, 'Easy', 180, 100, 70, 40, green, bright_green, output_difficulty, 'easy')
        button(15, 2, 'Hard', 260, 100, 70, 40, green, bright_green, output_difficulty, 'hard')
        message_display(20, 'Map:', 75, 200)
        button(15, 3, 'Normal', 100, 185, 70, 40, green, bright_green, output_map, 'normal')
        button(15, 4, 'Ice', 180, 185, 70, 40, green, bright_green, output_map, 'ice')
        button(15, 5, 'Desert', 260, 185, 70, 40, green, bright_green, output_map, 'desert')
        button(15, 6, 'Fire', 340, 185, 70, 40, green, bright_green, output_map, 'fire')
        button(20, None, 'Back', 170, 370, 70, 40, green, bright_green, initial_interface)
        pygame.display.update()
        pygame.time.Clock().tick(15)
# End


# Kevin - depending on the options chosen, previously selected options become unchecked
def output_difficulty(option):
    global difficulty, clicked
    difficulty = option
    if option == 'normal':
        clicked[1] = False
        clicked[2] = False
    elif option == 'easy':
        clicked[0] = False
        clicked[2] = False
    elif option == 'hard':
        clicked[0] = False
        clicked[1] = False


def output_map(option):
    global map, clicked
    map = option
    if option == 'normal':
        clicked[4] = False
        clicked[5] = False
        clicked[6] = False
    elif option == 'ice':
        clicked[3] = False
        clicked[5] = False
        clicked[6] = False
    elif option == 'desert':
        clicked[3] = False
        clicked[4] = False
        clicked[6] = False
    elif option == 'fire':
        clicked[3] = False
        clicked[4] = False
        clicked[5] = False
# End

def game_loop(player, fps=10):
    pygame.display.set_caption("Gluttonous")
    game.restart_game()
    # Kevin - apply settings to game
    game_settings = Settings()
    game_settings.difficulty(difficulty)
    game_settings.map(map)
    # End

    # Integration
    # easy mode: no walls spawn and slow snake base speed
    if difficulty == "easy":
        game.random_walls(0)
        fps = 4
    # normal mode: 2-4 walls spawn and medium snake base speed
    elif difficulty == "normal":
        game.random_walls(random.randint(2, 4))
        fps = 6
    # hard mode: 6-8 walls spawn and fast snake base speed
    elif difficulty == "hard":
        game.random_walls(random.randint(6, 8))
        fps = 8

    game_settings.fps(fps)

    while not game.game_end():

        pygame.event.pump()

        move = human_move()

        game.do_move(move)

        if map == "ice":
            screen.fill(0xADD8E6)
        elif map == "fire":
            screen.fill(0xFF814A)
        elif map == "desert":
            screen.fill(0xFFE14B)
        else:
            screen.fill(black)
        fps = game_settings.grab_fps()
        print(fps)
        # Jerry's modification
        index = 0
        while index < len(game.walls):
            game.walls[index].blit(screen, map)
            index += 1
        # END

        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)

        pygame.display.flip()

        fpsClock.tick(fps)

    crash()


def human_move():
    direction = snake.facing

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        elif event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    move = game.direction_to_int(direction)
    return move


if __name__ == "__main__":
    initial_interface()
