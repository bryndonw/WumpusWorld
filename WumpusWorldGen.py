import random

class WumpusWorldGen():
    def __init__(self):
        pass

    def generateGrid(self, size, ppit, pwumpus, pobstacle):
        """ Kieran Ringel
        Iterates over 2D array of board and populates pits, wumpuses, obstacles and one spot for gold
        """
        grid = []
        arrows = 0
        for i in range(size):
            row = []
            for j in range(size):
                num = random.uniform(0, 1)
                if num < ppit:  #if prob says cell is a pit
                    row.append('p')
                elif ppit < num < ppit + pwumpus:   #if prob says cell is a wumpus
                    arrows += 1 #one arrow for each wumpus
                    row.append('w')
                elif ppit + pwumpus < num < ppit + pwumpus + pobstacle: #if prob says cell is an obstacle
                    row.append('o')
                else:
                    row.append('f')     #frontier space
            grid.append(row)

        # adds gold to the board
        done = False
        while not done: #keeps going until it finds an empty cell for gold
            row = int(random.uniform(0, size))
            col = int(random.uniform(0, size))
            if grid[row][col] == 'f':   #if frontier cell
                grid[row][col] = 'g'    #add gold
                done = True

        #for i in range(size):
        #print(grid[i])

        return grid, arrows

    def startloc(self, grid):
        """ Kieran Ringel
        finds frontier cell for explorer to start at"""
        loc = []
        while True:
            row = int(random.uniform(0, len(grid)))
            col = int(random.uniform(0, len(grid)))
            if grid[row][col] == 'f':
                loc = [row, col]
                return loc
