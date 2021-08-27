import pygame, sys, random
from random import sample
from copy import deepcopy

"""
formats and creates solved sudoku boards of varying difficulty
"""

pygame.font.init() # initializing the constructor 

def solve(grid):
    # recursive backtracking algorithm 
    find = is_empty(grid)
    if not find:  # if it cannot find a blank space then the board must be solved
        return True # board is solved
    else:
        row, col = find # find is (x,y)
    
    for i in range(1,10):
        i = random.sample(range(1,10),1)[0] # randomizes board
        if check(grid, i, (row, col)): # iterates through board and attemps to place i. 
            grid[row][col] = i # if valid, set tile to that value
            
            if solve(grid): # starts recursion, will return True when there are no more spaces to find
                return True # ends recursion, solve will only return True when it cannot find an blank space
            
            grid[row][col] = 0 # i is valid but solve is False, set to 0
        
    return False # if no valid spots, return False

def check(grid, num, pos):
   # checks if num is in row, column, or block
   if num in row(grid, pos[0]) or num in column(grid, pos[1]) or num in block(grid, pos):
       return False
   return True


def is_empty(grid): 
    # checks if cell is empty
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                return (i, j) # if it's empty return (x,y) of empty tile
    return None

def solution():
    # makes empty grid, then returns solved grid
    grid = [[0 for n in range(9)] for m in range(9)] # produces empty grid (9x9 2D array containing only zeros)
    solve(grid) # which is then passed to the solve method to create a solved grid
    return grid

def maker(diff):
    # used in mainMenu.py, starts the process of creating a board 
    sol = solution() # starts with an empty grid then solves it
    puzzle = deepcopy(sol) # creates a copy
  
    for i in sample(range(81), diff): # we then iterate through the array diff amount of times, then i is set to a random number from 1-81
        puzzle[i//9][i%9] = 0 # we then set i to zero so that the board is now incomplete 
    
    # starts with empty 9x9 grid, randomizes and solves it, then randomly sets tiles to zero (amount of tiles is decided by difficulty), creating a new, random board ready for sudoku
    return [puzzle] 

def format(puzzle):
    # formats the puzzle so it can be called in mainMenu.py
    newBoard = []
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            newBoard.append(puzzle[i][j]) # creates 2D array full of zeros

    return newBoard

"""
3 functions below are used to access row, column, and block relative to position
"""
def row(grid, row):
    return grid[row]

def column(grid, col):
    return [grid[i][col] for i in range(len(grid))]

def block(grid, pos): 
    box = (pos[0] // 3, pos[1] // 3)                           
    box_num = [
                grid[i][j] 
                for i in range(box[0]*3, box[0]*3 + 3) 
                for j in range(box[1]*3, box[1]*3 + 3)
                ] 
    return box_num
