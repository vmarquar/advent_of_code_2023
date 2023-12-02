### IMPORTS AND GLOBAL CONSTANTS
import requests
import re

### HELPER FUNCTIONS
def read_input_from_file(filepath:str):
    with open(filepath) as f:
        lines = f.readlines()
        lines = [l.replace('\n', '') for l in lines]
        return(lines)
    
def find_calibration_value_from_str(input_str:str):
    """This function retrieves the first and last digit from a string and returns the combination of both as an integer.
        
        On each line, the calibration value can be found by combining the first digit
        and the last digit (in that order) to form a single two-digit number.

    Args:
        input_str (str): input string

    Raises:
        Exception: An Exception is raised when less than two digits can be found in a string or a different error occurs.
    Returns:
        calibration_value (int): the calibration value as integer, that is found in the string
    """
    digits = re.findall('\d', input_str)

    if(len(digits) == 1):
        # if there's only one digit in the string, repeat the it like in 'treb7uchet' -> '77'
        first_digit = digits[0]
        last_digit  = digits[0]

    if(len(digits) >= 2): 
        # '1abc2' --> '12'
        first_digit = digits[0]
        last_digit = digits[-1]

    if(first_digit and last_digit):
        calibration_value = f"{first_digit}{last_digit}"
        return(int(calibration_value))
    
    else:
        raise Exception(f"Error! Please check the digits={digits}.\nfirst_digit={first_digit} and/or last_digit={last_digit}")

def replace_digitwords(input_str:str):
    mapping_dict = {
                    'zero':'0',
                    'one':'1',
                    'two':'2',
                    'three':'3',
                    'four':'4',
                    'five':'5',
                    'six':'6',
                    'seven':'7',
                    'eight':'8',
                    'nine':'9'
                    }
    
    # 1) find all replacement words and order them by their beginning of the string
    #NOTE: a normal .find wont work here!
    all_findings = []
    for m in mapping_dict:       
        for found in re.finditer(m, input_str):
            all_findings.append({  'found_word':m,
                                    'start_index':found.start(),
                                    'end_index': found.end()
                                })
    all_findings_sorted = sorted(all_findings, key=lambda d: d['start_index'])

    # 2) try to replace all found words with their corresponding digits,
    #    if two digits overlap like in 'eightwo' only the first word will be replaced 'eightwo' --> '8wo' 
    replaced_str = input_str
    for finding in all_findings_sorted:
        word = finding.get('found_word')
        if(word in replaced_str):
            replaced_str = replaced_str.replace(word, mapping_dict.get(word), 1)

    return(replaced_str)

def _get_sum_from_str(line:str):
    ## ALTERNATIVE LÖSUNG, Die Rangfolge von one, two, ..., zählt vor der Rangfolge im string, e.g. 'eightwo' -> 'eigh2'
    LETTERS_TO_DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    }

    first_number, last_number = None, None

    for i, char in enumerate(line):
        if char.isdigit():
            if first_number is None:
                first_number = int(char)
            last_number = int(char)
        else:
            if i < len(line) - 2 and line[i:i+3] in LETTERS_TO_DIGITS:
                if first_number is None:
                    first_number = LETTERS_TO_DIGITS[line[i:i+3]]
                last_number = LETTERS_TO_DIGITS[line[i:i+3]]
                continue
            if i < len(line) - 3 and line[i:i+4] in LETTERS_TO_DIGITS:
                if first_number is None:
                    first_number = LETTERS_TO_DIGITS[line[i:i+4]]
                last_number = LETTERS_TO_DIGITS[line[i:i+4]]
                continue
            if i < len(line) - 4 and line[i:i+5] in LETTERS_TO_DIGITS:
                if first_number is None:
                    first_number = LETTERS_TO_DIGITS[line[i:i+5]]
                last_number = LETTERS_TO_DIGITS[line[i:i+5]]
                continue
    return(first_number, last_number, f"{first_number}{last_number}")


def get_calibration_sum(lines: list[str]) -> int:
    ### ALTERNATIVE LÖSUNG
    calibration_sum = 0

    for line in lines:
        first_number, last_number, _ = _get_sum_from_str(line)
        
        calibration_sum += int(f"{first_number}{last_number}") if first_number and last_number else 0

    return calibration_sum



### MAIN
if __name__ == "__main__":
    
    # ### PART 1
    # 1) Read input
    input = read_input_from_file('day1_input.txt')

    # 2) Retrieve calibration value
    calibration_values = [find_calibration_value_from_str(input_str) for input_str in input]
    
    # 3.1) Check the intermediary result
    if(len(calibration_values) == len(input)):
        print("Die Ergebnisse haben die gleiche Länge...proceed!")
    else:
        raise Exception("ACHTUNG: Es wurde nicht für jeden input string eine calibration value gefunden!")
    
    # 3.2) sum up everything for the checksum
    checksum_result = sum(calibration_values)
    print(f"Das Endergebnis für Part 1 lautet: '{checksum_result}'")


    ### PART 2 - FALSCH ABER DENNOCH IM LÖSUNGSBEREICH!
    # 1) Read input
    original_input = read_input_from_file('day1_input.txt')

    # 2.1 Replace digit words with digits
    replaced_input = [{'o':i, 'r':replace_digitwords(i)} for i in original_input]

    # 2.2) Retrieve calibration value
    calibration_values = [  {   'original':input_str.get('o'),
                                'replaced':input_str.get('r'),
                                'cal_val': find_calibration_value_from_str(input_str.get('r')),
                                'cal_val_correct': _get_sum_from_str(input_str.get('o'))
                            }
                        for input_str in replaced_input]
    
    # 3.1) Check the intermediary result
    if(len(calibration_values) == len(original_input)):
        print("Die Ergebnisse haben die gleiche Länge...proceed!")
    else:
        raise Exception("ACHTUNG: Es wurde nicht für jeden input string eine calibration value gefunden!")
    
    # 3.2) sum up everything for the checksum
    ## ERSTE LÖSUNG, Die Rangfolge im String zählt vor dem "Rang" der Zahl e.g. 'eightwo' -> '8wo'
    checksum_result = sum([cv.get('cal_val') for cv in calibration_values])
    print(f"Das Endergebnis für Part 2 lautet: '{checksum_result}'")

    # 4) sum up everything for the checksum --> CORRECT ANSWER!
    ## ALTERNATIVE LÖSUNG, Die Rangfolge von one, two, ..., zählt vor der Rangfolge im string, e.g. 'eightwo' -> 'eigh2'
    #### DIESE STIMMT!
    alternative_cal_sum = get_calibration_sum(original_input)
    print(f"Das alternative Endergebnis für Part 2 lautet: '{alternative_cal_sum}'")

    ###
    print("ok")

