from Explorer import Explorer
from WumpusWorldGen import WumpusWorldGen
from Explorer import Explorer
import random

from InferenceSystem import InferenceSystem

def main():
    iss = InferenceSystem()
    iss.updateKB(1, 1, ['s'])
    iss.bestAction(3,3)
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
