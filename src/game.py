import pygame
from const import *

class Game:

    def __init__(self):
        pass

    # show methods
    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200) # light green
                else:
                    color = (119, 154, 88) # dark green

                # squares
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                
                # drawing the squares
                pygame.draw.rect(surface, color, rect)