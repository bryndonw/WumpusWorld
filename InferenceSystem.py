
class InferenceSystem():
    def __init__(self):
        self.rule = {'~s': '~s(row,col) | (w(row-1, col) | w(row+1, col) | w(row, col-1) | w(row, col+1))',
                     '~b': '~b(row,col) | (p(row-1, col) | p(row+1, col) | p(row, col-1) | p(row, col+1))',
                     's': '(s(row,col) | ~w(row-1,col)) & (s(row,col) | ~w(row+1,col)) & (s(row,col) | ~w(row,col-1))'
                          '& (s(row,col) | ~w(row,col+1))',
                     'b': '(b(row,col) | ~p(row-1,col)) & (b(row,col) | ~p(row+1,col)) & (b(row,col) | ~p(row,col-1))'
                           '& (b(row,col) | ~p(row,col+1))',
                     'bump': 'o(row,col)'}
        self.KB = []
        pass

    def updateKB(self, rowloc, colloc, percepts):
        """
        if 's' in percepts:
            x = ~s(row,col)
            y = ~s(rowlow,colloc)
            s = {row: rowloc,
                 col: collow}
            x = w(row-1, col)
            y = 1

           #self.unify(self.rule['s'], rowloc, )
        else:
            #self.unify(self.rule['~s'])
        if 'b' in percepts:
            #self.unify(self.rule['b'])
        else:
            #self.unify(self.rule['~b'])
        if percepts == 'bump':
            self.unify(self.rule['bump'])
            """
        pass

    def updateKBshot(self):
        pass

    def bestAction(self, rowloc, colloc):
        return action

    def unify(self, x, rowloc, colloc, z):
        #given x: a rule and
        #y: the location
        #returns rule including location
        return z

    def resolution(self, KB, sentence):
        # combines rules into FACTS
        return bool