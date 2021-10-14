import random

from InferenceSystem import InferenceSystem

import numpy as np

class Explorer():
    def __init__(self, grid):
        self.grid = grid

        # facing is the current direction the agent is facing. 1 is up, 2 is right, 3 is down, 4 is left
        self.points = 0
        self.facing = 1
        self.move = 0
        self.shoot = False

    def action(self, curr_pos, next_pos, act):
        # act is either shoot, or move (for every shoot or move, action will turn if needed).
        #   This is indicated by the next_pos. If we are shooting, we will face that direction and shoot, but not move
        #   If we are moving, we will face that direction AND move
        # curr_pos and next_pos are structured (row, column)
        # 0,0 is top left of board

        # every time we call action, we are either moving to a new square or we are shooting so we increment move
        self.move += 1

        # moving down (row is bigger on next position)

        if next_pos[0] > curr_pos[0]:
            if self.facing != 3:
                # since the agent isn't facing the correct way, we must add 1 to our moves and subtract 1 from points
                self.move += 1
                self.points -= 1
                # if agent is facing opposite direction, we have to make an additional move to face correct way
                if self.facing == 1:
                    self.move += 1
                    self.points -= 1
                self.facing = 3

        # moving left (col is smaller on next position)
        elif next_pos[1] < curr_pos[1]:
            if self.facing != 4:
                # since the agent isn't facing the correct way, we must add 1 to our moves
                self.move += 1
                self.points -= 1
                # if agent is facing opposite direction, we have to make an additional move to face correct way
                if self.facing == 2:
                    self.move += 1
                    self.points -= 1
                self.facing = 4

        # moving right (col is bigger on next position)
        elif next_pos[1] > curr_pos[1]:

            if self.facing != 2:
                # since the agent isn't facing the correct way, we must add 1 to our moves
                self.move += 1
                self.points -= 1
                # if agent is facing opposite direction, we have to make an additional move to face correct way
                if self.facing == 4:
                    self.move += 1
                    self.points -= 1
                self.facing = 2

        # moving up (row is smaller on next position)
        elif next_pos[0] < curr_pos[0]:
            if self.facing != 1:
                # since the agent isn't facing the correct way, we must add 1 to our moves
                self.move += 1
                self.points -= 1
                # if agent is facing opposite direction, we have to make an additional move to face correct way
                if self.facing == 3:
                    self.move += 1
                    self.points -= 1
                self.facing = 1

        if act == 'shoot':
            # shooting costs 10 points
            self.points -= 10
            self.shoot = True
            return curr_pos

        # moving forward costs 1 point
        self.points -= 1
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
                if self.grid[loc[0]][loc[1]] == 'w':
                    self.grid[loc[0]][loc[1]] = 'f'
                else:
                    self.grid[loc[0]][loc[1]] = 'g'
                return 'scream'
        return []




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
                print('Points: ' + str(self.points))
                return self.move
            elif percepts == 'win':
                print('won')
                # picking up the gold costs 1 point and is 1 move
                self.move += 1
                self.points -= 1
                # we have found the gold so we get 100 points
                self.points += 100
                print('Points: ' + str(self.points))
                return self.move + 1
            elif percepts == 'bump':
                location = self.action([rowloc, colloc], [prevrow, prevcol], 'move')
                self.move -= 1  #moving to wall and away from wall are counted, this should just be 1 move
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
                else:
                    location = self.action([rowloc, colloc], [rowloc, colloc], 'shoot')
            else:
                if prob < arrow:
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
            prevrow = rowloc
            prevcol = colloc
            rowloc = location[0]
            colloc = location[1]

        return self.move



    def inferenceAgent(self, rowloc, colloc):
        prevrow = rowloc
        prevcol = colloc
        while True:
            percepts = self.sense(rowloc, colloc)
            if percepts == 'dead':
                return self.move
            elif percepts == 'win':
                return self.move + 1
            elif percepts == 'bump':
                #update KB
                self.action([rowloc, colloc], [prevrow, prevcol], 'move')
                self.move -= 1  # moving to wall and away from wall are counted, this should just be 1 move
            elif percepts == 'scream':
                InferenceSystem.updateKBshot()      #EDIT MORE
            else:
                if self.grid[rowloc][colloc] == 'f':
                    infsys = InferenceSystem()
                    infsys.updateKB(rowloc, colloc, percepts)
                    self.grid[rowloc][colloc] == 'v'
            prevrow = rowloc
            prevcol = colloc
            location = self.action()
            rowloc = location[0]
            colloc = location[1]
