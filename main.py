from WumpusWorldGen import WumpusWorldGen
from Explorer import Explorer

def main():
    cellstot1 = 0
    pointstot1 = 0
    cellstot2 = 0
    pointstot2 = 0
    for i in range(10):
        puzzle, arrows = WumpusWorldGen.generateGrid(WumpusWorldGen, 25, .02, .02, .2) #ppit, pwumpus, pobstacle

        start = WumpusWorldGen.startloc(WumpusWorldGen, puzzle)
        one = Explorer(puzzle, arrows)
        two = Explorer(puzzle, arrows)
        print("Reactive Agent")
        cells1, points1 = one.reactiveAgent(start[0], start[1])
        cellstot1 += cells1
        pointstot1 += points1
        print("Inference Agent")
        cells2, points2 = two.inferenceAgent(start[0], start[1])
        cellstot2 += cells2
        pointstot2 += points2
        #print("Moves: ", test2)
    print("Reactive cells", cellstot1/10)
    print("Reactive points", pointstot1 / 10)
    print("Inference cells", cellstot2 / 10)
    print("Inference points", pointstot2 / 10)



if __name__ == '__main__':
    main()
