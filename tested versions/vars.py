import pygame
import pygame_menu
from pygame_menu import themes
import copy
import sys
from math import *


import pygame.mixer


# Initialization of Pygame
pygame.init()

width  = 480
height = 480
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Colors
background = (20, 20, 20)
border = (208, 211, 212)
Red = (231, 76, 60)
white = (244, 246, 247)
Violet = (136, 78, 160)
Orange = (245, 113, 5)
Blue = (79, 121, 247)

playerColor = [Red, Blue]

font = pygame.font.Font('8-BIT WONDER.TTF', 20)
font2 =  pygame.font.SysFont("Times New Roman", 30)

#default values
cols = 4
rows = 4
blocks = 120
noPlayers = 2
total_moves=0
d=blocks // 2 - 2 #center of a cell
pygame.display.set_caption("Chain Reaction %d Player" % noPlayers)


score = []
for i in range(noPlayers):
    score.append(0)

players = []
for i in range(noPlayers):
    players.append(playerColor[i])




grid = [] 

# Quit or Close the Game Window
def close():
    pygame.quit()
    sys.exit()


# Class for Each Spot in Grid
class Spot():
    def __init__(self, i, j):
        self.color = border
        self.neighbors = []
        self.noAtoms = 0
        self.i = i  # Column placement
        self.j = j  # row placement

    def addNeighbors(self, i, j):
        if i > 0:
            self.neighbors.append(grid[i - 1][j])
        if i < rows - 1:
            self.neighbors.append(grid[i + 1][j])
        if j < cols - 1:
            self.neighbors.append(grid[i][j + 1])
        if j > 0:
            self.neighbors.append(grid[i][j - 1])


# Initializing the Grid with "Empty or 0"
def initializeGrid():
    global grid, score, players
    # score = []
    # for i in range(noPlayers):
    #     score.append(0)

    # players = []
    # for i in range(noPlayers):
    #     players.append(playerColor[i])

    grid = [[] for _ in range(cols)]
    for i in range(cols):
        for j in range(rows):
            newObj = Spot(i,j)
            grid[i].append(newObj)
    for i in range(cols):
        for j in range(rows):
            grid[i][j].addNeighbors(i, j)


# Draw the Grid 
def drawGrid(currentIndex):
    r = 0
    c = 0
    for i in range(width // blocks):
        r += blocks
        c += blocks
        pygame.draw.line(display, players[currentIndex], (c, 0), (c, height)) #vertical line
        pygame.draw.line(display, players[currentIndex], (0, r), (width, r)) #horizontal line


# Draw the Present Situation of Grid
def showPresentGrid(vibrate=1): #
    try:
        r = -blocks 
        padding = 2
        for i in range(cols):
            r += blocks
            c = -blocks
            for j in range(rows):
                c += blocks
                if grid[i][j].noAtoms == 0:
                    grid[i][j].color = border
                elif grid[i][j].noAtoms == 1:
                    pygame.draw.ellipse(display, grid[i][j].color,
                                        (r + blocks / 2 - d / 2 + vibrate, c + blocks / 2 - d / 2, d, d))
                elif grid[i][j].noAtoms == 2:
                    pygame.draw.ellipse(display, grid[i][j].color, (r+5, c + blocks / 2 - d / 2 - vibrate, d, d))
                    pygame.draw.ellipse(display, grid[i][j].color,
                                        (r + d / 2 + blocks / 2 - d / 2 + vibrate, c + blocks / 2 - d / 2, d, d))
                elif grid[i][j].noAtoms == 3:
                    angle = 90
                    x = r + (d / 2) * cos(radians(angle)) + blocks / 2 - d / 2
                    y = c + (d / 2) * sin(radians(angle)) + blocks / 2 - d / 2
                    pygame.draw.ellipse(display, grid[i][j].color, (x - vibrate, y, d, d))
                    x = r + (d / 2) * cos(radians(angle + 90)) + blocks / 2 - d / 2
                    y = c + (d / 2) * sin(radians(angle + 90)) + 5
                    pygame.draw.ellipse(display, grid[i][j].color, (x + vibrate, y, d, d))
                    x = r + (d / 2) * cos(radians(angle - 90)) + blocks / 2 - d / 2
                    y = c + (d / 2) * sin(radians(angle - 90)) + 5
                    pygame.draw.ellipse(display, grid[i][j].color, (x - vibrate, y, d, d))

        pygame.display.update()
    except RecursionError:
        pass



def copyGrid():
    global grid
    return copy.deepcopy(grid)


# Increase the Atom when Clicked
def addAtom(grid,i, j, color):
    # print("added :",i,j)
    grid[i][j].noAtoms += 1
    grid[i][j].color = color
    if grid[i][j].noAtoms >= len(grid[i][j].neighbors):
        overFlow(grid[i][j], color)

MAX_DEPTH = 800
# Split the Atom when it Increases the "LIMIT"
def overFlow(cell, color, depth=0):
    if depth > MAX_DEPTH:
        return

    cell.noAtoms = 0
    for neighbor in cell.neighbors:
        neighbor.noAtoms += 1
        neighbor.color = color
        if neighbor.noAtoms >= len(neighbor.neighbors):
            overFlow(neighbor, color, depth + 1)

def critical_mass(grid, pos):
    i, j = pos
    total_neighbors = len(grid[i][j].neighbors)
    return total_neighbors



def countCriticalBlock(grid, start, currentPlayer):
    visited = set()
    stack = [start]
    count = 0

    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue

        visited.add((x, y))

        if grid[x][y].color == players[currentPlayer] and grid[x][y].noAtoms >= critical_mass(grid, (x, y)) - 1:
            count += 1

            for neighbor in grid[x][y].neighbors:
                stack.append((neighbor.i, neighbor.j))

    return count

# Checking if Any Player has WON!
def isPlayerInGame():
    global score
    playerScore = []
    for i in range(noPlayers):
        playerScore.append(0)
    for i in range(cols):
        for j in range(rows):
            for k in range(noPlayers):
                if grid[i][j].color == players[k]:
                    playerScore[k] += grid[i][j].noAtoms
    score = playerScore[:]

pygame.mixer.init()
win_sound = pygame.mixer.Sound('win.wav')
lose_sound = pygame.mixer.Sound('fail2.wav')
beep_sound=pygame.mixer.Sound('beep.wav')

# GAME OVER
def gameOver(playerIndex): 
    global total_moves, totalremove
    alpha = 0  # Initial alpha value for fade-in effect


    if playerIndex == 0:
        lose_sound.play()
    else:
        win_sound.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    gameLoop()
        
        if playerIndex == 0:
            text = font.render(" AI Won", True, (255, 255, 255, alpha))
            text2 = font2.render("Press 'r' to Reset!", True, (255, 255, 255, alpha))
            total_moves = 0
        else:
            text = font.render(" You Won", True, (207, 188, 188, alpha))
            text2 = font2.render("Press 'r' to Reset!", True, (207, 188, 188, alpha))
            total_moves = 0

        # separate surface to render the text
        text_surface = pygame.Surface((text.get_width() + 20, text.get_height() + 20), pygame.SRCALPHA)
        text_surface.fill((0, 0, 0, 100))  # Semi-transparent black fill

        # Blit the text onto the text_surface
        text_surface.blit(text, (10, 10))

        # Fade-in effect for the text

        display.fill((0, 0, 0, 100))  # Semi-transparent black fill for the main display surface
        display.blit(text_surface, (width / 3, height / 3))
        display.blit(text2, (width / 3, height / 2))

        pygame.display.update()
        clock.tick(60)




def removeAtom(grid,i, j, currentPlayer):
    # print("removed :",i,j)
    # Decrement the atom count of the cell at position (i, j)
    grid[i][j].noAtoms -= 1
    # If the cell becomes empty, update its color to the currentPlayer's color
    if grid[i][j].noAtoms == 0:
        grid[i][j].color = border



def checkWon(grid,x):
    # playerScore[]==user    &&  playerScore[1]=AI
    playerScore = []
    for i in range(noPlayers):
        playerScore.append(0)
    for i in range(cols):
        for j in range(rows):
            for k in range(noPlayers):
                if grid[i][j].color == players[k]:
                    playerScore[k] +=1
    
    # print("playerScore", playerScore[0],playerScore[1])
    # print(playerScore)
    if playerScore[1]==0 and playerScore[0]==0:
        # print(playerScore,1,x)
        return 9999
    elif playerScore[1]==0 and x>=3:
        # print(playerScore,2,x)
        return 1
    elif playerScore[0]==0 and x>=3:
        # print(playerScore,3,x)
        return 0
    else:
        # print(playerScore,4,x)
        return 9999
        
def evaluateBoard(grid, currentPlayer):
    
    playerScore = [0] * noPlayers
    criticalBlocks = []
    count=0
    for i in range(cols):
        for j in range(rows):
            if grid[i][j].color == players[1-currentPlayer]:
                count=count+1
    # print("checkWon(total_moves): ",checkWon(grid,total_moves))
    if checkWon(grid,total_moves)==0:
        playerScore[currentPlayer] += 10000
        # print("wiiiiiin")
        
    elif checkWon(grid,total_moves)==1:
        playerScore[currentPlayer] -= 10000
        # print("loose")


    else:


        for i in range(cols):
            for j in range(rows):
                
                total_neighbors = len(grid[i][j].neighbors)
                # print("total_neighbors",total_neighbors,i,j)
                
                if grid[i][j].color == border:
                    continue
                #6.For every orb of the player's color, add 1 to the value.

                if grid[i][j].color == players[currentPlayer]:
                    # print("rule1= ",i,j,"(+1)")
                    playerScore[currentPlayer] += 1
                

                if grid[i][j].noAtoms >= total_neighbors - 1:
                    criticalBlocks.append((i, j))
                
                #4. In case, the orb has no critical enemy cells in its adjacent cells at all, add 2 to the value if it is an edge cell or 3 if it is a corner cell.
                if grid[i][j].color == players[currentPlayer]:
                    for neighbor in grid[i][j].neighbors:
                        n_crit=len(neighbor.neighbors)
                        if neighbor.color == players[1-currentPlayer] and neighbor.noAtoms < n_crit:
                            if total_neighbors == 2 :
                                # print("rule2= ",i,j,"(+3)")
                                playerScore[currentPlayer] += 3
                
                            if total_neighbors == 3 :
                                # print("rule3= ",i,j,"(+2)")
                                playerScore[currentPlayer] += 2
                    #5. In case, the orb has no critical enemy cells in its adjacent cells at all, add 2 to the value, if the cell is critical.
                    if(grid[i][j].noAtoms == total_neighbors-1) : #nije critical
                        count = 0
                        for neighbor in grid[i][j].neighbors:
                            n_crit=len(neighbor.neighbors)
                            if neighbor.color == players[1-currentPlayer] and neighbor.noAtoms >= n_crit-1:
                                count = count + 1 #neighbour e enemy critical cell
                        if count==0: #jodi neighbouring crit na thake tahole
                            # print("rule4= ",i,j,"(+2)")
                            playerScore[currentPlayer] += 2

                #3. For every orb, for every enemy critical cell surrounding the orb, subtract 5 minus the critical mass of that cell from the value.
                if grid[i][j].color == players[currentPlayer]:
                    for neighbor in grid[i][j].neighbors:
                        n_crit=len(neighbor.neighbors)
                    
                        if neighbor.color == players[1-currentPlayer] and neighbor.noAtoms >= n_crit-1:
                            # print("rule5= ",i,j,"(--))")
                            playerScore[currentPlayer] -= (5 - n_crit)

    score = playerScore[currentPlayer]
    #7. For every contiguous blocks of critical cells of the player's color, add twice the number of cells in the block to the score.
    for block in criticalBlocks:
        # print("rule6= ",i,j,"(x)")
        score += 2 * countCriticalBlock(grid, block, currentPlayer)
    # print("score",score)
    return score

def minimax(gridcpy, depth, alpha, beta, maximizingPlayer):
    global total_moves
    # print("total_moves",total_moves)
    # print("hii ami mini   1")
    available_cells = []
    if depth == 0 or checkWon(gridcpy,total_moves) != 9999:
        return evaluateBoard(gridcpy, 1),None

    if maximizingPlayer:
        best_pos = None
        # print("maximizingPlayer")
        maxEval = float('-inf')
        for i in range(cols):
            for j in range(rows):
                if gridcpy[i][j].color == players[maximizingPlayer] or gridcpy[i][j].color == border:
                    available_cells.append((i, j))
                    
        for cell in available_cells:  # Iterate over available cells
            
            i, j = cell
            # print("max turn cell : ",i,j)
            total_moves+=1
            addAtom(gridcpy,i, j, players[maximizingPlayer])
            
            eval,pos = minimax(gridcpy, depth - 1, alpha, beta, 1 - maximizingPlayer)
            
            removeAtom(gridcpy,i, j, maximizingPlayer)
            total_moves-=1
            if eval>maxEval:
                best_pos = (i, j)
                maxEval = eval
            #maxEval = max(maxEval, eval)
            # print("maxEval= ",maxEval)
            alpha = max(alpha, eval)

            if beta <= alpha:
                break
        # print("maxval ",maxEval,best_pos)
        return maxEval,best_pos

    else:
        best_pos=None
        # print("miniimizingPlayer")
        minEval = float('inf')
        for i in range(cols):
            for j in range(rows):
                if gridcpy[i][j].color == players[0] or gridcpy[i][j].color == border:
                    available_cells.append((i, j))

        for cell in available_cells:  # Iterate over available cells
            i, j = cell
            # print("min turn cell : ",i,j)
            addAtom(gridcpy,i, j, players[0])
            total_moves+=1
            eval,pos = minimax(gridcpy, depth - 1, alpha, beta,1- maximizingPlayer)
            removeAtom(gridcpy,i, j,players[0])
            total_moves-=1
            if eval < minEval:
                minEval = eval
                best_pos = (i, j)
            beta = min(beta, eval)

            if beta <= alpha:
                break

        return minEval,best_pos

def findBestMove(grid, currentPlayer):
    bestScore = float('-inf')
    gridcopy = grid.copy()
    bestMove = None
    available_cells = []
    score,bestMove = minimax(gridcopy, 3, float('-inf'), float('inf'),  currentPlayer)
    grid = gridcopy.copy()
    return bestMove
 


# Main Loop
import random

# ...






def gameLoop():
    global total_moves,grid
    initializeGrid()
    
    loop = True
    turns = 0
    currentPlayer = 0
    vibrate = 0.5
    

    while loop:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                print("Sry to see you goo :( ")
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                total_moves+=1
                # print(total_moves)
                x, y = pygame.mouse.get_pos()
                i = x // blocks
                j = y // blocks
                if grid[i][j].color == players[currentPlayer] or grid[i][j].color == border:
                    turns += 2    
                    addAtom(grid,i, j, players[currentPlayer])
                    currentPlayer += 1
                    if currentPlayer >= noPlayers:
                        currentPlayer = 0
                if turns >= noPlayers:
                    isPlayerInGame()
                pygame.time.delay(10)
            display.fill(background)
            vibrate *= -1

            
            drawGrid(currentPlayer)
            showPresentGrid(vibrate)
            if currentPlayer == 1:
                    pygame.time.wait(500)     
            pygame.display.update()
            res = checkWon(grid,total_moves)
            if res < 9999:
                gameOver(res)

        clock.tick(20)

        if currentPlayer == 1:
            total_moves+=1
            grid_copy = copyGrid()
            move = findBestMove(grid_copy, currentPlayer)
  
            i, j = (move)
             
            addAtom(grid,i, j, players[currentPlayer])
            beep_sound.play()
            
            currentPlayer += 1
            if currentPlayer >= noPlayers:
                currentPlayer = 0
            display.fill(background)
            vibrate *= -1
            
            drawGrid(currentPlayer)
            showPresentGrid(vibrate)
            if currentPlayer == 1:
                    pygame.time.wait(500)     
            pygame.display.update()
            res = checkWon(grid,total_moves)
            if res < 9999:
                gameOver(res)

pygame.init()

#menu
surface = pygame.display.set_mode((480, 480))

def set_color(color, value):
    if value==1:
        playerColor[0] =Red
    elif value==2:
        playerColor[0] =Violet
    elif value==3:
        playerColor[0] =Orange
    

def set_size(value, id):
    global rows, cols,blocks,d
    if id == 1:
        rows, cols= 4, 4
    elif id == 2:
        rows, cols = 6, 6
    elif id == 3:
        rows, cols = 8, 8
    elif id == 4:
        rows, cols = 10, 10
    blocks = height//rows
    d = blocks // 2 - 2   #center



def start_the_game():
    mainmenu._open(loading)
    pygame.time.set_timer(update_loading, 30)

def color_menu():
    mainmenu._open(color)

def grid_menu():
    mainmenu._open(grd)


# background_image = pygame.image.load('hCUwLQ.png')

# surface.blit(background_image, (0, 0))

# custom theme for the menus
new_theme = pygame_menu.themes.Theme(
    background_color=(30, 30, 30),
    title_background_color=(20, 20, 20),
    title_font_size=20,
    widget_font_size=20,
    widget_font_color=(255, 255, 255),
    selection_color=(200, 200, 200),
    widget_padding=(0, 10),
    widget_margin=(0, 25),
    title_font='8-BIT WONDER.TTF', 
    widget_font='8-BIT WONDER.TTF'  
)


mainmenu = pygame_menu.Menu('Welcome', 480, 480, theme=new_theme)
mainmenu.add.label('Chain Reaction', font_size=33, font_color=(255, 255, 255))

mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Select Color', color_menu)
mainmenu.add.button('Select Grid Size', grid_menu)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)

grd = pygame_menu.Menu('Select a Size', 480, 480, theme=new_theme)
grd.add.selector('Color :', [('4 * 4', 1), ('6 * 6', 2), ('8 * 8', 3), ('10 * 10', 4)], onchange=set_size)

color = pygame_menu.Menu('Select a Color', 480, 480, theme=new_theme)
color.add.selector('Color :', [('Red', 1), ('Violet', 2) , ('Orange', 3)], onchange=set_color)
color.add.button('Back', pygame_menu.events.BACK)
loading = pygame_menu.Menu('Loading the Game...', 480, 480, theme=new_theme)
loading.add.progress_bar("", progressbar_id="1", default=0, width=300, box_progress_color=(250, 72, 93),progress_text_font_color=(173, 173, 173))

grd.add.button('Back', pygame_menu.events.BACK)
arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(20, 30))  


update_loading = pygame.USEREVENT + 0

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == update_loading:
            progress = loading.get_widget("1")
            progress.set_value(progress.get_value() + 1)
            if progress.get_value() == 100:
                pygame.time.set_timer(update_loading, 0)
                gameLoop()
        if event.type == pygame.QUIT:
            exit()

    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(surface)
        if mainmenu.get_current().get_selected_widget():
            selected_widget = mainmenu.get_current().get_selected_widget()
            pygame.draw.rect(
                surface,
                (255, 255, 255),
                (
                    selected_widget.get_rect().x - 5,
                    selected_widget.get_rect().y - 5,
                    selected_widget.get_rect().width + 10,
                    selected_widget.get_rect().height + 10,
                ),
                3,
            )
            arrow.draw(surface, mainmenu.get_current().get_selected_widget())

    pygame.display.update()
