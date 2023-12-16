# --- Day 6: Wait For It ---
# started: 2023-12-16 10:00
# end part 1: 2023-12-16 11:15
# end part 2: 2023-12-16 11:30

### IMPORTS AND GLOBAL CONSTANTS
from time import perf_counter as pfc
STARTING_SPEED = 0 # mm/ms zero millimeters per millisecond
ACCERATION = 1 # mm/ms^2

### HELPER FUNCTIONS
def read_input_from_file(filepath:str):
    with open(filepath) as f:
        lines = f.readlines()
        lines = [l.replace('\n', '') for l in lines]
        times = []
        record_distances = []
        for index, line in enumerate(lines):
            line = line.split(':')[1].strip().split(' ')
            line = [int(t.strip()) for t in line if t != '']
            if(index == 0):
                times = line
            else:
                record_distances = line

        # create a list of races with the time and record distance as key value pairs
        races = [ {'time': t, 'record_distance': d} for t, d in zip(times, record_distances) ]
        return(races)
    

def can_break_record(hold_down_time:int, race_time:int, record_distance:int) -> bool:
    speed = STARTING_SPEED + (hold_down_time * ACCERATION) # mm/ms 2
    distance =  (race_time - hold_down_time) * speed # mm 7-2=5 * 2 = 10
    if(distance > record_distance): 
        return(True) 
    else:
        return(False)

def get_hold_down_times_for_race_win(race: dict) -> int:    
        min_hold_down_time = 1 # ms
        while(not can_break_record(hold_down_time=min_hold_down_time,
                                race_time=race['time'],
                                record_distance=race['record_distance'])):
            min_hold_down_time += 1

        max_hold_down_time = race['time'] - 1 # ms
        while(not can_break_record(hold_down_time=max_hold_down_time,
                            race_time=race['time'],
                            record_distance=race['record_distance'])):
            max_hold_down_time -= 1

        print(min_hold_down_time, max_hold_down_time)
        num_hold_down_times_to_win_per_race = max_hold_down_time - min_hold_down_time + 1
        return(num_hold_down_times_to_win_per_race)
    
def multiplyList(myList: list) -> int:
    result = 1
    for x in myList:
        result = result * x
    return result


### PART 2 FUNCTIONS
def read_input_from_file_part2(path:str):
    with open(path) as f:
        lines = f.readlines()
        lines = [l.replace('\n', '') for l in lines]
        time = int(''.join([c for c in lines[0].split(':')[1] if c != ' ']))
        distance = int(''.join([c for c in lines[1].split(':')[1] if c != ' ']))
        return({'time': time, 'record_distance': distance})


### MAIN
if __name__ == "__main__":

    ### PART 1 ###
    # 0) start timer
    start = pfc()    
    # 1) Read input file and parse data to a list of dicts with time and record distance
    races = read_input_from_file('./input/day06_input.txt')

    # 2) calucate the hold_down_times to win each reace and store them in a list
    hold_down_times = []
    for race in races:
        hold_down_times.append(get_hold_down_times_for_race_win(race=race))

    # 3) multiply the list hold_down_times = [1,2,3] with each element
    result = multiplyList(hold_down_times)
    print(f"PART 1: The Multiplication of all hold down times is '{result}' ({pfc() - start:.4f}s).")

    ### PART 2 ###
    start2 = pfc()
    race = read_input_from_file_part2('./input/day06_input.txt')
    hold_down_times = get_hold_down_times_for_race_win(race=race)
    print(f"PART 2: The hold down times are '{hold_down_times}' ({pfc() - start2:.4f}s).")