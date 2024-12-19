import math

from Modules.GenericPuzzle import Puzzle

class register:
    # the puzzle takes as input a filename
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.print = None

    def combo(self, operand):
        if operand == 4:
            return self.a
        elif operand == 5:
            return self.b
        elif operand == 6:
            return self.c
        else:
            return operand

    def stardv(self, operand):
        return math.floor(self.a / pow(2, self.combo(operand)))

    def toprint(self, val):
        if self.print is None:
            self.print = str(val)
        else:
            self.print+=',' + str(val)

    # run the given instruction return -1 to indicate the operator should increment through the list by 2
    # returns 0-N to indicate where the operand should jump to if requested
    def run_instruction(self, opcode, operand):
        match opcode:
            # The adv instruction (opcode 0)  performs division. The numerator is the value in the A register.
            # The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand
            # of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division
            # operation is truncated to an integer and then written to the A register
            case 0:
                self.a = self.stardv(operand)
                return -1
            #The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal
            # operand, then stores the result in register B.
            case 1:
                self.b = self.b^operand
                return -1
            #The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
            # (thereby keeping only its lowest 3 bits), then writes that value to the B register.
            case 2:
                self.b = self.combo(operand) % 8
                return -1
            # The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero,
            # it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps,
            # the instruction pointer is not increased by 2 after this instruction.
            case 3:
                if self.a == 0:
                    return -1
                else:
                    return operand
            #The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the
            # result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
            case 4:
                self.b = self.b^self.c
                return -1
            #The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value.
            # (If a program outputs multiple values, they are separated by commas.)
            case 5:
                self.toprint(self.combo(operand) % 8)
                return -1
            #The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in
            #  the B register. (The numerator is still read from the A register.)
            case 6:
                self.b = self.stardv(operand)
                return -1
            #The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in
            # the C register. (The numerator is still read from the A register.)
            case 7:
                self.c = self.stardv(operand)
                return -1

class PuzzleDay17(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.register = None

    def read_file(self):
        f = open(self.filename,"r")
        a, b, c = None, None, None

        # for this file we have three parts
        for line in f.readlines():
            if "Register A:" in line:
                a = int(line.split(": ")[1])
            elif "Register B:" in line:
                b = int(line.split(": ")[1])
            elif "Register C:" in line:
                c = int(line.split(": ")[1])
            elif "Program: " in line: # we are reading the program instructions
                self.input = line.rstrip().split(": ")[1]

        self.register = register(a, b, c)
        f.close()

    def part1(self):
        input_list = [int(item) for item in self.input.split(',')]
        i = 0

        while i < len(input_list):
            j = self.register.run_instruction(input_list[i], input_list[i+1])
            # increment appropriately
            if j != -1:
                i = j
            else:
                i += 2

        print(self.register.print)

    def register_solver(self, possible_min_value):
        # we always must scan 0-7 because we dont know which will give us the correct string but we must always try
        # the lowest value first
        for i in range(possible_min_value, possible_min_value + 8):
            # reset our register
            self.register.a = i
            self.register.b = 0
            self.register.c = 0
            self.register.print = None

            # rerun our register
            self.part1()

            # if we match exactly game over -- return our value
            if self.register.print == self.input:
                return i

            # otherwise we are still trying to find a partial match with the input
            if self.input.endswith(self.register.print):
                # if we have a partial match test if it has a solution
                value  = self.register_solver(i * 8)
                # if we return anything other than 0 we have found a match!
                if value != 0:
                    return value

        # if we have explored all our options without finding a match, return 0 so we know to continue looking
        return 0

    def part2(self):
        # to reverse engineer this the second to last instruction is to divide A by 8
        # we can predict the last element by finding which number 0-7 matches our input
        return self.register_solver(0)