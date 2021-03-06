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
        self.cap = len(grid)*len(grid) * 3

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
        #print('moved to ', next_pos)
        self.points -= 1
        self.cells += 1
        # we return current position
        return next_pos

    def sense(self, rowloc, colloc):
        """ Kieran Ringel
        Checks current cell for wumpus, pit obtacle or gold and adjacent cells for stench or breeze"""
        senses = []
        if self.shoot:  #if we have shot
            senses = self.shot(rowloc, colloc)  #checks if hit wumpus/ scream
            self.shoot = False
            return senses   #return if scream

        checks = [[rowloc + 1, colloc], [rowloc - 1, colloc], [rowloc, colloc + 1], [rowloc, colloc - 1]] #checks adjacent cells
        for check in checks:
            if check[0] < len(self.grid) and check[0] >= 0 and check[1] < len(self.grid) and check[1] >= 0: #checks valid adjacent cells
                if 'w' in self.grid[check[0]][check[1]]:    #if wumpus adjacent
                    senses.append('s')  #add stench
                elif 'p' in self.grid[check[0]][check[1]]:  #if pit adjacent
                    senses.append('b')  #add breeze
        if 'w' in self.grid[rowloc][colloc]:    #if explorer hit a wumpus
            senses = 'dead' #explorer dies
            print('Wumpus Death')
        elif 'p' in self.grid[rowloc][colloc]:  #if explorer hit a pit
            senses = 'dead' #explorer dies
            print('Pit Death')
        elif 'g' in self.grid[rowloc][colloc]:  #if explorer hit gold
            senses = 'win'  #explorer wins
        elif 'o' in self.grid[rowloc][colloc]:  #if explorer hits an obstacle
            senses = 'bump' #explorer adds obstacle
        elif self.cells == self.cap:    #if explorer is stuck and runs out of moves
            print('Starved to death in a cave')
            senses = 'dead' #explorer dies
        return senses

    def shot(self, rowloc, colloc):
        """Kieran Ringel
        checks if shot hits a wumpus or an obstacle"""
        if self.facing == 1:
            row = list(range(rowloc - 1, 0, -1))    #starts at next cell and goes to the edge of the board
            col = [colloc for i in range(len(row))] #gets column for every row val
        elif self.facing == 2:
            col = list(range(colloc + 1, len(self.grid)))
            row = [rowloc for i in range(len(col))]
        elif self.facing == 3:
            row = list(range(rowloc + 1, 0))
            col = [colloc for i in range(len(row))]
        elif self.facing == 4:
            col = list(range(colloc - 1, 0, -1))
            row = [rowloc for i in range(len(col))]
        test = np.array(list(zip(row, col)))    #gets 2d cordinates for every cell it is shooting at

        for loc in test:
            if 'o' in self.grid[loc[0]][loc[1]]:    #if an obstacle is hit, the arrow stops
                break
            elif 'w' in self.grid[loc[0]][loc[1]]:  #if a wumpus is hit, sense is a scream
                print('shot a wumpus')
                return 'scream'
        return []

    def finishGame(self):
        """Bryndon Wilkerson
        Prints information when the game is over"""
        print('Points:\t', self.points)
        print('Cells visited:',self.cells)
        #for g in self.grid:
        #    print(g)

    def reactiveAgent(self, rowloc, colloc):
        """Kieran Ringel
        Moves based on the percepts of the current cell, has no memory"""
        prevrow = rowloc
        prevcol = colloc
        arrow = .05 #probability of shooting arrow
        safe = .3   #probability of making safe move
        while True: #keep running until game ends and returns
            percepts = self.sense(rowloc, colloc)   #get senses from current cell
            if percepts == 'dead':  #if dead, game over
                print("dead")
                self.points -= 1000
                self.finishGame()
                return self.cells, self.points
            elif percepts == 'win': #if win, game over
                print('won')
                # picking up the gold costs 1 point and is 1 move, but we also get 100 points for winning
                self.points += 99
                self.finishGame()
                return self.cells, self.points
            elif percepts == 'bump':    #if explorer hits an obstacle it never moved to that cell
                # since we never make it into an obstacle, we remove one from the cells explored
                self.cells -= 1

                rowloc = prevrow
                colloc = prevcol
                #print('bump, move back to', rowloc, colloc)

            prob = random.uniform(0,1)  #random num to determine if shooting, moving safe or moving to potentially dangerous
            if percepts == []:  #no percepts means that every square around you is safe
                if prob > arrow:    #if every square is safe safe and dangerous prob are combined
                    notValid = True
                    while notValid: #loops until it finds a valid next move (not off board)
                        nextmove = random.randint(0,3)  #moves randomly to adjacent cell
                        if nextmove == 0:
                            if rowloc + 1 < len(self.grid): #checks if move is valid
                                location = self.action([rowloc, colloc], [rowloc + 1, colloc], 'move')  #calls action to count moves and points
                                notValid = False
                        elif nextmove == 1:
                            if colloc + 1 < len(self.grid):#checks if move is valid
                                location = self.action([rowloc, colloc], [rowloc, colloc + 1], 'move') #calls action to count moves and points
                                notValid = False
                        elif nextmove == 2:
                            if rowloc - 1 >= 0:#checks if move is valid
                                location = self.action([rowloc, colloc], [rowloc - 1, colloc], 'move') #calls action to count moves and points
                                notValid = False
                        elif nextmove == 3:
                            if colloc - 1 >= 0:#checks if move is valid
                                location = self.action([rowloc, colloc], [rowloc, colloc - 1], 'move') #calls action to count moves and points
                                notValid = False
                else: # if it's safe and we have an arrow, we will shoot randomly
                    if self.arrows > 0:
                        location = self.action([rowloc, colloc], [rowloc, colloc], 'shoot')
            else: # percieve stench or breeze
                if prob < arrow:    #small prob we shoot
                    if self.arrows > 0:
                        location = self.action([rowloc, colloc], [rowloc, colloc], 'shoot')
                elif arrow < prob and prob < arrow + safe:  #savemove
                    location = self.action([rowloc, colloc], [prevrow, prevcol], 'move')   #moves to previous cell since that is guarenteed to be safe
                else:   #dangerous move
                    notValid = True
                    while notValid: #loops until finds valid move
                        nextmove = random.randint(0, 3)
                        if nextmove == 0:
                            if rowloc + 1 < len(self.grid) and rowloc + 1 != prevrow: #checks if move is valid
                                location = self.action([rowloc, colloc], [rowloc + 1, colloc], 'move')  #calls action to count moves and points
                                notValid = False
                        elif nextmove == 1:
                            if colloc + 1 < len(self.grid) and colloc + 1 != prevcol:#checks if move is valid
                                location = self.action([rowloc, colloc], [rowloc, colloc + 1], 'move') #calls action to count moves and points
                                notValid = False
                        elif nextmove == 2:
                            if rowloc - 1 >= 0 and rowloc - 1 != prevrow:#checks if move is valid
                                location = self.action([rowloc, colloc], [rowloc - 1, colloc], 'move') #calls action to count moves and points
                                notValid = False
                        elif nextmove == 3:
                            if colloc - 1 >= 0 and colloc - 1 != prevcol:#checks if move is valid
                                location = self.action([rowloc, colloc], [rowloc, colloc - 1], 'move') #calls action to count moves and points
                                notValid = False
            # to see the cells that the reactive guy visits
            if self.grid[rowloc][colloc] == 'f':
                self.grid[rowloc][colloc] = 'v'
            prevrow = rowloc
            prevcol = colloc
            rowloc = location[0]
            colloc = location[1]
        # we shouldn't get here
        return self.cells, self.points



    def inferenceAgent(self, rowloc, colloc):
        """Kieran Ringel and Bryndon Wilkerson"""
        prevrow = rowloc
        prevcol = colloc
        infsys = InferenceSystem(len(self.grid))
        while True: #while we have not won or died
            percepts = self.sense(rowloc, colloc)   #sense current cell
            if percepts == 'dead':  #if we died
                self.points -= 1000 #minus 1000 points
                print('dead')
                #print(infsys.KB)
                self.finishGame()
                return self.cells, self.points
            elif percepts == 'win': #if we win
                # if we will, we take off 1 point for grabbing the gold and get 99 points for winning
                self.points += 99
                print('won')
                self.finishGame()
                return self.cells, self.points
            elif percepts == 'bump':    #if we hit obstacle
                #update KB
                infsys.updateKB(rowloc, colloc, percepts)   #update KB to include obstacle
                # we don't actually go to an obstacle cell, so we remove one from cells visited
                self.cells -= 1
                rowloc = prevrow
                colloc = prevcol
            elif percepts == 'scream':  #if a wumpus screams
                infsys.updateKBshot(rowloc, colloc, self.facing)    #update KB to kill that wumpus
            else:   #if we percieve stench, breeze, or nothing
                if self.grid[rowloc][colloc] == 'f':    #if we havent been there before
                    infsys.updateKB(rowloc, colloc, percepts)   #update KB with percepts
                    self.grid[rowloc][colloc] = 'v' #mark cell as visited
                location, act = infsys.bestAction(rowloc, colloc, self.cells)   #query KB to determine best move
                #print(location, act)
                #for i in range(len(self.grid)):
                #    print(self.grid[i])
                prevrow = rowloc
                prevcol = colloc
                newpos = self.action([rowloc, colloc], location, act)   #calls action to count moves and points
                rowloc = newpos[0]
                colloc = newpos[1]
        #shouldn't get here
        return self.cells, self.points

