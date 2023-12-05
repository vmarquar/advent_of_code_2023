"""
started: 21:08
end part 1: 21:43 

Day 04 --- Scratchcards ---


Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11

In the above example, card 1 has five winning numbers (41, 48, 83, 86, and 17) and eight numbers you have (83, 86, 6, 31, 17, 9, 48, and 53). 

Of the numbers you have, four of them (48, 83, 17, and 86) are winning numbers! 

That means card 1 is worth 8 points (1 for the first match, then doubled three times for each of the three matches after the first).

Card 2 has two winning numbers (32 and 61), so it is worth 2 points.
Card 3 has two winning numbers (1 and 21), so it is worth 2 points.
Card 4 has one winning number (84), so it is worth 1 point.
Card 5 has no winning numbers, so it is worth no points.
Card 6 has no winning numbers, so it is worth no points.
So, in this example, the Elf's pile of scratchcards is worth 13 points.

Take a seat in the large pile of colorful cards. How many points are they worth in total?
"""
### IMPORTS AND GLOBAL CONSTANTS
from time import perf_counter as pfc
import re
from typing import List

### GENERAL FUNCTIONS
def read_input_from_file(filepath:str):
    with open(filepath) as f:
        lines = f.readlines()
        lines = [l.replace('\n', '') for l in lines]
        return(lines)
    

def string_to_array_of_ints(_string:str) -> List[int]:
    _list = re.findall('\d+', _string)
    ints = [int(i) for i in _list]
    return(ints)

### PART 1 FUNCTIONS
def apply_point_logic(owned_winning_numbers: List[int]) -> int:
    """
    # 3) apply point logic to this numbers
    # 1 won -> 1 point
    # 2 wons -> 2 points
    # 4 wons -> 8 points
    # 1: 1*2 = 2
    # 2: 2*2 = 4
    # 3: 4*2 = 8
    # apply point logic
    """
    points = 0
    for i, won in enumerate(owned_winning_numbers):
        if(i == 0):
            points = 1
        else:
            points = points * 2
    return(points)

def count_points_from_game_line(line:str) -> int:
    """
    # 1) split each line into card_nr, winning_numbers, owned_numbers
    # 2) check which of the owned numbers are winning numbers

    """
    #card_nr = int(re.findall('\d+', line.split(': ')[0])[0])
    winning_numbers = string_to_array_of_ints(_string = line.split(': ')[1].split(' | ')[0])
    owned_numbers = string_to_array_of_ints(_string = line.split(': ')[1].split(' | ')[1] )
    owned_winning_numbers = [won for won in owned_numbers if won in winning_numbers]
    
    points = apply_point_logic(owned_winning_numbers)

    return(points)

### PART 2 FUNCTIONS
def process_card(line:str, prev_instances: int) -> List[int]:
    """
    # 1) split each line into card_nr, winning_numbers, owned_numbers
    # 2) check which of the owned numbers are winning numbers
    # return current card_nr, current_instances, won_card_indices

    """
    card_nr = int(re.findall('\d+', line.split(': ')[0])[0])
    winning_numbers = string_to_array_of_ints(_string = line.split(': ')[1].split(' | ')[0])
    owned_numbers = string_to_array_of_ints(_string = line.split(': ')[1].split(' | ')[1] )
    owned_winning_numbers = [won for won in owned_numbers if won in winning_numbers]

    won_card_nrs = [card_nr + 1 + i for i,value in enumerate(owned_winning_numbers)]
    won_card_indeces = [card_nr + i for i,value in enumerate(owned_winning_numbers)]

    won_copies = won_card_nrs

    curr_instances = prev_instances + 1
    simple_dict = {card_nr:len(won_copies)+1}
    return({"card_nr":card_nr, "instances":curr_instances, "won_copies":won_copies, "total_cards":len(won_copies)+1}, simple_dict)



### MAIN
if __name__ == "__main__":
    
    input = read_input_from_file('./input/day04_input_test.txt')
    
    # PART 1
    start = pfc()
    all_points = [count_points_from_game_line(line) for line in input]
    print(f"PART 1: The sum of all points is '{sum(all_points)}' ({pfc() - start:.4f}s).")



    # PART 2
    """
    There's no such thing as "points". Instead, scratchcards only cause you to win more scratchcards equal to the number of winning numbers you have.

    len(won) => new scratchcards

    Card 1 has four matching numbers, so you win one copy each of the next four cards: cards 2, 3, 4, and 5.

    Your original card 2 has two matching numbers, so you win one copy each of cards 3 and 4.
    Your copy of card 2 also wins one copy each of cards 3 and 4.
    Your four instances of card 3 (one original and three copies) have two matching numbers, so you win four copies each of cards 4 and 5.
    Your eight instances of card 4 (one original and seven copies) have one matching number, so you win eight copies of card 5.
    Your fourteen instances of card 5 (one original and thirteen copies) have no matching numbers and win no more cards.
    Your one instance of card 6 (one original) has no matching numbers and wins no more cards.

    Once all of the originals and copies have been processed, you end up with 1 instance of card 1, 2 instances of card 2, 4 instances of card 3, 8 instances of card 4, 14 instances of card 5, and 1 instance of card 6. In total, this example pile of scratchcards causes you to ultimately have 30 scratchcards!

    """
    # 1) iteriere alle scratchcards
    # 2) wenn won, dann: 


    # copies = []
    # lookup_dict = {}
    # for line in input:
    #     copy, simple_copy = process_card(line, prev_instances=0)
    #     copies.append(copy)
    #     lookup_dict.update(simple_copy)

    # for copy in copies:
    #     card_wons_per_card = 0
    #     for won_nr in copy['won_copies']:
    #         nr_cards = lookup_dict[won_nr]
    #         card_wons_per_card += nr_cards
    #     print(f"{copy['card_nr']}: gewonnene Karten {card_wons_per_card}")

    # cards = 0
    # total_cards = []  # [{card_nr: 1, instances: X}, {card_nr_2, instances: N}, etc...] # {card_nr: 1, instances: 2, winning_no: [1,2,3,4]}

    # for line in input:
    #     print(line)
    #     cards += 1
    #     copies_idx = process_card(line)
    #     for copy_idx in copies_idx:
    #         copy_line = input[copy_idx]
    #         process_card(copy_line)
    #         cards += 1

    # print("ok")


    # result: card nr : numer of instances,