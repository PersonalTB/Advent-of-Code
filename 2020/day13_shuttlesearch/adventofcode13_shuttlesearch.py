"""
*** *** ADVENT OF CODE - DAY 13 - SHUTTLE SEARCH *** ***

Src: https://adventofcode.com/2020/day/13
Setting: we need to get the first bus that arrives according to its schedule (input)
Challenge: find out how long we need to wait for the first bus arrives 

Input: input.txt, a .txt file containing your notes on the bus schedule

e.g.

939
7,13,x,x,59,x,31,19

For part 1:

The first line is the earliest timestamp you could depart on a bus. 
The second line lists the bus IDs in service.
The ID number indicates how often the bus leaves for the airport:
The bus with ID 5 departs from the sea port at time 0, 5, 10, 15, etc. 
The bus with ID 11 departs at 0, 11, 22, 33, etc.
At timestamp 0, all buses depart simultaneously.
Entries that show x must be out of service.

In this example:
The earliest bus you could take is bus ID 59. 
It doesn't depart until timestamp 944, so you would need to wait 5 min. 

For part 2: 

We need to find the earliest timestamp such that the bus ID departs at the time matching the index it occurs in the list. 
This means that for the example above we are looking for the earliest timestamp t such that:

Bus ID 7 departs at timestamp t.
Bus ID 13 departs one minute after timestamp t.
There are no requirements or restrictions on departures at two or three minutes after timestamp t.
Bus ID 59 departs four minutes after timestamp t.
There are no requirements or restrictions on departures at five minutes after timestamp t.
Bus ID 31 departs six minutes after timestamp t.
Bus ID 19 departs seven minutes after timestamp t.

The challenge consists of two parts:
Part 1: What (since your arrival) will be the earliest bus ID * the minutes you'll need to wait for it?
Part 2: What is the earliest time all IDs leave at offsets matching their list-indices?

"""

import math
from sympy.ntheory.modular import crt

data_file = open('input.txt','r')
#data_file = open('test_input.txt','r')
data = data_file.read().strip().split('\n')

# *** PART 1: earliest bus ID * minutes you'll need to wait?***

print("Part 1: earliest bus ID * minutes you'll need to wait?")

arrival_time = int(data[0])
buses = data[1].split(',')
buses = [int(b) for b in buses if b not in 'x']
earliest_times = [(b, b * math.ceil(arrival_time / b)) for b in buses]
earliest_time = min(earliest_times, key=lambda x: x[1])
print(earliest_time[0] * (earliest_time[1] - arrival_time))

# solution for test_input.txt: 295
# solution for input.txt: 6559

# *** PART 2: ***

print("Part 2: ")

# Part 2 is actually a mathematical problem called the Chinese Remainder Theorem
# https://en.wikipedia.org/wiki/Chinese_remainder_theorem
# in short, it states that a system of linear congruent equations X = Ri (mod Mi), provided the moduli are pairwise co-prime, and 0 <= Ri <= Mi
# has **one** unique solution of X (mod M), where M is the product of the Mi (i.e. a unique solution that repeats itself each M cycles)

buses = data[1].split(',')
buses = [(i, int(buses[i])) for i in range(len(buses)) if buses[i] not in 'x']

# custom crt solver
# implementation derived from: https://www.youtube.com/watch?v=zIFehsBHB8o - Chinese Remainder Theorem (by Maths with Jay)
# in the theorem: 
# the bus ids are the moduli, 
# the indices are the remainders,

def inv_mod(ni, mod):

	inv = 1
	ni = ni % mod
	mod_remainder = ni % mod

	while mod_remainder != 1:

		inv += 1
		mod_remainder = (ni * inv) % mod

	return inv

def custom_crt_solver(moduli, remainders):

	N = math.prod(moduli)
	Ni = [N // m for m in moduli]
	xi = [inv_mod(Ni[i], moduli[i]) for i in range(len(moduli))]
	biNixi = [remainders[i] * Ni[i] * xi[i] for i in range(len(moduli))]
	X = sum(biNixi) % N
	return X

# our system of equations (see the CRT wiki link above) need to ALL refer to the same X
# so, our equations need to be re-written so that ALL refer to the same timestamp (the one where the bus at index 0 departs)
# this means that the other buses, *at that point in time*, are still "en route" to the bus station, and are due to arrive by i minutes
# in other words, there is a **remainder** in these buses' equation to timepoint X
# so: in order to calculate the remainders, we need to subtract the offsets/index of the bus FROM their ID/departure times/moduli

r = [m - o for (o,m) in buses] # remainders to timepoint X0 are the "departure times"/moduli - the offset/index in the list
m = [m for (o,m) in buses] # moduli (arrival times)
#r = [3,1,6] # for testing, should give 78
#m = [5,7,8] # for testing, should give 78

#timestamp = custom_crt_solver(m,r)
timestamp = crt(m,r)[0]

print(timestamp)

# solution for test_input.txt: 1068788
# solution for input.txt: 626670513163231

"""

Reflection:

- This one was difficult until I discovered it was a CRT problem. Had to research it for a while before I understood the problem.
- I then implemented my own version based on a youtube video by Maths with Jay (https://www.youtube.com/watch?v=zIFehsBHB8o) on the problem
- I still got wrong answers until I saw I had to take into account the offsets, and deduct them from the moduli to get the remainders proper
- Turns out it could also just be solved more easily by loading the correct library (sympy), as it already has a crt solver.

"""
