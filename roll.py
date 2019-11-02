import random
from char import *

############### Shell Fn ################
def action(arg, dictionary, dice, bonus):
    if arg in dictionary:
        print(roll_d(dice) + bonus)
    else:
        print("ERROR: {} not found".format(arg))

def check(stat):
    if stat in CHAR_STAT:
        print(roll_d(20) + CHAR_STAT[stat])
    else:
        print_err_msg(stat)

def attack(weapon):
    if weapon in WEAPON:
        print(roll_d(20) + WEAPON[weapon]["mod"] + WEAPON[weapon]["prof"])
    else:
        print_err_msg(weapon)

def damage(weapon):
    if weapon in WEAPON:
        print(roll_d(WEAPON[weapon]["dice"]) + WEAPON[weapon]["mod"])
    else:
        print_err_msg(weapon)

def test():
    return -1

############### Helper Fn ###############
def roll_d(n):
    return random.randint(1,n)

# def print_err_msg(arg):
#     print("ERROR: {} not found".format(arg))