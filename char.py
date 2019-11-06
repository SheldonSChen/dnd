from __future__ import print_function
from sharedHelpers import *

############### Char Stats ##############
LEVEL = 3

CHAR_MODS = {
    "str": 0,
    "dex": 0,
    "con": 1,
    "int": 1,
    "wis": 2,
    "cha": 3,
}

PROF = 2

CHAR_STATS = {
    # STRENGTH
    "str":       CHAR_MODS["str"],
    "str save":  CHAR_MODS["str"],
    "athletics": CHAR_MODS["str"],

    # DEXTERITY
    "dex":        CHAR_MODS["dex"],
    "dex save":   CHAR_MODS["dex"],
    "acrobatics": CHAR_MODS["dex"],
    "sleight":    CHAR_MODS["dex"],
    "stealth":    CHAR_MODS["dex"],

    # CONSTITUTION
    "con":      CHAR_MODS["con"],
    "con save": CHAR_MODS["con"],

    # INTELLIGENCE
    "int":           CHAR_MODS["int"],
    "int save":      CHAR_MODS["int"],
    "arcana":        CHAR_MODS["int"],
    "history":       CHAR_MODS["int"] + PROF,
    "investigation": CHAR_MODS["int"],
    "nature":        CHAR_MODS["int"],
    "religion":      CHAR_MODS["int"],

    # WISDOM
    "wis":        CHAR_MODS["wis"],
    "wis save":   CHAR_MODS["wis"] + PROF,
    "animal":     CHAR_MODS["wis"],
    "insight":    CHAR_MODS["wis"] + PROF,
    "medicine":   CHAR_MODS["wis"] + PROF,
    "perception": CHAR_MODS["wis"],
    "survival":   CHAR_MODS["wis"],

    # CHARISMA
    "cha":          CHAR_MODS["cha"],
    "cha save":     CHAR_MODS["cha"] + PROF,
    "deception":    CHAR_MODS["cha"],
    "intimidation": CHAR_MODS["cha"],
    "performance":  CHAR_MODS["cha"],
    "persuasion":   CHAR_MODS["cha"] + PROF,

    # SPELL
    "spell attack": CHAR_MODS["wis"] + PROF,
    "spell save dc": 8 + CHAR_MODS["wis"] + PROF,
}

MAX_HP = 18
CUR_HP = 18

############### Money ###############
# Only the wealthy have platinum
COINAGES = ["copper", "silver", "gold", "platinum"]
EXCHANGE = [1, 10, 100, 1000]
MONEY = [0, 13, 42, 0]

############### Weapons ##############
WEAPONS = {
    "mace": {
        "mod": CHAR_STATS["str"],
        "prof": PROF,
        "dice": 6,
        },
    "dart": {
        "mod": CHAR_STATS["dex"],
        "prof": PROF,
        "dice": 4,
        },
}

############### Spells ##############
SPELLS = {
    # Level 0 (Cantrips)
    "light": {
        # touch
        # light something/someone
        "level": 0,
        },
    "spare the dying": {
        # touch
        # 0 HP being becomes stable
        "level": 0,
        },
    "toll the dead": {
        # 60ft
        # WIS save or 1d8 necrotic damage
        # 1d12 if target is missing any HP 
        "level": 0,
        "action":
            lambda _: print("d8: {} or d12: {} necrotic damage".format(roll_d(8), roll_d(12)))
        },
    "resistance": {
        # touch
        # Target roll d4 and add to saving throw once
        "level": 0,
        },
    "word of radiance": {
        # 5ft, choose target(s)
        # CON save or 1d6 radiant damage
        "level": 0,
        "action": 
            lambda _: print("{} radiant damage".format(roll_d(6)))
        },
    
    # Level 1
    "bane": {
        # 30ft, up to (2 + cast level) targets
        # CHA save or 1d4 penalty to attacks/saves
        "level": 1,
        "prepared": False,
        },
    "false life": {
        # self
        # I gain 1d4 + 5(cast level) - 1 temp HP
        "level": 1,
        "prepared": True,
        "self heal":
            lambda cast_level: roll_d(4) + 5 * cast_level -1
        },
    "command": {
        # 60ft, (cast level) targets
        # WIS save or follow command, no self harm
        "level": 1,
        "prepared": True,
        },
    "inflict wounds": {
        # touch
        # melee spell attack to hit
        # (cast level + 2)d10 necrotic damage
        "level": 1,
        "prepared": True,
        "attack roll": True,
        "action":
            lambda cast_level: print("{} necrotic damage".format(roll_d(10, cast_level + 2)))
        },
    "bless": {
        # 30ft, up to (2 + cast level) targets
        # 1d4 boost to attacks/saves
        "level": 1,
        "prepared": False,
        },
    "healing word": {
        # 60ft
        # bonus action
        # Regain (cast level)d4 + CHAR_STATS["wis"] HP
        "level": 1,
        "prepared": True,
        "action":
            lambda cast_level: print("Target regained {} HP".format(roll_d(4, cast_level) + CHAR_STATS["wis"]))
        },
    "protection from evil and good": {
        # touch
        # protection from aberrations, celestials, 
        # elementals, fey, fiends, and undead.
        # disadvantage enemy attack rolls
        # can't be charmed, frightened, or possessed
        # or advantange on save throw to rid above
        "level": 1,
        "prepared": False,
        },
    
    # Level 2
    "prayer of healing": {
        # 30ft, choose up to 6 targets
        # Each regain (cast level)d8 + CHAR_STATS["wis"] HP
        "level": 2,
        "prepared": True,
        "action":
            lambda cast_level: print("Target(s) regained {} HP".format(roll_d(8, cast_level) + CHAR_STATS["wis"]))
        },
    "aid": {
        # 30ft, choose up to 3 allies
        # Each gain 5 HP and 5 max HP
        "level": 2,
        "prepared": True,
        },
}

#TODO: get set reset uses
LONG_REST_SPELLS = {
    "healing hands": {
        # touch
        # Regain level HP
        "uses": 1,
        "max uses": 1,
        "action":
            lambda: print("Target regained {} HP".format(LEVEL))
        },
    "turn undead": {
        # 30ft
        # WIS save or undead turned
        },
    "path to the grave": {
        # 30ft
        # Target vulnerable to all of attack's damage.
        },
    "necrotic shroud": {
        # 10ft
        # CHA save or be frightened
        # TODO: LEVEL extra necrotic damage for attacks/spells
        "uses": 1,
        "max uses": 1,
        },
    "circle of mortality": {
        # When healing 0 HP creature, 
        # use max of each dice instead.
        },
    "eyes of the grave": {
        # 60ft
        # Until end of next turn,
        # know location of any undead
        # that's not hidden or protected.
        "uses": CHAR_STATS["wis"],
        "max uses": CHAR_STATS["wis"],
        },
}

SPELL_SLOTS_MAX = {
    1: 4,
    2: 2,
}

SPELL_SLOTS_REMAIN = {
    1: 4,
    2: 2,
}

############### Helper Fn ###############
def coin_to_index(coin, coinages):
    if coin in coinages:
        return coinages.index(coin)
    else:
        return -1

def print_cur_money(money, coinages):
    print("Current balance:")
    val = ""
    for i in range(len(coinages)):
        val += "{} {}, ".format(money[i], coinages[i])
    val = val[: -2]
    print(val)

def print_cur_spell_slots(spell_slots_remain, level=None):
    def print_slots(level):
        print("lvl {}: {}".format(level, spell_slots_remain[level]))

    print("Current spell slots:")
    if not level:
        for lvl in spell_slots_remain:
            print_slots(lvl)
    elif level in spell_slots_remain:
        print_slots(level)
    else:
        print("ERROR: level {} not found".format(level))

def print_long_rest_spells(long_rest_spells, spell=None):
    def print_spell(spell):
        if "uses" in long_rest_spells[spell]:
            uses = long_rest_spells[spell]["uses"]
            print("{}: {} uses remain".format(spell, uses))
        
    print("Current long spell usages left:")
    if not spell:
        for spl in long_rest_spells:
            print_spell(spl)
    elif spell in long_rest_spells:
        print_spell(spell)
    else:
        print("ERROR: long spell {} not found".format(spell))