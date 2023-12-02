### IMPORTS AND GLOBAL CONSTANTS
MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

### HELPER FUNCTIONS
def read_input_from_file(filepath:str):
    with open(filepath) as f:
        lines = f.readlines()
        lines = [l.replace('\n', '') for l in lines]
        return(lines)
    
def parse_game_from_str(line:str):
    # 1) parse input string to receive
    game_id = int(line.split(': ')[0].replace('Game ',''))

    # count all red, blues and green cubes per game
    sets = line.split(': ')[1].split('; ')
    reds_possible = []
    greens_possible = []
    blues_possible = []
    reds = []
    greens = []
    blues = []
    
    for set in sets:
        subsets = set.split(', ')
        for subset in subsets:
            if('red' in subset):
                red = int(subset.split(' ')[0])
                reds.append(red)
                reds_possible.append(MAX_RED >= red)
            if('green' in subset):
                green = int(subset.split(' ')[0])
                greens.append(green)
                greens_possible.append(MAX_GREEN >= green)
            if('blue' in subset):
                blue = int(subset.split(' ')[0])
                blues.append(blue)
                blues_possible.append(MAX_BLUE >= blue)

    # would the game be possible?
    game_possible = True if (all(reds_possible) and all(blues_possible) and all(greens_possible)) else False
    print(f"The game #{game_id} would be {'possible' if(game_possible) else 'NOT possible'}!")

    #The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
    #  The power of the minimum set of cubes in game 1 is 48. 
    # In games 2-5 it was 12, 1560, 630, and 36, respectively. 
    # Adding up these five powers produces the sum 2286.
    min_greens = max(greens if len(greens) > 0 else [0])
    min_blues = max(blues if len(blues) > 0 else [0])
    min_reds = max(reds if len(reds) > 0 else [0])
    power = min_blues * min_reds * min_greens

    game = {
        'input':line,
        'game_id':game_id,
        'min_blues':min_blues,
        'min_reds':min_reds,
        'min_greens':min_greens,
        'power':power,
        'game_possible': game_possible
    }
    return(game)



### MAIN
if __name__ == "__main__":
    input = read_input_from_file('./input/day2_input.txt')

    # 1) parse input string to receive
    games = [parse_game_from_str(i) for i in input]    
    
    # 2) Sum up game ids
    correct_games = [game for game in games if game.get('game_possible')]
    correct_game_ids = [game.get('game_id') for game in games if game.get('game_possible')]
    sum_of_game_ids = sum(correct_game_ids)
    print(f"Die Summe der richtigen Game-IDs lautet {sum_of_game_ids}")
    
    # 3) Create power sums
    #For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
    sum_of_powers = sum([game['power'] for game in games])   
    print(f"Die Summe der Power-Zahl lautet {sum_of_powers}")

    print("ok")