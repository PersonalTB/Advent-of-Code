"""
*** *** ADVENT OF CODE - DAY 9 - Encoding Error

Src: https://adventofcode.com/2020/day/9
Setting: we connect to an open data port. The data it transmits is coded in eXchange-Masking Addition System cypher, which has a weakness we can exploit.
Challenge: find and exploit the weakness in XMAS

Input: input.txt, a .txt file with the port's data encoded in the XMAS cypher, as a series of integers, 1 per row

e.g.

35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576

XMAS starts by transmitting a preamble of 25 numbers. 
After that, each number you receive should be the sum of any two of the 25 immediately previous numbers. 
The two numbers will have different values, and there might be more than one such pair.

26 would be a valid next number, as it could be 1 plus 25 (or many other pairs, like 2 and 24).
49 would be a valid next number, as it is the sum of 24 and 25.
100 would not be valid; no two of the previous 25 numbers sum to 100.
50 would also not be valid; although 25 appears in the previous 25 numbers, the two numbers in the pair must be different.

Part 1 of the XMAS-exploit: find the number not conforming to the XMAS property

In the above example, after the 5-number preamble, almost every number is the sum of two of the previous 5 numbers; 
the only number that does not follow this rule is 127.

Part 2 of the exploit: find the contiguous set of numbers that sum to the non-XMAS number, and sum the smallest and largest of those

In this list, adding up all of the numbers from 15 through 40 produces the invalid number from step 1, 127. 
(Of course, the contiguous set of numbers in your actual list might be much longer.)
To find the encryption weakness, add together the smallest and largest number in this contiguous range; 
in this example, these are 15 and 47, producing 62.

The challenge consists of two parts:
Part 1: What is the first number that does not have this XMAS property?
Part 2: Find the encryption weakness - add together the smallest and largest of the contiguous set of numbers that sum to the non-conforming number

"""

import itertools

data_file = open('input.txt', 'r')
#data_file = open('test_input.txt', 'r')
data = data_file.read().strip().split('\n')
data = [int(d) for d in data]

preamble = 25 # for test_input.txt, use a preamble of 5, for input.txt, use a preamble of 25

# *** PART 1: What is the first number that does not have the XMAS property? ***

print('Part 1: What is the first number that does not have the "XMAS" property?')

def get_invalid_row(data, preamble, combination_size):
	for row in range(preamble, len(data)):
		if not any([sum(combi) == data[row] for combi in itertools.combinations(data[row-preamble:row], combination_size)]):
			return (row, data[row]) 

invalid_row, invalid_value = get_invalid_row(data, preamble, 2) 
print(f'invalid row: {invalid_row}, value: {invalid_value}')

# solution for test_input.txt (with preamble value being 5): invalid row: 14 value: 127
# solution for input.txt (with preamble value being 25): invalid row: 498 value: 15690279

# *** Part 2: Find the encryption weakness - add together the smallest and largest of the contiguous set of numbers that sum to the non-XMAS number ***

print('Part 2: Find the encryption weakness - add together the smallest and largest of the contiguous set of numbers that sum to the non-XMAS number')

def find_contiguous_set_for_sum(data, invalid_value):

	for starting_index in range(len(data)-1):
		ending_index = starting_index+1

		oversum = False 
		while not oversum:
			summation = sum(data[starting_index:ending_index])
			if summation == invalid_value:
				return (starting_index, ending_index), data[starting_index:ending_index]

			elif summation > invalid_value:
				oversum = True

			else:
				ending_index += 1

	return False

found_set = find_contiguous_set_for_sum(data, invalid_value)

if found_set != False:
	starting_index, ending_index = found_set[0]
	solution_range_sorted = sorted(found_set[1])
	solution = solution_range_sorted[0] + solution_range_sorted[-1]
	print(f'contiguous range from {starting_index} to {ending_index} gives range {found_set[1]} with min value {solution_range_sorted[0]} and max value {solution_range_sorted[-1]} making solution: {solution}')

# solution for test_input.txt: contiguous range from 2 to 6 gives range [15, 25, 47, 40] with min value 15 and max value 47 making solution: 62
# solution for input.txt: contiguous range from 388 to 405 gives range [778163, 791844, 769435, 781000, 803409, 849260, 825818, 990027, 870560, 947003, 948223, 931655, 966228, 916145, 1025840, 1404797, 1090872] with min value 769435 and max value 1404797 making solution: 2174232
# so: solution: 2174232

"""

Reflection:

- fun, not much else to say about it 

"""
