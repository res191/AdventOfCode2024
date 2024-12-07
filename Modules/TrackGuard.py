import numpy

# function to turn the guard location
# 0 indicates that is not the direction of movement
# -1 indicates the guard is moving in the negative direction
#
# if we are moving left(0, -1) -> up(-1, 0) and right(0, 1)->down (1, 0)
# if we are moving up (-1, 0)->right(0, 1) and down(1, 0)->left(0, -1)
# this can be simply modeled by swapping the first and second element
# the second element being set to negative
def turn_guard_clockwise(start_direction):
    start_direction[0], start_direction[1] = [start_direction[1], -start_direction[0]]

# based on walking on the line of sight return the next location of #
def find_next_turn(input_line):
    occlusions = numpy.where(input_line =='#')[0]
    if len(occlusions) == 0: # no occlusions walk the full length
        return len(input_line)
    else:
        return min(occlusions)

def get_next_turn(input_map, guard_pos):
    if guard_pos[1, 0] == 0:
        occ_ind = find_next_turn(input_map[guard_pos[0, 0], guard_pos[0, 1]::guard_pos[1, 1]])
        guard_pos[0, 1] = guard_pos[0, 1] + guard_pos[1, 1] * (occ_ind - 1)
    else:
        occ_ind = find_next_turn(input_map[guard_pos[0, 0]::guard_pos[1, 0], guard_pos[0, 1]])
        guard_pos[0,0] = guard_pos[0,0] + guard_pos[1,0] * (occ_ind - 1)
    turn_guard_clockwise(guard_pos[1])

# input_map is a 2D numpy array where # indicate obstacles
# start_pos is a 2D numpy array where:
#   -the first row indicates the 2D position of the guard in the array
#   - the second row indicates the direction of movement
def fill_in_next_line(input_map, start_pos):
    end_pos = start_pos.copy()
    get_next_turn(input_map, end_pos)

    if start_pos[1,0] == 0:
        columns = numpy.arange(start_pos[0,1], end_pos[0,1] + start_pos[1,1], start_pos[1,1])
        rows = end_pos[0,0]
    else:
        rows = numpy.arange(start_pos[0,0], end_pos[0,0] + start_pos[1,0], start_pos[1,0])
        columns = end_pos[0,1]

    input_map[rows, columns] = "X"
    return end_pos

# find the location and the direction the guard is facing
# start_pos is a 2D numpy array where:
#   -the first row indicates the 2D position of the guard in the array
#   - the second row indicates the direction of movement
def find_guard(input_map):
    guard = numpy.where(numpy.logical_and(input_map != '.', input_map != '#'))
    start_pos =numpy.array([guard[0][0], guard[1][0]])
    if input_map[guard] == "^": # facing up
        start_pos = numpy.stack((start_pos,[-1, 0]))
    elif input_map[guard] == "v": # facing down
        start_pos = numpy.stack((start_pos,[1, 0]))
    elif input_map[guard] == ">": # facing left
        start_pos = numpy.stack((start_pos,[0, 1]))
    if input_map[guard] == "<": # facing right
        start_pos = numpy.stack((start_pos,[0, -1]))
    return start_pos

def count_steps(input_map):
    # first find where the guard is
    guard_pos = find_guard(input_map)

    # start by filling in the first line
    guard_pos = fill_in_next_line(input_map, guard_pos)

    # while the guard is on the map
    while not(guard_pos[0,0] == 0 or guard_pos[0,0] == input_map.shape[0] - 1
              or guard_pos[0,1] == 0 or guard_pos[0,1] == input_map.shape[1] - 1):
        # fill in the next line
        guard_pos = fill_in_next_line(input_map, guard_pos)

    # count X in the map
    return numpy.count_nonzero(input_map=='X')

def take_step(input_map, guard_pos):
    temp = guard_pos[0] + guard_pos[1]
    # we are at an obstacle so turn
    if input_map[temp[0], temp[1]] == "#":
        turn_guard_clockwise(guard_pos[1])

    # mark my previous position with an X
    input_map[guard_pos[0,0],guard_pos[0,1]] ='X'
    # take a step
    guard_pos[0] = guard_pos[0] + guard_pos[1]


# we need to know continue going until one of three conditions are met
# we end up going off the map -> return 0
# we end up at the same position 4 steps ago -> return 1
def is_in_loop(input_map, guard_pos):
    #copy my guard pose
    est_pos = guard_pos.copy()

    # find the next turn
    get_next_turn(input_map, est_pos)

    # create our cache
    cache_pos = []
    step = 0

    # just added a random stop criteria
    while step < 5000:
        # if we have gotten here we are not in a loop so check if we are exiting the map
        if (est_pos[0,0] == 0 or est_pos[0,0] == input_map.shape[0] - 1
            or est_pos[0,1] == 0 or est_pos[0,1] == input_map.shape[1] - 1):
            return False

        # if we exactly match our position we have entered a loop -- so return
        for i in range (step%4, len(cache_pos), 4):
            if numpy.all(cache_pos[i] == est_pos):
                return True

        # we still do not know if we are in a loop
        cache_pos.append(est_pos.copy())

        # find the next turn
        get_next_turn(input_map, est_pos)
        step += 1

    # we should never reach here so I am going to return a True value
    print('We have reached 10000 steps!')
    return True


def count_obstacles(input_map):
    # first find where the guard is
    guard_pos = find_guard(input_map)

    # cache the guard starting position
    start_pos = guard_pos.copy()

    # create my output map
    count_steps(input_map)
    possible_obstacles = numpy.where(input_map == 'X')

    count = 0
    for x,y in zip(possible_obstacles[0], possible_obstacles[1]):
        if (start_pos[0,0] == x and start_pos[0,1] == y):
            continue

        input_map[x,y] ='#'
        new_pose = start_pos.copy()
        if is_in_loop(input_map, new_pose):
            count += 1
        input_map[x,y] ='.'

    return count