from Explorer import Explorer
from WumpusWorldGen import WumpusWorldGen
from Explorer import Explorer
import random

from InferenceSystem import InferenceSystem

def main():
    puzzle, arrows = WumpusWorldGen.generateGrid(WumpusWorldGen, 25, .05, .05, .15) #ppit, pwumpus, pobstacle

    start = WumpusWorldGen.startloc(WumpusWorldGen, puzzle)
    print(start)
    one = Explorer(puzzle, arrows)
    test = one.inferenceAgent(start[0], start[1])
    print(test)



if __name__ == '__main__':
    main()
