from WumpusWorldGen import WumpusWorldGen
from Explorer import Explorer
import random

def main():
    puzzle = WumpusWorldGen.generateGrid(WumpusWorldGen, 5, .1, .1, .1)
    start = WumpusWorldGen.startloc(WumpusWorldGen, puzzle)
    print(start)
    #one = Explorer(puzzle)
    #test = one.reactiveAgent(start[0], start[1])


if __name__ == '__main__':
    main()
