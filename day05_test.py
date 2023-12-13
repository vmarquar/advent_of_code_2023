# Requirements: pytest

from day05 import read_input_from_file, parse_seeds, parse_all_mappings, apply_mappings, parse_seeds_as_range_pairs

def test_part_1():
    input = read_input_from_file('./input/day05_input_test.txt')
    seeds = parse_seeds(input[0])
    mappings = parse_all_mappings(input)
    seeds_with_mappings = apply_mappings(seeds, mappings)

    # Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    assert seeds_with_mappings[0]['seed'] == 79
    assert seeds_with_mappings[0]['soil'] == 81
    assert seeds_with_mappings[0]['fertilizer'] == 81
    assert seeds_with_mappings[0]['water'] == 81
    assert seeds_with_mappings[0]['light'] == 74
    assert seeds_with_mappings[0]['temperature'] == 78
    assert seeds_with_mappings[0]['humidity'] == 78
    assert seeds_with_mappings[0]['location'] == 82
    
    min_location = min([seed['location'] for seed in seeds_with_mappings])
    assert min_location == 35, "Test failed: Incorrect minimum location value."


def test_part_2():
    input = read_input_from_file('./input/day05_input_test.txt')
    seeds = parse_seeds_as_range_pairs(input[0])
    assert len(seeds) == 27
    mappings = parse_all_mappings(input)
    seeds_with_mappings = apply_mappings(seeds, mappings)
    min_location = min([seed['location'] for seed in seeds_with_mappings])
    assert min_location == 46, "Test failed: Incorrect minimum location value."