import random

class WumpusWorldGen():
    def __init__(self):
        pass

    def generateGrid(self, size, ppit, pwumpus, pobstacle):
        grid = []
        for i in range(size):
            row = []
            for j in range(size):
                num = random.uniform(0, 1)
                if num < ppit:
                    row.append('p')
                elif ppit < num < ppit + pwumpus:
                    row.append('w')
                elif ppit + pwumpus < num < ppit + pwumpus + pobstacle:
                    row.append('o')
                else:
                    row.append('s')
            grid.append(row)

        # adds gold to the board
        done = False
        while not done:
            row = int(random.uniform(0, size))
            col = int(random.uniform(0, size))
            if grid[row][col] == 's':
                grid[row][col] = 'g'
                done = True

        for i in range(size):
            print(grid[i])

        return grid
