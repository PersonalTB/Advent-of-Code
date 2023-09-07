"""
*** *** ADVENT OF CODE - DAY 20 - JURASSIC JIGSAW *** ***

Src: https://adventofcode.com/2020/day/20
Setting: After finding the valid satellite messages, we need to reassemble the pictures from the camera array back into a single image
Challenge: The tiles (your puzzle input) arrived in a random order, orientation. Re-assemble them and find the seaslug in the image.

Input: input.txt, a .txt file containing the image tiles and id's, separated by 2 newlines, in the format: Tile [num]:\n<tile>
Where each tile is composed of rows of binary values, with # being 1, and . being 0

e.g.

Tile 2311:  Tile 1951:  Tile 1171:  Tile 1427:  Tile 1489:  Tile 2473:  Tile 2971:  Tile 2729:  Tile 3079:
..##.#..#.  #.##...##.  ####...##.  ###.##.#..  ##.#.#....  #....####.  ..#.#....#  ...#.#.#.#  #.#.#####.
##..#.....  #.####...#  #..##.#..#  .#..#.##..  ..##...#..  #..#.##...  #...###...  ####.#....  .#..######
#...##..#.  .....#..##  ##.#..#.#.  .#.##.#..#  .##..##...  #.##..#...  #.#.###...  ..#.#.....  ..#.......
####.#...#  #...######  .###.####.  #.#.#.##.#  ..#...#...  ######.#.#  ##.##..#..  ....#..#.#  ######....
##.##.###.  .##.#....#  ..###.####  ....#...##  #####...#.  .#...#.#.#  .#####..##  .##..##.#.  ####.#..#.
##...#.###  .###.#####  .##....##.  ...##..##.  #..#.#.#.#  .#########  .#..####.#  .#.####...  .#...#.##.
.#.#.#..##  ###.##.##.  .#...####.  ...#.#####  ...#.#.#..  .###.#..#.  #..#.#..#.  ####.#.#..  #.#####.##
..#....#..  .###....#.  #.##.####.  .#.####.#.  ##.#...##.  ########.#  ..####.###  ##.####...  ..#.###...
###...#.#.  ..#.#..#.#  ####..#...  ..#..###.#  ..##.##.##  ##...##.#.  ..#.#.###.  ##..#.##..  ..#.......
..###..###  #...##.#..  .....##...  ..##.#..#.  ###.##.#..  ..###.#.#.  ...#.#.#.#  #.##...##.  ..#.###...

By rotating, flipping, and rearranging them, you can find a square arrangement that causes all adjacent borders to line up:

#...##.#.. ..###..### #.#.#####.
..#.#..#.# ###...#.#. .#..######
.###....#. ..#....#.. ..#.......
###.##.##. .#.#.#..## ######....
.###.##### ##...#.### ####.#..#.
.##.#....# ##.##.###. .#...#.##.
#...###### ####.#...# #.#####.##
.....#..## #...##..#. ..#.###...
#.####...# ##..#..... ..#.......
#.##...##. ..##.#..#. ..#.###...

#.##...##. ..##.#..#. ..#.###...
##..#.##.. ..#..###.# ##.##....#
##.####... .#.####.#. ..#.###..#
####.#.#.. ...#.##### ###.#..###
.#.####... ...##..##. .######.##
.##..##.#. ....#...## #.#.#.#...
....#..#.# #.#.#.##.# #.###.###.
..#.#..... .#.##.#..# #.###.##..
####.#.... .#..#.##.. .######...
...#.#.#.# ###.##.#.. .##...####

...#.#.#.# ###.##.#.. .##...####
..#.#.###. ..##.##.## #..#.##..#
..####.### ##.#...##. .#.#..#.##
#..#.#..#. ...#.#.#.. .####.###.
.#..####.# #..#.#.#.# ####.###..
.#####..## #####...#. .##....##.
##.##..#.. ..#...#... .####...#.
#.#.###... .##..##... .####.##.#
#...###... ..##...#.. ...#..####
..#.#....# ##.#.#.... ...##.....

For reference, the IDs of the above tiles are:

1951    2311    3079
2729    1427    2473
2971    1489    1171

To check that you've assembled the image correctly, multiply the IDs of the four corner tiles together. 
If you do this with the assembled tiles from the example above, you get 1951 * 3079 * 2971 * 1171 = 20899048083289.

In part 2: 

we will look at the fully compiled image to find the seamonster:

                  # 
#    ##    ##    ###
 #  #  #  #  #  #   

To do this, throw away the edges of the individual tiles (as they were only for matching tile to tile), 
then concatenate them,
then find the seaslug pattern in the images (see below for an example, where O is part of the seaslug)

.####...#####..#...###..
#####..#..#.#.####..#.#.
.#.#...#.###...#.##.O#..
#.O.##.OO#.#.OO.##.OOO##
..#O.#O#.O##O..O.#O##.##
...#.#..##.##...#..#..##
#.##.#..#.#..#..##.#.#..
.###.##.....#...###.#...
#.####.#.#....##.#..#.#.
##...#..#....#..#...####
..#.##...###..#.#####..#
....#.##.#.#####....#...
..##.##.###.....#.##..#.
#...#...###..####....##.
.#.##...#.##.#.#.###...#
#.###.#..####...##..#...
#.###...#.##...#.##O###.
.O##.#OO.###OO##..OOO##.
..O#.O..O..O.#O##O##.###
#.#..##.########..#..##.
#.#####..#.#...##..#....
#....##..#.#########..##
#...#.....#..##...###.##
#..###....##.#...##.##.#

Now we can calculate the noise in the original image as how much of the image was marked as 'part of the sea slug' without actually being one
In the above example, the noise / water roughness is 273

The challenge consists of two parts:
Part 1: What do you get if you multiply together the IDs of the four corner tiles?
Part 2: How much of the original image is noise as compared to actual seaslug signal?

"""

from enum import IntEnum
import math
from operator import mul
from scipy import ndimage
import numpy as np
from matplotlib import pyplot as plt
import re
from functools import reduce

FLIPS = [False, True] # possible vertical flips (not necessary to horizontally flip, as it is the same as a vertical flip + a 180 deg rotation)
ROTATIONS = [0,90,180,270] # possible rotations in degrees

class Side(IntEnum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

class Tile:
    def __init__(self, idx, img):
        self.img = img
        self.idx = idx
        self.variants = []
        self.fitting_variant_idx = None # which flip/rotation variant fits in the position this tile is currently slotted in
        self.PrecalculateTileVariants()

    def GetImage(self):
        """ Get the actual borderless part of the image, since the border is only there for matching tiles together """
        return self.variants[self.fitting_variant_idx][1:-1,1:-1]

    def PrecalculateTileVariants(self):
        """ Pre-calculate all possible flip/rotated variations of the original tile image"""
        for flip in FLIPS:
            for rotation in ROTATIONS:
                im = self.img
                im = np.flipud(im) if flip else im
                im = ndimage.rotate(im, rotation) if rotation > 0 else im
                self.variants.append(im)

    def GetBorderOnSide(self, side):
        """ Get the top/left/bottom/right side of the tile to use when trying to fit it to another one"""
        img = self.variants[self.fitting_variant_idx]
        if side == Side.LEFT:
            return img[:,0] 
        elif side == Side.RIGHT:
            return img[:,-1]
        elif side == Side.TOP:
            return img[0,:] 
        elif side == Side.BOTTOM:
            return img[-1,:]

class Puzzle:
    """
    Puzzle class holds the tile objects, and the slots in which these tiles are to be placed (as an n_rows x n_rows matrix)
    """

    def __init__(self, tiles):
        self.tiles = tiles
        self.n_rows = self.n_cols = int(math.sqrt(len(tiles)))
        self.tile_slots = [[None for j in range(0,self.n_cols)] for i in range(0,self.n_cols)]

    def CheckLeftRight(left, right):
        """ check if the edges of two horizontal tiles match """
        return np.all(left.GetBorderOnSide(Side.RIGHT) == right.GetBorderOnSide(Side.LEFT))

    def CheckTopBottom(top, bottom):
        """ check if the edges of two vertical tiles match """
        return np.all(top.GetBorderOnSide(Side.BOTTOM) == bottom.GetBorderOnSide(Side.TOP))

    def CheckPosition(self, tile, row, col):
        """
        To check if a tile fits in a position in the puzzle (given by its row and col indices),
        check if the tile fits with its leftward neighbour (if there is no neighbour there, it is an edge-tile, and it fits there by default),
        and check if the tile fits with its topward neighbour (if there is no neighbour above it, it is an edge-tile and fits there by default),
        If the tile fits for both, the puzzle piece fits in this position
        """
        fits_left_right = col == 0 or Puzzle.CheckLeftRight(self.tile_slots[row][col-1], tile)
        fits_top_bottom = row == 0 or Puzzle.CheckTopBottom(self.tile_slots[row-1][col], tile)
        return fits_left_right and fits_top_bottom

    def GetFullImage(self):
        """ constructs the full image by concatenating all tiles' (borderless) images together, and returns it """
        blocks = [[tile.GetImage() for tile in row] for row in self.tile_slots]
        image = np.block(blocks) 
        return image

    def GetCornerTiles(self):
        """ returns the topleft, topright, bottomleft and bottomright corner tiles """
        return [self.tile_slots[0][0].idx, # topleft
            self.tile_slots[0][self.n_cols-1].idx, # topright
            self.tile_slots[self.n_rows-1][0].idx, # bottomleft
            self.tile_slots[self.n_rows-1][self.n_cols-1].idx] # bottomright

# *** SETUP ***

def read_data():
    """ 
    read the input file, 
    split it into separate tiles, 
    and parse these into actual tile objects, as matrices of 0s and 1s
    then construct the puzzle object from the tiles

    also read in the sea monster's pattern from its file
    and parse it into a numpy matrix of 0s and 1s

    then return the constructed puzzle and the monster pattern
    """

    data_file = open('input.txt','r')
    #data_file = open('test_input.txt','r')
    data = data_file.read()
    data = re.findall('Tile ([0-9]+):([\n.#]+)',data)
    tiles = [Tile(int(indx), (np.array([np.array(list(row)) for row in img.strip().split('\n')]) == '#').astype(int)) for indx, img in data]
    puzzle = Puzzle(tiles)

    monster_file = open('sea_monster.txt','r')
    sea_monster = monster_file.read()
    sea_monster = (np.array([np.array(list(row)) for row in sea_monster.split('\n')]) == '#').astype(int)
    return puzzle, sea_monster

# *** PART 1: What do you get if you multiply together the IDs of the four corner tiles? ***

def dfs_solve_puzzle(puzzle, row, col, used_tiles):
    """
    Depth-first search to find the solution to the puzzle
    i.e. 
    For each position in the puzzle,
        For each possible action in tile laying option (i.e. every flip/rotate-variant), 
        Check if the action is valid (i.e. the tile fits)
            If so, recurse to find the next action, rinse and repeat
                If we find the goal state, i.e. if we get to the end of the puzzle with all pieces laid, return the solution
            Else, backtrack: undo the last action, take out the piece,...
        ...and continue trying with other options
    Continue for all possible positions and actions until we have either reached the goal, 
    or not, in which case we return that we failed
    """

    # the goal-state is the end of the puzzle where all tiles have been used up
    if len(used_tiles) == len(puzzle.tiles):
        return True

    # else, if we haven't reached the goal yet, we need to take an action, so:
    # for each unused tile
    for tile in puzzle.tiles:
        
        if tile.idx not in used_tiles:
        
            # flag it as being in use so we won't use the same tile twice later down the road
            used_tiles.add(tile.idx)

            # place it on the current position
            puzzle.tile_slots[row][col] = tile

            # for all possible rotations and flips
            for v in range(len(tile.variants)):

                # rotate/flip the puzzle piece to that orientation          
                tile.fitting_variant_idx = v
                
                # check if it fits in the current position
                if puzzle.CheckPosition(tile, row, col):
                    
                    # if so, try to find a piece for the next position
                    next_col = (col + 1)
                    next_row = row
                    # if we just placed a piece at the end of the puzzle's row, start at the beginning of the next row
                    if next_col >= puzzle.n_cols: 
                        next_col %= puzzle.n_cols
                        next_row += 1

                    # if we found a solution somewhere down the road, keep the puzzle piece's positions as they are, and just return
                    if dfs_solve_puzzle(puzzle, next_row, next_col, used_tiles):
                        return puzzle
                
                # if it doesn't fit, or this variant tile-placement didn't lead to a solution, don't use this rotation/flip-variant
                tile.fitting_variant_idx = None
            
            # if this tile placement didn't lead to a solution, backtrack: take the piece out again, and keep looking for the rest pieces
            puzzle.tile_slots[row][col] = None
            used_tiles.remove(tile.idx)

    # be sad if we didn't find a solution at all
    return False

def part1(puzzle):

    print("PART 1: What do you get if you multiply together the IDs of the four corner tiles?")

    puzzle = dfs_solve_puzzle(puzzle, 0, 0, set())
    if puzzle:
      print(reduce(mul, [1] + puzzle.GetCornerTiles())) # calculate the product of the corner tiles

    # solution for test_input.txt: 20899048083289
    # solution for input.txt: 32287787075651

# *** PART 2: How much of the original image is noise as compared to actual seaslug signal? ***

def get_patterns_in_image(image, pattern):
    """
    search for EXACT MATCHES of a given pattern in an image.
    returns the count of the pattern in the image, as well as a convolved image showing where the pattern was found.
    pattern is a np array of values that can be convolved with the image to find the pattern in the image.
    """
    # let image and pattern be sequences of 0 and 1
    # convolution iterates over each point in the image, 
    # at each point, it calculates the "amount of match" between the pattern and the patch of the image around that point
    # it does so by multiplying the pattern and the patch of the image surrounding the point considered element-wise, and then summing it
    # e.g.
    # 10101 convolved with a 10101 pattern would give us 1*1 + 0*0 + 1*1 + 0*0 + 1*1 = 1 + 0 + 1 + 0 + 1 = 3
    # 11111 convolved with a 10101 pattern would give us 1*1 + 1*0 + 1*1 + 1*0 + 1*1 = 1 + 0 + 1 + 0 + 1 = 3
    # 01110 convolved with a 10101 pattern would give us 0*1 + 1*0 + 1*1 + 0*0 + 1*1 = 0 + 0 + 1 + 0 + 0 = 1
    # 11110 convolved with a 10101 pattern would give us 1*1 + 1*0 + 1*1 + 0*0 + 1*1 = 1 + 0 + 1 + 0 + 0 = 2
    # Note that the sum of the pattern itself is 3, and that ONLY those patches of the image that contain the pattern fully, sum up to 3 also
    # so, in this case, if the convolution of the pattern with the image is *exactly* the same as the sum of the pattern, there is an EXACT match
    c_image = ndimage.convolve(image, pattern, mode='constant', cval=0) == pattern.sum().sum()
    count = c_image.sum().sum() # count how many exact matches of the pattern were found in the image
    found_pattern_image = ndimage.convolve(c_image, pattern, mode='constant', cval=0).astype(int) # reconstruct the image of the seaslugs

    return count, found_pattern_image

def part2(puzzle, sea_monster):

    print("PART 2: How much of the original image is noise as compared to actual seaslug signal? ")

    image = puzzle.GetFullImage()

    # flip and rotate the image to each possible orientation and count any sea monsters in the picture. If so, stop rotating
    seamonster_cnt = 0
    seamonster_img = None
    for flip in FLIPS:
        for rotation in ROTATIONS:
            im = image
            im = np.flipud(im) if flip else im 
            im = ndimage.rotate(im, rotation) if rotation > 0 else im
            seamonster_cnt, seamonster_img = get_patterns_in_image(im, sea_monster)
            if seamonster_cnt > 0:
                break
        if seamonster_cnt > 0:
            break

    # the noise in the image are all 1's in the image that are not those that belong to the seamonsters
    noise = image.sum().sum() - seamonster_img.sum().sum() 
    print(noise)

    # bonus: show the seamonsters in the noise
    plt.imshow(image*0.25 + seamonster_img); plt.show()

    # solution to test_input2.txt: 273
    # solution to input.txt: 1939

def main():
    puzzle, sea_monster = read_data()
    part1(puzzle)
    part2(puzzle, sea_monster)

if __name__ == '__main__':
    main()

"""

Reflection:

- This was a difficult one.
- Figured I'd actually make some Tile and Puzzle classes for this
- Figured I'd need to use some kind of depth-first search strategy for this.
- After searching around, I implemented the scramble puzzle solver like in: https://liorsinai.github.io/coding/2020/06/26/scramble-puzzle.html
- Started off computing each flip/rotation in the DFS loop, and by remembering the still-available tiles
- but something seemed to go wrong, and I got stuck in an infinite loop
- I then switched to pre-computed variants, and memorizing the already-used tiles, which worked way better for some mysterious reason
- now everything works like a charm
- the only mystery remaining now is why I need to flip my convolution kernel when scanning for the seaslug... :/
- I solved the mystery: after having found the sea creature first time around, I "break" out of the loop...
- however, in python, when you break, it only breaks the inner loop 
- so after that, it would continue searching in the outer loop, flipping the image.
- in other words, I had set up my searching code such that I would ONLY exit if I found the seaslug in the FLIPPED image
- so, in order to find the solution in **this** iteration that would exit with a found seaslug, I needed to flip the kernel!
- Lessons learnt: when you want to break out of a loop, ALSO BREAK THE OUTER LOOP!

"""
