import sys
import os
import pygame
import config

from pygame.locals import *

white = [255, 255, 255]
black = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
fill = [200, 200, 200]


class Grid:
    def __init__(self, width, height, cellSize = 20):
        self.width = width
        self.height = height
        self.cellSize = cellSize

    def initGrid(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        bgRect = pygame.Rect(0, 0, self.width, self.height)
        bgImage = pygame.image.load(os.path.join('src/assets', 'bg.png'))
        scaledBgImage = pygame.transform.scale(bgImage, (self.width, self.height))
        pygame.Surface.blit(self.screen, scaledBgImage, bgRect)
       # self.screen.fill(white)

        self.drawGrid()

    def drawGrid(self):
        """ Initializes grid defined by width and height """
        x = 0
        y = 0

        # Fit max amount of cells into user defined grid dimensions
        w = self.width // self.cellSize

        for l in range(w):
            pygame.draw.aaline(self.screen, black, (0, y), (self.width, y))
            pygame.draw.aaline(self.screen, black, (x, 0), (x, self.height))
            x = x + self.cellSize
            y = y + self.cellSize

    def fillSquare(self, row, col, color):
        # Calculate actual x and y values
        row_actual = row * self.cellSize
        col_actual = col * self.cellSize
        rec = pygame.Rect(col_actual, row_actual, self.cellSize - 1, self.cellSize - 1)
        pygame.draw.rect(self.screen, color, rec)
        pygame.display.update(rec)
        
    def fillImage(self, row, col, image):
        row_actual = row * self.cellSize
        col_actual = col * self.cellSize
        rec = pygame.Rect(col_actual, row_actual, self.cellSize - 1, self.cellSize - 1)
        pygame.Surface.blit(self.screen, image, rec)
        pygame.display.update(rec)

    def getCell(self, x, y):
        x = x - (x % self.cellSize)
        y = y - (y % self.cellSize)
        coord = (x, y)
        return coord
