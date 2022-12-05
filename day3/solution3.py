#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 09:13:36 2022

@author: eo
"""

# Solution for: https://adventofcode.com/2022/day/3

#%% Load data

in_path = "input.txt"
#in_path = "test.txt"
with open(in_path, "r") as in_file:
    raw_data = in_file.read()
    
"""
data looks like:
    
rNZNWvMZZmDDmwqNdZrWTqhJMhhgzggBhzBJBchQzzJJ
pHlSVbVbFHgHBzzhQHqg
nVsqGpbbtDtTNmrmfZ
zrBMnbzBchshsttfbMRBgmJggmmCHGgDhDgNDGHL
VddZqQqdvSQMJHJGdCDCDDmH
pZWWllPQlPZQvZvwpSVlqlvtfswMRzBbntzRbzbfstsRzF
etc.

"""

#%% Part 1

str_per_sack = raw_data.strip().splitlines()

shared_items_per_sack = []
for each_sack_str in str_per_sack:
    
    num_items_total = len(each_sack_str)
    sack_length = num_items_total // 2
    sack_1_str = each_sack_str[:sack_length]
    sack_2_str = each_sack_str[sack_length:]
    
    shared_item = set(sack_1_str).intersection(sack_2_str).pop()
    shared_items_per_sack.append(shared_item)

def get_char_priority(char):
    
    # For clarity
    a_ord = ord("a")
    A_ord = ord("A")
    char_ord = ord(char)
    is_lowercase = (char_ord >= a_ord)
    
    # Priority scoring rules
    char_priorty = None
    if is_lowercase:
        char_priorty = char_ord - a_ord + 1
    else:
        char_priorty = char_ord - A_ord + 27
    
    return char_priorty
    
    

# Convert to priorty
priority_per_sack = []
for each_char in shared_items_per_sack:
    char_priorty = get_char_priority(each_char)    
    priority_per_sack.append(char_priorty)

total_priority = sum(priority_per_sack)
print("Solution 1:", total_priority)


#%% Part 2


strs_per_group = zip(str_per_sack[0::3], str_per_sack[1::3], str_per_sack[2::3])

shared_items_per_group = []
priority_per_group = []
for [elf1, elf2, elf3] in strs_per_group:
    
    shared_item = set(elf1).intersection(elf2).intersection(elf3).pop()
    shared_items_per_group.append(shared_item)
    

    char_priority = get_char_priority(shared_item)
    priority_per_group.append(char_priority)


total_group_priority = sum(priority_per_group)
print("Solution 2:", total_group_priority)

