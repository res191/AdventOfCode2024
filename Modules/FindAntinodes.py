import numpy

# only return coordinates that are in bounds of the map
def filter_coordinates(row_inds, col_inds, map_size):
    good_elems = (row_inds >= 0) & (col_inds >= 0) & (row_inds < map_size[0]) & (col_inds < map_size[1])
    return row_inds[good_elems], col_inds[good_elems]


def place_antinodes(input_map):
    antenna_keys = numpy.unique(input_map)
    # strip out the empty item from the antenna_keys
    antenna_keys = antenna_keys[antenna_keys !='.']

    all_rows = []
    all_cols = []
    for key in antenna_keys:
        # find all the locations of the key in the map
        antenna_locations = numpy.nonzero(input_map == key)
        antenna_locations = numpy.stack([antenna_locations[0], antenna_locations[1]])

        # for each antenna position
        for i in range(0, antenna_locations.shape[1]):
            # calculate the offset position of the element
            row_offset = antenna_locations[0,i] - antenna_locations[0,i+1::]
            col_offset = antenna_locations[1,i] - antenna_locations[1,i+1::]

            # positions offset by the first element
            row_pos1 =  antenna_locations[0,i] + row_offset
            col_pos1 = antenna_locations[1,i] + col_offset

            # positions offset by the second element
            row_pos2 = antenna_locations[0,i+1::] - row_offset
            col_pos2 =antenna_locations[1,i+1::] - col_offset

            all_rows = numpy.concatenate([all_rows, row_pos1, row_pos2])
            all_cols = numpy.concatenate([all_cols, col_pos1, col_pos2])

    good_rows, good_cols = filter_coordinates(all_rows, all_cols, input_map.shape)
    input_map[good_rows.astype(int), good_cols.astype(int)] ='#'

    return  numpy.count_nonzero(input_map =='#')

# compute all the good positions for antinode based on the
# starting antenna position, the antinode_step and the map_size
def compute_harmonics(antenna, antinode_step, map_size):
    good_pos = antenna

    new_pos = antenna + antinode_step
    while numpy.all(new_pos >= 0) and numpy.all(new_pos < map_size):
        good_pos = numpy.append(good_pos, new_pos, axis=1)
        new_pos = new_pos + antinode_step

    new_pos = antenna - antinode_step
    while numpy.all(new_pos >= 0) and numpy.all(new_pos < map_size):
        good_pos = numpy.append(good_pos, new_pos, axis=1)
        new_pos = new_pos - antinode_step

    return good_pos

def place_harmonic_antinodes(input_array):
    antenna_keys = numpy.unique(input_array)
    # strip out the empty item from the antenna_keys
    antenna_keys = antenna_keys[antenna_keys !='.']

    all_good_pos = numpy.array([[], []])
    for key in antenna_keys:
        # find all the locations of the key in the map
        antenna_locations = numpy.nonzero(input_array == key)
        antenna_locations = numpy.stack([antenna_locations[0], antenna_locations[1]])
        for i in range(0, antenna_locations.shape[1]):
            # calculate the offset position of the element
            offset = antenna_locations[:,i:i+1] - antenna_locations[:,i+1::]

            for j in range(0, offset.shape[1]):
                all_good_pos = numpy.append(all_good_pos,
                                            compute_harmonics(antenna_locations[:,i:i+1], offset[:,j:j+1], input_array.shape), axis =1)
    input_array[all_good_pos[0].astype(int), all_good_pos[1].astype(int)] ='#'
    return  numpy.count_nonzero(input_array =='#')
