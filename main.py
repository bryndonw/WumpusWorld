from Explorer import Explorer
from WumpusWorldGen import WumpusWorldGen
from Explorer import Explorer
import random

from InferenceSystem import InferenceSystem

def main():
    puzzle, arrows = WumpusWorldGen.generateGrid(WumpusWorldGen, 5, .05, .05, .15) #ppit, pwumpus, pobstacle

    start = WumpusWorldGen.startloc(WumpusWorldGen, puzzle)
    one = Explorer(puzzle, arrows)
    print(start)
    test = one.inferenceAgent(start[0], start[1])
    print("Moves: ", test)



if __name__ == '__main__':
    main()
