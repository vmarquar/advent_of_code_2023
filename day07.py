#--- Day 7: Camel Cards ---

### IMPORTS AND GLOBAL CONSTANTS
from time import perf_counter as pfc

### HELPER FUNCTIONS
def read_input_from_file(filepath:str):
    with open(filepath) as f:
        lines = f.readlines()
        lines = [l.replace('\n', '') for l in lines]
        hands = [{"hand":l.split(' ')[0], "bid":int(l.split(' ')[1])} for l in lines]
        return(hands)

def get_secord_order_rank(hand:str) -> dict[int]:
    # prework: get all unique cards
    # from functools import reduce
    # lines = f.readlines()
    # lines = [line.split(' ')[0] for line in lines]
    # set(reduce(lambda x,y: x+y, [list(i) for i in lines]))

    # A is the highest card, 2 the lowest create a constant card_to_rank dict A to Z, 9 to 2
    card_to_rank = {'A':12,
                    'K':11,
                    'Q':10,
                    'J':9,
                    'T':8,
                    '9':7,
                    '8':6,
                    '7':5,
                    '6':4,
                    '5':3,
                    '4':2,
                    '3':1,
                    '2':0
                    }
    first_card_rank = card_to_rank[hand[0]]
    second_card_rank = card_to_rank[hand[1]]
    third_card_rank = card_to_rank[hand[2]]
    fourth_card_rank = card_to_rank[hand[3]]
    fifth_card_rank = card_to_rank[hand[4]]
    return({"second_order_rank_first_card_rank":first_card_rank,
            "second_order_rank_second_card_rank":second_card_rank,
            "second_order_rank_third_card_rank":third_card_rank,
            "second_order_rank_fourth_card_rank":fourth_card_rank,
            "second_order_rank_fifth_card_rank":fifth_card_rank})

def get_type_of_hand(hand:dict[str | int]) -> dict[str | int]:
    counts = {}
    for c in hand['hand']:
        if(counts.get(c, None) is not None):
            counts[c] += 1
        else:
            counts[c] = 1
    
    hand_type = None
    hand_type_rank = 0
    card1 = None
    card2 = None
    if(max(counts.values()) == 5):
        hand_type = "Five of a kind"
        hand_type_rank = 6
        card1 = max(counts, key=counts.get)
        card2 = None
    elif(max(counts.values()) == 4):
        hand_type = "Four of a kind"
        hand_type_rank = 5
        card1 = max(counts, key=counts.get)
        card2 = None
    elif(max(counts.values()) == 3 and min(counts.values()) == 2):
        hand_type = "Full house"
        hand_type_rank = 4
        card1 = [k for k,v in counts.items() if v == 3][0]
        card2 = [k for k,v in counts.items() if v == 2][0]
    elif(max(counts.values()) == 3):
        hand_type = "Three of a kind"
        hand_type_rank = 3
        card1 = max(counts, key=counts.get)
        card2 = None
    elif(max(counts.values()) == 2 and len(counts.values()) == 3):
        hand_type = "Two pairs"
        hand_type_rank = 2
        card1, card2 = [k for k,v in counts.items() if v == 2]
    elif(max(counts.values()) == 2):
        hand_type = "One pair"
        hand_type_rank = 1
        card1 = max(counts, key=counts.get)
        card2 = None
    else:
        hand_type_rank = 0
        hand_type = "Nothing"
    
    additional_ranks = get_secord_order_rank(hand['hand'])

    return({**{"hand_type": hand_type, 
            "hand_type_rank":hand_type_rank,
            "card1": card1,
            "card2": card2,
            "bid": hand['bid'],
            "hand": hand['hand']}, **additional_ranks})

def order_typed_hands(typed_hands:list[dict[str | int]]) -> list[dict[str | int]]:
    unique_hand_type_ranks = sorted(set([h['hand_type_rank'] for h in typed_hands])) # get full dict of unique hand_types
    #unique_hand_type_ranks = [0,1,2,3,4,5,6] # faster than a sorted set?

    ordered_hands = []
    for hand_type_rank in unique_hand_type_ranks: 
        # FIRST ORDERING RULE IS AUTOMATICALY FULFILLED BY LOOPING BY HAND_TYPE_RANK
        print(hand_type_rank)
        # filter typed_hands by hand_type
        filtered_hands = [h for h in typed_hands if h['hand_type_rank'] == hand_type_rank]
        # sort filtered_hands by card1 and card2 (completety unneccessary but nice to have)
        filtered_hands = sorted(filtered_hands, key=lambda k: [k['card1'],k['card2']] , reverse=False)


        # SECOND ORDERING RULE
        filtered_hands = sorted(filtered_hands, key=lambda k: (k['second_order_rank_first_card_rank'],
                                                                k['second_order_rank_second_card_rank'], 
                                                                k['second_order_rank_third_card_rank'],
                                                                k['second_order_rank_fourth_card_rank'],
                                                                k['second_order_rank_fifth_card_rank']
                                                                ) , reverse=False)
        ordered_hands.extend(filtered_hands)      
    return(ordered_hands)

### MAIN
if __name__ == "__main__":
    
    #0) start counter
    start = pfc()

    # 1) read input and parse hands and bids
    hands = read_input_from_file('./input/day07_input.txt')
    
    # 2) get type of hands
    typed_hands = [get_type_of_hand(hand) for hand in hands]

    # 3) order hands by hand_type_rank and second_order_rank
    ordered_hands = order_typed_hands(typed_hands)

    # 4) calculate score
    multiplied_bids = [(index_hand[0]+1) * index_hand[1]['bid'] for index_hand in enumerate(ordered_hands)]
    print(f"PART 1: The sum of the multiplied bids are '{sum(multiplied_bids)}' ({pfc() - start:.4f}s).")