#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 08:53:22 2022

@author: eo
"""

# Solution for: https://adventofcode.com/2022/day/10

#%% Load/parse data

in_path = "input.txt"
#in_path = "test.txt"
with open(in_path, "r") as in_file:
    raw_data = in_file.read()

"""
data looks like:

addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
etc.

"""


#%% Calculate register values

str_rows = raw_data.strip().splitlines()

register_values_list = [1]
for each_str in str_rows:
    
    prev_value = register_values_list[-1]
    
    if each_str.startswith("noop"):
        new_value = prev_value
        register_values_list.append(new_value)
    else:
        _, amount_to_add_str = each_str.split(" ")
        
        new_value = prev_value + int(amount_to_add_str)
        register_values_list.append(prev_value)
        register_values_list.append(new_value)
    
    pass


#%% Part 1

# Calculate signal strength at 20 + 40*k register indexes
idx_list = [20 + 40 * k for k in range(6)]
signal_strengths_list = [idx * register_values_list[idx-1] for idx in idx_list]

answer_1 = sum(signal_strengths_list)
print("Solution 1:", answer_1)


#%% Part 2

disp_strs_list = []

# Loop over display rows & columns, we'll manually increment our register indexing
reg_idx = 0
for row_idx in range(6):
    
    # Decide what character to draw for each column
    row_strs_list = []
    for col_idx in range(40):
        
        # Check if the sprite is centered near the current column
        sprite_position = register_values_list[reg_idx]
        is_overlapped = abs(sprite_position - col_idx) < 2
        
        # Draw appropriate character, depending on sprite overlap, as given in question
        new_char = "#" if is_overlapped else "."
        row_strs_list.append(new_char)
        
        # Update indexing after check, as-per ordering given in the question
        reg_idx += 1
    
    # Concatenate all characters in the row into a single string for printing
    disp_strs_list.append("".join(row_strs_list))

answer_2 = "\n".join(disp_strs_list)
print("Solution 2:", "", answer_2, sep = "\n")

