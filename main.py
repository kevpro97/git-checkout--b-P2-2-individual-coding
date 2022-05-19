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
# clicked = [easy, hard, ice, desert, fire], expands dependent on the number of options in settings
clicked = [False]*5
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
def button(buttontype, msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
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
    
    smallText = pygame.font.SysFont('comicsansms', 20)
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
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(white)
        message_display(50, 'Gluttonous', game.settings.width / 2 * 15, game.settings.height / 4 * 15)

        button(None, 'Play Game', 160, 160, 100, 40, green, bright_green, game_loop, 'human')
        # Kevin - button on initial interface to take the user to the settings page
        button(None, 'Settings', 160, 220, 100, 40, green, bright_green, settings_page)
        # End
        button(None, 'Quit', 160, 280, 100, 40, red, bright_red, quitgame)

        pygame.display.update()
        pygame.time.Clock().tick(15)

# Kevin - settings page
def settings_page():
    intro = True
    while intro:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill(white)
        message_display(50, 'Settings', 210, 40)
        message_display(20, 'Difficulty:', 50, 115)
        button(0, 'Easy', 110, 100, 80, 40, green, bright_green, output_difficulty, 'easy')
        button(1, 'Hard', 210, 100, 80, 40, green, bright_green, output_difficulty, 'hard')
        message_display(20, 'Map:', 75, 200)
        button(2, 'Ice', 110, 185, 80, 40, green, bright_green, output_map, 'ice')
        button(3, 'Desert', 210, 185, 80, 40, green, bright_green, output_map, 'desert')
        button(4, 'Fire', 310, 185, 80, 40, green, bright_green, output_map, 'fire')
        button(None, 'Back', 170, 370, 80, 40, green, bright_green, initial_interface)
        pygame.display.update()
        pygame.time.Clock().tick(15)
        # End
# Kevin
def output_difficulty(option):
    # change the difficulty global variable
    global difficulty
    difficulty = option
    # reset previously selected buttons to inactive color
    print(difficulty)
    if option == 'easy':
        global clicked
        clicked[1] = False
    elif option == 'hard':
        clicked
        clicked[0] = False

def output_map(option):
    global map
    map = option
    if option == 'ice':
        global clicked
        clicked[3] = False
        clicked[4] = False
    elif option == 'desert':
        clicked[2] = False
        clicked[4] = False
    elif option == 'fire':
        clicked[2] = False
        clicked[3] = False
# End

def game_loop(player, fps=10):
    game.restart_game()
    # Kevin - apply settings to game
    game_settings = Settings()
    game_settings.difficulty(difficulty)
    game_settings.map(map)
    # End

    if difficulty == "easy":
      game.random_walls(0)
    elif difficulty == "normal":
      game.random_walls(random.randint(2,4))
    elif difficulty == "hard":
      game.random_walls(random.randint(6,8))
      
  
    
    while not game.game_end():
        
        pygame.event.pump()

        move = human_move()
        # Kevin - Code for "speed up fruit" and "slow down fruit". to be determined
        if game.snake.score == 0 or game.strawberry.style == "1":
            fps = 5
        elif game.strawberry.style == "4":
            fps = 10
        elif game.strawberry.style == "3":
            fps = 3
        else:
            fps = 5
        # End

        game.do_move(move)
        
        if map == "ice":
          screen.fill(0xADD8E6)
        elif map == "fire":
          screen.fill(0xFF814A)
        elif map == "desert":
          screen.fill(0xFFE14B)
        else:
          screen.fill(black)

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
