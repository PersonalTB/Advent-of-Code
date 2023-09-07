"""
*** *** ADVENT OF CODE - DAY 10 - Adapter Array *** ***

Src: https://adventofcode.com/2020/day/10
Setting: at the airport, our charger won't work, as the charging outlet produces the wrong amount of "jolts"
Challenge: in our bag we have a lot of adapters (input), find the ways in which we can connect our laptop to the outlet.

Input: input.txt, a .txt file with a series of ints, each representing a joltage adapter's output joltage (your puzzle input).

e.g.

16
10
15
5
1
11
7
19
6
12
4

Each of your joltage adapters is rated for a specific output joltage (your puzzle input). 
Any given adapter can take an input 1, 2, or 3 jolts lower than its rating and still produce its rated output joltage.
In addition, your device has a built-in joltage adapter rated for 3 jolts higher than the highest-rated adapter in your bag. 
(If your adapter list were 3, 9, and 6, your device's built-in adapter would be rated for 12 jolts.)

With the above adapters, your device's built-in joltage adapter would be rated for 19 + 3 = 22 jolts, 3 higher than the highest-rated adapter.

Treat the charging outlet near your seat as having an effective joltage rating of 0.

The challenge consists of 2 parts:
Part 1: If you use every adapter in your input, what is the number of 1-jolt differences multiplied by the number of 3-jolt differences?
Part 2: What is the total number of distinct ways you can arrange the adapters to connect the charging outlet to your device?

"""

import numpy as np
import collections

data_file = open('input.txt', 'r')
#data_file = open('test_input.txt', 'r')
data = data_file.read().strip().split('\n')

adapters = sorted([int(d) for d in data])
outlet = 0
laptop = max(adapters) + 3
chain = [outlet] + adapters + [laptop]

# *** PART 1: If you use every adapter in your input, what is the number of 1-jolt differences multiplied by the number of 3-jolt differences ***

print('Part 1: If you use every adapter in your input, what is the number of 1-jolt differences multiplied by the number of 3-jolt differences')

differences = np.diff(chain) # calculate the differences between each following pair in our chain
cnt = collections.Counter(differences) # counter counts the occurrences of each element in the list
print(cnt[1] * cnt[3])

# solution for test input: 220
# solution for proper input: 2048

# *** PART 2: What is the total number of distinct ways you can arrange the adapters to connect the charging outlet to your device? ***

print('Part 2: What is the total number of distinct ways you can arrange the adapters to connect the charging outlet to your device?')

# to find out the total number of distinct ways we can go from our outlet to our laptop, we need to:
# for each of our adaptors, and remember how many paths we find up to that point in the chain
# then, we do NOT try to simulate or exhaustively try to find each path, 
# rather, whilst working from low to high joltage adapters, we update all the adapters we can reach from here with the paths that got us here
# we do this for all adaptors, until we reach the last device in the chain, namely the laptop

chain = dict([ (a, 0) for a in chain ]) # dict to store by how many paths adaptors can be **reached** as jolts:paths pairs
chain[outlet] = 1 # outlet (0 jolts) is by default reachable in 1 way (the starting set-up)

for jolts in chain: # then, for every adaptor
	for i in range(1,3+1): # look ahead to the **potential** adaptors up to 3 jolts higher than the current one
		if jolts + i in chain: # if we actually have that adaptor
			chain[jolts + i] += chain[jolts] # increment the paths by which that adaptor can be reached by how many paths can reach the current one

print(chain[laptop]) # print the number of paths that lead to your laptop

# solution for test input: 19208
# solution for proper input: 1322306994176

"""

Reflection:

- I started off with a depth first search kind of strategy in which I actively tried to generate all possible paths, but this seemed wasteful
- Instead, I chose for a sort of up-climbing update function, 
- from the low joltage adapters up to the high joltage ones, increment the possible paths to high-joltage adapters with the paths of the lower ones
- this is more efficient and more elegant

"""
