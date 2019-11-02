import random
from char import *

############### Shell Fn ################
def check(stat):
    action(stat, CHAR_STAT, 20, [])

def attack(weapon):
    action(weapon, WEAPON, 20, ["mod", "prof"])

def damage(weapon):
    action(weapon, WEAPON, "dice", ["mod"])

def test():
    return -1

############### Helper Fn ###############
def roll_d(n):
    return random.randint(1,n)

def action(arg, dictionary, dice, bonus_sub_cats):
    """
    Rolls a dice and adds corresponding bonuses.
    dice           - either num or "dice" if dependent on arg
    bonus_sub_cats - list of sub categories for dictionary[arg]
    """

    if arg not in dictionary:
        print("ERROR: {} not found".format(arg))
        return 
    
    bonus = 0
    if len(bonus_sub_cats) == 0:
        bonus = dictionary[arg]
    else:
        for cat in bonus_sub_cats:
            bonus += dictionary[arg][cat]
    
    n = dictionary[arg][dice] if dice == "dice" else dice
    print(roll_d(n) + bonus)