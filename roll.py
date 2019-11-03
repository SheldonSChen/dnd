import random
from char import *

############### Shell Fn ################
def check(stat):
    action(stat, CHAR_STATS, 20, [])

def attack(weapon):
    action(weapon, WEAPONS, 20, ["mod", "prof"])

def damage(weapon):
    action(weapon, WEAPONS, "dice", ["mod"])

def cast(spell):
    action(spell, SPELLS, 20, [], True)

def get_slots(level):    
    if not level:
        print(SPELL_SLOTS_REMAIN)
    elif int(level) in SPELL_SLOTS_REMAIN:
        print(SPELL_SLOTS_REMAIN[int(level)])
    else:
        print("ERROR: level {} not found".format(level))

def set_slots(level_slots_flat):
    level_slots = map(int, level_slots_flat.split())
    if len(level_slots) == 0 or len(level_slots) % 2 != 0:
        print("ERROR: invalid arg {}".format(level_slots_flat))
        return

    # level_slots is list of (level, slot) pairs
    level_slots = zip(level_slots[0::2], level_slots[1::2])
    for level, num_slots in level_slots:
        SPELL_SLOTS_REMAIN[level] = num_slots

def reset_slots():
    global SPELL_SLOTS_REMAIN # need global tag for global var assignment in func
    SPELL_SLOTS_REMAIN = SPELL_SLOTS.copy()

def test():
    return -1

############### Helper Fn ###############
def roll_d(n):
    return random.randint(1,n)

def action(arg, dictionary, dice, bonus_sub_cats, is_spell=False):
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
        
        # spell slot available?
        level = dictionary[arg]["level"]
        success = consume_spell_slot(level)
        if not success:
            print("ERROR: Spell slot not available for level {} spell".format(level))
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