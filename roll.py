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
        print(SPELL_SLOTS)
    elif int(level) in SPELL_SLOTS:
        print(SPELL_SLOTS[int(level)])
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
        SPELL_SLOTS[level] = num_slots

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
        level = dictionary[arg]["level"]
        success = consume_spell_slot(level)
        if not success:
            print("ERROR: Spell slot not available for level {} spell".format(level))
    
    bonus = 0
    if len(bonus_sub_cats) == 0:
        bonus = dictionary[arg]
    else:
        for cat in bonus_sub_cats:
            bonus += dictionary[arg][cat]
    
    n = dictionary[arg][dice] if dice == "dice" else dice
    print(roll_d(n) + bonus)

def consume_spell_slot(level):
    return