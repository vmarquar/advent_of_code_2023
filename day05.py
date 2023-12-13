# advent of code day 05
# author Valentin M

from typing import List, Tuple, Dict, Set, Optional
import re
from time import perf_counter as pfc


### IMPORTS AND GLOBAL CONSTANTS
PART_2_PARALLEL = True
PART_2_REVERSED = True


### HELPER FUNCTIONS
def read_input_from_file(filepath:str):
    with open(filepath) as f:
        lines = f.readlines()
        lines = [l.replace('\n', '') for l in lines]
        return(lines)
    
### FUNCTIONS FOR PART 1
def map_x_to_y(seed, mapping_rules):
    for rule in mapping_rules:
        dest_start, src_start, length = rule # parse the 44 34 2 string
        if src_start <= seed < src_start + length:
            return dest_start + (seed - src_start)
    return seed

def parse_seeds(first_line:str) -> List[int]:
    # first_line = 'seeds: 79 14 55 13'
    seeds = first_line.split(':')[1].strip().split(' ') # ['79', '14', '55', '13']  
    seeds = list(map(int, seeds)) # [79, 14, 55, 13]
    return seeds

def parse_all_mappings(lines:List[str]):
    mappings = []
    new_mapping = {}

    for index, line in enumerate(lines):

        if('map:' in line):
            new_mapping = {}
            name_of_mapping = line.split(' map:')[0].strip()
            new_mapping['name'] = name_of_mapping
            new_mapping['mappings'] = []

        elif(re.match(r'\d+ \d+ \d+', line)):
            mapping = line.split(' ')
            new_mapping['mappings'].append(list(map(int, mapping)))
        
        if((line == '' and new_mapping != {}) or (index == (len(lines)-1) and new_mapping != {})):
            mappings.append(new_mapping)

    return mappings 

def get_rules_from_dict(mappings, name= 'seed-to-soil'):
    return([mapping for mapping in mappings if mapping['name'] == name][0]['mappings'])

def apply_mappings(seeds, mappings):
    seeds_with_mappings = []
    for seed in seeds:
        soil = map_x_to_y(seed, get_rules_from_dict(mappings, name= 'seed-to-soil'))
        fertilizer = map_x_to_y(soil, get_rules_from_dict(mappings, name= 'soil-to-fertilizer'))
        water = map_x_to_y(fertilizer, get_rules_from_dict(mappings, name= 'fertilizer-to-water'))
        light = map_x_to_y(water, get_rules_from_dict(mappings, name= 'water-to-light'))
        temperature = map_x_to_y(light, get_rules_from_dict(mappings, name= 'light-to-temperature'))
        humidity = map_x_to_y(temperature, get_rules_from_dict(mappings, name= 'temperature-to-humidity'))
        location = map_x_to_y(humidity, get_rules_from_dict(mappings, name= 'humidity-to-location'))

        print(f'Seed {seed}, soil {soil}, fertilizer {fertilizer}, water {water}, light {light}, temperature {temperature}, humidity {humidity}, location {location}.')

        seed_with_mappings = {
            "seed": seed, 
            "soil": soil,
            "fertilizer": fertilizer,
            "water": water,
            "light": light,
            "temperature": temperature,
            "humidity": humidity,
            "location": location
        }

        seeds_with_mappings.append(seed_with_mappings)
    
    return seeds_with_mappings
    
### FUNCTIONS FOR PART 2
def parse_seeds_as_range_pairs(first_line:str) -> List[int]:
    # parse_seeds_part2(first_line
    # - Pair
    # - p1=start of the range
    # - P2=length of the range
    # - Example (p1 = 79, p2=14) => 79:92, length=14

    # - Consider a total of 27 seed numbers

    seed_pairs = first_line.split(':')[1].strip().split(' ')
    seed_pairs = list(map(int, seed_pairs))
    seeds = []
    # ATTENTION: a brute force approach would be to create a list of all seeds and then apply the mappings to each seed
    # However, this would be very inefficient, as we would have to create a list of >1000000 elements
    # Memory consumption would be too high (45 GigaByte!!!)
    # Instead, we can use the fact that the mappings are linear and apply them to the seed ranges
    # for i in range(0, len(seed_pairs), 2):
    #     start_of_seed_range, length_of_seed_range = seed_pairs[i:i+2]
    #     seed_range = list(range(start_of_seed_range, start_of_seed_range+length_of_seed_range))
    #     seeds += seed_range

    pairs = []
    seed_ranges = []
    for i in range(0, len(seed_pairs), 2):
        start_of_seed_range, length_of_seed_range = seed_pairs[i:i+2]
        end_of_seed_range = start_of_seed_range + length_of_seed_range
        pairs.append((start_of_seed_range, end_of_seed_range))
        seed_ranges.append((start_of_seed_range, end_of_seed_range))

    return seed_ranges

def retrieve_min_location(seeds, mappings):
    min_location = None
    for seed in seeds:
        soil = map_x_to_y(seed, get_rules_from_dict(mappings, name= 'seed-to-soil'))
        fertilizer = map_x_to_y(soil, get_rules_from_dict(mappings, name= 'soil-to-fertilizer'))
        water = map_x_to_y(fertilizer, get_rules_from_dict(mappings, name= 'fertilizer-to-water'))
        light = map_x_to_y(water, get_rules_from_dict(mappings, name= 'water-to-light'))
        temperature = map_x_to_y(light, get_rules_from_dict(mappings, name= 'light-to-temperature'))
        humidity = map_x_to_y(temperature, get_rules_from_dict(mappings, name= 'temperature-to-humidity'))
        location = map_x_to_y(humidity, get_rules_from_dict(mappings, name= 'humidity-to-location'))
        #print(f'Seed {seed}, soil {soil}, fertilizer {fertilizer}, water {water}, light {light}, temperature {temperature}, humidity {humidity}, location {location}.')
        if(min_location == None):
            min_location = location

        elif(location < min_location):
            min_location = location 
    
    return min_location

def create_lists_from_range_max_min_blocksize(_min,_max, blocksize=100_000):
    lists = []
    while(_min < _max):
        lists.append(list(range(_min, _min+blocksize)))
        _min += blocksize
    return lists

def map_y_to_x(location, mappings):
    for rule in reversed(mappings):
        dest_start, src_start, length = rule
        if dest_start <= location < dest_start + length:
            return src_start + (location - dest_start)
    return location

def reverse_mappings_humidity_to_seed(humidities, mappings):
    locations_with_mappings = []

    for humidity in humidities:
        # humidity = map_y_to_x(location, get_rules_from_dict(mappings, name= 'humidity-to-location'))
        location = map_x_to_y(humidity, get_rules_from_dict(mappings, name= 'humidity-to-location')) # exception: forward mapping
        temperature = map_y_to_x(humidity, get_rules_from_dict(mappings, name= 'temperature-to-humidity'))
        light = map_y_to_x(temperature, get_rules_from_dict(mappings, name= 'light-to-temperature'))
        water = map_y_to_x(light, get_rules_from_dict(mappings, name= 'water-to-light'))
        fertilizer = map_y_to_x(water, get_rules_from_dict(mappings, name= 'fertilizer-to-water'))
        soil = map_y_to_x(fertilizer, get_rules_from_dict(mappings, name= 'soil-to-fertilizer'))
        seed = map_y_to_x(soil, get_rules_from_dict(mappings, name= 'seed-to-soil'))
        
        print(f'Seed {seed}, soil {soil}, fertilizer {fertilizer}, water {water}, light {light}, temperature {temperature}, humidity {humidity}, location {location}.')

        location_with_mappings = {
            "seed": seed, 
            "soil": soil,
            "fertilizer": fertilizer,
            "water": water,
            "light": light,
            "temperature": temperature,
            "humidity": humidity,
            "location": location
        }
        locations_with_mappings.append(location_with_mappings)

    return locations_with_mappings

### MAIN
if __name__ == "__main__":
    
    # 0) Read input from file
    input = read_input_from_file('./input/day05_input.txt')
    
    ########################################################################
    # PART 1
    ########################################################################
    # PART1-1) Parse input to readable data formats
    start = pfc()
    seeds = parse_seeds(input[0])
    mappings = parse_all_mappings(input)

    # PART1-2) Apply Mappings
    seeds_with_mappings = apply_mappings(seeds, mappings)

    # PART1-3) Calculate the minimum of all location values in the list of seeds
    min_location = min([seed['location'] for seed in seeds_with_mappings])
    print(f'PART 1 - The minimum location is {min_location} [{pfc() - start:.4f}sec].')

    ########################################################################
    # PART 2 - Parallel
    ########################################################################
    if(PART_2_PARALLEL):
        # not really effective, but a good excuse to use multiprocessing
        from multiprocessing import Pool, cpu_count
        from functools import partial

        seed_ranges = parse_seeds_as_range_pairs(input[0])
        mappings = parse_all_mappings(input)

        global_mins = []
        for _min,_max in seed_ranges:
            seeds_lists = create_lists_from_range_max_min_blocksize(_min,_max, blocksize=1_000) # [list(range(79, 100000)), list(range(100000, 200000)), ...]
                
            with Pool(cpu_count() - 2) as pool:
                retrieve_min_location_parallel=partial(retrieve_min_location, mappings=mappings)
                min_locations = pool.map(retrieve_min_location_parallel, seeds_lists) # process 100_000 seeds in parallel
                min_location = min(min_locations)
                global_mins.append(min_location)
                print(f'PART 2 - The minimum location is {min_location} [{pfc() - start:.4f}sec].')

        print(f'PART 2 - The global minimum location is {min(global_mins)} [{pfc() - start:.4f}sec].')
    
    ########################################################################
    # PART 2 - Reversed
    ########################################################################
    if(PART_2_REVERSED):

        # WIP - work in progess
        print("Part 2 - reversed")
        seed_ranges = parse_seeds_as_range_pairs(input[0])
        mappings = parse_all_mappings(input)

        humidities = [78,43,82,34]
        humidities_with_mappings = reverse_mappings_humidity_to_seed(humidities, mappings)
        print(humidities_with_mappings)