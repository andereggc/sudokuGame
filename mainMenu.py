 import pygame, random, time
from random import sample
from copy import deepcopy
from sudokuGen import * # contains functions used to create and solve boards that will be given to the user 

class Grid:
    # creates the grid Sudoku is played on
    def __init__(self, rows, cols, width, height, win, board):
        # constructor
        self.rows = rows
        self.cols = cols # rows and cols for board
        self.cubes = [[Cube(board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height # width and height of board
        self.model = None # updates the board
        self.update_model() # updates the board
        self.selected = None # which tile is selected
        self.win = win # pygame window

    def update_model(self):
        # updates the board
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        # places a number on an empty tile if number is correct
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and self.solve():
                # checks if the placement is a valid tile
                return True
            else:
                # if it's not valid, leave the space blank
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        # gives values and selects tile
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        # draws grid lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4 # creates the thick lines that divides the board into nine sections
            else:
                thick = 1 # creates the thin lines between each tile
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # draws cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        # selects a tile
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False # sets all tiles to not selected

        self.cubes[row][col].selected = True # set the tile passed by params to .selected = True, meaning it is the only tile selected
        self.selected = (row, col) # updates .selected with (x,y)

    def clear(self):
        # deletes input if user doesn't press return
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        # checks that the mouse is in the window then returns the (x,y) coordinates of wherever the mouse is
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        # checks if the board is finished
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False # if any tile is blank then it's not solved
        return True

    def solve(self):
        # recursive backtracking algorithm used by placement function
        find = find_empty(self.model)
        if not find: # if it cannot find a blank space then the board must be solved
            return True # board is solved
        else:
            row, col = find # find is (x,y)

        for i in range(1, 10):
            if valid(self.model, i, (row, col)): # iterates through board and attemps to place i 
                self.model[row][col] = i

                if self.solve(): # starts recursion, will return True when there are no more spaces to find
                    return True # ends recursion, solve will only return True when it cannot find an blank space
        
                self.model[row][col] = 0 # i is valid but solve is False, set to 0

        return False # if no valid spots, return False

    def solveGUI(self):
        # recursive backtracking algorithm used for GUI
        self.update_model() # updates model
        find = find_empty(self.model) 
        if not find: # if it cannot find a blank space then the board must be solved
            return True # board is solved
        else:
            row, col = find # find is (x,y)

        for i in range(1, 10): 
            if valid(self.model, i, (row, col)): # iterates through board and attemps to place i 
                self.model[row][col] = i 
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(20) # speed displayed solving

                if self.solveGUI(): # starts recursion, will return True when there are no more spaces to find
                    return True # ends recursion, solveGUI will only return True when it cannot find an blank space

                self.model[row][col] = 0 # i is valid but solve is False, set to 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update() # updates frames
                pygame.time.delay(20) # speed displayed solving

        return False # if no valid spots, return False

class Cube:
    # each tile on the board
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        #  constructor
        self.value = value # tile's value
        self.temp = 0 # temporary tile value
        self.row = row
        self.col = col
        self.width = width
        self.height = height  # row, col, width, height of the board
        self.selected = False # if tile is selected

    def draw(self, win):
        # draws the number on the tile
        fnt = pygame.font.SysFont("comicsans", 40) # font for text
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:  # if tile is blank
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0)) # if tile is not blank don't change it
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        if self.selected:
            pygame.draw.rect(win, (230,122,0), (x,y, gap ,gap), 3)  # creates orange outline on selected tile

    def draw_change(self, win, g=True):
        # draws changes on the board when recursive algorithm is running
        fnt = pygame.font.SysFont("comicsans", 40) # font for text
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0) # originally makes background white
        text = fnt.render(str(self.value), 1, (0, 0, 0)) 
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3) # green outline if correct
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3) # red outline if incorrect

    def set(self, val):
        # sets value
        self.value = val

    def set_temp(self, val):
        # sets temp value
        self.temp = val

def find_empty(bo):
    # iterates through board and returns (x,y) of first blank space
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None

def valid(bo, num, pos):
    # checks for all validity
    # check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True # if it gets to this point it must be valid

def redraw_window(win, board, time, strikes, hits):
    # redraws the grid
    win.fill((255,255,255)) # fills board white
    fnt = pygame.font.SysFont("comicsans", 30) # font for text
    # counter for hits and misses, timer, new game button
    textMiss = fnt.render("Misses: " + str(strikes), 1, (255, 0, 0))
    win.blit(textMiss, (20, 560))
    textHit = fnt.render("Hits: " + str(hits), 1, (0, 255, 0))
    win.blit(textHit, (150, 560))
    timer = fnt.render("Time: " + formatTime(time), 1, (0,0,0))
    win.blit(timer, (380, 560))
    mouse = pygame.mouse.get_pos()
    # button changes color if mouse is hovering over it
    if 247 <= mouse[0] <= 361 and 550 <= mouse[1] <= 583: 
        pygame.draw.rect(win,(0,255,0),[247,553,111,30]) # while hovering turn button green
    else:
        pygame.draw.rect(win,(255,0,0),[247,553,111,30]) # while not hovering turn button red

    newGame = fnt.render('New Game' , True , (0, 0, 0)) 
    win.blit(newGame, (250,560)) 
    board.draw() # draw grid and board

def formatTime(secs):
    # formats how the timer is displayed
    sec = secs%60
    minute = secs//60
    if sec < 10:
        mat = " " + str(minute) + ":0" + str(sec) # adds extra 0 for first 9 seconds of each minute
    else:
        mat = " " + str(minute) + ":" + str(sec) 
    return mat

def formMake(difficulty):
    # creates and returns board of user selected difficulty
    board = format(maker(difficulty)) # difficulty is the amount of blank spaces on the board, the more blank spaces, the harder it is
    return board

def sudGame(difficulty):
    # suduoku game
    win = pygame.display.set_mode((540,600))  # game window
    grid = formMake(difficulty) 
    board = Grid(9, 9, 540, 540, win, grid) # calls Grid class to create a board
    
    # change caption based on difficulty
    if difficulty == 44:
        pygame.display.set_caption('Sudoku - Easy')
    elif difficulty == 50:
        pygame.display.set_caption('Sudoku - Medium')
    elif difficulty == 58:
        pygame.display.set_caption('Sudoku - Hard')
    elif difficulty == 64:
        pygame.display.set_caption('Sudoku - Impossible')

    key = None # key pressed by user
    start = time.time() # timer
    strikes = 0 
    hits = 0 # hits and strikes for the counter
    returnKeyGate = False # fixes error where hitting return before clicking a square would crash the program
    while True:
        play_time = round(time.time() - start) # starts timer
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN: # user inputs
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear() # deletes input if return isn't pressed
                    key = None # reset key
                if event.key == pygame.K_SPACE:
                    board.solveGUI() # runs recursive solving algorithm
                if (event.key == pygame.K_RETURN) and returnKeyGate == True:
                    # will attempt to enter user's input to the tile, hit and strike react accordingly
                    i, j = board.selected 
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            hits += 1
                        else:
                            strikes += 1
                        key = None # reset key
                            
            if event.type == pygame.MOUSEBUTTONDOWN:
                returnKeyGate = True # fixes reutrn key error 
                mouse = pygame.mouse.get_pos()
                clicked = board.click(mouse)
                if clicked: # board is clicked, select the tile that was clicked
                    board.select(clicked[0], clicked[1])
                    key = None # resets key
                if 247 <= mouse[0] <= 361 and 550 <= mouse[1] <= 583:
                    diffMenu() # if user clicks new game send them to difficulty menu
                    pygame.quit() 

        if board.selected and key != None:
            board.sketch(key) # sketches key
        
        redraw_window(win, board, play_time, strikes, hits)
        pygame.display.update() # updates frames 

def diffMenu():
    # difficulty menu
    pygame.init() # initializing the constructor   
    res = (720,720) # screen resolution 
    screen = pygame.display.set_mode(res) # opens up a window 
    pygame.display.set_caption('Difficulty Menu')
    screen.fill((0,0,0)) # black screen
    color_light = (170,170,170) # light shade of the button 
    color_dark = (100,100,100) # dark shade of the button
    txtColor = (18, 196, 255) # color of text
    title2 = pygame.font.SysFont('Georgia', 50)
    # menu text
    title2Card = title2.render("Choose your difficulty", True, txtColor)
    button = pygame.font.SysFont('Verdana', 35) 
    easyBut = button.render('Easy', True, txtColor) 
    medBut = button.render('Medium', True, txtColor) 
    hardBut = button.render('Hard', True, txtColor) 
    impBut = button.render('Hardest', True, txtColor) 
    quitBut = button.render('Quit', True, txtColor)

    while True:       
        mouse = pygame.mouse.get_pos()   # stores the (x,y) coordinates into the variable as a tuple    
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()  
            #checks if a mouse is clicked 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 280 <= mouse[0] <= 420 and 220 <= mouse[1] <= 260: 
                    sudGame(44) # easy
                elif 280 <= mouse[0] <= 420 and 320 <= mouse[1] <= 360: 
                    sudGame(50) # medium
                elif 280 <= mouse[0] <= 420 and 420 <= mouse[1] <= 460: 
                    sudGame(58) # hard
                elif 280 <= mouse[0] <= 420 and 520 <= mouse[1] <= 560:
                    sudGame(64) # impossible
                elif 280 <= mouse[0] <= 420 and 620 <= mouse[1] <= 660:
                    pygame.quit() # quit

        # if mouse is hovered on a button it changes to lighter shade 
        if 280 <= mouse[0] <= 420 and 220 <= mouse[1] <= 260:
            pygame.draw.rect(screen,color_light,[280,220,140,40]) 
        elif 280 <= mouse[0] <= 420 and 320 <= mouse[1] <= 360: 
            pygame.draw.rect(screen,color_light,[280,320,140,40]) 
        elif 280 <= mouse[0] <= 420 and 420 <= mouse[1] <= 460: 
            pygame.draw.rect(screen,color_light,[280,420,140,40]) 
        elif 280 <= mouse[0] <= 420 and 520 <= mouse[1] <= 560: 
            pygame.draw.rect(screen,color_light,[280,520,140,40]) 
        elif 280 <= mouse[0] <= 420 and 620 <= mouse[1] <= 660: 
            pygame.draw.rect(screen,color_light,[280,620,140,40]) 
        else:
            pygame.draw.rect(screen,color_dark,[280,220,140,40]) 
            pygame.draw.rect(screen,color_dark,[280,320,140,40]) 
            pygame.draw.rect(screen,color_dark,[280,420,140,40]) 
            pygame.draw.rect(screen,color_dark,[280,520,140,40]) 
            pygame.draw.rect(screen,color_dark,[280,620,140,40])  
        
        # superimposing the text onto our button 
        screen.blit(easyBut, (305, 216))
        screen.blit(medBut, (281, 316))
        screen.blit(hardBut, (305, 418)) 
        screen.blit(impBut, (280, 518))  
        screen.blit(quitBut, (305, 616))
        screen.blit(title2Card, (120, 129))  
      
        pygame.display.update() # updates the frames of the game 

def main():
    # main menu
    pygame.init() # initializing the constructor   
    res = (720,720) # screen resolution 
    screen = pygame.display.set_mode(res) # opens up a window 
    pygame.display.set_caption('Main Menu')
    screen.fill((0,0,0)) # black screen
    color_light = (170,170,170) # light shade of the button 
    color_dark = (100,100,100) # dark shade of the button 
    txtColor = (18, 196, 255) # color of text
    title = pygame.font.SysFont('Georgia', 100)
    button = pygame.font.SysFont('Verdana', 35) # fonts for text
    info = pygame.font.SysFont('Verdana', 24)
    # main menu info
    titleCard = title.render("Cam's Sudoku", True, txtColor)
    startButton = button.render('Start' , True , txtColor) 
    quitButton = button.render('Quit' , True , txtColor) 
    info1 = info.render('Hello and welcome to my Sudoku game! All standard', True, txtColor) 
    info2 = info.render('Sudoku rules apply. To input a number simply click', True, txtColor) 
    info3 = info.render('a square, choose 1-9, and press return.', True, txtColor) 
    info4 = info.render('You can press the spacebar at any point and watch my', True, txtColor)     
    info5 = info.render('recursive backtracking algorithm solve the board', True, txtColor)     

    while True: 
        mouse = pygame.mouse.get_pos() # stores the (x,y) coordinates into the variable as a tuple 
        for event in pygame.event.get(): # any action from user
            if event.type == pygame.QUIT: # quits game
                pygame.quit()       
            if event.type == pygame.MOUSEBUTTONDOWN: # checks if a mouse is clicked 
                if 280 <= mouse[0] <= 420 and 360 <= mouse[1] <= 400: 
                    diffMenu() # sends user to difficulty menu
                if 280 <= mouse[0] <= 420 and 460<= mouse[1] <= 500: 
                    pygame.quit() 

        # if mouse is hovered on a button it changes to lighter shade 
        if 280 <= mouse[0] <= 420 and 360 <= mouse[1] <= 400: 
            pygame.draw.rect(screen,color_light,[280,360,140,40])
            
        elif 280 <= mouse[0] <= 420 and 460 <= mouse[1] <= 500: 
            pygame.draw.rect(screen,color_light,[280,460,140,40]) 
        else:
            pygame.draw.rect(screen,color_dark,[280,360,140,40]) 
            pygame.draw.rect(screen,color_dark,[280,460,140,40]) 
      
        # superimposing the text onto our button 
        screen.blit(startButton, (303,356))
        screen.blit(quitButton, (310, 455)) 
        screen.blit(info1, (20,535))  
        screen.blit(info2, (20,560))  
        screen.blit(info3, (20,585))  
        screen.blit(info4, (20,630))  
        screen.blit(info5, (20,655))  
        screen.blit(titleCard, (50, 120))
        
        pygame.display.update() # updates the frames of the game 
        
main() # starts program
