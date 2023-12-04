"""
--- Day 3: Gear Ratios ---
"""
### IMPORTS AND GLOBAL CONSTANTS
import re
from time import perf_counter as pfc

### PART 1 FUNCTIONS
def read_input_from_file(filepath:str):
    with open(filepath) as f:
        lines = f.readlines()
        lines = [l.replace('\n', '') for l in lines]
        matrix = [[c for c in line] for line in lines]
        return(matrix, lines)

def is_marker_symbol(char):
    return(char != '.' and not char.isdigit())

def find_numbers(line:str):
    starts_and_ends = [(m.start(), m.end()-1) for m in re.finditer(r"\d+", line)]
    return(starts_and_ends)

def calc_neighbours(_x,_y, max_x=11, max_y=10, min_x = 0, min_y = 0):
    north = (_x, _y-1) if(_y-1 >= min_y) else None
    east = (_x+1, _y) if(_x+1 <= max_x) else None
    south = (_x, _y+1) if(_y+1 <= max_y) else None
    west = (_x-1, _y) if (_x-1 >= min_x) else None
    north_east = (_x+1,_y-1) if ( (_x+1 <= max_x) and (_y-1 >= min_y)) else None 
    north_west = (_x-1,_y-1) if ( (_x-1 >= min_x) and (_y-1 >= min_y)) else None
    south_east = (_x+1,_y+1) if ( (_x+1 <= max_x) and (_y+1 <= max_y)) else None
    south_west = (_x-1,_y+1) if ( (_x-1 >= min_x) and (_y+1 <= max_y)) else None
    neighbours = [north, north_east, east, south_east, south, south_west, west, north_west]
    neighbours_valid = [nei for nei in neighbours if nei is not None]
    return(neighbours_valid)


def removeDuplicates(lst):
    return [t for t in (set(tuple(i) for i in lst))]

def find_engine_parts_and_calc_sum(matrix,lines):

    sum_of_engine_parts = 0
    for y_index, line in enumerate(lines):
        numbers = find_numbers(line=line)
        for start, end in numbers:
            start_neighbours = calc_neighbours(start, y_index, max_x=len(line)-1, max_y=len(lines)-1)
            end_neighbours = calc_neighbours(end, y_index, max_x=len(line)-1, max_y=len(lines)-1)
            neighbours = removeDuplicates(start_neighbours + end_neighbours)
        
            for n_x,n_y in neighbours:
                char = matrix[n_y][n_x]
                if(is_marker_symbol(char)):
                    number = int(''.join(matrix[y_index][start:end+1]))
                    sum_of_engine_parts += number
                    #print(f"Number {number} is part of the motor. Marked by {char} at ({n_x},{n_y})")
                    break

    return(sum_of_engine_parts)

## PART 2 FUNCTIONS

def search_left_right_to_get_complete_number(x,y, matrix):
    # check both sides until no digits are found
    left_x = x
    line = matrix[y]
    # scan left side until no more digits are found
    while((-1 < (x-1)) and matrix[y][left_x-1].isdigit()):
        left_x -= 1
    # scan right side until no more digits are found
    right_x = x
    while((len(line)>(right_x+1)) and matrix[y][right_x+1].isdigit()):
        right_x += 1

    number = int(''.join(matrix[y][left_x:right_x+1]))
    
    left_coords = left_x, y
    right_coords = right_x, y
    return(number, left_coords, right_coords)


def find_stars(line:str):
    starts_and_ends = [(m.start(), m.end()-1) for m in re.finditer(r"\*", line)]
    return(starts_and_ends)

def find_stars_and_calc_sum(matrix,lines):
    all_gear_ratios = []
    for y_index, line in enumerate(lines):
        stars = find_stars(line=line)

        for start, end in stars:
            neighbours = calc_neighbours(start, y_index, max_x=len(line)-1, max_y=len(lines)-1)
            
            gears = []
            for n_x,n_y in neighbours:
                char = matrix[n_y][n_x]
                if(char.isdigit()):
                    gear_number, left_coords, right_coords = search_left_right_to_get_complete_number(n_x,n_y, matrix)
                    gear = gear_number, left_coords, right_coords
                    gears.append(gear)
            
            # remove duplicates
            gears = removeDuplicates(gears)

            # if exactly two different gears -> calculate ratio
            if(len(gears)==2):
                gear_ratio = gears[0][0] * gears[1][0] 
                all_gear_ratios.append((gear_ratio, gears[0][0], gears[1][0], y_index))

    sum_of_all_gear_ratios = sum([g[0] for g in all_gear_ratios])
    return(sum_of_all_gear_ratios, all_gear_ratios)

### MAIN
if __name__ == "__main__":
    # READ INPUT
    matrix, lines = read_input_from_file('./input/day03_input.txt')
    
    # PART 1
    start = pfc()
    engine_sum = find_engine_parts_and_calc_sum(matrix,lines)
    print(f"PART 1: The engine sum is '{engine_sum}' ({pfc() - start:.4f}s).")

    # PART 2
    start = pfc()
    gear_ratio_sum, all_data = find_stars_and_calc_sum(matrix, lines)
    print(f"PART 1: The gear_ratio sum is '{gear_ratio_sum}' ({pfc() - start:.4f}s).")
