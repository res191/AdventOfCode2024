
import sys
from Modules.PuzzleDay3 import PuzzleDay3


def main (argv):
    puzzle = PuzzleDay3(argv[0])
    puzzle.solve()

if __name__ == '__main__':
    main(sys.argv[1:])