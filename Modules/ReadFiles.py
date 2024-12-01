import numpy

# Read in a text file and return as an 2D-array
def read_lines(txtfile):
  f = open(txtfile, "r")
  input_list =[list(map(int, line.split())) for line in f.readlines()]
  input_np = numpy.array(input_list)
  return input_np