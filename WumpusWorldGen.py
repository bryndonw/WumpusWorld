import random

class WumpusWorldGen():
    def __init__(self):
        pass

    def generateGrid(self, size, ppit, pwumpus, pobstacle):
        grid = []
        arrows = 0
        for i in range(size):
            row = []
            for j in range(size):
                num = random.uniform(0, 1)
                if num < ppit:
                    row.append('p')
                elif ppit < num < ppit + pwumpus:
                    arrows += 1
                    row.append('w')
                elif ppit + pwumpus < num < ppit + pwumpus + pobstacle:
                    row.append('o')
                else:
                    row.append('f')     #frontier space
            grid.append(row)

        # adds gold to the board
        done = False
        while not done:
            row = int(random.uniform(0, size))
            col = int(random.uniform(0, size))
            if grid[row][col] == 'f':
                grid[row][col] = 'g'
                done = True

        for i in range(size):
            print(grid[i])

        return grid, arrows

    def startloc(self, grid):
        loc = []
        while True:
            row = int(random.uniform(0, len(grid)))
            col = int(random.uniform(0, len(grid)))
            if grid[row][col] == 'f':
                loc = [row, col]
                return loc
