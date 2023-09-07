"""
*** *** ADVENT OF CODE - DAY 12 - RAIN RISK *** ***

Src: https://adventofcode.com/2020/day/12
Setting: our ferry needs to take evasive action.
Challenge: figure out where we are based on our starting position and the actions we take

Input: input.txt, a .txt file containing the navigational actions the ship took. 
Format: each row has one action, in the format {Letter}{Number} where the letter denotes the action, and the number denotes how much.
Letters: F (forward x miles), N (north x miles), E (east), W (west), S (south), L (turn leftward by x degrees), R (turn right by x degrees)

e.g.

F10
N3
F7
R90
F11

Note: Manhattan distance is the sum of the absolute values of its position

2 methods for navigating:

1. ABSOLUTE NAVIGATION: navigates the ship as per the actions
In this example, from its starting position heading east, we go forward (east) 10, north 3, forward (east) 7, rotate south, forward (south) 11
In this example, the Manhattan distance = 17 + 8 = 25.

2. WAYPOINT NAVIGATION: navigates the ship forward/backward towards a waypoint relative to the ship. N/E/S/W and L/R change the position of the waypoint
In this example, from its starting waypoint (1, 10) (north, east), we go forward to (10 * 1, 10 * 10) = (10, 100), then shift the waypoint to (4, 10), etc.
In this example, the Manhattan distance = 214 + 72 = 286.

The challenge consists of two parts:
Part 1: What is the Manhattan distance between our final location and the ship's starting position using absolute navigation?
Part 2: What is the Manhattan distance between our final location and the ship's starting position using waypoint navigation

"""

import math
import re

data_file = open('input.txt','r')
#data_file = open('test_input.txt','r')
data = data_file.read().strip()
actions = re.findall(r'([LRNSEWFB])([0-9]+)', data)

# *** PART 1: What is the Manhattan distance between that location and the ship's starting position using absolute navigation? ***

print("Part 1: What is the Manhattan distance between that location and the ship's starting position using absolute navigation?")

directions = dict([('N',(1,0)), ('E',(0,1)), ('S',(-1,0)), ('W',(0,-1))])

heading = 'E'
position = (0,0)

for action in actions:
	atype = action[0]
	modifier = int(action[1])

	if atype in ['L','R']:
		dirs = list(reversed(directions.keys())) if atype == 'L' else list(directions.keys())
		heading = dirs[((dirs.index(heading) + modifier // 90) % len(dirs))]

	elif atype in ['F','B']:
		d = directions[heading]
		modifier = modifier if atype == 'F' else -modifier
		position = (position[0] + d[0] * modifier, position[1] + d[1] * modifier)

	elif atype in ['N','S','E','W']:
		d = directions[atype]
		position = (position[0] + d[0] * modifier, position[1] + d[1] * modifier)

print(abs(position[0]) + abs(position[1]))

# solution for test_input.txt: 25
# solution for input.txt: 1687

# *** PART 2: What is the Manhattan distance between that location and the ship's starting position using waypoint navigation?***

print("Part 2: What is the Manhattan distance between that location and the ship's starting position using waypoint navigation?")

directions = dict([('N',(1,0)), ('E',(0,1)), ('S',(-1,0)), ('W',(0,-1))])

waypoint = (1,10) # north 1, east 10
position = (0,0)

for action in actions:

	atype = action[0]
	modifier = int(action[1])

	if atype in ['L','R']:
		x = waypoint[1]
		y = waypoint[0]
		degrees = math.radians(modifier) * (-1 if atype in ['R'] else 1)
		waypoint = (round(x * math.sin(degrees) + y * math.cos(degrees)), round(x * math.cos(degrees) - y * math.sin(degrees)))
		
	elif atype in ['F','B']:
		modifier = modifier if atype == 'F' else -modifier
		position = (position[0] + waypoint[0] * modifier, position[1] + waypoint[1] * modifier)

	elif atype in ['N','S','E','W']:
		d = directions[atype]
		waypoint = (waypoint[0] + d[0] * modifier, waypoint[1] + d[1] * modifier)

print(abs(position[0]) + abs(position[1]))

# solution for test_input.txt: 286
# solution for input.txt: 20873

"""

Reflection:

- This was quite fun, and quite easy to do
- Wrestled a bit with the rotations of the waypoint, and had some floating point errors as well, so I just rounded them to ints.

"""
