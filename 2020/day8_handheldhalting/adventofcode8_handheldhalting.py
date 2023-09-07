"""
*** *** ADVENT OF CODE - DAY 8 - HANDHELD HALTING *** ***

Src: https://adventofcode.com/2020/day/8
Setting: a game console won't turn on. We need to debug it.
Challenge: find the infinite loop in the instructions of the boot code (input)

Input: input.txt, a .txt file with the boot instructions, with one instruction per line.

e.g.

nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
(etc.)

Where nop does No Operation, acc alters the accumulator value with the specified value, jmp jumps the specified number of instructions back/forward

The challenge consists of 2 parts.
Part 1: Immediately before any instruction is executed a second time (i.e. before the loop is entered), what value is in the accumulator?
Part 2: Fix the program so it terminates normally. What is the value of the accumulator after the program terminates?

"""

import re # regex, to match and group instructions

# decode the instruction from a string to an (operator, value) tuple
def decode_instruction(instr):

	match = re.search('([nopacjmp]+) ([+-])([0-9]+)', instr)

	operator = match.group(1)
	modifier = (1 if match.group(2) == '+' else -1)
	value = int(match.group(3)) * modifier 

	return (operator, value)

input_data = open('input.txt','r').read().strip() # read the input data, strip trailing whitespace and newlines
operations = input_data.split('\n') # split into a list of individual operations strings
operations = [decode_instruction(op) for op in operations] # decode the operations list to a list of (operator,value) tuples

# *** Part 1: Immediately before any instruction is executed a second time, what value is in the accumulator? ***

print('PART 1: ')

# execute one single instruction for a given line and accumulator value; return the resultant line and accumulator values
def do_operator(instr, line, accumulator):
	(operator, value) = instr
	if operator == 'nop':
		line += 1
	elif operator == 'acc':
		accumulator += value
		line += 1
	elif operator == 'jmp':
		line += value
	return line, accumulator

# runs a set of instructions from the beginning until either done (finished the instructions and reached the bottom), or error (infinite loop)
# returns the final line and accumulator before stopping, and whether we finished the instructions (done) or we entered an infinite loop (error)
def run_instructions(operations):

	accumulator = 0
	line = 0
	checked = []
	done = False
	error = False

	# continue running if we haven't already finished, and we haven't encountered an infinite loop
	while not done and not error:

		# if we are at the end of the instruction list, we have successfully completed the boot
		if line == len(operations):
			done = True
			break

		# if we already encountered this instruction line, we are in an infinite loop
		elif line in checked:
			error = True
			break

		# remember which lines we already checked out so we can detect if we are entering a loop in the instructions
		checked.append(line)

		# execute the operator
		line, accumulator = do_operator(operations[line], line, accumulator)

	return line, accumulator, done, error

line, accumulator, done, error = run_instructions(operations)

if error:
	print('error! acc:', accumulator)
else:
	print('completed normally with acc:', accumulator)

# solution: 1859

# *** PART 2: Fix the program so it terminates normally. What is the value of the accumulator after the program terminates? ***

# Rules: 
# (1) we can only change exactly one jmp (to nop) or nop (to jmp)
# (2) normal termination is when it reaches and completes the final instruction

print('PART 2: ')

changeable = [i for i in range(len(operations)) if operations[i][0] in ['jmp', 'nop']] # find all changeable lines according to our rules
changed = [] # to remember which lines we already tried to change
done = False # whether we exited normally

# while we haven't fixed and run the instructions successfully yet, or if we've tried all the changeable lines and still have an error
while not done or (len(changeable) == 0 and error):

	# run the current set of instructions
	line, accumulator, done, error = run_instructions(operations)

	# if we entered an infinite loop in our run
	if error: 

		# if we already changed something, change it back
		if len(changed) > 0:
			instr = operations[changed[-1]] # get the instruction we changed previously
			instr = ('nop' if instr[0] == 'jmp' else 'jmp', instr[1]) # switch back nop and jmp values as per the rules
			operations[changed[-1]] = instr # put the reverted instruction back into the instruction set

		# change something that we haven't already tried before
		change_ind = changeable.pop() # get the next changeable instruction
		instr = operations[change_ind] 
		instr = ('nop' if instr[0] == 'jmp' else 'jmp', instr[1]) # switch nop and jmp values as per the rules
		operations[change_ind] = instr # put the changed instruction back into the instruction set
		changed.append(change_ind) # remember the instruction we changed

if not done and len(changeable) == 0: # if we didn't exit formally, and we can't try to change anything anymore, the code is unfixable
	print('unfixable! acc:', accumulator)
elif done and len(changed) > 0: # else if we changed something and we exited normally, the code is fixed
	print('fixed! completed normally with acc', accumulator, 'after having changed line', changed[-1], 'to', operations[changed[-1]])
else: # else, we exited normally and our code was functional from the beginning
	print('completed normally with acc', accumulator)

# solution: 1235

"""

Reflection:

- fun!

"""
