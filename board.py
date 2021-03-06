import random
from tile import Tile, EmptyTile, MAXTILE
import pygame

class Board(object):
    def __init__(self):
        self.grid = [[EmptyTile()]*4 for _ in range(4)]
        self.score = 0
        self._initialiseLayout()
              
    def display(self):
        for row in self.grid:
            print('', end='|')
            for entry in row:
                print(entry, end= '|')
            print('\n', end='')
            print('-'*9)
        print("Score: ", self.score)
        print('\n', end ='')
            
    def _initialiseLayout(self):
        a,b = random.sample(range(16),2)
        aRow = a % 4
        aCol = int((a - aRow)/4)
        self.grid[aRow][aCol] = Tile()
        bRow = b % 4
        bCol = int((b - bRow) / 4)
        self.grid[bRow][bCol] = Tile()
    
    def reset_tiles(self):
        for row in self.grid:
            for tile in row:
                tile.set_display()
                tile.speed = (0,0)
                tile.scale = 1

    def move(self, direction):
        newTile = False
        if direction == pygame.K_LEFT:
            newTile = self._moveLeft()
        elif direction == pygame.K_RIGHT:
            newTile = self._moveRight()
        elif direction == pygame.K_DOWN:
            newTile = self._moveDown()
        elif direction == pygame.K_UP:
            newTile = self._moveUp()

        if newTile:
            tile, pos = self.addTile()
            return (newTile, tile, pos)
        return (False, 0, 0)
        

    def _moveLeft(self):
        success = False
        for i in range(4):  # for each row
            k=0
            mergeAllow = True
            for j in range(4):   # search for the next non empty tile
                if not self.grid[i][j].isEmpty():
                    tile = self.grid[i][j]  # pick up non empty tile
                    self.grid[i][j] = EmptyTile()   # free up the space
                    if k > 0 and self.grid[i][k-1] == tile and mergeAllow:
                        self.grid[i][k-1].value += tile.value
                        self.score += tile.value * 2
                        success = True
                        mergeAllow = False
                        tile.speed = (k-1-j,0)
                    else:
                        self.grid[i][k] = tile  # place the tile in the leftmost pos
                        tile.speed = (k-j,0)
                        if k != j:
                            success = True
                        k+=1
                        mergeAllow = True
                        
        return success

    def _moveRight(self):
        success = False
        for i in range(4):  # for each row
            k=0
            mergeAllow = True
            for j in range(k, 4):   # search for the next non empty tile
                if not self.grid[i][3-j].isEmpty():
                    tile = self.grid[i][3-j]  # pick up non empty tile
                    self.grid[i][3-j] = EmptyTile()   # free up the space
                    if k > 0 and self.grid[i][4-k] == tile and mergeAllow:
                        self.grid[i][4-k].value += tile.value
                        self.score += tile.value * 2
                        success = True
                        mergeAllow = False
                        tile.speed = (1- k + j,0)
                    else:
                        self.grid[i][3-k] = tile  # place the tile in the rightmost pos
                        tile.speed = (j-k,0)
                        if k != j:
                            success = True
                        k+=1
                        mergeAllow = True
        return success

    def _moveDown(self):
        success = False
        for i in range(4):  # for each col
            k=0
            mergeAllow = True
            for j in range(k, 4):   # ...search for the next non empty tile
                if not self.grid[3-j][i].isEmpty():
                    tile = self.grid[3-j][i]  # pick up non empty tile
                    self.grid[3-j][i] = EmptyTile()   # free up the space
                    if k > 0 and self.grid[4-k][i] == tile and mergeAllow:
                        self.grid[4-k][i].value += tile.value
                        self.score += tile.value * 2
                        success = True
                        mergeAllow = False
                        tile.speed = (0, 1-k+j)
                    else:
                        self.grid[3-k][i] = tile  # place the tile in the bottom pos
                        tile.speed = (0, j-k)
                        if k != j:
                            success = True
                        k+=1
                        mergeAllow = True
        return success

    def _moveUp(self):
        success = False
        for i in range(4):  # for each col
            k=0
            mergeAllow = True
            for j in range(k, 4):   # ...search for the next non empty tile
                if not self.grid[j][i].isEmpty():
                    tile = self.grid[j][i]  # pick up non empty tile
                    self.grid[j][i] = EmptyTile()   # free up the space
                    if k > 0 and self.grid[k-1][i] == tile and mergeAllow:
                        self.grid[k-1][i].value += tile.value
                        self.score += tile.value * 2
                        success = True
                        mergeAllow = False
                        tile.speed = (0, k-1-j)
                    else:
                        self.grid[k][i] = tile  # place the tile in the leftmost pos
                        tile.speed = (0, k-j)
                        if k != j:
                            success = True
                        k+=1
                        mergeAllow = True
        return success

    def emptySpaces(self):
        spaces = []
        for i in range(4):
            for j in range(4):
                if self.grid[i][j].isEmpty():
                    spaces.append(i + 4*j)
        return spaces

    def addTile(self):
        spaces = self.emptySpaces()
        a = random.choice(spaces)
        aRow = a % 4
        aCol = int((a - aRow)/4)
        new_tile = Tile()
        new_tile.scale = 0.2
        self.grid[aRow][aCol] = new_tile
        return (new_tile, (aRow, aCol))

    
    def stillAlive(self):
        if len(self.emptySpaces()) > 0:
            return True
        else:
            for i in range(4):
                for j in range(3):
                    if self.grid[i][j] == self.grid[i][j+1]:
                        return True
            for i in range(4):
                for j in range(3):
                    if self.grid[j][i] == self.grid[j+1][i]:
                        return True
    
    def checkWin(self):
        win = False
        for row in self.grid:
            for t in row:
                if t.image_index == MAXTILE - 1:
                    win = True
        return win

                    
                