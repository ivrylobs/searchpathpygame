import sys
import os
import pygame
import time
import config
import queue
import threading
from tkinter import *
from tkinter import ttk
from pygame.locals import *

# Local defined modules
from grid import Grid
from search import Search
from window import *

gridQ = queue.Queue()

config.init()

# Start an instance of tkinter window to get options from user
opt = GridOptions()
opt.mainloop()

# Record options selected by user
game_size = opt.shared_data["game_size"].get()
s_r = opt.shared_data["s_row"].get()
s_c = opt.shared_data["s_col"].get()
g_r = opt.shared_data["g_row"].get()
g_c = opt.shared_data["g_col"].get()
algorithm = opt.shared_data["algorithm"].get()

row = (0, 0)
col = (0, 0)

# NOTE: Grid size is square at this point. Implementing with row/col values so I have the option
# to make grid rectangular or more user-defined later on
if game_size == "Small":
    row = (200, 10)
    col = (200, 10)
elif game_size == "Medium":
    row = (500, 10)
    col = (500, 10)
elif game_size == "Large":
    row = (800, 10)
    col = (800, 10)

# Main instances of search grid (Grid) and search algorithms(Search)
myGrid = Grid(row[0], col[0], int(row[0]/row[1]))
myMatrix = Search(gridQ, row[1], col[1], (s_r, s_c), (g_r, g_c), int(row[0]/row[1]))


# Start the visualisation and initialize the grid
pygame.init()
myGrid.initGrid()

# Add the starting and goal states to the grid
startImage = pygame.image.load(os.path.join('src/assets', 'tank.png'))
scaledStartImage = pygame.transform.scale(startImage, (int(row[0]/row[1]) - 1, int(row[0]/row[1]) - 1))
myGrid.fillImage(s_r, s_c, scaledStartImage)
# myGrid.fillSquare(s_r, s_c, config.yellow)
myGrid.fillSquare(g_r, g_c, config.yellow)

# Local vars for recording mouse input from pygame
pos_x = 0
pos_y = 0
getWalls = True
fillCells = False

# While spacebar hasn't been pressed, record mouse clicks to record walls input by user
while getWalls:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_SPACE:
                getWalls = False
        elif event.type == MOUSEBUTTONDOWN:
            fillCells = True
        elif event.type == MOUSEBUTTONUP:
            fillCells = False

        # Check if user has selected any walls to add to the grid
        if fillCells:
            try:
                # Get event pos and then convert coordinates to an actual location on the grid
                # Color in the cell and set the coordinates in matrix to non-visitable
                pos_x, pos_y = event.pos
                pos_x, pos_y = myGrid.getCell(pos_x, pos_y)
                rec = pygame.Rect(pos_x, pos_y, int(row[0]/row[1]), int(row[0]/row[1]))
                barbImage = pygame.image.load(os.path.join('src/assets', 'barb.png'))
                scaledBarbImage = pygame.transform.scale(barbImage, (int(row[0]/row[1]), int(row[0]/row[1])))
                pygame.Surface.blit(myGrid.screen, scaledBarbImage, rec)
                myMatrix.setCell(pos_y // int(row[0]/row[1]), pos_x // int(row[0]/row[1]), "B")
                pygame.display.update()
            except:
                pass
    pygame.display.flip()

# Start a thread of the algorithm user selected
if algorithm == "BFS":
    t1 = threading.Thread(target=myMatrix.bfs())
elif algorithm == "DFS":
    t1 = threading.Thread(target=myMatrix.dfs())
elif algorithm == "A-Star":
    t1 = threading.Thread(target=myMatrix.a_star())

t1.start()

# Color in cells from the search algorithm and wait for quitgame
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    if not gridQ.empty():
        x, y, img = gridQ.get()
        myGrid.fillImage(x, y, img)
        pygame.display.update()


# main()
