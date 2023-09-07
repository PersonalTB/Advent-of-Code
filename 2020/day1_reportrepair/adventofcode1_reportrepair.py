"""
*** *** ADVENT OF CODE - DAY 1 - REPORT REPAIR *** ***

Src: https://adventofcode.com/2020/day/1
Setting: we need to fix our expenses report (our input data), something "isn't adding up" (for whatever reason)
Challenge: find the entries that sum up to 2020, and multiply these together.

Input: input.txt, a .txt file, with our expenses listed, each newline being one item's price

e.g.
1544
1560
1947
(etc.)

The assignment has two parts:
Part 1 wants us to find the 2 entries that sum to 2020, 
Part 2 wants us to find 3 entries that sum to 2020.

"""

import itertools
from operator import mul
from functools import reduce
import numpy as np
import pandas as pd

expenses_list = pd.read_csv("input.txt", names = ['numbers'])

def get_mult_for_sum_total_in_expenses_list(expenses_list, n, sum_total):
	# possibly inefficient implementation

	# get all n-wise combinations of the expenses
	perms = list(itertools.combinations(expenses_list, n))

	# a solution is defined when all elements of the permutation sum to the sum_total
	solutions = []

	# for all permutation, see if the sum of the elements is equal to the sum_total
	# we want to find as a solution to our problem the PRODUCT / MULTIPLICATION of these elements together
	# if we have found this solution, and we haven't already found this solution before, we add it to the solutions list
	for p in perms:

		# sum up all the elements, and if it equals the sum_total, we have found a solution
		sum_expenses = np.sum(p)
		if sum_expenses == sum_total:
			# for found solutions, multiply its elements
			mult_expenses = np.prod(p)
			# store it in the solutions array
			solutions.append((p, mult_expenses))

	return solutions

# *** PART 1 - Find the two entries that sum to 2020; what do you get if you multiply them together? ***

print("PART 1: Find the two entries that sum to 2020; what do you get if you multiply them together?" )

n = 2
sum_total = 2020
solutions = get_mult_for_sum_total_in_expenses_list(expenses_list.numbers, n, sum_total)
for sol in solutions: 
	print(sol)

# solution: ([704, 1316], 926464)

# *** PART 2 - what is the product of the three entries that sum to 2020? ***

print("\nPART 2: what is the product of the three entries that sum to 2020?" )

n = 3
solutions = get_mult_for_sum_total_in_expenses_list(expenses_list.numbers, n, sum_total)
for sol in solutions: 
	print(sol)

# solution: ([69, 968, 983], 65656536)

"""

Reflection:

- originally used the permutation function to generate all combinations, then I sorted these, and kept track of already-checked permutations
- this solved duplicate checking and storing of solutions, but the generation of duplicates still felt unnecessary
- switched to the combinations function

"""
