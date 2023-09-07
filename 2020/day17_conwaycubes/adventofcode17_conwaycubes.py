"""
*** *** ADVENT OF CODE - DAY 17 - CONWAY CUBES *** ***

Src: https://adventofcode.com/2020/day/17
Setting: the conway cubes in our pocket dimension satellite is malfunctioning! oh no! we need to fix it.
Challenge: calculate the final state after 6 

Input: input.txt, a .txt file containing a small region of the conway cube space with active (#) and inactive (.) cells

e.g. 

.#.
..#
###

The pocket dimension contains an infinite 3-dimensional grid. 
At every integer 3-dimensional coordinate (x,y,z), there exists a single cube which is either active or inactive.

In the initial state of the pocket dimension, almost all cubes start inactive. 
The only exception to this is a small flat region of cubes (your puzzle input); 
the cubes in this region start in the specified active (#) or inactive (.) state.

The energy source then proceeds to boot up by executing six cycles.

Each cube only ever considers its neighbors: any of the 26 other cubes where any of their coordinates differ by at most 1. 
For example, given the cube at x=1,y=2,z=3, its neighbors include the cube at x=2,y=2,z=2, the cube at x=0,y=2,z=3, and so on.

During a cycle, all cubes simultaneously change their state according to the following rules:

If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.

e.g. for the example given above

After 1 cycle:

z=-1    z=0     z=1
#..     #.#     #..
..#     .##     ..#
.#.     .#.     .#.

After 2 cycles:

z=-2    z=-1    z=0     z=1     z=2
.....   ..#..   ##...   ..#..   .....
.....   .#..#   ##...   .#..#   .....
..#..   ....#   #....   ....#   ..#..
.....   .#...   ....#   .#...   .....
.....   .....   .###.   .....   .....

After 3 cycles:

z=-2        z=-1        z=0         z=1         z=2
.......     ..#....     ...#...     ..#....     .......
.......     ...#...     .......     ...#...     .......
..##...     #......     #......     #......     ..##...
..###..     .....##     .......     .....##     ..###..
.......     .#...#.     .....##     .#...#.     .......
.......     ..#.#..     .##.#..     ..#.#..     .......
.......     ...#...     ...#...     ...#...     .......

After the full six-cycle boot process completes, 112 cubes are left in the active state.

In part 2, instead of 3 dimensions, we use 4 dimensions to apply the rules:

z=-1, w=-1  z=0, w=-1   z=1, w=-1   
#..         #..         #..         
..#         ..#         ..#         
.#.         .#.         .#.         

z=-1, w=0   z=0, w=0    z=1, w=0
#..         #.#         #..
..#         .##         ..#
.#.         .#.         .#.

z=-1, w=1   z=0, w=1    z=1, w=1
#..         #..         #..
..#         ..#         ..#
.#.         .#.         .#.

(etc.)

After the full six-cycle boot process completes, 848 cubes are left in the active state for the test case above in 4-D.

The challenge consists of two parts:
Part 1: Starting with your given initial configuration, simulate six cycles. How many cubes are left in the active state after the sixth cycle?
Part 2: simulate six cycles. How many cubes are left in the active state after the sixth cycle for the 4th-Dimensional case?

"""

from scipy import ndimage
import numpy as np

data_file = open('input.txt','r')
#data_file = open('test_input.txt','r')
data_raw = data_file.read().strip().split('\n')
data_raw = np.array([list(d) for d in data_raw])
data = np.zeros(data_raw.shape)
data[data_raw == '#'] = 1

# *** PART 1: Starting with the given configuration, simulate six cycles. How many cubes are left in the active state after the sixth cycle? ***

print("Part 1: Starting with the given configuration, simulate six cycles. How many cubes are left in the active state after the sixth cycle?")

def state_to_str1(state):
    s = ''
    for d in range(state.shape[2]):
        slic = state[:,:,d].reshape(state.shape[0],state.shape[1])
        if d > 0: 
            s += '\n'
        s += 'z={0}\n'.format(d) + '\n'.join([''.join(['.' if el == 0 else '#' for el in row]) for row in slic]) + '\n'
    return s 

def update1(curr_state):

    curr_state = np.pad(curr_state, pad_width=1, mode='constant', constant_values=0)

    next_state = np.zeros(curr_state.shape)

    rows = curr_state.shape[0]
    cols = curr_state.shape[1]
    dept = curr_state.shape[2]

    for r, c, z in np.ndindex(curr_state.shape): # iterate over the matrix cells

        # the amount of alive neighbours are the count of all cells in a 3x3 square neighborhood (minus the cell itself)
        num_alive = np.sum(curr_state[max(0,r-1):min(r+2,rows), max(0,c-1):min(c+2,cols), max(0,z-1):min(z+2,dept)]) - (curr_state[r,c,z])

        if curr_state[r,c,z] == 0 and num_alive in [3]:
            next_state[r,c,z] = 1
        elif curr_state[r,c,z] == 1:
            if num_alive in [2,3]:
                next_state[r,c,z] = 1
            else:
                next_state[r,c,z] = 0
        else:
            next_state[r,c,z] = curr_state[r,c,z]

        #print(curr_state[r-1:r+2, c-1:c+2])
        #print(curr_alive[r-1:r+2, c-1:c+2])
        #print(r,c,num_alive)

    return next_state

def GOL1(data, max_iterations):

    current_data = np.copy(data)
    current_data = np.expand_dims(current_data,2)
    iterations = 0

    while iterations < max_iterations:

        current_data = update1(current_data)
        iterations += 1

    print('FINAL state at iterations:',iterations, 'with n active cubes:', np.sum(current_data))
    #print(state_to_str1(current_data))

GOL1(data, 6)

# solution for test_input.txt: 112
# solution for input.txt: 293

# *** PART 2: ***

print("Part 2: ")

def update2(curr_state):

    curr_state = np.pad(curr_state, pad_width=1, mode='constant', constant_values=0)

    next_state = np.zeros(curr_state.shape)

    rows = curr_state.shape[0]
    cols = curr_state.shape[1]
    dept = curr_state.shape[2]
    wdep = curr_state.shape[3]

    for r, c, z, w in np.ndindex(curr_state.shape): # iterate over the matrix cells

        # the amount of alive neighbours are the count of all cells in a 3x3 square neighborhood (minus the cell itself)
        num_alive = np.sum(curr_state[max(0,r-1):min(r+2,rows), max(0,c-1):min(c+2,cols), max(0,z-1):min(z+2,dept), max(0,w-1):min(w+2,wdep)]) - (curr_state[r,c,z,w])

        if curr_state[r,c,z,w] == 0 and num_alive in [3]:
            next_state[r,c,z,w] = 1
        elif curr_state[r,c,z,w] == 1:
            if num_alive in [2,3]:
                next_state[r,c,z,w] = 1
            else:
                next_state[r,c,z,w] = 0
        else:
            next_state[r,c,z,w] = curr_state[r,c,z,w]

        #print(curr_state[r-1:r+2, c-1:c+2])
        #print(curr_alive[r-1:r+2, c-1:c+2])
        #print(r,c,num_alive)

    return next_state

def GOL2(data, max_iterations):

    current_data = np.copy(data)
    current_data = np.expand_dims(current_data,[2,3])
    iterations = 0

    while iterations < max_iterations:

        current_data = update2(current_data)
        iterations += 1

    print('FINAL state at iterations:',iterations, 'with n active cubes:', np.sum(current_data))

GOL2(data, 6)

# solution for test_input.txt: 848
# solution for input.txt: 1816

def update_better(curr_state, kernel):
    curr_state = np.pad(curr_state, 1, 'constant', constant_values=0) # grow the current state so the activation can spread one more row
    n_neighbors = ndimage.convolve(curr_state, kernel, mode='constant', cval=0) # convolve the neighborhood kernel over the current state
    # cells with 3 neighbors always come/stay alive; 2 neighbors stay alive if the current cell is alive now
    next_state = np.bitwise_or(n_neighbors == 3, np.bitwise_and(n_neighbors == 2, curr_state == 1).astype('int'))
    return next_state

def GOL(data, max_iterations, dims):
    state = np.copy(data)
    for i in range(len(data.shape),dims): 
        state = np.expand_dims(state,i) # expand state to the dimensionality we want
    
    kernel = np.ones([3 for i in range(dims)]) # create neighborhood kernel: all 1's in 3x3x(for each dimension), with the center (current cell) 0
    kernel[tuple([1 for i in range(dims)])] = 0 # don't count the center as a neighbor

    for t in range(max_iterations):
        state = update_better(state, kernel) # update state with neighborhood kernel

    return state

print('active cells after 6 iterations for dims:')
print(3, np.sum(GOL(data, 6, 3)))
print(4, np.sum(GOL(data, 6, 4)))
print(5, np.sum(GOL(data, 6, 5)))
print('nice')

"""

Reflection:

- game of life, fun
- in 4D >.<
- feel like it can be done more efficiently, by shrinking inactive dimensional slices (where they are all 0s), e.g., but haven't implemented it
- also felt like the iteration over the dimensions can be done more effectively; 
- this has been improved by using a neighborhood convolution as a neighbor-counting method

"""
