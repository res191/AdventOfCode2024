
import sys
from Modules.PuzzleDay4 import PuzzleDay4

def main (argv):
    puzzle = PuzzleDay4(argv[0])
    puzzle.solve()

if __name__ == '__main__':
    main(sys.argv[1:])