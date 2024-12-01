import numpy

def compute_distance(array1, array2):
  array1.sort()
  array2.sort()
  diffarray = numpy.subtract(array1, array2)
  return numpy.sum(numpy.abs(diffarray))

def compute_similarity_score(array1, array2):
  return sum(list(map(lambda key: key*numpy.sum(array2==key), array1)))
