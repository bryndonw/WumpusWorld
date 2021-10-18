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
                     'bump(row,col)': 'o(row,col) & ~w(row,col) & ~p(row,col)',
                     '~bump(row,col)': '~o(row,col)'}

        self.KB = []

    def updateKB(self, rowloc, colloc, percepts):
        """Kieran Ringel and Bryndon Wilkerson
        Recieves percepts, unifys percept with rule, adds knowledge to KB"""
        z = []
        self.KB.append('v(' + str(rowloc) + ',' + str(colloc) + ')')    #marks cell as visited
        self.KB.append('~p(' + str(rowloc) + ',' + str(colloc) + ')')   #we didnt die so there is not pit
        self.KB.append('~w(' + str(rowloc) + ',' + str(colloc) + ')')   #we didnt die so there is no wumpus

        if percepts == 'bump':  #if we hit an obstacle
            replace = self.unify('bump(row,col)', 'bump(' + str(rowloc) + ',' + str(colloc) + ')', z)   #unify knowledge with format for rules
            newreplace = replace.copy()
            for key, val in replace.items():    #if rule contains row +/- 1 or column +/- 1 need to include in dict for replacement
                newreplace[str(key) + '-1'] = int(val) - 1
                newreplace[str(key) + '+1'] = int(val) + 1
            check = self.rule['bump(row,col)']  #get rule related to knowledge
            for key, val in newreplace.items().__reversed__():  #replace variables with constants
                check = check.replace(key, str(val))
            check = check.replace(' ', '')  #get rid of spaces
            check = check.split('&')    #split on & since every fact is KB is &ed together
            for fact in check:
                if str(self.gridsize) in fact or str(-1) in fact:   #if fact contains value that is off board
                    if '|' in fact: #if the fact is a disjunction
                        fact = fact.split('|')
                        newfact = ''
                        for f in fact:  #iterate over disjuncts in rule
                            if str(self.gridsize) not in f and str(-1) not in f:    #if disjunct on board
                                newfact = newfact + f + '|' #add to new fact as disjuntion
                        self.KB.append(newfact[:-1])    #add fact to KB
                else:
                    self.KB.append(fact)    #if it is on board add to KB
        else:   #if we see stench or breeze
            if 's' in percepts: #if stench
                replace = self.unify('s(row,col)', 's(' + str(rowloc) + ',' + str(colloc) + ')', z) #unify knowledge with format for rules
                newreplace = replace.copy()
                for key, val in replace.items(): #if rule contains row +/- 1 or column +/- 1 need to include in dict for replacement
                    newreplace[str(key) + '-1'] = int(val) - 1
                    newreplace[str(key) + '+1'] = int(val) + 1
                check = self.rule['s(row,col)'] #get rule related to knowledge
                for key, val in newreplace.items().__reversed__():  #replace variables with constants
                    check = check.replace(key, str(val))
                check = check.replace(' ','') #get rid of spaces
                check = check.split('&') #split on & since every fact is KB is &ed together
                for fact in check:
                   if str(self.gridsize) in fact or str(-1) in fact:  #if fact contains value that is off board
                        if '|' in fact: #if the fact is a disjunction
                            fact = fact.split('|')
                            newfact = ''
                            for f in fact: #iterate over disjuncts in rule
                                if str(self.gridsize) not in f and str(-1) not in f:  #if disjunct on board
                                    newfact = newfact + f + '|' #add to new fact as disjuntion
                            self.KB.append(newfact[:-1])  #add fact to KB
                   else:
                        self.KB.append(fact)  #if it is on board add to KB
            else:   #if there is not a stench
                replace = self.unify('~s(row,col)', '~s(' + str(rowloc) + ',' + str(colloc) + ')', z) #unify knowledge with format for rules
                newreplace = replace.copy()
                for key, val in replace.items(): #if rule contains row +/- 1 or column +/- 1 need to include in dict for replacement
                    newreplace[str(key) + '-1'] = int(val) - 1
                    newreplace[str(key) + '+1'] = int(val) + 1
                check = self.rule['~s(row,col)']  #get rule related to knowledge
                for key, val in newreplace.items().__reversed__(): #replace variables with constants
                    check = check.replace(key, str(val))
                check = check.replace(' ', '') #get rid of spaces
                check = check.split('&') #split on & since every fact is KB is &ed together
                for fact in check:
                    if str(self.gridsize) in fact or str(-1) in fact: #if fact contains value that is off board
                        if '|' in fact: #if the fact is a disjunction
                            fact = fact.split('|')
                            newfact = ''
                            for f in fact:  #iterate over disjuncts in rule
                                if str(self.gridsize) not in f and str(-1) not in f: #if disjunct on board
                                    newfact = newfact + f + '|' #add to new fact as disjuntion
                            self.KB.append(newfact[:-1])  #add fact to KB
                    else:
                        self.KB.append(fact) #if it is on board add to KB
            if 'b' in percepts: #if we feel a breeze
                replace = self.unify('b(row,col)', 'b(' + str(rowloc) + ',' + str(colloc) + ')', z)  #unify knowledge with format for rules
                newreplace = replace.copy()
                for key, val in replace.items(): #if rule contains row +/- 1 or column +/- 1 need to include in dict for replacement
                    newreplace[str(key) + '-1'] = int(val) - 1
                    newreplace[str(key) + '+1'] = int(val) + 1
                check = self.rule['b(row,col)'] #get rule related to knowledge
                for key, val in newreplace.items().__reversed__(): #replace variables with constants
                    check = check.replace(key, str(val))
                check = check.replace(' ', '') #get rid of spaces
                check = check.split('&') #split on & since every fact is KB is &ed together
                for fact in check:
                    if str(self.gridsize) in fact or str(-1) in fact: #if fact contains value that is off board
                        if '|' in fact:  #if the fact is a disjunction
                            fact = fact.split('|')
                            newfact = ''
                            for f in fact: #iterate over disjuncts in rule
                                if str(self.gridsize) not in f and str(-1) not in f: #if disjunct on board
                                    newfact = newfact + f + '|'#add to new fact as disjuntion
                            self.KB.append(newfact[:-1])  #add fact to KB
                    else:
                        self.KB.append(fact)#if it is on board add to KB
            else:   #if there in not a breeze
                replace = self.unify('~b(row,col)', '~b(' + str(rowloc) + ',' + str(colloc) + ')', z) #unify knowledge with format for rules
                newreplace = replace.copy()
                for key, val in replace.items():  #if rule contains row +/- 1 or column +/- 1 need to include in dict for replacement
                    newreplace[str(key) + '-1'] = int(val) - 1
                    newreplace[str(key) + '+1'] = int(val) + 1
                check = self.rule['~b(row,col)'] #get rule related to knowledge
                for key, val in newreplace.items().__reversed__(): #replace variables with constants
                    check = check.replace(key, str(val))
                check = check.replace(' ', '')#get rid of spaces
                check = check.split('&')#split on & since every fact is KB is &ed together
                for fact in check:
                    if str(self.gridsize) in fact or str(-1) in fact: #if fact contains value that is off board
                        if '|' in fact: #if the fact is a disjunction
                            fact = fact.split('|')
                            newfact = ''
                            for f in fact: #iterate over disjuncts in rule
                                if str(self.gridsize) not in f and str(-1) not in f: #if disjunct on board
                                    newfact = newfact + f + '|' #add to new fact as disjuntion
                            self.KB.append(newfact[:-1]) #add fact to KB
                    else:
                        self.KB.append(fact)#if it is on board add to KB

    def unify(self, x, y, z):
       """Kieran Ringel
        Unifies rule with variables with knowledge with values
        """
       x = re.split(r'[(,)]\s*', x) #gets variables
       y = re.split(r'[(,)]\s*', y) #get values
       z = {x[1]: y[1], x[2]: y[2]} #creates dict of relation
       #do we need to
       # given x: a rule and
       # y: the location
       # returns rule including location
       return z


    def updateKBshot(self, rowloc, colloc, facing):
        """Kieran Ringel
        Explorer will only shoot if KB says there is a wumpus in the adjacent cell if is shooting at
        This will add that wumpus to the KB"""
        if facing == 1:
            self.KB.append('w(' + str(rowloc - 1) + ',' + str(colloc) + ')')
        elif facing == 2:
            self.KB.append('w(' + str(rowloc) + ',' + str(colloc  + 1) + ')')
        elif facing == 3:
            self.KB.append('w(' + str(rowloc + 1) + ',' + str(colloc) + ')')
        elif facing == 4:
            self.KB.append('w(' + str(rowloc) + ',' + str(colloc  - 1) + ')')

    def bestAction(self, rowloc, colloc, moves):
        #print(self.KB)
        actions = [[rowloc + 1, colloc], [rowloc - 1, colloc], [rowloc, colloc + 1], [rowloc, colloc - 1]]  #checks add 4 adjacent cells
        # lists of moves
        safeUnvisited = []
        safeVisited = []
        shoot = []
        unsafe = []
        for act in actions:
            if act[0] >= 0 and act[0] < self.gridsize and act[1] >= 0 and act[1] < self.gridsize:   #if action query is on board
                wumpus = self.resolution(self.KB, '~w('+ str(act[0]) + ',' + str(act[1]) + ')') #query for wumpus
                pit = self.resolution(self.KB, '~p(' + str(act[0]) + ',' + str(act[1]) + ')')   #query for pit
                obstacle = self.resolution(self.KB, '~o(' + str(act[0]) + ',' + str(act[1]) + ')')  #query for obstacle
                visited = self.resolution(self.KB, '~v(' + str(act[0]) + ',' + str(act[1]) + ')')   #query for visited
                #print('\n', act)
                #print('wumpus\t|', wumpus)
                #print('pit\t\t|', pit)
                #print('obstacle|', obstacle)
                #print('visited\t|', visited)
                if not visited and not wumpus and not pit and not obstacle: #if safe unvisted cell
                    safeUnvisited.append(act)
                elif not wumpus and not pit and not obstacle and visited:   #if safe visited cell
                    safeVisited.append(act)
                elif wumpus or pit: #if unsafe cell
                    unsafe.append(act)
                elif wumpus and not visited and not obstacle and not pit:   #if it is a wumpus
                    shoot.append(act)

        if len(safeUnvisited) != 0: #if safe unvisited move exists
            #('unvisisted')
            prob = random.randint(0, len(safeUnvisited) - 1)    #choose one of those moves
            return safeUnvisited[prob], 'move'
        elif len(safeVisited) != 0: #if safe visisted move exists
            #('visited')
            prob = random.randint(0, len(safeVisited) - 1)  #randomly choose of those moves
            return safeVisited[prob], 'move'
        elif len(unsafe) != 0:  #if unsafe move exists
            prob = random.randint(0, len(unsafe) - 1)   #randomly choose one of those moves
            return unsafe[prob], 'move'
        elif len(shoot) != 0:   # if explorer can shoot
            prob = random.randint(0, len(shoot) - 1)    #randomly choose one of those moves
            return shoot[prob], 'shoot'
        else:   #shouldnt reach, but default if none of the above moves can be made, move randomly
            prob = random.randint(0, len(act) - 1)
            while not (actions[prob][0] >= 0 and actions[prob][0] < self.gridsize and actions[prob][1] >= 0 and actions[prob][1] < self.gridsize):
                prob = random.randint(0, len(act) - 1)
            return actions[prob], 'move'

    def resolution(self, KB, sentence):
        """Kieran Ringel and Bryndon Wilkerson
        Resolves entire KB against itself
        If 2 clauses contradict return true (query is true)
        Otherwise add resolved statement to temporary KB
        If the new fact already exists in KB entire KB has been resolved, return false"""
        currKB = KB.copy()
        currKB.append(sentence)
        new = []
        while True:
            for KBi in currKB:
                for KBj in currKB:
                    if KBi != KBj:  #cant query statement against self
                        resolvents = self.resolve(KBi, KBj) #resolve statements
                        if len(resolvents) == 0: return True    #if statements contradict return true
                        if resolvents[0] != -1: #if statments were about same fact and location so they could be resolved
                            for resolve in resolvents:  #iterate over list of resolved facts
                                new.append(resolve)
                            new = list(set(new))    #get union of new facts
            if set(new).issubset(currKB): return False  #if fact is already in KB entire KB has been resolved return False
            for n in new:
                currKB.append(n)
            currKB = list(set(currKB))  #get union of currKb and new

    def resolve(self, clause1, clause2):
        """Kieran Ringel and Bryndon Wilkerson
        Resolves two facts checking for contradicts to be removed from disjunction
        Or contradictions of facts indicating a query is true"""
        clauses = []
        #remove spaces and {}
        clause1 = clause1.replace('{', "")
        clause1 = clause1.replace('}', "")
        clause1 = clause1.replace(' ', "")
        clause2 = clause2.replace('{', "")
        clause2 = clause2.replace('}', "")
        clause2 = clause2.replace(' ', "")
        if '|' in clause1:  #if is disjuntion
            clause1dis = clause1.split('|') #disjoin
        else:   #otherise list is the one value
            clause1dis = [clause1]
        if '|' in clause2: #if is disjuntion
            clause2dis = clause2.split('|')#disjoin
        else: #otherise list is the one value
            clause2dis = [clause2]
        resolving = False   #by default assume clauses cannot be resolved
        for d1 in clause1dis:
            for d2 in clause2dis:
                if d1 == '~' + d2 or '~' + d1 == d2:    #if disjunctions are opposite
                    #remove contradiction from clause
                    check2 = clause2dis.copy()
                    check2.remove(d2)
                    check1 = clause1dis.copy()
                    check1.remove(d1)
                    if check2 != [] and check1 == []:   #if one is not empty list
                        out = ''
                        for item in list(set(check2)):  #turn list of clauses back into disjunction
                            out = out + item + '|'
                        clauses.append(out[:-1])        #append disjunct to facts to return
                    if check2 == [] and check1 != []:   #if one is not empty list
                        out = ''
                        for item in list(set(check1)): #turn list of clauses back into disjunction
                            out = out + item + '|'
                        clauses.append(out[:-1])  #append disjunct to facts to return
                    if check2 != [] and check1 != []:   #if both are not empty lists
                        out = ''
                        for item in list(set(check1 + check2)): #turn back to disjunction
                            out = out + item + '|'
                        clauses.append(out[:-1])    #add to facts to return
                    #if there are both empty [] would be appended, dont need to deal with
                    resolving = True
        if resolving == True:   #if the facts could be resolved
            return clauses  #return resolved facts
        else:   #otherwise indicate facts could not be resolved
            return [-1]
