import random
from char import *

############### Shell Fn ################
def check(stat):
    action(stat, CHAR_STATS, 20, [])

def attack(weapon):
    action(weapon, WEAPONS, 20, ["mod", "prof"])

def damage(weapon):
    action(weapon, WEAPONS, "dice", ["mod"])

def cast(spell, level=None):
    '''
    Casts a spell.

    Args:
        spell (str): The spell to be cast.
        level (int): The level at which to cast the spell. (default=None)
    '''
    action(spell, SPELLS, 20, [], True, level)

def get_slots(level=None):    
    if not level:
        print_cur_spell_slots()
    elif level in SPELL_SLOTS_REMAIN:
        print("lvl {}: {}".format(level, SPELL_SLOTS_REMAIN[level]))
    else:
        print("ERROR: level {} not found".format(level))

def set_slots(level_slots):
    levels, slots = zip(*level_slots)
    if not all(level in SPELL_SLOTS_MAX for level in levels):
        print("ERROR: Invalid levels: {}".format(levels))
        return
    if not all(slot >= 0 for slot in slots):
        print("ERROR: Invalid slots: {}".format(slots))
        return

    for level, slots in level_slots:
        SPELL_SLOTS_REMAIN[level] = slots
    
    print("SUCCESS: Your slots are now: {}".format(SPELL_SLOTS_REMAIN))

def reset_slots():
    global SPELL_SLOTS_REMAIN # need global tag for global var assignment in func
    SPELL_SLOTS_REMAIN = SPELL_SLOTS_MAX.copy()

def get_money():
    print_cur_money()

def transaction(amounts_coinage, earn_or_spend):
    amounts, coinages = zip(*amounts_coinage)
    if not all(coinage in COINAGE for coinage in coinages):
        print("ERROR: Invalid coinages: {}".format(coinages))
        return
    if not all(amount >= 0 for amount in amounts):
        print("ERROR: Invalid amounts: {}".format(amounts))
        return
    if not (earn_or_spend == "earn" or earn_or_spend == "spend"):
        print("ERROR: Invalid transaction type: {}".format(earn_or_spend))
        return

    if earn_or_spend == "spend":
        # check if I have enough money
        total_spend = 0
        for amount, coinage in amounts_coinage:
            total_spend += amount * (10 ** coin_to_index(coinage))

        total_money = 0
        for amount in reversed(MONEY):
            total_money = total_money * 10 + amount

        if total_spend > total_money:
            print("ERROR: Insufficient funds")
            return 
        
        remaining_money = total_money - total_spend
        # Ignore platinum. Exchange for least coins possible
        for i in range(coin_to_index("gold")):
            MONEY[i] = remaining_money % 10
            remaining_money /= 10
        MONEY[coin_to_index("gold")] = remaining_money

    elif earn_or_spend == "earn":
        # Assumed cannot exchange when receiving specific coins.
        for amount, coinage in amounts_coinage:
            MONEY[coin_to_index(coinage)] += amount

    print_cur_money()

def get_hp():
    print("Your current HP: {}".format(CUR_HP))
    print("Your current MAX HP: {}".format(MAX_HP))

def set_hp(hp, hp_type=None):
    '''
    Sets either the current hp or max hp.
    hp - (int) new hp value
    hp_type - (string) "max" if max hp is to be set.
    '''
    if not num_in_str(hp, all):
        print("ERROR: Invalid hp {}".format(hp))
        return
    hp = int(hp)
    
    if hp_type and hp_type != "max":
        print("ERROR: Invalid HP type: {}".format(hp_type))
        return
    
    if hp_type == None:
        global CUR_HP
        CUR_HP = hp
    elif hp_type == "max":
        global MAX_HP
        MAX_HP = hp

    get_hp()

def take_damage(damage):
    '''
    Player takes damage.
    damage - (int) damage received.
    '''
    remaining_hp = CUR_HP - damage
    set_hp(remaining_hp)

def test(arg):
    print(arg)

############### Helper Fn ###############
def coin_to_index(coin):
    if coin in COINAGE:
        return COINAGE.index(coin)
    else:
        return -1

def print_cur_money():
    print("Current balance:")
    val = ""
    for i in range(len(COINAGE)):
        val += "{} {}, ".format(MONEY[i], COINAGE[i])
    val = val[: -2]
    print(val)

def print_cur_spell_slots():
    print("Current spell slots:")
    val = ""
    for level in SPELL_SLOTS_REMAIN:
        val += "lvl {}: {}, ".format(level, SPELL_SLOTS_REMAIN[level])
    val = val[: -2]
    print(val)

def num_in_str(input_string, any_or_all):
    return any_or_all(char.isdigit() for char in input_string)

def roll_d(n):
    return random.randint(1,n)

def action(arg, dictionary, dice, bonus_sub_cats, is_spell=False, spell_level=None):
    '''
    Rolls a dice and adds corresponding bonuses.
    dice           - either num or "dice" if dependent on arg
    bonus_sub_cats - list of sub categories for dictionary[arg]
    '''

    if arg not in dictionary:
        print("ERROR: {} not found".format(arg))
        return 
    
    if is_spell:
        # spell prepared? (level 0 always prepared)
        if dictionary[arg]["level"] > 0 and not dictionary[arg]["prepared"]:
            print("ERROR: {} is not prepared. Cannot be cast".format(arg))
            return
        
        # cast level greater than base level?
        base_level = dictionary[arg]["level"]
        if not spell_level:
            spell_level = base_level
        if spell_level < base_level:
            print("Spell must be cast at level {} or higher.".format(base_level))
            return
        
        # spell slot available? 
        success = consume_spell_slot(spell_level)
        if not success:
            print("ERROR: Spell slot not available for level {}".format(spell_level))
            return
    
    bonus = 0
    if len(bonus_sub_cats) == 0:
        bonus = dictionary[arg]
    else:
        for cat in bonus_sub_cats:
            bonus += dictionary[arg][cat]
    
    n = dictionary[arg][dice] if dice == "dice" else dice
    print(roll_d(n) + bonus)

def consume_spell_slot(level):
    '''
    Every time a spell is casted, a level's spell slot is consumed.
    Level 0 spells (i.e. Cantrips) do not consume any slots.
    Spells can be casted at a higher level as well.
    '''
    if level == 0:
        return True

    curr_level = level
    consumed = False
    while not consumed and curr_level in SPELL_SLOTS_REMAIN:
        if SPELL_SLOTS_REMAIN[curr_level] > 0:
            SPELL_SLOTS_REMAIN[curr_level] -= 1
            consumed = True
        else:
            curr_level += 1
    
    return consumed

def convert_flat_to_pairs(flat_list, dictionary, key_map_fn, val_map_fn, pre_convert_key_fn=None):
    ''' Converts a string into a list of (key, value) pairs.

    Applies the appropriate mappings to keys and values
    Values must all be non-negative.

    Args:
        flat_list (str): The string representation of the pairs ("<key> <value> ...")
        dictionary (dict): The dict that should contain all the keys in flat_list
        key_map_fn (func): The function to be mapped to keys
        val_map_fn (func): The function to be mapped to values
        pre_convert_key_fn (func): function to be mapped to keys before dict check (default=None)
    
    Returns:
        The new list of pairs, or None if error
    '''

    flat_list = flat_list.split()
    if len(flat_list) == 0 or len(flat_list) % 2 != 0:
        print("ERROR: invalid arg {}".format(flat_list))
        return None

    keys = flat_list[0::2]
    if pre_convert_key_fn:
        keys = map(pre_convert_key_fn, keys)
    if not all(key in dictionary for key in keys):
        print("ERROR: given key(s) does not exist: {}".format(keys))
        return None

    keys = map(key_map_fn, flat_list[0::2])
    values = map(val_map_fn, flat_list[1::2])
    
    if any(val < 0 for val in values):
        print("ERROR: Invalid values: {}".format(values))
        return None
    
    return zip(keys, values)