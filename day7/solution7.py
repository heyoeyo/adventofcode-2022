#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 10:06:38 2022

@author: eo
"""

# Solution for: https://adventofcode.com/2022/day/7

#%% Load/parse data

in_path = "input.txt"
#in_path = "test.txt"
with open(in_path, "r") as in_file:
    raw_data = in_file.read()

"""
data looks like:
    
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

"""


#%% Helpers

# .....................................................................................................................

def get_line_type(line_str):
    
    ''' Example lines: "$ cd /"  "$ ls"  "dir a"  "123 file"  "$ cd .." '''
    
    # Figure out what type of line we're dealing with
    line_type = None
    if line_str.startswith("$"):
        cmd_str = line_str.strip().split(" ")[1]
        is_cd = (cmd_str == "cd")
        line_type = "cd" if is_cd else "ls"
    elif line_str.startswith("dir"):
        line_type = "dir"
    else:
        line_type = "file"
    
    return line_type

# .....................................................................................................................

def get_sub_dict(original_dict, key_sequence):
    
    '''
    Programmatically index into a dictionary using a sequence of keys
    -> If the key sequence indexes to a value stored by reference (e.g. another dict),
       then modifying the return value of this function will modify the original dictionary!
    '''
    
    sub_dict = original_dict
    for each_key in key_sequence:
        sub_dict = sub_dict[each_key]
    
    return sub_dict

# .....................................................................................................................

def add_file(fs, path_list, line_str):
    
    '''
    Called when we see instructions like: "8033020 d.log"
    -> Requires that we add a file to the current directory
    -> For example, if we're at path: ["/"] and have fs: {"/": {}}, then "123 file" means:
        fs becomes {"/": {"file": 123}}
    '''
    
    # Get file name and size for storage
    size_str, name_str = line_str.strip().split(" ")
    
    # Add file entry
    # -> Note, this modifies the original fs!
    mod_fs = get_sub_dict(fs, path_list)
    mod_fs[name_str] = int(size_str)
    
    return fs

# .....................................................................................................................

def add_dir(fs, path_list, line_str):
    
    '''
    Called when we see instructions like: "dir a"
    -> Requires that we add a new (empty) directory at our current path
    -> For example, if we're at a path: ["/"] and have fs: {"/": {}}, then "dir a" means:
        fs becomes {"/": {"a": {}}}
    '''
    
    # Get the name of the new direction to add
    _, new_dir_name = line_str.strip().split(" ")
    
    # Add 'empty' directory
    # -> Note this modifies the original fs!
    mod_fs = get_sub_dict(fs, path_list)
    mod_fs[new_dir_name] = {}
    
    return fs

# .....................................................................................................................

def change_dir(fs, path_list, line_str):
    
    '''
    Called when we get an instruction like: "$ cd /" or "$ cd .."
    -> Only two cases to handle (cd into dir, relative to current path or cd back one folder)
    -> There is no absolute pathing! (i.e. no instances of "cd /a/b/c" to handle)
    '''
    
    # Handle "cd .." vs. "cd dir" commands
    is_cd_back = ".." in line_str
    if is_cd_back:
        path_list.pop()
    else:
        _, _, target_dir = line_str.split(" ")
        path_list.append(target_dir)
    
    return path_list

# .....................................................................................................................

def record_dir_size_recursive(fs, path_list, size_dict = None):
    
    '''
    Recursively sums up total size of directory contents
    Takes the file system tree, the pathing list (i.e. a list of folders we've entered)
    Returns (total size of dir at path_list, size_dict)
    
    -> Where the size_dict has each path (as a string) for keys, and the dir size as a value
    -> For example:
        {
         '/a/e': 584,
         '/a': 94853,
         '/d': 24933642,
         '/': 48381165
         }
    '''
    
    # Initialize outputs
    total_size = 0
    if size_dict is None:
        size_dict = {}
    
    # Sum up all files/directory sizes
    sub_fs = get_sub_dict(fs, path_list)
    for each_name, each_value in sub_fs.items():
        
        is_int = (type(each_value) == int)
        if is_int:
            total_size += each_value
        else:
            path_list.append(each_name)
            dir_size, size_dict = record_dir_size_recursive(fs, path_list, size_dict)
            total_size += dir_size
            path_list.pop()
        pass
    
    # Record new size entry
    path_str = "/".join(path_list).replace("//", "/")
    size_dict[path_str] = total_size
    
    return total_size, size_dict


#%% Build the file system as a dict

# Initialize the file system tree structure
fs_tree = {"/": {}}
curr_path_list = []

# Build file system from input data
line_strs_list = raw_data.strip().splitlines()
for each_line in line_strs_list:
    
    # Figure out what type of line to handle and bundle data for convenience
    line_type = get_line_type(each_line)
    mod_tree_args = (fs_tree, curr_path_list, each_line)
    
    if line_type == "file":
        fs_tree = add_file(*mod_tree_args)
    elif line_type == "dir":
        fs_tree = add_dir(*mod_tree_args)
    elif line_type == "cd":
        curr_path_list = change_dir(*mod_tree_args)
    
    # We can ignore ls commands
    # -> should already be in the right context to interpret follow-up lines
    
    pass


#%% Part 1

# Traverse the file system to find size of each path
_, fs_size_dict = record_dir_size_recursive(fs_tree, ["/"])

# Sum up all paths with sizes <= 100000
small_size_paths = [size for path, size in fs_size_dict.items() if size <= 100000]

answer_1 = sum(small_size_paths)
print("Solution 1:", answer_1)


#%% Part 2

# From question
total_space = 70000000
min_unused_space = 30000000

# Figure out much unused space we already have (deleting dirs. will add to this)
curr_space_used = fs_size_dict["/"]
curr_unused_space = (total_space - curr_space_used)

# Find the directory with the minimum size, that clears enough space to reach target unused amount
min_excess = float("inf")
min_path = None
min_size = None
for each_path, each_size in fs_size_dict.items():
    
    # Figure out how much unused space (above min target) we'd have after deleting each directory
    unused_space_if_deleted = (curr_unused_space + each_size)
    excess_space_if_deleted = (unused_space_if_deleted - min_unused_space)
    
    # Ignore cases where there isn't any excess (i.e. we're not clearing enough to reach min target)
    if excess_space_if_deleted < 0:
        continue
    
    # Record minimums
    if excess_space_if_deleted < min_excess:
        min_excess = excess_space_if_deleted
        min_path = each_path
        min_size = each_size

    pass

print("Solution 2:", min_size)
