#not include &s in KB, every sentence in KB is &ed together
import random
import re
class InferenceSystem():
    def __init__(self, gridsize):
        self.gridsize = gridsize
        self.rule = {'~s(row,col)': '~s(row,col) & ~w(row-1,col) & ~w(row+1,col) & ~w(row,col-1) & ~w(row,col+1)',
                     '~b(row,col)': '~b(row,col) & ~p(row-1,col) & ~p(row+1,col) & ~p(row,col-1) & ~p(row,col+1)',
                     's(row,col)': 's(row,col) & {w(row-1, col) | w(row+1, col) | w(row, col-1) | w(row, col+1)}',
                     'b(row,col)': 'b(row,col) & {p(row-1, col) | p(row+1, col) | p(row, col-1) | p(row, col+1)}',
                     'bump(row,col)': 'o(row,col)',
                     '~bump(row,col)': '~o(row,col)'}

        self.KB = ['w(2,3)']

    def updateKB(self, rowloc, colloc, percepts):
        z = []
        self.KB.append('v(' + str(rowloc) + ',' + str(colloc) + ')')
        if 's' in percepts:
            replace = self.unify('s(row,col)', 's(' + str(rowloc) + ',' + str(colloc) + ')', z)
            newreplace = replace.copy()
            for key, val in replace.items():
                newreplace[str(key) + '-1'] = int(val) - 1
                newreplace[str(key) + '+1'] = int(val) + 1
            check = self.rule['s(row,col)']
            for key, val in newreplace.items().__reversed__():
                check = check.replace(key, str(val))
            check = check.replace(' ','')
            check = check.split('&')
            for fact in check:
                self.KB.append(fact)
        else:
            replace = self.unify('~s(row,col)', '~s(' + str(rowloc) + ',' + str(colloc) + ')', z)
            newreplace = replace.copy()
            for key, val in replace.items():
                newreplace[str(key) + '-1'] = int(val) - 1
                newreplace[str(key) + '+1'] = int(val) + 1
            check = self.rule['~s(row,col)']
            for key, val in newreplace.items().__reversed__():
                check = check.replace(key, str(val))
            check = check.replace(' ', '')
            check = check.split('&')
            for fact in check:
                self.KB.append(fact)
        if 'b' in percepts:
            replace = self.unify('b(row,col)', 'b(' + str(rowloc) + ',' + str(colloc) + ')', z)
            newreplace = replace.copy()
            for key, val in replace.items():
                newreplace[str(key) + '-1'] = int(val) - 1
                newreplace[str(key) + '+1'] = int(val) + 1
            check = self.rule['b(row,col)']
            for key, val in newreplace.items().__reversed__():
                check = check.replace(key, str(val))
            check = check.replace(' ', '')
            check = check.split('&')
            for fact in check:
                self.KB.append(fact)
        else:
            replace = self.unify('~b(row,col)', '~b(' + str(rowloc) + ',' + str(colloc) + ')', z)
            newreplace = replace.copy()
            for key, val in replace.items():
                newreplace[str(key) + '-1'] = int(val) - 1
                newreplace[str(key) + '+1'] = int(val) + 1
            check = self.rule['~b(row,col)']
            for key, val in newreplace.items().__reversed__():
                check = check.replace(key, str(val))
            check = check.replace(' ', '')
            check = check.split('&')
            for fact in check:
                self.KB.append(fact)
        if percepts == 'bump':
            replace = self.unify('bump(row,col)', 'bump(' + str(rowloc) + ',' + str(colloc) + ')', z)
            newreplace = replace.copy()
            for key, val in replace.items():
                newreplace[str(key) + '-1'] = int(val) - 1
                newreplace[str(key) + '+1'] = int(val) + 1
            check = self.rule['bump(row,col)']
            for key, val in newreplace.items().__reversed__():
                check = check.replace(key, str(val))
            check = check.replace(' ', '')
            check = check.split('&')
            for fact in check:
                self.KB.append(fact)

    def unify(self, x, y, z):
       x = re.split(r'[(,)]\s*', x)
       y = re.split(r'[(,)]\s*', y)
       z = {x[1]: y[1], x[2]: y[2]}
       #do we need to
       # given x: a rule and
       # y: the location
       # returns rule including location
       return z


    def updateKBshot(self, rowloc, colloc, facing):
        if facing == 1:
            self.KB.append('w(' + rowloc - 1 + ',' + colloc + ')')
        elif facing == 2:
            self.KB.append('w(' + rowloc + ',' + colloc  + 1 + ')')
        elif facing == 3:
            self.KB.append('w(' + rowloc + 1 + ',' + colloc + ')')
        elif facing == 4:
            self.KB.append('w(' + rowloc + ',' + colloc  - 1 + ')')

    def bestAction(self, rowloc, colloc):
        actions = [[rowloc + 1, colloc], [rowloc - 1, colloc], [rowloc, colloc + 1], [rowloc, colloc - 1]]
        safeUnvisited = []
        safeVisited = []
        shoot = [] #is this really a list ?
        unsafe = []
        for act in actions:
            if act[0] >= 0 and act[0] < self.gridsize and act[1] >= 0 and act[1] < self.gridsize:
                wumpus = self.resolution(self.KB, '~w('+ str(act[0]) + ',' + str(act[1]) + ')')
                pit = self.resolution(self.KB, '~p(' + str(act[0]) + ',' + str(act[1]) + ')')
                obstacle = self.resolution(self.KB, '~o(' + str(act[0]) + ',' + str(act[1]) + ')')
                visited = self.resolution(self.KB, '~v(' + str(act[0]) + ',' + str(act[1]) + ')')
                print('wumpus', wumpus)
                print('pit', pit)
                print('obstacle', obstacle)
                print('visited', visited)
                if not visited and not wumpus and not pit and not obstacle:
                    safeUnvisited.append(act)
                elif not wumpus and not pit and not obstacle and visited:
                    safeVisited.append(act)
                elif wumpus and not visited and not obstacle and not pit:
                    shoot.append(act)
                elif wumpus or pit:
                    unsafe.append(act)
        if len(safeUnvisited) != 0:
            prob = random.randint(0, len(safeUnvisited) - 1)
            return safeUnvisited[prob], 'move'
        elif len(safeVisited) != 0:
            prob = random.randint(0, len(safeVisited) - 1)
            return safeVisited[prob], 'move'
        elif len(shoot) != 0:
            prob = random.randint(0, len(shoot) - 1)
            return shoot[prob], 'shoot'
        elif len(unsafe) != 0:
            prob = random.randint(0, len(unsafe) - 1)
            return unsafe[prob], 'move'



            #do logic on bools to determine best move

        #check all 4 squares around
        #no wumpus
        #no pit
        #no obstacle
        #not visited

        #return action

    def resolution(self, KB, sentence):
        currKB = KB.copy()
        currKB.append(sentence)
        new = []
        while True:
            for KBi in currKB:
                for KBj in currKB:
                    if KBi != KBj:
                        resolvents = self.resolve(KBi, KBj)
                        if len(resolvents) == 0: return True
                        if resolvents[0] != -1:
                            for resolve in resolvents:
                                new.append(resolve)
                            new = list(set(new))
            if set(new).issubset(currKB): return False
            for n in new:
                currKB.append(n)
            currKB = list(set(currKB))

    def resolve(self, clause1, clause2):
        clauses = []
        clause1.replace('{', "")
        clause1.replace('}', "")
        clause1.replace(' ', "")
        clause2.replace('{', "")
        clause2.replace('}', "")
        clause2.replace(' ', "")
        if '|' in clause1:
            clause1dis = clause1.split('|')
        else:
            clause1dis = [clause1]
        if '|' in clause2:
            clause2dis = clause2.split('|')
        else:
            clause2dis = [clause2]
        resolving = False
        for d1 in clause1dis:
            for d2 in clause2dis:
                if d1 == '~' + d2 or '~' + d1 == d2:
                    #isnt making them disjuntins again
                    if clause2dis.copy().remove(d2) != None and clause1dis.copy().remove(d1) == None:
                        for item in list(set(clause1dis.copy().remove(d1))):
                            clauses.append(item)
                    if clause2dis.copy().remove(d2) == None and clause1dis.copy().remove(d1) != None:
                        for item in list(set(clause1dis.copy().remove(d1))):
                            clauses.append(item)
                    if clause2dis.copy().remove(d2) != None and clause1dis.copy().remove(d1) != None:
                        for item in list(set(clause1dis.copy().remove(d1) + clause2dis.copy().remove(d2))):
                            clauses.append(item)
                    resolving = True
        if resolving == True:
            return clauses
        else:
            return [-1]
