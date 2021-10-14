#not include &s in KB, every sentence in KB is &ed together

import re
class InferenceSystem():
    def __init__(self):
        self.rule = {'~s(row,col)': '~s(row,col) & ~w(row-1,col) & ~w(row+1,col) & ~w(row,col-1) & ~w(row,col+1)',
                     '~b(row,col)': '~b(row,col) & ~p(row-1,col) & ~p(row+1,col) & ~p(row,col-1) & ~p(row,col+1)',
                     's(row,col)': 's(row,col) & {w(row-1, col) | w(row+1, col) | w(row, col-1) | w(row, col+1)}',
                     'b(row,col)': 'b(row,col) & {p(row-1, col) | p(row+1, col) | p(row, col-1) | p(row, col+1)}',
                     'bump(row,col)': 'o(row,col)',
                     '~bump(row,col)': '~o(row,col)'}

        self.KB = ['w(2,3)']

    def updateKB(self, rowloc, colloc, percepts):
        z = []
        #self.KB.append('v(' + str(rowloc) + ',' + str(colloc) + ')')
        if 's' in percepts:
            replace = self.unify('s(row,col)', 's(' + str(rowloc) + ',' + str(colloc) + ')', z)
            newreplace = replace.copy()
            for key, val in replace.items():
                newreplace[str(key) + '-1'] = int(val) - 1
                newreplace[str(key) + '+1'] = int(val) + 1
            check = self.rule['s(row,col)']
            for key, val in newreplace.items().__reversed__():
                check = check.replace(key, str(val))
            check = check.split('&')
            for fact in check:
                self.KB.append(fact)
        '''        
        else:
            replace = self.unify('~s(row,col)', '~s(' + str(rowloc) + ',' + str(colloc) + ')', z)
            newreplace = replace.copy()
            for key, val in replace.items():
                newreplace[str(key) + '-1'] = int(val) - 1
                newreplace[str(key) + '+1'] = int(val) + 1
            check = self.rule['~s(row,col)']
            for key, val in newreplace.items().__reversed__():
                check = check.replace(key, str(val))
            self.KB.append(check)
        if 'b' in percepts:
            replace = self.unify('b(row,col)', 'b(' + str(rowloc) + ',' + str(colloc) + ')', z)
            newreplace = replace.copy()
            for key, val in replace.items():
                newreplace[str(key) + '-1'] = int(val) - 1
                newreplace[str(key) + '+1'] = int(val) + 1
            check = self.rule['b(row,col)']
            for key, val in newreplace.items().__reversed__():
                check = check.replace(key, str(val))
            self.KB.append(check)
        else:
            replace = self.unify('~b(row,col)', '~b(' + str(rowloc) + ',' + str(colloc) + ')', z)
            newreplace = replace.copy()
            for key, val in replace.items():
                newreplace[str(key) + '-1'] = int(val) - 1
                newreplace[str(key) + '+1'] = int(val) + 1
            check = self.rule['~b(row,col)']
            for key, val in newreplace.items().__reversed__():
                check = check.replace(key, str(val))
            self.KB.append(check)
        if percepts == 'bump':
            replace = self.unify('bump(row,col)', 'bump(' + str(rowloc) + ',' + str(colloc) + ')', z)
            newreplace = replace.copy()
            for key, val in replace.items():
                newreplace[str(key) + '-1'] = int(val) - 1
                newreplace[str(key) + '+1'] = int(val) + 1
            check = self.rule['bump(row,col)']
            for key, val in newreplace.items().__reversed__():
                check = check.replace(key, str(val))
            self.KB.append(check)
        '''

    def unify(self, x, y, z):
       x = re.split(r'[(,)]\s*', x)
       y = re.split(r'[(,)]\s*', y)
       z = {x[1]: y[1], x[2]: y[2]}
       #do we need to
       # given x: a rule and
       # y: the location
       # returns rule including location
       print(z)
       return z


    def updateKBshot(self):
        pass

    def bestAction(self, rowloc, colloc):
        actions = [[rowloc + 1, colloc], [rowloc - 1, colloc], [rowloc, colloc + 1], [rowloc, colloc - 1]]
        #for act in actions:
        #true means ~ ?? I thinkgs
        act = actions[0]
        wumpus = self.resolution(self.KB, '~w('+ str(act[0]) + ',' + str(act[1]) + ')')
        print(wumpus)
        pit = self.resolution(self.KB, '~p(' + str(act[0]) + ',' + str(act[1]) + ')')
        obstacle = self.resolution(self.KB, '~o(' + str(act[0]) + ',' + str(act[1]) + ')')
        visited = self.resolution(self.KB, '~v(' + str(act[0]) + ',' + str(act[1]) + ')')
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
                        new = set(new.append(resolvents))
            if new.issubset(currKB): return False
            currKB = set(currKB.append(new))

    def resolve(self, clause1, clause2):
        clauses = []
        #drop {}
        if '|' in clause1:
            clause1dis = clause1.split('|')
        else:
            clause1dis = [clause1]
        if '|' in clause2:
            clause2dis = clause2.split('|')
        else:
            clause2dis = [clause2]
        for d1 in clause1dis:
            for d2 in clause2dis:
                if d1 == '~' + d2 or '~' + d1 == d2:
                    list(set(clause2.remove(d1) + clause1.remove(d2)))
                    clauses.append(list(set(clause2.remove(d1) + clause1.remove(d2))))
        return clauses





        # combines rules into FACTS
        #check if lines in KB resolve w/ sentence
        #else add sentence to KB