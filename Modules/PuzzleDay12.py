import numpy
from torch.nn.init import orthogonal

from Modules.ReadFiles import read_file_as_char_map
from Modules.GenericPuzzle import Puzzle

#in order down, up, right, left
directions = numpy.array([[1, 0], [-1, 0], [0, 1], [0, -1]])

''' count the number of corners for the tile centers on item.'''
def at_corner(item, indices):
    count = 0
    # compute the convex corners
    internal_edges = [numpy.any(numpy.all(indices == (item + x), axis=1)) for x in directions]

    for i in range(0,4):
        # we are a convex corner if both directions are not in our list
        if not internal_edges[i%2] and not internal_edges[i//2 + 2]:

            count +=1
        #if both directions are in our list and are combination is then we are a concave corner
        if (internal_edges[i%2] and internal_edges[i//2 + 2]
                and not numpy.any(numpy.all(indices == (item + directions[i%2]+directions[i//2 + 2]), axis=1))):
            count+=1

    return count


''' compute the area and the perimeter of the region defined by val in input_map
return area * perimeter '''
def compute_region(input_map, val, use_perimeter):
    indices = numpy.argwhere(input_map == val)

    # if we do not have the value at all, oops return 0
    if indices.size == 0:
        return 0

    # how many elements we have == area
    area = indices.shape[0]

    # how many free edges do we have on the perimeter
    perimeter = 0
    # we are using 4 connectivity
    if use_perimeter:
        for item in indices:
            perimeter += 4 - sum([numpy.any(numpy.all(indices == (item + x ), axis=1)) for x in directions])
    else:
        perimeter = sum([at_corner(item, indices) for item in indices])

    # return the product of the two
    return perimeter*area

''' find the region in the input_map
    for all identical elements connected by the seed
'''
def grow_region(input_map, possible_seeds, value, region_id):
    # if possible seeds are not valid return
    possible_seeds = possible_seeds[numpy.all(possible_seeds > -1, axis=1) & numpy.all(possible_seeds < input_map.shape, axis=1), :]
    if possible_seeds.size == 0:
        return

    # we now have possible seeds evaluate if they have the correct value
    region_index = possible_seeds[input_map[possible_seeds[:,0], possible_seeds[:,1]] == value, :]
    # if no possible seeds have the correct value return
    if region_index.size == 0:
        return

    # set the input map to the region id
    input_map[region_index[:,0], region_index[:,1]] = region_id

    # expand on the possible seeds from the good region_index
    possible_seeds = numpy.empty((0,2), dtype='int64')
    for seed in region_index:
        possible_seeds = numpy.append(possible_seeds,[seed + x for x in directions], axis = 0)

    # call the recursive function make sure to remove duplicate seeds!
    grow_region(input_map, numpy.unique(possible_seeds, axis=0), value, region_id)

class PuzzleDay12(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.output_map = None

    def read_file(self):
        self.input = numpy.array(read_file_as_char_map(self.filename), dtype='<U5')

    def part1(self):
        seeds = numpy.argwhere(numpy.char.isalpha(self.input))
        count = 0
        region_id = 0

        # to not screw up the file input
        input_map = self.input.copy()
        # if we have a region we have not yet assigned an id
        while not seeds.size == 0:
            # using the next seed find the next region
            grow_region(input_map, numpy.array([seeds[0]]), input_map[seeds[0,0], seeds[0,1]], str(region_id))

            # add that region to our count using the perimeter counting method
            count += compute_region(input_map, str(region_id), True)

            #increment the id
            region_id+=1
            # reinitialise the seeds
            seeds = numpy.argwhere(numpy.char.isalpha(input_map))
        self.output_map = input_map
        return count

    def part2(self):
        region_ids = numpy.unique(self.output_map)
        count = 0
        # sum up all the regions using the corner method
        for id in region_ids:
            count+= compute_region(self.output_map, id, False)

        return count