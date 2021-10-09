from InferenceSystem import InferenceSystem

class Explorer():
    def __init__(self, grid):
        self.grid = grid

        # facing is the current direction the agent is facing. 1 is up, 2 is right, 3 is down, 4 is left
        self.facing = 1
        self.move = 0
        self.shoot = False

        pass


    def action(self, curr_pos, next_pos, act):
        # act is either turn_left, turn_right, shoot, or move
        # curr_pos and next_pos are structured (row, column)
        # 0,0 is top left of board
        print(act)
        self.move += 1

        if act == 'shoot':
            print('shoot')
            return curr_pos
        elif act == 'turn_left':
            if self.facing == 1:
                self.facing = 4
            else:
                self.facing -= 1
            return curr_pos
        elif act == 'turn_right':
            if self.facing == 4:
                self.facing = 1
            else:
                self.facing += 1
            return curr_pos
        else:
            # moving down (row is bigger on next position)
            if next_pos[0] > curr_pos[0]:
                if self.facing != 3:
                    # since the agent isn't facing the correct way, we must add 1 to our count
                    self.move += 1
                    # if agent is facing opposite direction, we have to make an additional move to face correct way
                    if self.facing == 1:
                        self.move += 1
                    self.facing = 3

            # moving left (col is smaller on next position)
            elif next_pos[1] < curr_pos[1]:
                if self.facing != 4:
                    # since the agent isn't facing the correct way, we must add 1 to our count
                    self.move += 1
                    # if agent is facing opposite direction, we have to make an additional move to face correct way
                    if self.facing == 2:
                        self.move += 1
                    self.facing = 4

            # moving right (col is bigger on next position)
            elif next_pos[1] > curr_pos[1]:

                if self.facing != 2:
                    # since the agent isn't facing the correct way, we must add 1 to our count
                    self.move += 1
                    # if agent is facing opposite direction, we have to make an additional move to face correct way
                    if self.facing == 4:
                        self.move += 1
                    self.facing = 2

            # moving up (row is smaller on next position)
            elif next_pos[0] < curr_pos[0]:
                if self.facing != 1:
                    # since the agent isn't facing the correct way, we must add 1 to our count
                    self.move += 1
                    # if agent is facing opposite direction, we have to make an additional move to face correct way
                    if self.facing == 3:
                        self.move += 1
                    self.facing = 1
            # we return current position
            return next_pos

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
