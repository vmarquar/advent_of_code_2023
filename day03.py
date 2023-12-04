"""
Started: 10:07

--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

To begin, get your puzzle input.
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

def search_left_right_to_get_complete_word(x,y, matrix):
    # check both sides until no digits are found
    left_x = x
    while(matrix[y][left_x-1].isdigit()):
        left_x -= 1

    right_x = x
    while(matrix[y][right_x+1].isdigit()):
        right_x += 1

    word = ''.join(matrix[y][left_x:right_x+1])
    print(word)
    return(left_x,right_x)


def find_stars(line:str):
    starts_and_ends = [(m.start(), m.end()-1) for m in re.finditer(r"\*", line)]
    return(starts_and_ends)

def find_stars_and_calc_sum(matrix,lines):

    all_numbers = []
    for y_index, line in enumerate(lines):
        all_numbers.append(find_numbers(line=line))

    for y_index, line in enumerate(lines):
        stars = find_stars(line=line)

        for start, end in stars:
            neighbours = calc_neighbours(start, y_index, max_x=len(line)-1, max_y=len(lines)-1)
            
            gears = []
            gears_ny = []
            for n_x,n_y in neighbours:
                char = matrix[n_y][n_x]
                print(f"Star * with neighbour {char} at ({n_x},{n_y})")
                if(char.isdigit() and n_y not in gears_ny):
                    gear = char, n_x, n_y
                    gears.append(gear)
                    gears_ny.append(n_y)
                    search_left_right_to_get_complete_word(n_x,n_y, matrix)
            
            print(gears)

                # if(is_marker_symbol(char)):
                #     number = int(''.join(matrix[y_index][start:end+1]))
                #     sum_of_engine_parts += number
                #     #print(f"Number {number} is part of the motor. Marked by {char} at ({n_x},{n_y})")
                #     break


### MAIN
if __name__ == "__main__":
    
    # PART 1
    matrix, lines = read_input_from_file('./input/day03_input_test.txt')
    
    start = pfc()
    engine_sum = find_engine_parts_and_calc_sum(matrix,lines)
    print(f"PART 1: The engine sum is '{engine_sum}' ({pfc() - start:.4f}s).")

    # PART 2
    # 1) find all starts
    # 2) calc neighbours of all stars
    # 3) check if exactly two neighbors are numbers/digits
    # 4) return the two numbers (the two gears)
    # 5) multiply the two numbers to get the gear_ratio
    # 6) sum up all gear_ratio numbers to get the result
    find_stars_and_calc_sum(matrix, lines)
