# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 15:19:25 2018

@author: zou
"""
import pygame, random
import numpy as np

class Settings:
    def __init__(self):
        # 屏幕属性
        self.width = 28
        self.height = 28
        self.rect_len = 15

class Snake:
    def __init__(self):
        
        self.image_up = pygame.image.load('images/head_up.bmp')
        self.image_down = pygame.image.load('images/head_down.bmp')
        self.image_left = pygame.image.load('images/head_left.bmp')
        self.image_right = pygame.image.load('images/head_right.bmp')

        self.tail_up = pygame.image.load('images/tail_up.bmp')
        self.tail_down = pygame.image.load('images/tail_down.bmp')
        self.tail_left = pygame.image.load('images/tail_left.bmp')
        self.tail_right = pygame.image.load('images/tail_right.bmp')
            
        self.image_body = pygame.image.load('images/body.bmp')

        self.facing = "right"
        self.initialize()

    def initialize(self):
        self.position = [0, 0]
        self.segments = [[6 - i, 6] for i in range(3)]
        self.score = 0

    def blit_body(self, x, y, screen):
        screen.blit(self.image_body, (x, y))
        
    def blit_head(self, x, y, screen):
        if self.facing == "up":
            screen.blit(self.image_up, (x, y))
        elif self.facing == "down":
            screen.blit(self.image_down, (x, y))  
        elif self.facing == "left":
            screen.blit(self.image_left, (x, y))  
        else:
            screen.blit(self.image_right, (x, y))  
            
    def blit_tail(self, x, y, screen):
        tail_direction = [self.segments[-2][i] - self.segments[-1][i] for i in range(2)]
        
        if tail_direction == [0, -1]:
            screen.blit(self.tail_up, (x, y))
        elif tail_direction == [0, 1]:
            screen.blit(self.tail_down, (x, y))  
        elif tail_direction == [-1, 0]:
            screen.blit(self.tail_left, (x, y))  
        else:
            screen.blit(self.tail_right, (x, y))  
    
    def blit(self, rect_len, screen):
        self.blit_head(self.segments[0][0]*rect_len, self.segments[0][1]*rect_len, screen)                
        for position in self.segments[1:-1]:
            self.blit_body(position[0]*rect_len, position[1]*rect_len, screen)
        self.blit_tail(self.segments[-1][0]*rect_len, self.segments[-1][1]*rect_len, screen)                
            
    
    def update(self):
        if self.facing == 'right':
            self.position[0] += 1
        if self.facing == 'left':
            self.position[0] -= 1
        if self.facing == 'up':
            self.position[1] -= 1
        if self.facing == 'down':
            self.position[1] += 1
        self.segments.insert(0, list(self.position))
        
class Strawberry():
    def __init__(self, settings):
        self.settings = settings
        
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')        
        self.initialize()

    # Jerry's modification: added a list as a parameter
    def random_pos(self, snake, walls: list):
        # END
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')                
        
        self.position[0] = random.randint(0, self.settings.width-1)
        self.position[1] = random.randint(0, self.settings.height-1)

        self.position[0] = random.randint(9, 19)
        self.position[1] = random.randint(9, 19)
        
        if self.position in snake.segments:
            self.random_pos(snake, walls)

        # Jerry's modification: just making sure the berry doesn't spawn within the walls
        index = 0
        while index < len(walls):
            current_wall_bounds = walls[index].getBounds()

            if self.position[0] * 15 > current_wall_bounds[0][0] and \
                    self.position[0] * 15 <= current_wall_bounds[0][1] and \
                    self.position[1] * 15 > current_wall_bounds[1][0] and \
                    self.position[1] * 15 <= current_wall_bounds[1][1]:
                # NOTE: using a recursive function here.
                self.random_pos(snake, walls)
            index += 1
        # END

    def blit(self, screen):
        screen.blit(self.image, [p * self.settings.rect_len for p in self.position])
   
    def initialize(self):
        self.position = [15, 10]

# Jerry's modification: implementing the walls to add different maps to the gameplay
class Wall:
    def __init__(self, x_start: int, y_start: int, rows: int, columns: int):
        self.settings = Settings()

        # NOTE: the wall textures are assigned below
        self.image_desert = pygame.image.load('images/desert_wall.png')
        self.image_ice = pygame.image.load('images/ice_wall.png')
        # self.image_fire = pygame.image.load('images/fire_wall.png')

        # NOTE: the max number of rows and columns are defined in the Settings class
        #   as height and width. That is, in pixel terms, height * rect_len and
        #   width * rect_len.
        self.MAX_ROWS = self.settings.height
        self.MAX_COLUMNS = self. settings.width

        # NOTE: the starting points of a Wall object.
        self.x_start = x_start
        self.y_start = y_start

        # NOTE: how many rows and columns of walls are there?
        self.rows = rows
        self.columns = columns

        # NOTE: input validation starts from here. The validation rationales are as follows:
        #           + The starting points x and y must be divisible by 15 because
        #               rect_len is 15, and rect_len is the discrete building block of this game.
        #           + The pixel length of rows and columns, taking the starting points into account,
        #               must not exceed the pixel dimensions of the display.
        if (x_start % self.settings.rect_len) != 0 or (y_start % self.settings.rect_len) != 0:
            raise ValueError("Invalid starting coordinate. The (x,y) values must be divisible by 15.")
        elif (rows * self.settings.rect_len + y_start) > self.settings.height * 15 or \
                (columns * self.settings.rect_len + x_start) > self.settings.width * 15:
            error_message = "Invalid value(s) for columns and/or rows." + \
                "The dimensions for the columns and rows must not exceed the display's dimensions."
            raise ValueError(error_message)

    # NOTE: this function is used to display the walls.
    def blit(self, screen, map: str) -> None:
        chosen_wall = 0
        if map == "desert":
            chosen_wall = self.image_desert
        elif map == "ice":
            chosen_wall = self.image_ice
        # elif map == "fire":
            # chosen_wall = self.image_fire

        i = 1
        while i < self.rows + 1:
            j = 1
            while j < self.columns + 1:
                screen.blit(chosen_wall, \
                            (15 * j + self.x_start, 15 * i + self.y_start))
                j += 1
            i += 1
        return None

    # NOTE: this function is used to get the bounds of the walls to see if the
    #   snake has crashed. The function returns a list of tuples. The first tuple
    #   in the list is the x bounds and the second tuple is the y bounds.
    def getBounds(self) -> list:
        x_leftbound = self.x_start
        x_rightbound = self.x_start + (self.columns + 0) * self.settings.rect_len
        y_topbound = self.y_start
        y_bottombound = self.y_start + (self.rows + 0) * self.settings.rect_len

        return [(x_leftbound, x_rightbound), (y_topbound, y_bottombound)]
# END

class Game:
    """
    """
    def __init__(self):
        self.settings = Settings()
        self.snake = Snake()
        self.strawberry = Strawberry(self.settings)
        self.move_dict = {0 : 'up',
                          1 : 'down',
                          2 : 'left',
                          3 : 'right'}

        # Jerry's modification
        self.walls = []
        # END

    # Jerry's modification: creating random walls
    def random_walls(self, number_of_walls: int) -> None:
        self.walls = []
        index = 0
        # NOTE: this generates random numbers to assign to a new instance
        #   of class Wall being appended into the list of self.walls at the end.
        while index < number_of_walls:
            MIN_SPACE = 4

            # NOTE: the starting coordinates start at 5 because the player needs time
            #   to react.
            x_start = random.randint(2, self.settings.width - MIN_SPACE)
            columns = random.randint(3, 7)
            y_start = random.randint(2, self.settings.height - MIN_SPACE)
            rows = random.randint(3, 7)

            # NOTE: this checks if the randomly generated integer is
            #   within an acceptable range.
            while x_start + columns >= self.settings.width:
                columns = random.randint(3, 7)
            while y_start + rows >= self.settings.height:
                rows = random.randint(3, 7)

            # NOTE: this function sets rows or columns to 1 randomly
            if random.randint(1,10) % 2:
                columns = 1
            else:
                rows = 1

            # NOTE: this adds a randomly generated Wall object to the list of Wall objects.
            self.walls.append(Wall(x_start * 15, y_start * 15, rows, columns))

            index += 1
    # END

    def restart_game(self):
        self.snake.initialize()
        self.strawberry.initialize()

    def current_state(self):         
        state = np.zeros((self.settings.width+2, self.settings.height+2, 2))
        expand = [[0, 1], [0, -1], [-1, 0], [1, 0], [0, 2], [0, -2], [-2, 0], [2, 0]]
        
        for position in self.snake.segments:
            state[position[1], position[0], 0] = 1
        
        state[:, :, 1] = -0.5        

        state[self.strawberry.position[1], self.strawberry.position[0], 1] = 0.5
        for d in expand:
            state[self.strawberry.position[1]+d[0], self.strawberry.position[0]+d[1], 1] = 0.5
        return state
    
    def direction_to_int(self, direction):
        direction_dict = {value : key for key,value in self.move_dict.items()}
        return direction_dict[direction]
        
    def do_move(self, move):
        move_dict = self.move_dict
        
        change_direction = move_dict[move]
        
        if change_direction == 'right' and not self.snake.facing == 'left':
            self.snake.facing = change_direction
        if change_direction == 'left' and not self.snake.facing == 'right':
            self.snake.facing = change_direction
        if change_direction == 'up' and not self.snake.facing == 'down':
            self.snake.facing = change_direction
        if change_direction == 'down' and not self.snake.facing == 'up':
            self.snake.facing = change_direction

        self.snake.update()
        
        if self.snake.position == self.strawberry.position:
            # Jerry's modification: added walls as an argument to make sure the berries
            #   don't spawn within the walls
            self.strawberry.random_pos(self.snake, self.walls)
            # END
            reward = 1
            self.snake.score += 1
        else:
            self.snake.segments.pop()
            reward = 0
                
        if self.game_end():
            return -1
                    
        return reward
    
    def game_end(self):
        end = False
        if self.snake.position[0] >= self.settings.width or self.snake.position[0] < 0:
            end = True
        if self.snake.position[1] >= self.settings.height or self.snake.position[1] < 0:
            end = True
        if self.snake.segments[0] in self.snake.segments[1:]:
            end = True

        # Jerry's modification: checking if the snake has hit the wall
        # NOTE: the variable i checks through the list of walls.
        index = 0
        while index < len(self.walls):
            current_wall_bounds = self.walls[index].getBounds()

            if self.snake.position[0] * 15 > current_wall_bounds[0][0] and \
                    self.snake.position[0] * 15 <= current_wall_bounds[0][1] and \
                    self.snake.position[1] * 15 > current_wall_bounds[1][0] and \
                    self.snake.position[1] * 15 <= current_wall_bounds[1][1]:
                return True
            index += 1
        # END

        return end
    
    def blit_score(self, color, screen):
        font = pygame.font.SysFont(None, 25)
        text = font.render('Score: ' + str(self.snake.score), True, color)
        screen.blit(text, (0, 0))

