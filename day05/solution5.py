#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 08:01:26 2022

@author: eo
"""

# Solution for: https://adventofcode.com/2022/day/5

#%% Load/parse data

in_path = "input.txt"
#in_path = "test.txt"
with open(in_path, "r") as in_file:
    raw_data = in_file.read()

"""
data looks like:

    [V] [G]             [H]        
[Z] [H] [Z]         [T] [S]        
[P] [D] [F]         [B] [V] [Q]    
[B] [M] [V] [N]     [F] [D] [N]    
[Q] [Q] [D] [F]     [Z] [Z] [P] [M]
[M] [Z] [R] [D] [Q] [V] [T] [F] [R]
[D] [L] [H] [G] [F] [Q] [M] [G] [W]
[N] [C] [Q] [H] [N] [D] [Q] [M] [B]
 1   2   3   4   5   6   7   8   9 

move 3 from 2 to 5
move 2 from 9 to 6
move 4 from 7 to 1
etc.
"""

# Separate input data into the stack state & instructions
raw_split = raw_data.split("\n\n")
raw_stack_strs, instr_str = raw_split[0:2]

# Transpose stack strings
# Strings now look like: (" ", "N", "Z", "1")
# -> i.e. each column of the original string is now a row
# -> the original brackets + spacing ensures everything is neatly aligned
# -> Entries are ordered top-to-bottom (i.e. left-most entry is on top of the stack)
stack_strs_transpose = list(zip(*raw_stack_strs.splitlines()))

# Now extract each stack as a list, with bottom most element on the left/0-index
# -> Also remove stack indexing (i.e. "1", "2", "3", etc.)
# -> Remove the empty strings from the top of the stacks (i.e. ["P"] instead of ["P", " ", " "])
stack_strs = []
for each_row in stack_strs_transpose:
    
    # Skip rows that aren't indexed (i.e. these always have " " as their right-most entry)
    is_empty = each_row[-1] == " "
    if is_empty:
        continue
    
    # Remove "1", "2", "3", etc. and empty entries and flip ordering before storing result
    list_no_idx = each_row[:-1]
    list_no_empties = [each_str for each_str in list_no_idx if len(each_str.strip()) > 0]
    list_bot_to_top = list(reversed(list_no_empties))
    stack_strs.append(list_bot_to_top)

# Separate instructions into move X from Y to Z (i.e. store X, Y and Z in separate lists)
move_inst = []
from_inst = []
to_inst = []
for each_row in instr_str.splitlines():
    
    # Parse out the move/from/to indices by repeatedly splitting on string keywords
    rem_str, to_str = each_row.split("to ")
    rem_str, from_str = rem_str.split("from ")
    rem_str, move_str = rem_str.split("move ")
    
    # Store instructions in separate (equal length!) lists
    # -> Account for 1-indexing (we'll need to use 0-indexing, so subtract the 1 here for ease of use)
    move_inst.append(int(move_str))
    from_inst.append(int(from_str) - 1)
    to_inst.append(int(to_str) - 1)


#%% Helpers

def get_top_most_letters(stack_list):
    
    topmost_letters = []
    for each_col_list in stack_list:
        topmost = each_col_list[-1]
        topmost_letters.append(topmost)
    
    return "".join(topmost_letters)


#%% Part 1

# Make copy of initial state stack
stack_state = [row.copy() for row in stack_strs]

# Perform stack pop-from, push-to instructions
for num_move, src_col_idx, dst_col_idx in zip(move_inst, from_inst, to_inst):
    for _ in range(num_move):
        top_stack = stack_state[src_col_idx].pop()
        stack_state[dst_col_idx].append(top_stack)
    pass


answer_1 = get_top_most_letters(stack_state)
print("Solution 1:", answer_1)


#%% Part 2

# Make copy of initial state stack
stack_state = [row.copy() for row in stack_strs]

# Perform stack copy-from, move-to instructions
for num_move, src_col_idx, dst_col_idx in zip(move_inst, from_inst, to_inst):
    
    # Remove top-most entries from source column
    stack_to_move = []
    for _ in range(num_move):
        top_stack = stack_state[src_col_idx].pop()
        stack_to_move.append(top_stack)
    
    # Flip entries (to account for new ordering) before appending to destination column
    stack_to_move = reversed(stack_to_move)
    stack_state[dst_col_idx].extend(stack_to_move)


answer_2 = get_top_most_letters(stack_state)
print("Solution 2:", answer_2)

