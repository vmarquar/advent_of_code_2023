# Requirements: pytest

from day07 import read_input_from_file, get_type_of_hand, order_typed_hands

def test_part_1():
    hands = read_input_from_file('./input/day07_input_test.txt')
    typed_hands = [get_type_of_hand(hand) for hand in hands]
    ordered_hands = order_typed_hands(typed_hands)
    multiplied_bids = [(index_hand[0]+1) * index_hand[1]['bid'] for index_hand in enumerate(ordered_hands)]
    assert sum(multiplied_bids) == 6440, "Test failed: Incorrect multiplication value."
