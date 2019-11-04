import random
from char import *

#TODO: All int converts need a check!

############### Shell Fn ################
def check(stat):
    action(stat, CHAR_STATS, 20, [])

def attack(weapon):
    action(weapon, WEAPONS, 20, ["mod", "prof"])

def damage(weapon):
    action(weapon, WEAPONS, "dice", ["mod"])

def cast(spell_level):
    if contains_num(spell_level):
        spell_level = spell_level.rsplit(" ", 1)
        spell = spell_level[0]
        level = int(spell_level[1])
    else:
        spell = spell_level
        level = None
    action(spell, SPELLS, 20, [], True, level)

def get_slots(level):    
    if not level:
        print(SPELL_SLOTS_REMAIN)
    elif int(level) in SPELL_SLOTS_REMAIN:
        print(SPELL_SLOTS_REMAIN[int(level)])
    else:
        print("ERROR: level {} not found".format(level))

def set_slots(level_slots_flat):
    level_slots = convert_flat_to_pairs(level_slots_flat, SPELL_SLOTS, int, int, int)
    if not level_slots:
        return

    for level, num_slots in level_slots:
        SPELL_SLOTS_REMAIN[level] = num_slots

def reset_slots():
    global SPELL_SLOTS_REMAIN # need global tag for global var assignment in func
    SPELL_SLOTS_REMAIN = SPELL_SLOTS.copy()

def get_money():
    print(MONEY)

def spend_money(coin_amount_flat):
    coin_amount = convert_flat_to_pairs(coin_amount_flat, COINAGE, coin_to_index, int)
    if not coin_amount:
        return

    # check if I have enough money
    MONEY_TEMP = MONEY
    spendable = True
    print(coin_amount)
    # for coin, amount_spent in coin_amount:
    #     if MONEY[coin]["amount"] > amount_spent:
    #         MONEY[coin]["amount"] -= amount_spent
    #     else:
    #         spent = False
    #         larger_coin = MONEY[coin]["next"]
    #         while larger_coin and not spent:
    #             coin = MONEY[coin]["next"]
    #             amount_spent /= 10.0
    #             if MONEY[coin]["amount"] > amount_spent:
    #                 MONEY[coin]["amount"] -= amount_spent
    
    # if not spendable:
    #     global MONEY
    #     MONEY = MONEY_TEMP
    #     print("ERROR: insufficient funds")
    #     return
    
    # print("{} remaining".format(MONEY))

def get_hp():
    print(CUR_HP)

def set_hp(hp):
    if not contains_num(hp):
        print("ERROR: Invalid hp {}".format(hp))
        return

    global CUR_HP
    CUR_HP = int(hp)

def take_damage(damage):
    if not contains_num(damage):
        print("ERROR: Invalid damage {}".format(damage))
        return

    remaining_hp = CUR_HP - int(damage)
    set_hp(remaining_hp)

def test(arg):
    print(arg)

############### Helper Fn ###############
def coin_to_index(coin):
    if coin in COINAGE:
        return COINAGE.index(coin)
    else:
        return -1

def contains_num(input_string):
    return any(char.isdigit() for char in input_string)

def roll_d(n):
    return random.randint(1,n)

def action(arg, dictionary, dice, bonus_sub_cats, is_spell=False, spell_level=None):
    """
    Rolls a dice and adds corresponding bonuses.
    dice           - either num or "dice" if dependent on arg
    bonus_sub_cats - list of sub categories for dictionary[arg]
    """

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
    
    # bonus = 0
    # if len(bonus_sub_cats) == 0:
    #     bonus = dictionary[arg]
    # else:
    #     for cat in bonus_sub_cats:
    #         bonus += dictionary[arg][cat]
    
    # n = dictionary[arg][dice] if dice == "dice" else dice
    # print(roll_d(n) + bonus)

def consume_spell_slot(level):
    """
    Every time a spell is casted, a level's spell slot is consumed.
    Level 0 spells (i.e. Cantrips) do not consume any slots.
    Spells can be casted at a higher level as well.
    """
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
    """
    Converts a string into a list of (key, value) pairs
    Applies the appropriate mappings to keys and values
    flat_list - raw string representation ("<key> <value> ...")
    dictionary - dict that should contain all the keys in flat_list
    key_map_fn - function to be mapped to keys
    val_map_fn - function to be mapped to values
    pre_convert_key_fn - function to be mapped to keys before dict check
    Returns the new list of pairs, or None if error
    """

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
    return zip(keys, values)
