### IMPORTS AND GLOBAL CONSTANTS


### HELPER FUNCTIONS
def read_input_from_file(filepath:str):
    with open(filepath) as f:
        lines = f.readlines()
        lines = [l.replace('\n', '') for l in lines]
        return(lines)
    
### MAIN
if __name__ == "__main__":
    
    input = read_input_from_file('dayN_input_test.txt')
    
    
    
    
    
    print("ok")