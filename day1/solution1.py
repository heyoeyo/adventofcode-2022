#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 15:46:08 2022

@author: eo
"""

# Solution for: https://adventofcode.com/2022/day/1

#%% Load data

with open("input.txt", "r") as in_file:
    raw_data = in_file.read()
    
"""
data looks like:

9524
12618
6755

4029
11446

6226
9901
6735

etc.

"""


#%% Part 1

# Get each grouping of calories per elf
# -> Gives something like: ['9524\n12618\n6755', '4029\n11446', '6226\n9901\n6735', etc.]
strs_per_elf = raw_data.split("\n\n")

# Convert each elf's calorie listing to number and total them
calories_per_elf = []
totals_per_elf = []
for each_elf_str in strs_per_elf:
    
    # For each elf, get integer version of each calorie entry & sum them for part 1 answer
    elf_calories_list = [int(each_str) for each_str in each_elf_str.splitlines()]
    total_calories = sum(elf_calories_list)
    
    calories_per_elf.append(elf_calories_list)
    totals_per_elf.append(total_calories)
    
    
max_calories = max(totals_per_elf)
print("Solution 1:", max_calories)


#%% Part 2

# Grab sum of top-3 elf totals for part 2 answer
sorted_calories = sorted(totals_per_elf, reverse = True)
top_3_total = sum(sorted_calories[0:3])
print("Solution 2:", top_3_total)
