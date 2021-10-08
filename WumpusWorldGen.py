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
        print(grid)
        return grid
