#!/usr/bin/python
from copy import deepcopy
import sys
import csv

sudoku_puzzle = [[int(line_items) for line_items in line.strip().split(',')] for line in open(sys.argv[1])]
sudoku_puzzle_dup = deepcopy(sudoku_puzzle)
total_possible_digits = 123456789
length_dict = {}


print '**************************************Initial Sudoku***************************************************'
for item in sudoku_puzzle:
    print item
def determine_digits(level):
    global sudoku_puzzle
    global sudoku_puzzle_dup
    global length_dict 
    length_dict = {}
    single_digit_value_determined = 'N'
    for j in range(9):
        for i in range(9):
            if sudoku_puzzle[i][j] == 0:
                total_possible_digits = 123456789
                for k in range(9):
                    total_possible_digits = str(total_possible_digits).replace(str(sudoku_puzzle[i][k]),'')
                for k in range(9):
                    total_possible_digits = str(total_possible_digits).replace(str(sudoku_puzzle[k][j]),'')
                for j_33 in range(3):
                    for i_33 in range(3):
                        index_i = i_33 + ((i/3) * 3)
                        index_j = j_33 + ((j/3) * 3)
                        if (index_i != i) & (index_j != j):
                            total_possible_digits = str(total_possible_digits).replace(str(sudoku_puzzle[index_i][index_j]),'')
                if level == 1:
                    if len(total_possible_digits) == 1:
                        single_digit_value_determined = 'Y'
                        sudoku_puzzle_dup[i][j] = int(total_possible_digits)
                else:
                    sudoku_puzzle_dup[i][j] = int(total_possible_digits)
                try:
                    length_dict[len(total_possible_digits)].append((i,j))
                except:
                    length_dict[len(total_possible_digits)] = [(i,j)]
            else:
                pass
    if single_digit_value_determined == 'Y':
        sudoku_puzzle = deepcopy(sudoku_puzzle_dup)
        determine_digits(1)
    else:
        return ;
    
def check_sudoku_valid(i,j):
    for k in range(9):
        if (sudoku_puzzle[i][k] == sudoku_puzzle[i][j]) & (k != j):
            return False
    for k in range(9):
        if (sudoku_puzzle[k][j] == sudoku_puzzle[i][j]) & (k != i):
            return False
    for i_33 in range(3):
        for j_33 in range(3):
            index_i = i_33 + ((i/3) * 3)
            index_j = j_33 + ((j/3) * 3)
            if (sudoku_puzzle[index_i][index_j] == sudoku_puzzle[i][j]) & ((index_i != i)&(index_j != j)):
                return False
    return True

determine_digits(1)
determine_digits(2)
sorted(length_dict.keys())
key_list = list(length_dict.keys())
length = len(key_list)
print key_list
j = 0
i = 0
count = 0
while j < length:
    item = key_list[j]
    each_list = list(set(length_dict[item]))
    while i < len(each_list):
        in_i = each_list[i][0]
        in_j = each_list[i][1]
        if (sudoku_puzzle[in_i][in_j] == 0):
            sudoku_puzzle[in_i][in_j] = int(str(sudoku_puzzle_dup[in_i][in_j])[:1])
        else:
            index = str(sudoku_puzzle_dup[in_i][in_j]).find(str(sudoku_puzzle[in_i][in_j]))
            if index == len(str(sudoku_puzzle_dup[in_i][in_j]))-1:
                sudoku_puzzle[in_i][in_j] = 0
                if i > 0:
                    i = i-1
                else:
                    j = j -1
                    i = len(list(set(length_dict[key_list[j]]))) - 1
                continue
            temp = str(sudoku_puzzle_dup[in_i][in_j])[index+1:index+2]
            sudoku_puzzle[in_i][in_j] = int(temp)
        if(check_sudoku_valid(in_i,in_j)):
            i = i + 1
            if i == len(each_list):
                j = j + 1
                i = 0
                break
            pass
        else:
            index = str(sudoku_puzzle_dup[in_i][in_j]).find(str(sudoku_puzzle[in_i][in_j]))
            if index == len(str(sudoku_puzzle_dup[in_i][in_j]))-1:
                sudoku_puzzle[in_i][in_j] = 0
                if i > 0:
                    i = i-1
                else:
                    j = j -1
                    i = len(list(set(length_dict[key_list[j]]))) - 1
            pass
print '***************************************Solved Sudoku**********************************'
for item in sudoku_puzzle:
    print item
with open('sudoku-solution.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(sudoku_puzzle)