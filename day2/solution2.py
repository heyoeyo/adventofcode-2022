#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 16:11:55 2022

@author: eo
"""

# Solution for: https://adventofcode.com/2022/day/2

#%% Load data

in_path = "input.txt"
#in_path = "test.txt"
with open(in_path, "r") as in_file:
    raw_data = in_file.read()
    
"""
data looks like:

C Y
B Z
B Z
C Y
B Y
etc.

"""

#%% Part 1

# Scoring for different choices
choice_scoring_lut = {"X": 1, "Y": 2, "Z": 3}

# Scoring for different choices, given the opponent's letter
# -> i.e. lut["A"]["Y"] is the score for responding with 'Y' given the opponent plays 'A'
outcome_scoring_lut = {
    "A": {"X": 3, "Y": 6, "Z": 0},
    "B": {"X": 0, "Y": 3, "Z": 6},
    "C": {"X": 6, "Y": 0, "Z": 3},
}

# Get letter pairs for each round (i.e. each row of raw data)
str_per_round = raw_data.splitlines()

scores_per_round_list = []
for each_round_str in str_per_round:
    
    # Ignore empty lines
    if each_round_str == "":
        continue
    
    # Calculate scoring based on opponent letter and our response letter
    [opp_letter, resp_letter] = each_round_str.split(" ")
    choice_score = choice_scoring_lut[resp_letter]
    outcome_score = outcome_scoring_lut[opp_letter][resp_letter]
    
    scores_per_round_list.append(choice_score + outcome_score)
    
total_score = sum(scores_per_round_list)
print("Solution 1:", total_score)


#%% Part 2

# Score for rock/paper/scissors choices
choice_scoring_lut_2 = {"R": 1, "P": 2, "S": 3}

# Scoring for choices, given opponent's letter
outcome_scoring_lut_2 = {
    "A": {"R": 3, "P": 6, "S": 0},
    "B": {"R": 0, "P": 3, "S": 6},
    "C": {"R": 6, "P": 0, "S": 3},
}

# Look-up for what to play (R, P or S), given response letter (i.e. X, Y or Z), based on opponent letter (A, B or C)
# -> X: lose, Y: draw, Z: win
response_lut = {
    "A": {"X": "S", "Y": "R", "Z": "P"},
    "B": {"X": "R", "Y": "P", "Z": "S"},
    "C": {"X": "P", "Y": "S", "Z": "R"},
}


scores_per_round_list_2 = []
for each_round_str in str_per_round:
    
    # Ignore empty lines
    if each_round_str == "":
        continue
    
    # Figure out what opponent played and how to response
    [opp_letter, resp_flag] = each_round_str.split(" ")
    resp_letter = response_lut[opp_letter][resp_flag]
    
    # Calculate scoring, just like part 1
    choice_score_2 = choice_scoring_lut_2[resp_letter]
    outcome_score_2 = outcome_scoring_lut_2[opp_letter][resp_letter]
    
    scores_per_round_list_2.append(choice_score_2 + outcome_score_2)

total_score_2 = sum(scores_per_round_list_2)
print("Solution 2:", total_score_2)
