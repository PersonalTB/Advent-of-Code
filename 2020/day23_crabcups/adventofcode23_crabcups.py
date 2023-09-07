"""
*** *** ADVENT OF CODE - DAY 23 - CRAB CUPS *** ***

Src: https://adventofcode.com/2020/day/23
Setting: The crab now wants to challenge us to a game, a game of cups.
Challenge: Play the game of cups. Simulate the game states up to n moves.

Input: a string of integer numbers, the labels of the cups, e.g. 389125467

Game rules:

The cups will be arranged in a circle and labeled clockwise (your puzzle input). 
For example, if your labeling were 32415, there would be five cups in the circle; 
going clockwise around the circle from the first cup, the cups would be labeled 3, 2, 4, 1, 5, and then back to 3 again.

Before the crab starts, it will designate the first cup in your list as the current cup. The crab is then going to do 100 moves.

Each move, the crab does the following actions:
The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from the circle; 
cup spacing is adjusted as necessary to maintain the circle.
The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. 
If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up. 
If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value instead.
The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. 
They keep the same order as when they were picked up.
The crab selects a new current cup: the cup which is immediately clockwise of the current cup.

For the above example (with () being the current cup):

-- move 1 --
cups: (3) 8  9  1  2  5  4  6  7 
pick up: 8, 9, 1
destination: 2

-- move 2 --
cups:  3 (2) 8  9  1  5  4  6  7 
pick up: 8, 9, 1
destination: 7 (current cup 2-1 = 1, but this was picked up; 1-1 = wraparound to 9, this was picked up too, -1 = 8, picked up, -1 = 7)

...

-- move 10 --
cups: (5) 7  4  1  8  3  9  2  6 
pick up: 7, 4, 1
destination: 3

-- final --
cups:  5 (8) 3  7  4  1  9  2  6 

The game state will be represented by the clockwise ordering of the cups after cup 1.
After 10 moves, this would be: 92658374
after 100 moves, the clockwise ordering after cup 1 would be: 67384529

In part 2:
We will use one million cups instead. Our starting state will then be the input, padded with numbers to 1 million
So: 389125467 + 10,11,12,13,...,1.000.000
Also, we will play the game for 10.000.000 moves instead
Furthermore, the final state of the game should be given as the multiplication of the labels of the two cups immediately after cup 1
In the above example, this would be 934001 and then 159792; multiplying these gives 149245887792

The challenge consists of two parts:
Part 1: Using your labeling, simulate 100 moves. What are the labels on the cups after cup 1?
Part 2: Determine which 2 cups will end up clockwise of cup 1 after playing 10mil rounds with 1mil cups. What is their product?

"""

from copy import deepcopy

def get_input(test = False):
	data = 624397158 # actual input
	test_data = 389125467 # test data
	data = test_data if test else data
	data = [int(d) for d in str(data)]
	return data

def do_move(cups, current_cup=-1, n_pickup=3):
	"""
	Applies the rules to the cups.
	
	Where cups is a DICTIONARY containing the cup labels (as keys), and their NEIGHBOURS as VALUES
	e.g., if we have a circle of cups in clockwise direction [1,2,3]
	cups[1] = 2 # means that cup 1's clockwise neighbour is cup 2
	cup[2] = 3 # 3 is next to 2
	cup[3] = 1 # and after that we are back around to the start of the circle
	
	current_cup is the PREVIOUS ROUND's considered cup. IF this is the first round, it will be -1
	
	n_pickup denotes how many cups we want to pickup
	"""

	n_cups = len(cups) # for the wrap-around

	if current_cup == -1: # if this is the first round, assign the first cup as the current cup
		current_cup = list(cups.keys())[0]
	else:
		current_cup = cups[current_cup] # else, get the (previous round's) current cup's neighbour

	# The pickup and replace operation:
	#
	# before: n0 | n1 n2 n3 | n4 d0 d1
	# after:  n0 n4 d0 | n1 n2 n3 | d1
	#
	# where n0 is the current cup,
	# n1-n3 are picked up, 
	# and placed behind the destination d0
	# so: 
	# n0 and n4 must become neighbours (current cup, and the previous neighbour of the last picked up cup)
	# d0 and n1 must become neighbours (the destination cup, and the first picked up cup)
	# n3 and d1 must become neighbours (the last picked up cup, and the previous neighbour of the destination cup)

	pick_up_cups = [cups[current_cup]] # first pickup out of n is the neighbour of the current cup (n1)
	for i in range(n_pickup-1): # the next n-1 pickups are the neighbours of the last picked up cup (n2,n3)
		pick_up_cups.append(cups[pick_up_cups[-1]])

	destination = current_cup 
	while True:
		destination -= 1 # to find the destination cup, subtract 1, starting from from the current cup, until we find a cup that's not picked up
		destination = n_cups if destination <= 0 else destination
		if destination not in pick_up_cups:
			break

	#print('current cup:',current_cup, 'picked up:', pick_up_cups, 'destination', destination)

	# with the picked up cups picked up, the current cup's neighbour is now the cup that was previously after the last pickup cup (n0 and n4)
	cups[current_cup] = cups[pick_up_cups[-1]] 

	# the picked up cups will be placed after the destination cup in the order they were picked up, (d0-n1-n2-n3-d1)
	# so, the picked up cups will still have each other as their neighbours, these don't change, (n1-n2-n3)
	# the last picked up cup will have as its neighbour the cup that was PREVIOUSLY next to the destination cup (n3-d1)
	# and the destination cup will have as its neighbour the first picked up cup (d0-n1)
	cups[pick_up_cups[-1]] = cups[destination]
	cups[destination] = pick_up_cups[0]

	return cups, current_cup

def play_rounds(data, n_moves, n_cups, n_pickup = 3):
	cups = deepcopy(data) + list(range(len(data)+1, n_cups+1))
	cups = dict([(cups[c],cups[(c+1)%len(cups)]) for c in range(len(cups))]) # store the cups arrangement in a dict as cup:neighbourcup pairs
	current_cup = -1
	for move in range(n_moves):
		cups, current_cup = do_move(cups, current_cup = current_cup, n_pickup = n_pickup)

	return cups

# *** PART 1: Using your labeling, simulate 100 moves. What are the labels on the cups after cup 1? ***

def part1(data):

	print("Part 1: Using your labeling, simulate 100 moves. What are the labels on the cups after cup 1? ")

	n_moves = 100
	n_cups = len(data)
	n_pickup = 3

	cups = play_rounds(data, n_moves, n_cups, n_pickup)

	cups_sorted = []
	cup = 1 # start at cup 1
	while cups[cup] != 1: # then, as long as our next neighbour in line hasn't arrived back at 1 yet
		cup = cups[cup] # get that next cup in line
		cups_sorted.append(str(cup)) # jot it down
	print(''.join(cups_sorted)) # join it as one big concatenation of digits

	# solution for test_input.txt: 67384529
	# solution for input.txt: 74698532

# *** PART 2: Determine which 2 cups will end up clockwise of cup 1 after playing 10mil rounds with 1mil cups. What is their product? ***

def part2(data):

	print("Part 2: Determine which 2 cups will end up clockwise of cup 1 after playing 10mil rounds with 1mil cups. What is their product?")

	n_moves = 10000000
	n_cups = 1000000
	n_pickup = 3

	cups = play_rounds(data, n_moves, n_cups, n_pickup)

	print('final:', cups[1] * cups[cups[1]]) # nultiply the cup that is the neighbour of cup1, and the one that is the neighbour of THAT one

	# solution for test_input.txt: 149245887792
	# solution for input.txt: 286194102744

def main():
	data = get_input(test = False)
	part1(data)
	part2(data)

if __name__ == '__main__':
	main()

"""

Reflection:

- Started off with an implementation that actually kept track of the list, and all the operations on it
- This made for a lot of list operations, creations of new lists, etc., and wasn't very efficient 
- During the second part especially, this made for a lot of churning for my poor, poor laptop :/
- So, I made the implementation more efficient. 
- Now, instead, I represented the cups as a dict, to just keep track of the cups and their neighbor
- So now, to pickup and replace cups, I only needed to switch the neighbor references around 

"""
