from InferenceSystem import InferenceSystem

class Explorer():
    def __init__(self, grid):
        self.grid = grid

    def action(self):
        pass

    def sense(self, rowloc, colloc):
        print(self.grid[rowloc][colloc])
        senses = []
        checks = [[rowloc + 1, colloc], [rowloc - 1, colloc], [rowloc, colloc + 1], [rowloc, colloc - 1]]
        for check in checks:
            if check[0] < len(self.grid) and check[0] >= 0 and check[1] < len(self.grid) and check[1] >= 0:
                if 'w' in self.grid[check[0]][check[1]]:
                    senses.append('s')
                elif 'p' in self.grid[check[0]][check[1]]:
                    senses.append('b')
        if 'w' in self.grid[rowloc][colloc]:
            senses = 'dead'
        elif 'g' in self.grid[rowloc][colloc]:
            senses = 'win'
        elif 'o' in self.grid[rowloc][colloc]:
            senses = 'bump'
        return senses

    def reactiveAgent(self, rowloc, colloc):
        while True:
            percepts = self.sense(rowloc, colloc)
            if percepts == 'dead':
                return self.move
            elif percepts == 'win':
                return self.move + 1
            elif percepts == 'bump':
                pass #player returns to previous location NEED TO STORE PREV
            elif percepts == []:
                pass #
            else:
                pass #move in accordance of what was just sensed


    def inferenceAgent(self, rowloc, colloc):
        while True:
            percepts = self.sense(rowloc, colloc)
            if percepts == 'dead':
                return self.move
            elif percepts == 'win':
                return self.move + 1
            elif percepts == 'bump':
                pass  # player returns to previous location NEED TO STORE PREV
            elif len(percepts) != 0:
                InferenceSystem.updateKB(rowloc, colloc, percepts)
