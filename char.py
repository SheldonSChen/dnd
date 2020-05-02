from __future__ import print_function
from sharedHelpers import *

############### Char Stats ##############
LEVEL = 6
#remember cantrips change next at lvl 11
#TODO: natural 20 rolls

CHAR_MODS = {
    "str": 0,
    "dex": 0,
    "con": 1,
    "int": 1,
    "wis": 3,
    "cha": 3,
}

PROF = 3

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

    # Initiative is just dex check.
    "initiative": CHAR_MODS["dex"],

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

MAX_HIT_DICE = LEVEL
# Saved in external file
# CUR_HIT_DICE = 5
HIT_DICE_TYPE = 8

MAX_HP = 41
# Saved in external file
# CUR_HP = 13

# Saved in external file
# DEATH_SAVE_SUCCESS = 0
# DEATH_SAVE_FAILURE = 0

# Saved in external file
BONUSES = {
    "attack": [],
    "damage": [],
    "save": [],
}

############### Money ###############
# Only the wealthy have platinum
COINAGES = ["copper", "silver", "gold", "platinum"]
EXCHANGE = [1, 10, 100, 1000]
# Saved in external file
# MONEY = [0, 13, 42, 0]

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
        # WIS save or 2d8 necrotic damage
        # 2d12 if target is missing any HP 
        "level": 0,
        "damage":
            lambda _: [roll_d(8, 2), roll_d(12, 2)]
        },
    "resistance": {
        # touch
        # Target roll d4 and add to saving throw once
        "level": 0,
        },
    "word of radiance": {
        # 5ft, choose target(s)
        # CON save or 2d6 radiant damage
        "level": 0,
        "damage": 
            lambda _: [roll_d(6, 2)]
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
        "prepared": False,
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
        "damage":
            lambda cast_level: [roll_d(10, cast_level + 2)]
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
        "heal":
            lambda cast_level: roll_d(4, cast_level) + CHAR_STATS["wis"]
        },
    "protection from evil and good": {
        # touch
        # protection from aberrations, celestials, 
        # elementals, fey, fiends, and undead.
        # disadvantage enemy attack rolls
        # can't be charmed, frightened, or possessed
        # or advantange on save throw to rid above
        "level": 1,
        "prepared": True,
        },
    
    # Level 2
    "prayer of healing": {
        # 30ft, choose up to 6 targets
        # Each regain (cast level)d8 + CHAR_STATS["wis"] HP
        "level": 2,
        "prepared": True,
        "heal":
            lambda cast_level: roll_d(8, cast_level) + CHAR_STATS["wis"]
        },
    "aid": {
        # 30ft, choose up to 3 allies
        # Each gain 5 HP and 5 max HP
        "level": 2,
        "prepared": True,
        },
    "spiritual weapon": {
        "level": 2,
        "prepared": False,
        "attack roll": True,
        "damage":
            lambda cast_level: [roll_d(8, 3 * cast_level / 2 - 2) + CHAR_STATS["wis"]]
        },
    "lesser restoration": {
        # touch
        # End disease or afflicted condition.
        "level": 2,
        "prepared": True,
    },

    # Level 3
    "beacon of hope": {
        # 30ft, any number of creatures
        # 1 minute
        # Adv on wis saves and death saves, and regains max from healing.
        "level": 3,
        "prepared": True,
        },
    "revivify": {
        # touch
        # Creature that has died within the last minute returns to life with 1 HP. 
        # Can't for died of old age, can't restore missing body parts.
        # Costs diamonds worth 300 gp.
        "level": 3,
        "prepared": True,

    }
}

CHANNEL_DIVINITY_USES = 2
# Saved in external file
# CHANNEL_DIVINITIES = {
#     "turn undead": {
#         # 30ft
#         # WIS save or undead turned
#         # If an undead fails its saving throw against your Turn Undead feature, 
#         # the creature is instantly destroyed if its challenge rating is at or below 1/2.
#         "uses": CHANNEL_DIVINITY_USES,
#         "max uses": CHANNEL_DIVINITY_USES,
#         },
#     "path to the grave": {
#         # 30ft
#         # Target vulnerable to all of attack's damage.
#         "uses": CHANNEL_DIVINITY_USES,
#         "max uses": CHANNEL_DIVINITY_USES,
#         },
#     "circle of mortality": {
#         # When healing 0 HP creature, 
#         # use max of each dice instead.
#         # ALWAYS APPLIES
#         },
# }

# Saved in external file
# LONG_REST_SPELLS = {
#     "healing hands": {
#         # touch
#         # Regain level HP
#         "uses": 1,
#         "max uses": 1,
#         "action":
#             lambda: print("Target regained {} HP".format(LEVEL))
#         },
#     "necrotic shroud": {
#         # 10ft
#         # CHA save or be frightened
#         # TODO: LEVEL extra necrotic damage for attacks/spells
#         "uses": 1,
#         "max uses": 1,
#         },
#     "eyes of the grave": {
#         # 60ft
#         # Until end of next turn,
#         # know location of any undead
#         # that's not hidden or protected.
#         "uses": CHAR_STATS["wis"],
#         "max uses": CHAR_STATS["wis"],
#         },
#     "sentinel at death's door": {
#         # 30ft
#         # Reaction, myself or ally
#         # change critical hit to 
#         # normal hit, effects cancelled.
#         "uses": CHAR_STATS["wis"],
#         "max uses": CHAR_STATS["wis"],
#         },
# }

SPELL_SLOTS_MAX = {
    1: 4,
    2: 2,
    3: 3,
}

# Saved in external file
# SPELL_SLOTS_REMAIN = {
#     1: 1,
#     2: 2,
# }

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