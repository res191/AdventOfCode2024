
import numpy
import re
from scipy.optimize import linprog
from Modules.GenericPuzzle import Puzzle

error = 1E-24
cost_a = 3
cost_b = 1

def solve_equation(eq_system, answer):
    inv_eq = numpy.linalg.inv(eq_system)
    steps = numpy.matmul(answer, inv_eq)

    if abs(round(steps[0]) - steps[0]) < error and abs(round(steps[1]) - steps[1]) < error :
        return steps

    return numpy.array([numpy.nan,numpy.nan])

def solve_equation_no_inverse(eq_system, answer):
    steps = numpy.linalg.solve(eq_system, answer)
    c=[3, 1]
    res = linprog(c, A_eq=numpy.transpose(eq_system), b_eq=answer, bounds=[(0, None), (0, None)], integrality=[1, 1], options={'presolve': False})
    if not res.x is None:
        return res.x

    return numpy.array([numpy.nan,numpy.nan])

class PuzzleDay13(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)

    def read_file(self):
        f = open(self.filename, "r")

        self.input=[]
        for line in f.readlines():
            inputs = re.split(r'\+|=|, ', line)
            if len(inputs) == 4:
                self.input.append((int(inputs[1]), int(inputs[3])))

        f.close()

    def part1(self):
        # first do a sense check that are input has the right number of elements
        if (len(self.input) % 3 != 0):
            print("File", self.filename, " generates an input of size, ", len(self.input))

        input_array = numpy.array(self.input)
        total_cost = 0
        for i in range(0, len(self.input), 3):
            # solve the equation
            solution = solve_equation(input_array[i:i+2,:], input_array[i+2,:])

            # check that there is a solution
            if numpy.all(solution < 101):
                total_cost+= solution[0]*cost_a + solution[1]*cost_b

        return total_cost

    def part2(self):
        # first do a sense check that are input has the right number of elements
        if (len(self.input) % 3 != 0):
            print("File", self.filename, " generates an input of size, ", len(self.input))

        input_array = numpy.array(self.input)
        total_cost = []
        for i in range(0, len(self.input), 3):
            # solve the equation
            solution = solve_equation_no_inverse(input_array[i:i+2,:], 10000000000000 + input_array[i+2,:])

            # check that there is a solution
            if numpy.all(solution > 0):
                total_cost.append(solution[0]*cost_a + solution[1]*cost_b)

        return sum(total_cost)
