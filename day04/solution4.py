#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 09:28:52 2022

@author: eo
"""

# Solution for: https://adventofcode.com/2022/day/4

#%% Load data

in_path = "input.txt"
#in_path = "test.txt"
with open(in_path, "r") as in_file:
    raw_data = in_file.read()

"""
data looks like:

1-2,2-96
17-75,14-75
33-92,93-93
18-18,18-83
14-30,15-30
6-92,6-6
15-16,15-90
etc.

"""


#%% Part 1

# Get each "a1-a2,b1-b2" pair (i.e. separate rows)
strs_per_pair = raw_data.strip().splitlines()

# Check how many times one pair full covers another
full_overlap_count = 0
for each_line in strs_per_pair:
    
    # Get start/end of each pair as integers
    rangeA, rangeB = each_line.split(",")
    a1, a2 = [int(each_str) for each_str in rangeA.split("-")]
    b1, b2 = [int(each_str) for each_str in rangeB.split("-")]
    
    # Check for full overlap conditions
    a_covers_b = (a1 <= b1) and (a2 >= b2)
    b_covers_a = (b1 <= a1) and (b2 >= a2)
    if a_covers_b or b_covers_a:
        full_overlap_count += 1

print("Solution 1:", full_overlap_count)


#%% Part 2


# Check how many times there is any amount of overlap
any_overlap_count = 0
for each_line in strs_per_pair:
    
    # Get start/end of each pair as integers
    rangeA, rangeB = each_line.split(",")
    a1, a2 = [int(each_str) for each_str in rangeA.split("-")]
    b1, b2 = [int(each_str) for each_str in rangeB.split("-")]
    
    # Avoid counting if there is NO overlap
    a_ends_before_b = a2 < b1
    b_ends_before_a = b2 < a1
    if a_ends_before_b or b_ends_before_a:
        continue
    
    any_overlap_count += 1
    

print("Solution 2:", any_overlap_count)
