import random

def num_in_col(input_col):
    return all(char.isdigit() for char in input_col)

def roll_d(dice, rolls=1):
    total = 0
    for i in range(rolls):
        total += random.randint(1,dice)
    return total

def convert_str_to_pairs(flat_list, key_map_fn, val_map_fn, key_check=None, val_check=None):
    ''' Converts a string into a list of (key, value) pairs.

    Args:
        flat_list (str): The string representation of the pairs ("<key> <value> ...")
        key_map_fn (func): The function to be mapped to keys
        val_map_fn (func): The function to be mapped to values
        key_check (func): Returns if key is valid type. (default=None)
        val_check (func): Returns if value is valid type. (default=None)
    
    Returns:
        The new list of pairs, or None if error
    '''

    flat_list = flat_list.split()
    if len(flat_list) == 0 or len(flat_list) % 2 != 0:
        print("ERROR: invalid list length: {}".format(flat_list))
        return None
    
    keys = flat_list[0::2]
    if key_check and not key_check(keys):
        print("Error: Invalid keys: {}".format(keys))
        return None
    keys = map(key_map_fn, keys)
    
    values = flat_list[1::2]
    if val_check and not val_check(values):
        print("Error: Invalid values: {}".format(values))
        return None
    values = map(val_map_fn, values)

    return zip(keys, values)