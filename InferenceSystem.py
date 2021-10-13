import re
class InferenceSystem():
    def __init__(self):
        self.rule = {'~s': '~s(row,col) | {w(row-1, col) | w(row+1, col) | w(row, col-1) | w(row, col+1)}',
                     '~b': '~b(row,col) | {p(row-1, col) | p(row+1, col) | p(row, col-1) | p(row, col+1)}',
                     's(row,col)': 's(row,col) | {~w(row-1,col) & ~w(row+1,col) & ~w(row,col-1) & ~w(row,col+1)}',
                     'b': 'b(row,col) | {~p(row-1,col) & ~p(row+1,col) & ~p(row,col-1) & ~p(row,col+1)}',
                     'bump': 'o(row,col)'}
        self.KB = []
        pass

    def updateKB(self, rowloc, colloc, percepts):
        z = []
        replace = self.unify('s(row, col)', 's(' + str(rowloc) + ', ' + str(colloc) + ')', z)
        newreplace = replace.copy()
        for key, val in replace.items():
            newreplace[str(key) + '-1'] = int(val) - 1
            newreplace[str(key) + '+1'] = int(val) + 1
        check = self.rule['s(row,col)']
        for key, val in newreplace.items().__reversed__():
            check = check.replace(key, str(val))
        print(check)
        '''
        if 's' in percepts:
            replace = self.unify('s(row, col)', 's('+rowloc+', ' + colloc+')', z)
            check = self.rule['s(row, col)']
            for key, val in replace.items():
                check.replace(key, val)
                print(check)
           #self.rule['s(row, col)'] #iterate over replace, look for key in rule and replace key w val
           #self.resolution(self.KB, #returned value)
        else:
            self.unify(self.rule['~s'], [rowloc, colloc], z)
        if 'b' in percepts:
            self.unify(self.rule['b'], [rowloc, colloc], z)
        else:
            self.unify(self.rule['~b'], [rowloc, colloc], z)
        if percepts == 'bump':
            self.unify(self.rule['bump'], [rowloc, colloc], z)
        '''
    def unify(self, x, y, z):
       x = re.split(r'[(,)]\s*', x)
       y = re.split(r'[(,)]\s*', y)
       z = {x[1]: y[1], x[2]: y[2]}
       # given x: a rule and
       # y: the location
       # returns rule including location
       print(z)
       return z


    def updateKBshot(self):
        pass

    def bestAction(self, rowloc, colloc):
        return action



    def resolution(self, KB, sentence):
        # combines rules into FACTS
        #check if lines in KB resolve w/ sentence
        #else add sentence to KB
        return bool