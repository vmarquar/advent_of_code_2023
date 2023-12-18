#--- Day 8: Haunted Wasteland ---
# PART1: 21:00 - 21:23 (23 min)

### IMPORTS AND GLOBAL CONSTANTS


### HELPER FUNCTIONS
def read_input_from_file(filepath:str):
    with open(filepath) as f:
        lines = f.readlines()
        lines = [l.replace('\n', '') for l in lines]

        navigation = list(lines[0])
        nodes = [{"current": l.split(' = (')[0], 
                    "L": l.split(' = (')[1].split(', ')[0],
                    "R": l.split(' = (')[1].split(', ')[1].split(')')[0]
                } for l in lines[2:]]

        return(navigation, nodes)
    

### PART 1 FUNCTIONS
def traverse_nodes_until_zzz(navigation:list[str], nodes:list[dict[str]]) -> int:
    starting_node = [n for n in nodes if n['current'] == 'AAA'][0] # AAA is the starting node
    next_node = starting_node
    print(next_node)
    zzz_reached = False
    number_of_turns = 0
    while(zzz_reached == False):
        for turn in navigation:
            next_node = [n for n in nodes if n['current'] == next_node[turn]][0]
            number_of_turns += 1
            print(next_node)
            if(next_node['current'] == 'ZZZ'):
                print(f"ZZZ reached after {number_of_turns} turns")
                #zzz_reached = True
                #break
                return(number_of_turns)

    
### MAIN
if __name__ == "__main__":
    
    #0) Read navigation and nodes from input file
    navigation, nodes = read_input_from_file('./input/day08_input.txt')

    ### PART 1 ###
    #1) Find the ZZZ node by travelling the navigation sequence, starting from AAA
    #number_of_turns = traverse_nodes_until_zzz(navigation, nodes)

    ### PART 2 ###
    starting_nodes = [n for n in nodes if n['current'][2] == 'A'] # xxA are the starting nodes
    end_nodes = [n for n in nodes if n['current'][2] == 'Z'] # xxZ are the end nodes
    
    next_nodes = starting_nodes
    print(next_nodes)
    all_xxZ_reached = False
    number_of_turns = 0
    while(all_xxZ_reached == False):
        for turn in navigation:
            
            next_node_ids = [n[turn] for n in next_nodes]
            next_nodes = [n for n in nodes if n['current'] in next_node_ids]
            #print(next_nodes)
            
            number_of_turns += 1
            
            if(all([next_node['current'][2] == 'Z' for next_node in next_nodes])):
                print(f"All xxZ reached after {number_of_turns} turns")
                all_xxZ_reached = True
                break

            if(number_of_turns % 100_000 == 0):
                print(f"Still running...Current number of turns: {number_of_turns:e}") # format in scientific notation
                
    print("ok")