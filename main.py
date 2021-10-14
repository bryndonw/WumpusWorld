from Explorer import Explorer
from WumpusWorldGen import WumpusWorldGen
from Explorer import Explorer
import random

from InferenceSystem import InferenceSystem

def main():
    iss = InferenceSystem()
    iss.updateKB(1, 0, ['s'])
    iss.updateKB(0, 1, ['s'])
    iss.updateKB(1, 2, ['s'])
    iss.updateKB(2, 1, ['s'])
    iss.bestAction(0,1)
    '''
    puzzle = WumpusWorldGen.generateGrid(WumpusWorldGen, 5, .1, .1, .1)
    start = WumpusWorldGen.startloc(WumpusWorldGen, puzzle)
    print(start)
    one = Explorer(puzzle)
    test = one.inferenceAgent(start[0], start[1])
    print(test)
    '''


if __name__ == '__main__':
    main()
