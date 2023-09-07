"""
*** *** ADVENT OF CODE - DAY 24 - LOBBY LAYOUT *** ***

Src: https://adventofcode.com/2020/day/24
Setting: the resort's lobby is being renovated; they are installing a new hexagonal tile floor in a specific pattern. You offer to help.
Challenge: Find out which tiles need to be flipped to their opposite color.

Input: input.txt, a .txt file containing a list of tiles that need to be flipped to their right color. 

The tiles are all white on one side and black on the other.
These tiles are specified by a series of directional 'steps' from the reference tile in the center of the lobby.
Because the tiles are hexagonal, every tile has six neighbors: east, southeast, southwest, west, northwest, and northeast. 
These directions are given in your list, respectively, as e, se, sw, w, nw, and ne. 
A tile is identified by a series of these directions with no delimiters
Each time a tile is identified, it flips from white to black or from black to white. Tiles might be flipped more than once.

For example, nwwswee identifies the tile you land on if you start at the reference and move northeast, west, southwest and east twice. 
In this example, you arrive back at the reference and flip it.

e.g.

sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew

Part 1:
Go through the renovation crew's list (your input) and determine which tiles they need to flip. 
After all of the instructions have been followed, how many tiles are left with the black side up?

In the above example, 10 tiles are flipped once (to black), 
and 5 more are flipped twice (to black, then back to white). 
After all of these instructions have been followed, a total of 10 tiles are black.

Part 2:
The tile floor in the lobby is meant to be a living art exhibit. Every day, the tiles are all flipped according to the following rules:
Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
This process executes simultaneously for every tile: it is first determined which tiles needs flipping, then they are all flipped together.

In the above example, the amount of black tiles facing up after x days would be:
Day 1: 15; Day 2: 12; Day 3: 25; ... Day 100: 2208

The challenge consists of two parts:
Part 1: After all of the instructions have been followed, how many tiles are left with the black side up?
Part 2: Using the update rules, how many tiles will be black after 100 days?

"""

import matplotlib.animation as animation
from collections import defaultdict
from scipy import ndimage
import numpy as np
from matplotlib import pyplot as plt
import re

def get_data(test = False):
    path = 'input.txt' if test == False else 'test_input.txt'
    data_file = open(path,'r')
    
    data = data_file.read().strip().split('\n')
    #data = ['nwwswee'] # for testing, will land you back at the reference tile (0,0), and will only flip that one to black
    
    # separate tile-finding instructions into separate steps
    data = [re.findall('(ne|se|nw|sw|e|w)',tile) for tile in data] # first elements in |-regexes get precedence, so we won't count the e's and w's double
    return data

# *** PART 1: After all of the instructions have been followed, how many tiles are left with the black side up? ***

# see also: https://zvold.blogspot.com/2010/01/bresenhams-line-drawing-algorithm-on_26.html#section_3_1
DIRS = { 'e': np.array([0, 1]), 'w': np.array([0, -1]), 'nw':  np.array([1,-1]), 'sw':  np.array([-1,0]), 'ne':  np.array([1,0]), 'se':  np.array([-1,1])}

def hex_coord_to_str(hex_coord):
    """ 
    Custom to_str method for hex coods. Used to generate hashable keys for dicts, and used over numpy's to_str operations, because we can str-to-hex / undo them easier later. 
    e.g. np.array: [8  9] becomes "8,9"
    """
    return ','.join([str(c) for c in hex_coord])

def GetTilestate(data):
    """ 
    Calculates the tile states for all tiles for which the tile flip instructions are given by the input. 
    Returns a dict of coord_str:flip_bool pairs, 
    where the coord_str is a string of "x,y" coordinates, 
    and the flip_bool is a boolean value reflecting if the tile is flipped to black (True) or not. 
    """
    hex_dict = defaultdict(bool) # where black tiles are true, and white tiles are false
    for tile in data:
        # final coordinate is the sum total of all direction-vectors * how often we step in those directions e.g. EWW = 1xEast, 2xWest = 1x[0,1], 2x[0,-1] = [0,-1]
        hex_coord = sum(hex_steps * tile.count(direction) for direction, hex_steps in DIRS.items())
        hex_coord_str = hex_coord_to_str(hex_coord)
        hex_dict[hex_coord_str] = not hex_dict[hex_coord_str]
    return hex_dict

def part1(data):
    print("Part 1: After all of the instructions have been followed, how many tiles are left with the black side up?")
    hex_dict = GetTilestate(data)
    print(f'black tiles: { list(hex_dict.values()).count(True) }, white tiles: { list(hex_dict.values()).count(False) }')

    # solution for test_input.txt: 10
    # solution for input.txt: 497

# *** PART 2: Using the update rules, how many tiles will be black after 100 days? ***

def hex_coord_from_str(s):
    """ Revert the str representation of a coordinate back to the actual coordinate array of integers. e.g. "8,9" becomes np.array: [8  9] """
    return np.array([int(si) for si in s.split(',')])

def CreateGridFromTileStates(tilestates):
    coords = list(tilestates.keys())
    values = list(tilestates.values())
    coords = np.array([hex_coord_from_str(coord) for coord in coords])
    mincoord = (np.min(coords[:,0]), np.min(coords[:,1])) # find the origin coordinate in our coordinate set
    coords = coords - mincoord # shift the coordinates such that the origin for the tileset is at 0,0
    bounds = (np.max(coords[:,0])+1, np.max(coords[:,1])+1) # find maximal bounding box size for the coordinates (+1 to account for exclusive max)
    grid = np.zeros(bounds).astype('int')
    grid[coords[:,0], coords[:,1]] = values
    return grid

def update(curr_state, kernel):
    curr_state = np.pad(curr_state, 1, 'constant', constant_values=0) # grow the current state so the activation can spread one more row
    n_neighbors = ndimage.convolve(curr_state, kernel, mode='constant', cval=0) # convolve the neighborhood kernel over the current state
    # Rewritten update rules such that they specify when cells become/stay black:
    # - a tile becomes black if they were white before, and have 2 black neighbours
    # - a tile stays black if they were black before and do NOT conform to the flipping rule (become white if neighbour-count is 0 or more than 2)
    white_tiles_rules = np.bitwise_and(curr_state == 0, n_neighbors == 2)
    black_tiles_rules = np.bitwise_and(curr_state == 1, ~np.bitwise_or(n_neighbors == 0, n_neighbors > 2))
    next_state = np.bitwise_or(white_tiles_rules, black_tiles_rules)
    return next_state.astype(int)

def GOL_HEX(data, max_iterations, animate = False):

    current_data = np.copy(data)

    # construct a hexagonal neighbor kernel around the kernel's central coordinate of (1,1) (hence the +1)
    kernel = np.zeros((3,3))
    for direction in DIRS.values(): 
        kernel[1 + direction[0], 1 + direction[1]] = 1 

    history = []
    if animate: history.append(current_data)

    for iteration in range(max_iterations):
        #if (iteration % 100) == 0: print(iteration)
        current_data = update(current_data, kernel)
        if animate: history.append(current_data)

    return current_data, history

def animate_grid_history(grids):
    grids = [np.pad(grids[i], len(grids) - 1 - i, 'constant', constant_values=0) for i in range(len(grids))] # pad all grids to the same size
    fig = plt.figure()
    plt.axis('off')
    ims = [[plt.imshow(grid, cmap='Greys')] for grid in grids]
    im_ani = animation.ArtistAnimation(fig, ims, interval=25)
    im_ani.save('im.mp4') # requires ffmpeg (download at https://ffmpeg.org/, unzip, then add its bin folder to the system environment path)
    plt.show()

plt.show()

def part2(data):
    print("Part 2: Using the update rules, how many tiles will be black after 100 days?")
    animate = False
    max_iterations = 100
    hex_dict = GetTilestate(data)
    hex_grid = CreateGridFromTileStates(hex_dict)
    hex_grid, history = GOL_HEX(hex_grid, max_iterations = max_iterations, animate = animate)
    print(f'final state has { sum(sum(hex_grid)) } flipped tiles')
    if animate: animate_grid_history(history)

    # solution for test_input.txt for day 1: 15
    # solution for test_input.txt for day 2: 12
    # solution for test_input.txt for day 3: 35
    # solution for test_input.txt for day 100: 2208
    # solution for input.txt: 4156

def main():
    data = get_data()
    part1(data)
    part2(data)

if __name__ == '__main__':
    main()

"""

Reflection:

- Fun! 
- Not too difficult once you figure out how the hex grid coordinate systems and 'stepping' in such a space works.
- Figured it was most efficient to only represent the states of the tiles we actually visit in a dict based on its location.
- For part 2, it was nice to see the game of life code from day 17 can be repurposed with a hexagonal convolution kernel.
- couldn't resist adding an animation

"""
