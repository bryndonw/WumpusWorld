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

        self.KB = []
        self.risk = 0

    def updateKB(self, rowloc, colloc, percepts):
        z = []
        self.KB.append('v(' + str(rowloc) + ',' + str(colloc) + ')')
        self.KB.append('~p(' + str(rowloc) + ',' + str(colloc) + ')')
        self.KB.append('~w(' + str(rowloc) + ',' + str(colloc) + ')')

        if 's' in percepts:
            replace = self.unify('s(row,col)', 's(' + str(rowloc) + ',' + str(colloc) + ')', z)
            newreplace = replace.copy()
            for key, val in replace.items():
                newreplace[str(key) + '-1'] = int(val) - 1
                newreplace[str(key) + '+1'] = int(val) + 1
            check = self.rule['s(row,col)']
            print(newreplace)
            for key, val in newreplace.items().__reversed__():
                check = check.replace(key, str(val))
            check = check.replace(' ','')
            check = check.split('&')
            for fact in check:
               if str(self.gridsize) in fact or str(-1) in fact:
                    if '|' in fact:
                        fact = fact.split('|')
                        newfact = ''
                        for f in fact:
                            if str(self.gridsize) not in f and str(-1) not in f:
                                newfact = newfact + f + '|'
                        self.KB.append(newfact[:-1])
               else:
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
                if str(self.gridsize) in fact or str(-1) in fact:
                    if '|' in fact:
                        fact = fact.split('|')
                        newfact = ''
                        for f in fact:
                            if str(self.gridsize) not in f and str(-1) not in f:
                                newfact = newfact + f + '|'
                        self.KB.append(newfact[:-1])
                else:
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
                if str(self.gridsize) in fact or str(-1) in fact:
                    if '|' in fact:
                        fact = fact.split('|')
                        newfact = ''
                        for f in fact:
                            if str(self.gridsize) not in f and str(-1) not in f:
                                newfact = newfact + f + '|'
                        self.KB.append(newfact[:-1])
                else:
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
                if str(self.gridsize) in fact or str(-1) in fact:
                    if '|' in fact:
                        fact = fact.split('|')
                        newfact = ''
                        for f in fact:
                            if str(self.gridsize) not in f and str(-1) not in f:
                                newfact = newfact + f + '|'
                        self.KB.append(newfact[:-1])
                else:
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
                if str(self.gridsize) in fact or str(-1) in fact:
                    if '|' in fact:
                        fact = fact.split('|')
                        newfact = ''
                        for f in fact:
                            if str(self.gridsize) not in f and str(-1) not in f:
                                newfact = newfact + f + '|'
                        self.KB.append(newfact[:-1])
                else:
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
            self.KB.append('w(' + str(rowloc - 1) + ',' + str(colloc) + ')')
        elif facing == 2:
            self.KB.append('w(' + str(rowloc) + ',' + str(colloc  + 1) + ')')
        elif facing == 3:
            self.KB.append('w(' + str(rowloc + 1) + ',' + str(colloc) + ')')
        elif facing == 4:
            self.KB.append('w(' + str(rowloc) + ',' + str(colloc  - 1) + ')')

    def bestAction(self, rowloc, colloc, moves):
        print(self.KB)
        if moves == ((self.gridsize * 10)/5):
            self.risk += .1
        actions = [[rowloc + 1, colloc], [rowloc - 1, colloc], [rowloc, colloc + 1], [rowloc, colloc - 1]]
        safeUnvisited = []
        safeVisited = []
        shoot = []
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
                elif wumpus or pit:
                    unsafe.append(act)
                elif wumpus and not visited and not obstacle and not pit:
                    shoot.append(act)
        prob_move = random.uniform(0,1)

        if len(safeUnvisited) != 0:
            print('unvisisted')
            prob = random.randint(0, len(safeUnvisited) - 1)
            return safeUnvisited[prob], 'move'
        elif len(safeVisited) != 0 and prob_move >= self.risk:
            print('visited')
            prob = random.randint(0, len(safeVisited) - 1)
            return safeVisited[prob], 'move'
        elif len(unsafe) != 0 and prob_move < self.risk:
            prob = random.randint(0, len(unsafe) - 1)
            return unsafe[prob], 'move'
        elif len(shoot) != 0:
            prob = random.randint(0, len(shoot) - 1)
            return shoot[prob], 'shoot'
        else:
            prob = random.randint(0, len(act) - 1)
            while not (actions[prob][0] >= 0 and actions[prob][0] < self.gridsize and actions[prob][1] >= 0 and actions[prob][1] < self.gridsize):
                prob = random.randint(0, len(act) - 1)
            return actions[prob], 'move'



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
        clause1 = clause1.replace('{', "")
        clause1 = clause1.replace('}', "")
        clause1 = clause1.replace(' ', "")
        clause2 = clause2.replace('{', "")
        clause2 = clause2.replace('}', "")
        clause2 = clause2.replace(' ', "")
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
                    check2 = clause2dis.copy()
                    check2.remove(d2)
                    check1 = clause1dis.copy()
                    check1.remove(d1)
                    if check2 != [] and check1 == []:
                        out = ''
                        for item in list(set(check2)):
                            out = out + item + '|'
                        clauses.append(out[:-1])
                    if check2 == [] and check1 != []:
                        out = ''
                        for item in list(set(check1)):
                            out = out + item + '|'
                        clauses.append(out[:-1])
                    if check2 != [] and check1 != []:
                        out = ''
                        for item in list(set(check1 + check2)):
                            out = out + item + '|'
                        clauses.append(out[:-1])
                    resolving = True
        if resolving == True:
            return clauses
        else:
            return [-1]
