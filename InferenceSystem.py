import re
# need to include way to mark visited squares
class InferenceSystem():
    def __init__(self):
        self.rule = {'~s': '~s(row,col) | {w(row-1, col) | w(row+1, col) | w(row, col-1) | w(row, col+1)}',
                     '~b': '~b(row,col) | {p(row-1, col) | p(row+1, col) | p(row, col-1) | p(row, col+1)}',
                     's': 's(row,col) | {~w(row-1,col) & ~w(row+1,col) & ~w(row,col-1) & ~w(row,col+1)}',
                     'b': 'b(row,col) | {~p(row-1,col) & ~p(row+1,col) & ~p(row,col-1) & ~p(row,col+1)}',
                     'bump': 'o(row,col)'}
        self.KB = []
        pass

    def updateKB(self, rowloc, colloc, percepts):
        z = []
        self.unify(self, 's(row, col)', 's(' + str(rowloc) + ', ' + str(colloc) + ')', z)
        """
        if 's' in percepts:
           replace = self.unify('s(row, col)', 's('+rowloc+', ' + colloc+')', z)
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
"""

    def unify(self, x, y, z):
       print(x)
       print(y)
       z = {x[2]: y[2], x[5]: y[5]}
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