"""
*** *** ADVENT OF CODE - DAY 15 - RAMBUNCTIOUS RECITATION *** ***

Src: https://adventofcode.com/2020/day/15
Setting: playing a memory game
Challenge: play the memory game, figure out what the nth spoken number will be

Input: an array of starting numbers, e.g. [0,3,6]

In this game, the players take turns saying numbers. 
They take turns reading from a list of numbers (your puzzle input). 
Then, each turn consists of considering the most recent number:
If that was the first time the number has been spoken, say 0.
Else, say how many turns the number is from its previous occurrence.

So, after the starting numbers, 
each turn results in that player speaking aloud:
either 0 (if the last number is new) 
or an age (if the last number is a repeat).

e.g. for input [0,3,6]

Turn 1: The 1st number spoken is a starting number, 0.
Turn 2: The 2nd number spoken is a starting number, 3.
Turn 3: The 3rd number spoken is a starting number, 6.
Turn 4: the last 6 was spoken before, for the first time, so say 0.
Turn 5: last number was 0. It wasn't the first time, and the last time was spoken 3 turns before the last one.
Turn 6: The last number spoken, 3 had also been spoken before, most recently on turns 5 and 2. So, the 6th number spoken is 5 - 2, 3.
Turn 7: Since 3 was just spoken twice in a row, and the last two turns are 1 turn apart, the 7th number spoken is 1.
Turn 8: Since 1 is new, the 8th number spoken is 0.
Turn 9: 0 was last spoken on turns 8 and 4, so the 9th number spoken is the difference between them, 4.
Turn 10: 4 is new, so the 10th number spoken is 0.
Turn 2020: 436

More examples:

Given the starting numbers 1,3,2, the 2020th number spoken is 1.
Given the starting numbers 2,1,3, the 2020th number spoken is 10.
Given the starting numbers 1,2,3, the 2020th number spoken is 27.
Given the starting numbers 2,3,1, the 2020th number spoken is 78.
Given the starting numbers 3,2,1, the 2020th number spoken is 438.
Given the starting numbers 3,1,2, the 2020th number spoken is 1836.


Given 0,3,6, the 30000000th number spoken is 175594.
Given 1,3,2, the 30000000th number spoken is 2578.
Given 2,1,3, the 30000000th number spoken is 3544142.
Given 1,2,3, the 30000000th number spoken is 261214.
Given 2,3,1, the 30000000th number spoken is 6895259.
Given 3,2,1, the 30000000th number spoken is 18.
Given 3,1,2, the 30000000th number spoken is 362.


The challenge consists of two parts:
Part 1: what will be the 2020th number spoken?
Part 2: what will be the 30000000th number spoken?

"""

test_data = [0,3,6]
data = [14,3,1,0,9,5]
data = data

# *** PART 1: what will be the 2020th number spoken? ***

def get_nth_turn(data, num_turns):

	# because we can insurt huge numbers in num_turns, we need to make the "memorization" function a more efficient than remembering everything
	# so, instead of remembering the entire history in a list, only remember at most the last 2 indices where a certain number has been said
	# then, when a certain number is said:
	# - we can just check the last occurrences, 
	# - if the number hadn't been said before, add that number to the memory and remember the current index
	# - if the number *has* been said before, ONLY remember the last index and the current one, and forget the rest

	memory = dict()
	turn_value = 0

	for turn_index in range(num_turns):

		if turn_index < len(data):
			turn_value = data[turn_index]
			memory[turn_value] = [turn_index]

		else:

			turn_value = 0 if len(memory[turn_value]) <= 1 else memory[turn_value][1] - memory[turn_value][0]

			if turn_value in memory:
				memory[turn_value] = [memory[turn_value][-1], turn_index]
			else:
				memory[turn_value] = [turn_index]

	return turn_value

print("Part 1: what will be the 2020th number spoken?")

print(get_nth_turn(data, 2020))

# solution for test_input.txt: 436
# solution for input.txt: 614

# *** PART 2: what will be the 30000000th number spoken? ***

print("Part 2: what will be the 30000000th number spoken?")

print(get_nth_turn(data, 30000000))

# solution for input.txt: 1065

"""

Reflection:

- started off with a less efficient implementation where I remembered all the numbers in a list.
- For the 30000000th number, this would make the remembering and calculating the differences very inefficient, 
- so I changed it to remember *just* the number said, and the last two indices at which they were said, 
- seems to work well

"""
