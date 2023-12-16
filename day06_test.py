# Requirements: pytest

from day06 import read_input_from_file, get_hold_down_times_for_race_win, multiplyList, read_input_from_file_part2

def test_part_1():
    races = read_input_from_file('./input/day06_input_test.txt')
    hold_down_times = []
    for race in races:
        hold_down_times.append(get_hold_down_times_for_race_win(race=race))
    result = multiplyList(hold_down_times)
    assert result == 288, "Test failed: Incorrect multiplication value."



def test_part_2():
    race = read_input_from_file_part2('./input/day06_input_test.txt')
    hold_down_times = get_hold_down_times_for_race_win(race=race)
    assert hold_down_times == 71503, "Test failed: Incorrect hold down times."