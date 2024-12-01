
import sys
from Modules import CompareIDs
from Modules import ReadFiles


def main (argv):
    input_array = ReadFiles.read_lines((argv[0]))
    array1 = input_array[:,0]
    array2 = input_array[:,1]
    print('Solution to puzzle 1 is: ', CompareIDs.compute_distance(array1, array2))
    print('Solution to puzzle 2 is:: ', CompareIDs.compute_similarity_score(array1, array2))

if __name__ == '__main__':
    main(sys.argv[1:])