"""
*** *** ADVENT OF CODE - DAY 3 - TOBOGGAN TRAJECTORY *** ***

Src: https://adventofcode.com/2020/day/3
Setting: we are at a ski slope, where there are trees on our path.
Challenge: we will be skiing down with a certain X- and Y-ward speed, how many trees do we encounter along the way?

Input: input.txt, a .txt file, with a 'map' of the ski slope, where . is an empty space, a # is a tree.

e.g. 
.#.......#...........#.........
..##.......#.#.#.....##...#....
.......#..#.....#...#..........
...#..........###...#........##

Note: the X-direction wraps around, so the final row of this input should actually be imagined as follows:

...#..........###...#........##...#..........###...#........##...#..........###...#........##...#..........###...#........## (etc.)

If our downward speed is 1 and right-ward speed is 2, 
.#.......#...........#......... --> O#.......#...........#.........
..##.......#.#.#.....##...#.... --> ..X#.......#.#.#.....##...#....
(where O denotes our positioning, but no tree, and X denotes our position AND there is a tree)
Then we encounter 1 tree in this example

The assignment has two parts:
Part 1: following a slope of right 3 and down 1, how many trees would you encounter?
Part 2: asks to find tree-occurrences for a certain amount of differing speeds, and to multiply these together.

""" 

from operator import mul
from functools import reduce

# read input data and split on new lines
inp_file = open('input.txt', 'r')
inp_data = inp_file.read()
inp_data = inp_data.strip().split('\n')

# *** PART 1 - following a slope of right 3 and down 1, how many trees would you encounter? ***

print("PART 1: following a slope of right 3 and down 1, how many trees would you encounter?")

# function to count the trees on the slope as defined by the inp_data, with a horizontal/vertical speed given by stepX and stepY
def count_trees_on_slope(inp_data, stepX, stepY):

	# get the size of the input area
	lenY = len(inp_data)
	lenX = len(inp_data[0]) # note: the X-range wraps to the beginning when the end

	# set starting x-position
	posX = 0

	# how many trees do we encounter?
	nTrees = 0

	# while we are not done with travelling down the slope
	for posY in range(0,lenY,stepY):

		# if we encounter a tree / #, increment the counter
		if inp_data[posY][posX] == '#':	nTrees += 1

		# go rightward, and wrap around when we reach the horizontal end of the arena
		posX = (posX + stepX) % lenX

	return nTrees

# count the trees with speeds
stepX = 3
stepY = 1
nTrees = count_trees_on_slope(inp_data, stepX, stepY)

# print the answer
print(nTrees)

# solution: 209


# *** PART 2 - What do you get if you multiply together the number of trees encountered on each of the listed slopes? ***

print('\nPART 2: What do you get if you multiply together the number of trees encountered on each of the listed slopes?')

"""
In Part 2 of the assignment, we travel down the slope n times, with different x/y-speeds.
We want to find out how many times we encounter trees during these speeds.
From this, we want to know what the PRODUCT / multiplication of these encounters are.
e.g. with speed 1 we 
"""

# practically the same as in part 1, but now, iterate over all our horizontal/vertical speeds
slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)]
nTrees = [count_trees_on_slope(inp_data, stepX, stepY) for stepX, stepY in slopes]
nTreesTotal = reduce(mul, nTrees) # multiply the current total with the trees found with the current speed

# print the answer
print(nTreesTotal)

# solution: 1574890240

"""

Reflection:

- this one was surprisingly easy
- originally used a "while not done" loop with a doneness-check on posY or if the line was the empty string ''
- but I found it slightly ugly, so I changed it to a for loop, with a defined stopping criterion
- made a function from the go-down-slope loop

"""
