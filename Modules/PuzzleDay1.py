import numpy

from Modules.GenericPuzzle import Puzzle
from Modules import ReadFiles

class PuzzleDay1(Puzzle):
  def __init__(self, filename):
    super().__init__(filename)

  """ For this puzzle each line contains only two integers split by a space. 
      For easy of use the list is converted to a numpy.array 
  """
  def read_file(self):
    input_list = ReadFiles.read_file_as_int_list(self.filename)
    self.input = numpy.array(input_list)

  """ Sum the differences between the two columns of the input ordered from smallest to largest
  """
  def part1(self):
    array1 = self.input[:, 0]
    array2 = self.input[:, 1]
    array1.sort()
    array2.sort()
    return numpy.sum(numpy.abs( numpy.subtract(array1, array2)))

  """ Compute a similarity score between the two columns. 
      Similarity score is the left column number multiplied by the times this number appears in the right column.
  """
  def part2(self):
    array1 = self.input[:, 0]
    array2 = self.input[:, 1]
    return sum(list(map(lambda key: key * numpy.sum(array2 == key), array1)))
