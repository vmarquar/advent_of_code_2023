# Requirements: pytest

from day03 import find_engine_parts_and_calc_sum, read_input_from_file

def test_part_1():
    dummy_matrix, dummy_lines = read_input_from_file('./input/day03_input_test.txt')
    assert find_engine_parts_and_calc_sum(dummy_matrix,dummy_lines) == 4361


# def test_part_2():
#     puzzle = dummy_puzzle("day02_example.txt")
#     assert solve_part_2(puzzle) == 2286
#     puzzle = dummy_puzzle("day02.txt")
#     assert solve_part_2(puzzle) == 72596
