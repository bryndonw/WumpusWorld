from WumpusWorldGen import WumpusWorldGen

def main():
    print('main')
    puzzle = WumpusWorldGen.generateGrid(WumpusWorldGen, 5, .1, .1, .1)

if __name__ == '__main__':
    main()
