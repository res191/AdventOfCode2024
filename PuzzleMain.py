
import sys
from Modules.PuzzleDay18 import PuzzleDay18

def main (argv):
    puzzle = PuzzleDay18(argv[0])
    puzzle.solve()

if __name__ == '__main__':
    main(sys.argv[1:])