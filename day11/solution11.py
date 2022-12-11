#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 07:35:19 2022

@author: eo
"""

# Solution for: https://adventofcode.com/2022/day/11

#%% Load/parse data

in_path = "input.txt"
#in_path = "test.txt"
with open(in_path, "r") as in_file:
    raw_data = in_file.read()

"""
data looks like:

Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

etc.

Note: All 'divisible by ...' numbers are prime values

"""

# Parse monkey data into objects for easier handling
monkey_str_blocks = raw_data.strip().split("\n\n")


#%% Set up helper class for representing monkey states

class Monkey:
    
    # .................................................................................................................
    
    def __init__(self, str_block):
        
        # Monkey-specific parameters (default to bad/empty data)
        self.id = -1
        self.items = []
        self.op = lambda x: None
        self.divisor_int = 0
        self.throw_to = {True: None, False: None}
    
        # Fill out monkey parameters based on the given string data
        self._parse_str_block(str_block)
        
        # Initialize inspection count
        self.num_inspected = 0
    
    # .................................................................................................................
    
    def _parse_str_block(self, str_block):
        
        # Get each of the lines making up a single block describing the monkey
        block_lines = str_block.strip().splitlines()
        
        # Get id. Example: "Monkey 0:" -> get 0
        id_line = block_lines[0]
        id_str = id_line.lower().replace("monkey", "").replace(":", "")
        self.id = int(id_str)

        # Get starting items. Example: "Starting items: 83, 62, 93" -> get [82, 62, 93]
        items_line = block_lines[1]
        _, items_str = items_line.split(":")
        self.items = [int(each_entry) for each_entry in items_str.strip().split(", ")]

        # *** Helpers for next few parsing operations
        get_last_str = lambda line_str: line_str.split(" ")[-1]
        get_last_int = lambda line_str: int(get_last_str(line_str))

        # Get operation. Example: "Operation: new = old * 17" -> get lambda old: old * 17
        op_line = block_lines[2]
        self._parse_op_line(op_line)

        # Get divisible int. Example: "Test: divisible by 2" -> get 2
        div_line = block_lines[3]
        self.divisor_int = get_last_int(div_line)

        # Get throw_to lookup
        # Example: "If true: throw to monkey 1" + "If false: throw to monkey 6" -> get {True: 1, False: 6}
        true_line = block_lines[4]
        false_line = block_lines[5]
        true_int = get_last_int(true_line)
        false_int = get_last_int(false_line)
        self.throw_to = {True: true_int, False: false_int}
        
        return
    
    # .................................................................................................................
    
    def _parse_op_line(self, op_line):
        
        # Figure out what type of operation we're doing
        is_add = ("+" in op_line)
        is_mult = ("*" in op_line)
        if not (is_add or is_mult):
            raise TypeError("Unexpected operation type: {}".format(op_line))
        
        # Handle last operation (can be integer or 'old' variable)
        last_op = op_line.strip().split(" ")[-1]
        last_op_is_old = (last_op == "old")
        if last_op_is_old:
            add_op = lambda old: old + old
            mult_op = lambda old: old * old
        else:
            op_int = int(last_op)
            add_op = lambda old: old + op_int
            mult_op = lambda old: old * op_int
        
        # Pick the appropriate operation function
        self.op = add_op if is_add else mult_op
        
        return
    
    # .................................................................................................................
    
    def inspect(self, worry_modifier_func):
        
        # Keep reading items until we run out
        while len(self.items) > 0:
            item_value = self.items.pop()
            self.num_inspected += 1            
            
            # Update item (worry) value according to rules
            worry_value = self.op(item_value)
            worry_value = worry_modifier_func(worry_value)
            
            # Figure out who to throw to
            is_divisible = (worry_value % self.divisor_int) == 0            
            throw_to_idx = self.throw_to[is_divisible]
            
            yield throw_to_idx, worry_value
        
        return
    
    # .................................................................................................................
    
    def catch(self, worry_value):
        self.items.append(worry_value)
    
    # .................................................................................................................


#%% Part 1

# Parse monkey parameters
monkeys_list = [Monkey(each_block) for each_block in monkey_str_blocks]

# Set up post-operation worry value modifier (i.e. divide by 3 and round down, according to part 1)
div_by_3 = lambda worry_value: worry_value // 3

# Run iterations of 'keep away'
num_keep_away = 20
for k in range(num_keep_away):
    for each_monkey in monkeys_list:        
        for throw_to, new_worry_value in each_monkey.inspect(div_by_3):
            monkeys_list[throw_to].catch(new_worry_value)
        pass
    pass

# Find the two monkeys with the highest number of items inspected
monkey_activity_list = [each_monkey.num_inspected for each_monkey in monkeys_list]
most_active, second_most_active = sorted(monkey_activity_list, reverse=True)[0:2]

answer_1 = most_active * second_most_active
print("Solution 1:", answer_1)


#%% Part 2

'''
As-per rules of part 2, we want to perform the following inspection rules for each monkey:
    
    worry_value = get_value_from_item_list(...)
    new_worry_value = apply_operation(worry_value)
    is_divisible = remainder(new_worry_value / divisor) == 0
    if is_divisible:
        throw_to_monkey_A(new_worry_value)
    else:
        throw_to_monkey_B(new_worry_value)

However, the worry values grow out of control after many iterations in part 2
(due to repeated multiplication of the values)

Notice that each monkey is deciding where to 'throw' depending on the result of: remainder( V / D ) == 0
-> We don't actually care about the value itself, just that it is an integer multiple of the divisor

The trick is to replace the worry value with the remainder of the worry value after dividing by
a shared divsor (so that it never grows too large), while also giving the same V / D remainder results

This is extremely unintuitive to me, especially that it works with the addition operations
To get my solution working, I had to follow: https://aoc.just2good.co.uk/2022/11#part-2
This explanation sounds plausible at least, but I still find it very hard to grasp!
'''

# Reset monkey list
monkeys_list = [Monkey(each_block) for each_block in monkey_str_blocks]

# Find shared divisor, needed to prevent the worry value calculations from exploding
# -> Can just use product of divisors here, since they are all prime numbers (confirmed by manual inspection)
shared_divisor = 1
for each_monkey in monkeys_list:
    shared_divisor = shared_divisor * each_monkey.divisor_int

# Set up post-operation worry value modifier (i.e. limit value to shared divisor to prevent overly large values)
limit_worry = lambda worry_value: (worry_value % shared_divisor)

# Run iterations of 'keep away'
num_keep_away = 10_000
for k in range(num_keep_away):    
    for mid, each_monkey in enumerate(monkeys_list):
        for throw_to, new_worry_value in each_monkey.inspect(limit_worry):
            limited_worry_value = new_worry_value % shared_divisor
            monkeys_list[throw_to].catch(limited_worry_value)
        pass
    pass

# Find the two monkeys with the highest number of items inspected
monkey_activity_list = [each_monkey.num_inspected for each_monkey in monkeys_list]
most_active, second_most_active = sorted(monkey_activity_list, reverse=True)[0:2]

answer_2 = most_active * second_most_active
print("Solution 2:", answer_2)
