# Requirements: pytest

from day03 import find_engine_parts_and_calc_sum, read_input_from_file, find_stars_and_calc_sum

def test_part_1():
    dummy_matrix, dummy_lines = read_input_from_file('./input/day03_input_test.txt')
    assert find_engine_parts_and_calc_sum(dummy_matrix,dummy_lines) == 4361

def test_example_part_2():
    dummy_matrix, dummy_lines = read_input_from_file('./input/day03_input_test.txt')
    gear_ratio_sum_example, all_data_example =  find_stars_and_calc_sum(dummy_matrix,dummy_lines)
    assert gear_ratio_sum_example == 467835

def test_part_2():
    dummy_matrix, dummy_lines = read_input_from_file('./input/day03_input.txt')
    gear_ratio_sum, all_data = find_stars_and_calc_sum(dummy_matrix,dummy_lines)
    assert gear_ratio_sum == 84159075