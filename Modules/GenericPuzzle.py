import time

class Puzzle:
    # the puzzle takes as input a filename
    def __init__(self, filename):
        self.filename = filename
        self.input = None

    # this file must set self.input using information from self.filename
    def read_file(self):
        raise NotImplementedError("Must override read_file")

    # run the solution to puzzle part 1
    def part1(self):
        raise NotImplementedError("Must override part1")

    # run the solution to puzzle part 2
    def part2(self):
        raise NotImplementedError("Must override part2")

    def solve(self):
        self.read_file()

        start_part1 = time.time()
        print('Solution to part 1 is: ', self.part1())
        end_part1 = time.time()
        print('Taking ', end_part1 - start_part1)

        start_part2 = time.time()
        print('Solution to part 2 is: ',  self.part2())
        end_part2 = time.time()
        print('Taking ', end_part2 - start_part2)
