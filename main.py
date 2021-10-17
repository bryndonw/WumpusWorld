from WumpusWorldGen import WumpusWorldGen
from Explorer import Explorer

def main():
    puzzle, arrows = WumpusWorldGen.generateGrid(WumpusWorldGen, 5, .05, .05, .15) #ppit, pwumpus, pobstacle

    start = WumpusWorldGen.startloc(WumpusWorldGen, puzzle)
    one = Explorer(puzzle, arrows)
    two = Explorer(puzzle, arrows)
    print("Reactive Agent")
    test1 = one.reactiveAgent(start[0], start[1])
    #print("Moves: ", test1)
    print("Inference Agent")
    test2 = two.inferenceAgent(start[0], start[1])
    #print("Moves: ", test2)



if __name__ == '__main__':
    main()
