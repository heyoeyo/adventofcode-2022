#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 08:47:04 2022

@author: eo
"""

# Solution for: https://adventofcode.com/2022/day/9

#%% Load/parse data

in_path = "input.txt"
#in_path = "test.txt"
#in_path = "test2.txt"
with open(in_path, "r") as in_file:
    raw_data = in_file.read()

"""
data looks like:

R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2

"""

# Get step instructions in terms of a list of (letter, integer) pair
str_rows = raw_data.strip().splitlines()
str_pairs_list = [each_row.split(" ") for each_row in str_rows]
dir_steps_list = [(dir_letter, int(steps_str)) for dir_letter, steps_str in str_pairs_list]


#%% Helpers

def follow_knot(target_knot_xys):
    
    result_xys = []
    for targ_x, targ_y in target_knot_xys:
        
        # Figure out how far away we are from target
        prev_x, prev_y = result_xys[-1] if len(result_xys) > 0 else (0, 0)
        delta_x = targ_x - prev_x
        delta_y = targ_y - prev_y

        # Find amount of change and direction, used to figure out diagonals/movement requirements        
        mag_x, sign_x = abs(delta_x), -1 if delta_x < 0 else +1
        mag_y, sign_y = abs(delta_y), -1 if delta_y < 0 else +1
        
        # Decide if we need to move
        need_to_move = (mag_x > 1) or (mag_y > 1)
        is_diag = (mag_x + mag_y) > 2
        
        # Handle stepping towards target, if needed
        x_step, y_step = 0, 0
        if is_diag:
            x_step = sign_x
            y_step = sign_y
        elif need_to_move:
            x_step = sign_x if (mag_x > 0) else 0
            y_step = sign_y if (mag_y > 0) else 0
        
        # Record next position
        new_xy = [prev_x + x_step, prev_y + y_step]
        result_xys.append(new_xy)
    
    return result_xys


#%% Generate full sequence of (x,y) coordinates of head

# Expand out step instructions to a full list of every (x,y) position visited by head
head_xys = [(0, 0)]
for letter, steps in dir_steps_list:
    
    # Determine stepping axis and +/- direction
    x_step_size = 1 if letter in {"R", "L"} else 0
    y_step_size = 1 if letter in {"U", "D"} else 0
    step_sign = +1 if letter in {"R", "U"} else -1
    
    # Iterate position, accord to stepping instructions
    prev_x, prev_y = head_xys[-1]
    for k in range(steps):
        x_step = step_sign * x_step_size * (k + 1)
        y_step = step_sign * y_step_size * (k + 1)
        new_xy = [prev_x + x_step, prev_y + y_step]
        head_xys.append(new_xy)
    
    pass


#%% Part 1

# Run following logic on head of rope to get full sequence of (x, y) visited by tail (includes duplicates!)
tail_xys = follow_knot(head_xys)

# Build a set of xy pairs as strings to find all unique co-ords. visted by the tail
unique_tail_xys = {"{},{}".format(x, y) for x, y in tail_xys}

num_unique_tail_xys = len(unique_tail_xys)
print("Solution 1:", num_unique_tail_xys)


#%% Part 2

# Initialize space for holding the 9 tailing knots, have first knot follow the head of the rope
knot_xys = [None for _ in range(9)]
knot_xys[0] = follow_knot(head_xys)

# Run follow logic on each consecutive knot pair, as in head-tail pairing from part 1
head_idx_list = list(range(9))
tail_idx_list = head_idx_list[1:]
for tail_idx, head_idx in zip(tail_idx_list, head_idx_list):
    knot_xys[tail_idx] = follow_knot(knot_xys[head_idx])

# Same as part one, find unique xy co-ords. for only the last knot
last_knot_xys = knot_xys[-1]
unique_last_knot_xys = {"{},{}".format(x, y) for x, y in last_knot_xys}

num_unique_last_knot_xys = len(unique_last_knot_xys)
print("Solution 2:", num_unique_last_knot_xys)

