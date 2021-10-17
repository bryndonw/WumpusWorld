import random

from InferenceSystem import InferenceSystem

import numpy as np

class Explorer():
    def __init__(self, grid, arrows):
        self.grid = grid
        self.arrows = arrows
        # facing is the current direction the agent is facing. 1 is up, 2 is right, 3 is down, 4 is left
        self.points = 0 # counts our points
        self.facing = 1
        self.cells = 0 #counts everytime we move to a new cell and everytime we shoot
        self.shoot = False

    def action(self, curr_pos, next_pos, act):
        # act is either shoot, or move (for every shoot or move, action will turn if needed).
        #   This is indicated by the next_pos. If we are shooting, we will face that direction and shoot, but not move
        #   If we are moving, we will face that direction AND move
        # curr_pos and next_pos are structured (row, column)
        # 0,0 is top left of board

        # moving down (row is bigger on next position)

        if next_pos[0] > curr_pos[0]:
            if self.facing != 3:
                # since the agent isn't facing the correct way, we must add 1 to our moves and subtract 1 from points
                self.points -= 1
                # if agent is facing opposite direction, we have to make an additional move to face correct way
                if self.facing == 1:
                    self.points -= 1
                self.facing = 3

        # moving left (col is smaller on next position)
        elif next_pos[1] < curr_pos[1]:
            if self.facing != 4:
                # since the agent isn't facing the correct way, we must add 1 to our moves
                self.points -= 1
                # if agent is facing opposite direction, we have to make an additional move to face correct way
                if self.facing == 2:
                    self.points -= 1
                self.facing = 4

        # moving right (col is bigger on next position)
        elif next_pos[1] > curr_pos[1]:

            if self.facing != 2:
                # since the agent isn't facing the correct way, we must add 1 to our moves
                self.points -= 1
                # if agent is facing opposite direction, we have to make an additional move to face correct way
                if self.facing == 4:
                    self.points -= 1
                self.facing = 2

        # moving up (row is smaller on next position)
        elif next_pos[0] < curr_pos[0]:
            if self.facing != 1:
                # since the agent isn't facing the correct way, we must subtract 1 from points
                self.points -= 1
                # if agent is facing opposite direction, we have to make an additional move to face correct way
                if self.facing == 3:
                    self.points -= 1
                self.facing = 1

        if act == 'shoot':
            # shooting costs 10 points
            print('shoot')
            self.points -= 10
            self.shoot = True
            self.arrows -= 1
            return curr_pos

        # moving forward costs 1 point and we enter a cell
        print('moved to ', next_pos)
        self.points -= 1
        self.cells += 1
        # we return current position
        return next_pos

    def sense(self, rowloc, colloc):
        senses = []
        if self.shoot:
            senses = self.shot(rowloc, colloc)
            self.shoot = False
            return senses

        checks = [[rowloc + 1, colloc], [rowloc - 1, colloc], [rowloc, colloc + 1], [rowloc, colloc - 1]]
        for check in checks:
            if check[0] < len(self.grid) and check[0] >= 0 and check[1] < len(self.grid) and check[1] >= 0:
                if 'w' in self.grid[check[0]][check[1]]:
                    senses.append('s')
                elif 'p' in self.grid[check[0]][check[1]]:
                    senses.append('b')
        if 'w' in self.grid[rowloc][colloc]:
            senses = 'dead'
            print('Wumpus Death')
        elif 'p' in self.grid[rowloc][colloc]:
            senses = 'dead'
            print('Pit Death')
        elif 'g' in self.grid[rowloc][colloc]:
            senses = 'win'
        elif 'o' in self.grid[rowloc][colloc]:
            senses = 'bump'
        return senses

    def shot(self, rowloc, colloc):
        if self.facing == 1:
            row = list(range(rowloc - 1, 0, -1))
            col = [colloc for i in range(len(row))]
        elif self.facing == 2:
            col = list(range(colloc + 1, len(self.grid)))
            row = [rowloc for i in range(len(col))]
        elif self.facing == 3:
            row = list(range(rowloc + 1, 0))
            col = [colloc for i in range(len(row))]
        elif self.facing == 4:
            col = list(range(colloc - 1, 0, -1))
            row = [rowloc for i in range(len(col))]
        test = np.array(list(zip(row, col)))

        for loc in test:
            if 'o' in self.grid[loc[0]][loc[1]]:
                break
            elif 'w' in self.grid[loc[0]][loc[1]]:
                print('shot a wumpus')
                return 'scream'
        return []

    def finishGame(self):
        print('Points:\t', self.points)
        print('Cells visited:',self.cells)
        for g in self.grid:
            print(g)

    def reactiveAgent(self, rowloc, colloc):
        prevrow = rowloc
        prevcol = colloc
        arrow = .05
        safe = .3
        while True:
            percepts = self.sense(rowloc, colloc)
            if percepts == 'dead':
                print("dead")
                self.points -= 1000
                self.finishGame()
                return self.cells
            elif percepts == 'win':
                print('won')
                # picking up the gold costs 1 point and is 1 move, but we also get 100 points for winning
                self.points += 99
                self.finishGame()
                return self.cells
            elif percepts == 'bump':
                # since we never make it into an obstacle, we remove one from the cells explored
                self.cells -= 1

                rowloc = prevrow
                colloc = prevcol
                #print('bump, move back to', rowloc, colloc)

            prob = random.uniform(0,1)
            if percepts == []:  #no percepts means that every square around you is safe
                if prob > arrow:    #if every square is safe safe and dangerous prob are combined
                    notValid = True
                    while notValid:
                        nextmove = random.randint(0,3)
                        if nextmove == 0:
                            if rowloc + 1 < len(self.grid):
                                location = self.action([rowloc, colloc], [rowloc + 1, colloc], 'move')
                                notValid = False
                        elif nextmove == 1:
                            if colloc + 1 < len(self.grid):
                                location = self.action([rowloc, colloc], [rowloc, colloc + 1], 'move')
                                notValid = False
                        elif nextmove == 2:
                            if rowloc - 1 >= 0:
                                location = self.action([rowloc, colloc], [rowloc - 1, colloc], 'move')
                                notValid = False
                        elif nextmove == 3:
                            if colloc - 1 >= 0:
                                location = self.action([rowloc, colloc], [rowloc, colloc - 1], 'move')
                                notValid = False
                else: # if it's safe and we have an arrow, we will shoot randomly
                    if self.arrows > 0:
                        location = self.action([rowloc, colloc], [rowloc, colloc], 'shoot')
            else: # if it's dangerous, we will shoot
                if prob < arrow:
                    if self.arrows > 0:
                        location = self.action([rowloc, colloc], [rowloc, colloc], 'shoot')
                elif arrow < prob and prob < arrow + safe:  #savemove
                    location = self.action([rowloc, colloc], [prevrow, prevcol], 'move')   #moves to previous cell since that is guarenteed to be safe
                else:   #dangerous move
                    notValid = True
                    while notValid:
                        nextmove = random.randint(0, 3)
                        if nextmove == 0:
                            if rowloc + 1 < len(self.grid) and rowloc + 1 != prevrow:
                                location = self.action([rowloc, colloc], [rowloc + 1, colloc], 'move')
                                notValid = False
                        elif nextmove == 1:
                            if colloc + 1 < len(self.grid) and colloc + 1 != prevcol:
                                location = self.action([rowloc, colloc], [rowloc, colloc + 1], 'move')
                                notValid = False
                        elif nextmove == 2:
                            if rowloc - 1 >= 0 and rowloc - 1 != prevrow:
                                location = self.action([rowloc, colloc], [rowloc - 1, colloc], 'move')
                                notValid = False
                        elif nextmove == 3:
                            if colloc - 1 >= 0 and colloc - 1 != prevcol:
                                location = self.action([rowloc, colloc], [rowloc, colloc - 1], 'move')
                                notValid = False
            # to see the cells that the reactive guy visits
            if self.grid[rowloc][colloc] == 'f':
                self.grid[rowloc][colloc] = 'v'
            prevrow = rowloc
            prevcol = colloc
            rowloc = location[0]
            colloc = location[1]
        # we shouldn't get here
        return self.cells



    def inferenceAgent(self, rowloc, colloc):
        prevrow = rowloc
        prevcol = colloc
        infsys = InferenceSystem(len(self.grid))
        while True:
            percepts = self.sense(rowloc, colloc)
            if percepts == 'dead':
                self.points -= 1000
                print('dead')
                #print(infsys.KB)
                self.finishGame()
                return self.cells
            elif percepts == 'win':
                # if we will, we take off 1 point for grabbing the gold and get 99 points for winning
                self.points += 99
                print('won')
                self.finishGame()
                return self.cells
            elif percepts == 'bump':
                #update KB
                infsys.updateKB(rowloc, colloc, percepts)
                # we don't actually go to an obstacle cell, so we remove one from cells visited
                self.cells -= 1
                rowloc = prevrow
                colloc = prevcol
            elif percepts == 'scream':
                infsys.updateKBshot(rowloc, colloc, self.facing)
            else:
                if self.grid[rowloc][colloc] == 'f':
                    infsys.updateKB(rowloc, colloc, percepts)
                    self.grid[rowloc][colloc] = 'v'
                location, act = infsys.bestAction(rowloc, colloc, self.cells)
                #print(location, act)
                #for i in range(len(self.grid)):
                #    print(self.grid[i])
                prevrow = rowloc
                prevcol = colloc
                newpos = self.action([rowloc, colloc], location, act)
                rowloc = newpos[0]
                colloc = newpos[1]

