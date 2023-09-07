"""
*** *** ADVENT OF CODE - DAY 11 - SEATING SYSTEMS *** ***

Src: https://adventofcode.com/2020/day/11
Setting: we want to choose the best seat on the ferry; so, we need to model the way people choose their seats
Challenge: from a map of the layout of the ferry, apply the seating rules people use to find the final, stable situation

Input: input.txt, a .txt file containing a map of the layout of the ferry

e.g.

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL

Where . is NOT a seat, and can't be filled
Where L is an EMPTY seat
Where # is a TAKEN seat.

Update rules for part 1:

If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied (#).
If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty (L).
Otherwise, the seat's state does not change (L stays L, # stays #).

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##

After a second round, the seats with four or more occupied adjacent seats become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##

This process continues for three more rounds, after which the situation stabilizes and no more seats change state. Then, you count 37 occupied seats.

Update rules for part 2:

Now, we don't look at the square neighborhood, but we 'look ahead' to the FIRST chair we see in each of our 9 looking directions (N/E/S/W/etc.).
Now, if a seat is occupied (#) and FIVE or more seats in its line of sight to it are also occupied, the seat becomes empty (L).

The challenge consists of two parts:
Part 1: How many seats end up occupied after applying the neighborhood seating rules until the state doesn't change anymore?
Part 2: How many seats end up occupied after applying the line of sight seating rules until the state doesn't change anymore?

"""

import numpy as np
from numpy.lib.stride_tricks import as_strided

data_file = open('input.txt','r')
#data_file = open('test_input.txt','r')
data = data_file.read().strip().split('\n')
data = np.array([np.array([c for c in r], dtype=str) for r in data])

# *** PART 1: ***

print("Part 1: How many seats end up occupied after applying the neighborhood seating rules until the state doesn't change anymore?")

"""
Rules: 
Look at the 3x3 square neighborhood around a cell
If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
Otherwise, the seat's state does not change.
"""

def state_to_str(state):
    return '\n'.join([''.join(row) for row in state])

def update(curr_state):
    
    next_state = np.empty(curr_state.shape, dtype=str)

    curr_alive = curr_state == '#' # where in the current matrix are alive cells?
    rows = curr_state.shape[0]
    cols = curr_state.shape[1]

    for r, c in np.ndindex(curr_state.shape): # iterate over the matrix cells

        # the amount of alive neighbours are the count of all cells in a 3x3 square neighborhood (minus the cell itself)
        num_alive = np.sum(curr_alive[max(0,r-1):min(r+2,rows), max(0,c-1):min(c+2,cols)]) - (curr_alive[r,c])
        
        #print(curr_state[r-1:r+2, c-1:c+2])
        #print(curr_alive[r-1:r+2, c-1:c+2])
        #print(r,c,num_alive)

        # apply rules:  
        if curr_state[r, c] == 'L': # if cell is empty (L), and has no alive neighbors, it becomes alive, else it stays empty
            if num_alive <= 0:
                next_state[r,c] = '#'
            else:
                next_state[r,c] = 'L'
        elif curr_state[r, c] == '#': # if it's taken, and has >= 4 alive neighbors, it empties, else it stays alive
            if num_alive >= 4:
                next_state[r, c] = 'L'
            else:
                next_state[r,c] = '#' 
        elif (curr_state[r,c] == '.'): # else, if the cell is empty/there is no seat, it stays empty
            next_state[r,c] = '.'

    return next_state

def check_seats_1(data, max_iterations):

    old_data = np.zeros(data.shape)
    current_data = np.copy(data)
    iterations = 0

    while not np.all(old_data == current_data) and iterations < max_iterations:
        
        #print('\nstate at iterations:',iterations, 'with n free seats:', np.sum(current_data == '#'))
        #print(state_to_str(current_data))

        old_data = current_data.copy()
        current_data = update(current_data)
        iterations += 1

    print('\nFINAL state at iterations:',iterations, 'with n free seats:', np.sum(current_data == '#'))
    print(state_to_str(current_data))

check_seats_1(data, 20000)

# solution for test_input.txt: 37
# solution for input.txt: FINAL state at iterations: 112 with n free seats: 2438

# *** PART 2: ***

print("Part 2: How many seats are occupied after stabilizing with line-of-sight rules? ")

"""
Rules: 
Look at the 9 directions around you UNTIL you find a chair, determine how many of those are occupied
If the seat we're considering is empty (L) and there are no occupied seats in its line of sight, the seat becomes occupied.
If the seat is occupied (#) and five or more seats in its line of sight around it are also occupied, the seat becomes empty.
Otherwise, the seat's state does not change.
"""

def get_visible_seats(curr_state, r, c):

    visible_seats = []
    directions = [(0,-1), (0,1), (1,0), (-1,0), (-1,1), (1,-1), (1,1), (-1,-1)] # West, East, North, South, SW, NE, NW, SE

    nrows = curr_state.shape[0]
    ncols = curr_state.shape[1]

    for d in directions:

        current_row = r + d[0]
        current_col = c + d[1]

        found_chair = False

        # while we haven't seen a chair yet, 'look' one seat further in the current direction
        while not found_chair and 0 <= current_row < nrows and 0 <= current_col < ncols:

            if curr_state[current_row, current_col] != '.': # if where we're looking isn't empty,

                visible_seats.append(curr_state[current_row, current_col]) # we found a chair, and append its VALUE to the list
                found_chair = True

            current_row += d[0]
            current_col += d[1]

    return np.array(visible_seats)

def update2(curr_state):
    
    nxt = np.empty(curr_state.shape, dtype=str)

    curr_alive = curr_state == '#'
    rows = curr_state.shape[0]
    cols = curr_state.shape[1]

    for r, c in np.ndindex(curr_state.shape):

        num_alive = sum(get_visible_seats(curr_state, r, c) == '#') # find how many seats are taken in our view
        
        #print(curr_state[r-1:r+2, c-1:c+2])
        #print(curr_alive[r-1:r+2, c-1:c+2])
        #print(r,c,num_alive)

        if curr_state[r, c] == 'L':
            if num_alive <= 0:
                nxt[r,c] = '#'
            else:
                nxt[r,c] = 'L'
        elif curr_state[r, c] == '#':
            if num_alive >= 5:
                nxt[r, c] = 'L'
            else:
                nxt[r,c] = '#'
        elif (curr_state[r,c] == '.'):
            nxt[r,c] = '.'

    return nxt

def check_seats_2(data, max_iterations):

    old_data = np.zeros(data.shape)
    current_data = np.copy(data)
    iterations = 0

    while not np.all(old_data == current_data) and iterations < max_iterations:
        
        #print('\nstate at iterations:',iterations, 'with n free seats:', np.sum(current_data == '#'))
        #print(state_to_str(current_data))

        old_data = current_data.copy()
        current_data = update2(current_data)
        iterations += 1

    print('\nFINAL state at iterations:',iterations, 'with n free seats:', np.sum(current_data == '#'))
    print(state_to_str(current_data))

check_seats_2(data, 20000)

# solution to test_input.txt: FINAL state at iterations: 88 with n free seats: 26
# solution to input.txt: FINAL state at iterations: 88 with n free seats: 2174

"""

Reflection:

- Conway's Game of Life's always fun.
- Had difficulty with numpy slicing, as I tried to not correct negative indices at first
- This obviously didn't work so I changed it to a min/max check, clamping it to 0 or the matrix length/width

"""
