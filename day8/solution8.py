#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 07:58:09 2022

@author: eo
"""

# Solution for: https://adventofcode.com/2022/day/8

#%% Load/parse data

in_path = "input.txt"
#in_path = "test.txt"
with open(in_path, "r") as in_file:
    raw_data = in_file.read()

"""
data looks like:

30373
25512
65332
33549
35390

"""

# Get data into a list-of-lists 'matrix' format, for easier use
row_data = raw_data.strip().splitlines()
matrix_data = []
for each_row_str in row_data:
    row_as_numbers = [int(each_char) for each_char in each_row_str]
    matrix_data.append(row_as_numbers)


#%% Helpers

# .....................................................................................................................

def get_max_map_leftright(matrix, left_to_right = True):
    
    # Flip the matrix if needed
    check_matrix = matrix
    if not left_to_right:
        check_matrix = [list(reversed(each_row)) for each_row in check_matrix]
    
    # Check for max-values going left-to-right (we flip the matrix to handle other direction)
    max_map = []
    for row_idx, each_row in enumerate(check_matrix):
        
        new_max_row = []
        for col_idx, cell_value in enumerate(each_row):
            
            new_max = -1
            left_col_idx = (col_idx - 1)            
            if left_col_idx >= 0:
                prev_max = new_max_row[left_col_idx]
                prev_cell = each_row[left_col_idx]
                new_max = max(prev_cell, prev_max)
            
            new_max_row.append(new_max)        
        max_map.append(new_max_row)
    
    # Un-flip our results if needed
    if not left_to_right:
        max_map = [list(reversed(each_row)) for each_row in max_map]
    
    return max_map

# .....................................................................................................................

def get_max_map_topbot(matrix, top_to_bottom = True):
    
    # Transpose matrix, so we can use existing left-to-right check (equiv. to top-to-bottom check)
    transposed_matrix = list(zip(*matrix))
    transposed_max_map = get_max_map_leftright(transposed_matrix, top_to_bottom)
    
    # Un-transpose to get back original    
    return list(zip(*transposed_max_map))

# .....................................................................................................................

def get_scenic_score_left_right(matrix, check_horizontally = True):
    
    check_matrix = matrix
    if not check_horizontally:
        check_matrix = list(zip(*matrix))
    
    # Initialize empty outputs
    left_score_matrix = []
    right_score_matrix = []
    
    # Process each row of the input matrix
    for row_idx, each_row in enumerate(check_matrix):
        
        # Initialize storage for scores along the current row
        left_score_row = []
        right_score_row = []
        
        # Within each row, search 'away' from cell entries to find first instances of values >= cell value
        for col_idx, cell_value in enumerate(each_row):
            
            # Get list of values to the left/right of the current cell
            left_of_list = each_row[:col_idx]
            right_of_list = each_row[(1+col_idx):]
            
            # Check how far left we can go before hitting an equal/greater value (i.e. tall tree)
            left_idx = -1
            for left_idx, each_left_value in enumerate(reversed(left_of_list)):
                if each_left_value >= cell_value:
                    break
            left_score_row.append(1 + left_idx)
            
            # Check how far right we can go
            right_idx = -1
            for right_idx, each_right_value in enumerate(right_of_list):
                if each_right_value >= cell_value:
                    break
            right_score_row.append(1 + right_idx)
        
        # Record scoring, row-by-row to build up final matrix values
        left_score_matrix.append(left_score_row)
        right_score_matrix.append(right_score_row)

    # Flip outputs if needed
    # -> If flipped, the 'left' matrix is equivalent to an 'up' matrix and same idea for 'right'/'down'
    if not check_horizontally:
        left_score_matrix = list(zip(*left_score_matrix))
        right_score_matrix = list(zip(*right_score_matrix))

    return left_score_matrix, right_score_matrix


#%% Pre-calculate max-maps

# Find matrices whose entries indicate the maximum value when travelling a center direction, from each cell
# -> For example, each entry of the 'max_to_right' matrix indicates the largest value you'd see to the right
#    of a given cell in the original matrix data
max_to_right = get_max_map_leftright(matrix_data, True)
max_to_left = get_max_map_leftright(matrix_data, False)
max_to_down = get_max_map_topbot(matrix_data, True)
max_to_up = get_max_map_topbot(matrix_data, False)


#%% Part 1

num_visible_on_edge = 0
for row_idx, each_row in enumerate(matrix_data):    
    for col_idx, cell_value in enumerate(each_row):
        
        # Use-precalculated max value maps to determine if the current cell value is the largest along each direction
        vis_on_right = cell_value > max_to_right[row_idx][col_idx]
        vis_on_left = cell_value > max_to_left[row_idx][col_idx]
        vis_on_down = cell_value > max_to_down[row_idx][col_idx]
        vis_on_up = cell_value > max_to_up[row_idx][col_idx]
        
        # Count every entry which has visibilty along any of the edges
        vis_on_edge = any((vis_on_right, vis_on_left, vis_on_down, vis_on_up))
        num_visible_on_edge += int(vis_on_edge)
    pass

print("Solution 1:", num_visible_on_edge)


#%% Part 2

# Calculate scenic scoring for left/right/up/down directions ahead of time
left_scores, right_scores = get_scenic_score_left_right(matrix_data, True)
up_scores, down_scores = get_scenic_score_left_right(matrix_data, False)
lrud_matrices = zip(left_scores, right_scores, up_scores, down_scores)

# Calculate scenic scoring for each cell and record highest value
highest_idx_debug = [None, None]
highest_score = 0
for row_idx, lrud_rows in enumerate(lrud_matrices):
    for col_idx, (l, r, u, d) in enumerate(zip(*lrud_rows)):        
        cell_score = l * r * u * d
        if cell_score > highest_score:
            highest_score = cell_score
            highest_idx_debug = [row_idx, col_idx]
        pass
    pass

print("Solution 2:", highest_score)

