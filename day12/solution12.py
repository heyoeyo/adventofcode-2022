#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 08:00:47 2022

@author: eo
"""

# Solution for: https://adventofcode.com/2022/day/12

#%% Load/parse data

in_path = "input.txt"
#in_path = "test.txt"
with open(in_path, "r") as in_file:
    raw_data = in_file.read()

"""
data looks like:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

"""

# Get each row as a single string
str_rows = raw_data.strip().splitlines()

# Figure out how many rows/cols there are
NUM_ROWS = len(str_rows)
NUM_COLS = len(str_rows[0])

# Build 'grid' of characters and find start/end points
START_ROW = START_COL = END_ROW = END_COL = None
char_grid = []
for row_idx, each_str in enumerate(str_rows):
    new_row = []
    for col_idx, each_char in enumerate(each_str):
        new_row.append(each_char)
        
        # Find start/end character positions
        if each_char == "S":
            START_ROW = row_idx
            START_COL = col_idx
        if each_char == "E":
            END_ROW = row_idx
            END_COL = col_idx
    char_grid.append(new_row)

# Replace S and E character with 'a' and 'z' to avoid handling as special cases
char_grid[START_ROW][START_COL] = "a"
char_grid[END_ROW][END_COL] = "z"


#%% Part 1

'''
Idea is to do a breadth-first-search (BFS) from the starting point
until we find the ending point. The first time we find it, we'll
have the shortest path (due to BFS properties). I'm not familiar
with graph traversal stuff at all... had to look this one up!

-> BFS just means that at each point, we check/record all neighbours,
   and then repeatedly check the neighbours of those neighbours etc.
   This is opposed to depth-first-search, which would pick a single
   neighbour and try to follow it as far as possible, then reset
   and try a different neighbour as far as possible etc. until the
   shortest valid path is found
   (I tried something like this first, it was a mess!)
-> Important for BFS: we need to avoid re-checking points we've already
   visited, as well as not double-checking a single point that
   belongs to two (or more) different neighbours. Can use sets for this
'''

# For convenience. Encode the different row/col changes to move right/up/left/down (ruld)
lrud_deltas = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Initialize storage for keeping tracking of which points we've visited/need to visit next
visited_set = set()
to_be_visited_next = {(START_ROW, START_COL)}

# Loop until we find the end!
num_steps = -1
found_end = False
while not found_end:
    
    # Update state tracking
    num_steps += 1
    to_be_visited_now = to_be_visited_next.copy()
    to_be_visited_next = set()
    
    # For each point to be visited, check if we need to visit all points that are adjacent
    for each_row, each_col in to_be_visited_now:
        
        # We're done if we reach the end!
        found_end = (each_row == END_ROW) and (each_col == END_COL)
        if found_end:
            break      
        
        # Mark this point as being visited
        visited_set.add((each_row, each_col))
        
        # Check if we can visit each of the right/up/left/down directions
        curr_char = char_grid[each_row][each_col]
        for drow, dcol in lrud_deltas:
            
            # Get next position to check
            next_row = each_row + drow
            next_col = each_col + dcol
            next_pos = (next_row, next_col)
            
            # Don't check points outside of grid
            good_row = (0 <= next_row < NUM_ROWS)
            good_col = (0 <= next_col < NUM_COLS)
            outside_of_grid = (not good_row) or (not good_col)
            if outside_of_grid:
                continue
            
            # Don't process positions we've already visited
            already_visited = next_pos in visited_set
            if already_visited:
                continue
            
            # Check if we can move in this direction
            next_char = char_grid[next_row][next_col]
            is_too_high = (ord(next_char) - ord(curr_char)) > 1
            if is_too_high:
                continue            
            
            # If we get here, we found a new point that needs to be visited
            to_be_visited_next.add(next_pos)
        
        pass    
    pass


print("Solution 1:", num_steps)


#%% Part 2

# Initialize storage for keeping tracking of which points we've visited/need to visit next
visited_set = set()
to_be_visited_next = {(END_ROW, END_COL)}

# Work backwards from the ending point, until we find a point with elevation "a"
num_steps = -1
found_start = False
while not found_start:
    
    # Update state tracking
    num_steps += 1
    to_be_visited_now = to_be_visited_next.copy()
    to_be_visited_next = set()
    
    # For each point to be visited, check if we need to visit all points that are adjacent
    for each_row, each_col in to_be_visited_now:
        
        # We're done if we reach the end!
        curr_char = char_grid[each_row][each_col]
        found_start = (curr_char == "a")
        if found_start:
            break
        
        # Mark this point as being visited
        visited_set.add((each_row, each_col))
        
        # Check if we can visit each of the right/up/left/down directions
        for drow, dcol in lrud_deltas:
            
            # Get next position to check
            next_row = each_row + drow
            next_col = each_col + dcol
            next_pos = (next_row, next_col)
            
            # Don't check points outside of grid
            good_row = (0 <= next_row < NUM_ROWS)
            good_col = (0 <= next_col < NUM_COLS)
            outside_of_grid = (not good_row) or (not good_col)
            if outside_of_grid:
                continue
            
            # Don't process positions we've already visited
            already_visited = next_pos in visited_set
            if already_visited:
                continue
            
            # Check if we would be able to move in this direction (if going in reverse)
            next_char = char_grid[next_row][next_col]
            reverse_would_be_too_high = (ord(curr_char) - ord(next_char)) > 1
            if reverse_would_be_too_high:
                continue            
            
            # If we get here, we found a new point that needs to be visited
            to_be_visited_next.add(next_pos)
        
        pass    
    pass

print("Solution 2:", num_steps)

