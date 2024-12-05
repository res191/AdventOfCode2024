import numpy

# return true if you get to the end of the file and have not swapped anything
def swap_incorrect_match(input_line, rulebook, startInd):
    for i in range(startInd, 0, -1):
        rules_to_check = rulebook[rulebook[:,0]==input_line[i],1]
        for j in range(0, i):
            if numpy.any(rules_to_check==input_line[j]):
                # swap the two elements
                input_line[i], input_line[j] = input_line[j], input_line[i]
                return i
    return 0

def validate_line(input_line, rulebook):
    for i in range(len(input_line)-1, 0, -1):
        rules_to_check = rulebook[rulebook[:,0]==input_line[i],1]
        for rule in rules_to_check:
            if numpy.any(input_line[0:i]==rule):
                return False
    return True

def generate_puzzle_one(input_list, rulebook):
    count = 0
    for input in input_list:
        if (validate_line(numpy.array(input), rulebook)):
            count += input[(len(input) - 1) // 2]
    return count

def generate_puzzle_two(input_list, rulebook):
    count = 0
    for input in input_list:
        input_arr = numpy.array(input)
        swap_ind = swap_incorrect_match(input_arr, rulebook, len(input_arr) - 1)

        while (swap_incorrect_match(input_arr, rulebook, swap_ind) != 0):
            pass

        if swap_ind > 0:
            count += input_arr[(len(input) - 1) // 2]
    return count
