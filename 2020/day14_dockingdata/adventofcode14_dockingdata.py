"""
*** *** ADVENT OF CODE - DAY 14 - DOCKING DATA *** ***

Src: https://adventofcode.com/2020/day/14
Setting: port has docking software incompatible with the ferry's due to a bitmask system in its initialization. 
Challenge: emulate the bitmask system to correctly initialize the docking parameters in memory

Input: input.txt, a .txt file containing the initialization program of the ferry

The initialization program (your puzzle input) can either update the bitmask or write a value to memory. 
Values and memory addresses are both 36-bit unsigned integers. 
For example, ignoring bitmasks for a moment, a line like mem[8] = 11 would write the value 11 to memory address 8.

The bitmask is always given as a string of 36 bits, 
written with the most significant bit (representing 2^35) on the left and the least significant bit (2^0, that is, the 1s bit) on the right. 

For Part 1:
The current bitmask is applied to values immediately before they are written to memory: 
- a 0 or 1 overwrites the corresponding bit in the value, 
- while an X leaves the bit in the value unchanged.

e.g.

mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0

Because of the mask, the value 11 is masked to 73, which is written to memory address 8. 
Then, the program tries to write 101 to address 7.
Finally, instead of 0, the masked value of 64 is written to address 8 instead
All memory addresses start at 0, the only two values in memory are not 0 - i.e. 101 (at address 7) and 64 (at address 8) - produce a sum of 165.

For Part 2:
Here, the mask doesn't modify the values being written at all. 
Instead, it acts as a memory address decoder. (https://www.youtube.com/watch?v=PvfhANgLrm4)
Immediately before a value is written to memory, each bit in the bitmask modifies the corresponding bit of the destination memory address like so:
- If the bitmask bit is 0, the corresponding memory address bit is unchanged.
- If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
- If the bitmask bit is X, the corresponding memory address bit is floating (floating bits will take on all possible values)

The challenge consists of two parts:
Part 1: What is the sum of all values left in memory after it completes using bitmasking?
Part 2: What is the sum of all values left in memory after it completes using the memory address decoder method?

"""

import re

data_file = open('input.txt','r')
#data_file = open('test_input.txt','r')
#data_file = open('test_input2.txt','r')
data = data_file.read().strip().split('\n')

# *** PART 1: What is the sum of all values left in memory after it completes using bitmasking? ***

print("Part 1: What is the sum of all values left in memory after it completes using bitmasking?")

# https://stackoverflow.com/questions/12173774/how-to-modify-bits-in-an-integer
def set_bit(v, index, x):
	"""Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
	mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
	v &= ~mask          # Clear the bit indicated by the mask (if x is False)
	if x:
		v |= mask         # If x was True, set the bit indicated by the mask.
	return v            # Return the result, we're done.

def apply_mask(mask, num):
	bits = num
	mask = list(reversed(mask))
	for i in range(len(mask)):
		if mask[i] not in 'X':
			bits = set_bit(bits, i, int(mask[i]))
	return bits

mask = ''
mem = dict()

for d in data:
	mem_match = re.match('mem\[([0-9]+)\] = ([0-9]+)', d)
	mask_match = re.match('mask = ([01X]+)', d)

	if mask_match:
		#print(mask_match.group(1))
		mask = mask_match.group(1)
	elif mem_match:
		#print(int(mem_match.group(1)), bin(int(mem_match.group(2))))
		mem[int(mem_match.group(1))] = apply_mask(mask, int(mem_match.group(2)))

print(sum(mem.values()))

# solution for test_input.txt: 165
# solution for input.txt: 17934269678453

# *** PART 2: What is the sum of all values left in memory after it completes using the memory address decoder method? ***

print("Part 2: What is the sum of all values left in memory after it completes using the memory address decoder method?")

def write_to_mask_memory_floating(mem, address, floating, value):

	if len(floating) == 0:
		mem[address] = value

	else:

		current_floating = floating.copy()
		at = current_floating.pop()

		address = set_bit(address, at, 0)
		mem = write_to_mask_memory_floating(mem, address, current_floating, value)

		address = set_bit(address, at, 1)
		mem = write_to_mask_memory_floating(mem, address, current_floating, value)

	return mem

def write_to_mask_memory(mem, mask, address, value):

	mask = list(reversed(mask))
	floating = []
	
	for i in range(len(mask)):
		if mask[i] in 'X':
			floating.append(i)
		elif int(mask[i]) == 1:
			address = set_bit(address, i, 1)

	return write_to_mask_memory_floating(mem, address, floating, value)

mask = ''
mem = dict()

for d in data:
	mem_match = re.match('mem\[([0-9]+)\] = ([0-9]+)', d)
	mask_match = re.match('mask = ([01X]+)', d)

	if mask_match:
		mask = mask_match.group(1)
	elif mem_match:
		mem = write_to_mask_memory(mem, mask, int(mem_match.group(1)), int(mem_match.group(2)))

print(sum(mem.values()))

# solution for test_input2.txt: 208
# solution for input.txt: 3440662844064

"""

REFLECTION:

- when recursing and altering a list, pass COPIES of the list in the recursing call! lists are altered by reference, not by value.
- feel like it can be done more efficient, considering it's binary arithmetic, this should be simpler

"""
