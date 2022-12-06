#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 09:20:46 2022

@author: eo
"""

# Solution for: https://adventofcode.com/2022/day/6

#%% Load/parse data

in_path = "input.txt"
#in_path = "test.txt"
with open(in_path, "r") as in_file:
    raw_data = in_file.read()

"""
data looks like:

mjqjpqmgbljsphdztnvjfqwrcgsmlb etc.

"""

# Grab each input code, for handling test inputs (we treat regular input as 1 and only 1 input)
sep_inputs = raw_data.splitlines()


#%% Helpers

def find_num_chars_until_unique_seq(n_char_sequences_list):
    
    num_chars_read = None
    for read_start_idx, char_seq in enumerate(n_char_sequences_list):

        # Get number of (potentially non-unique) characters in the sequence & number of unique characters
        num_chars = len(char_seq)
        num_unique = len(set(char_seq))

        # Stop searching when sequence is all unique characters
        is_all_unique = (num_chars == num_unique)
        if is_all_unique:
            num_chars_read = read_start_idx + num_chars
            break
    
    return num_chars_read


#%% Part 1

num_chars_packet_list = []
for each_input in sep_inputs:
    
    # Get a 'sliding window' of 4 characters from the input
    four_char_seq_list = zip(each_input[0:], each_input[1:], each_input[2:], each_input[3:])
    
    # Keep reading characters until we find a unique sequence
    num_read_4 = find_num_chars_until_unique_seq(four_char_seq_list)
    num_chars_packet_list.append(num_read_4)

print("Solution 1:", num_chars_packet_list)


#%% Part 2

num_chars_msg_list = []
for each_input in sep_inputs:
    
    # Sliding window, like part 1, but programmatically generated now
    fourteen_char_seq_list = zip(*(each_input[s:] for s in range(14)))
    
    # Like part one, read sequence until we find all unique characters
    num_read_14 = find_num_chars_until_unique_seq(fourteen_char_seq_list)
    num_chars_msg_list.append(num_read_14)

print("Solution 2:", num_chars_msg_list)
