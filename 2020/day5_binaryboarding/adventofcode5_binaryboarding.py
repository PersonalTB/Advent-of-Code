"""
*** *** ADVENT OF CODE - DAY 5 - BINARY BOARDING *** ***

Src: https://adventofcode.com/2020/day/5
Setting: we're boarding an airplane, but have forgotten our pass. We scan surrounding passes and try to find our seat by process of elimination.
Challenge: find our free seat based on which seats are already taken (given by the input), where each seat is coded by binary space partitioning.

Input: a .txt file with for each new line, a seat number coded through binary space partitioning (see: https://www.youtube.com/watch?v=oAHbLRjF0vo )

e.g. 
FBBFBBBRLR
BFFBBFFLLL
BFFBBBBRRR
BBBFBBFRLL
(etc.)

There are 128 rows on the plane, numbered 0 through 127, and 8 columns (numbered 0 through 7)
A seat is specified by 10 letters, where the first 7 are F or B (meaning "front" and "back"), and the last 3 are L or R ("left" or "right").
Each F and B letter tells you which half of rows your seat is in for a given region, with F being the lower half and B the upper half.
Each L and R letter tells you which half of columns your seat is in for a given region, with L being the lower half and R being the upper half.
Example for columns: 1st letter L means column 0 through 3; then a second letter R means col 2 through 3; then a third letter L means col 2.
Example for rows: 1st letter F means row 0 through 63; if the second letter is then B, that means the seat is in row 32 through 63, etc.

Every seat also has a unique seat ID: multiply the row by 8, then add the column.
So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5, with seat ID 44 * 8 + 5 = 357.

The challenge is made up of 2 parts:
Part 1 - What is the highest seat ID on a boarding pass?
Part 2 - find the seat id of the only seat left on the flight (that has id's +1 and -1 in the input)

"""

data_file = open('input.txt', 'r')
data = data_file.read()
split_data = data.strip().split('\n')

# *** PART 1 - What is the highest seat ID on a boarding pass? ***

print('PART 1: What is the highest seat ID on a boarding pass?')

def decode_boarding_pass_binary(bp):

	len_bp = len(bp)
	first_lr = bp.find(next(i for i in bp if i == 'L' or i == 'R')) # find the index where the string goes from front/back to left/right coding

	rows = bp[0:first_lr]
	cols = bp[first_lr:len_bp]

	rows = rows.replace('F','0').replace('B','1') # change to binary string representation
	cols = cols.replace('L','0').replace('R','1')

	current_row = int(rows,2) # decode binary string to int representation
	current_col = int(cols,2)

	return (bp, current_row, current_col, current_row * 8 + current_col)

boarding_pass_data = [decode_boarding_pass_binary(bp) for bp in split_data]
boarding_pass_data.sort(reverse = True, key = lambda x: x[3])

print(boarding_pass_data[0])

# solution: ('BBBFBBBRRR', 119.0, 7.0, 959.0), so: the highest seat id is 959

# *** PART 2 - find the seat id of the only seat left on the flight (that has id's +1 and -1 in the input)  ***

"""
It's a completely full flight, so your seat should be the only missing boarding pass in your list. 
However, there's a catch: some of the seats at the very front and back of the plane don't exist on this "plane", so they'll be missing from your list too.
Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.

So: find the missing seat id that has id+1 and id-1 in the input list
"""

print('\nPART 2: What is the ID of your seat?')

n_rows = 128
n_cols = 8

seat_ids = [bp[3] for bp in boarding_pass_data]

empty_seats = []

for current_row in range(n_rows):
	for current_col in range(n_cols):
		seat_id = current_row * 8 + current_col
		if not seat_id in seat_ids and seat_id+1 in seat_ids and seat_id-1 in seat_ids:
			empty_seats.append((current_row, current_col,seat_id))

print(empty_seats)

# solution: [(65, 7, 527)], so the seat at row 65, col 7, and seat id 527

"""

Reflection:

- originally implemented the function decode_boarding_pass that manually calculated the binary partitioning 
- then, I changed it to the the binary decoding function to do it without the manual calculation, I like this one more

"""
