############### Char Stats ##############
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
}

############### Weapons ##############
WEAPONS = {
    "mace": {
        "mod": CHAR_MODS["str"],
        "prof": PROF,
        "dice": 6,
        },
    "dart": {
        "mod": CHAR_MODS["dex"],
        "prof": PROF,
        "dice": 4,
        },
}

############### Spells ##############
SPELL_SAVE_DC = 8 + PROF + CHAR_MODS["wis"]
"""
Making a spell attack = 1d20 + Spell Attack Bonus
Spell Attack Bonus = Proficiency + Wisdom mod
Healing Word = 1d4/spell level + Wis mod
Cure Wounds = 1d8/spell level + Wis mod

Every time a spell is casted, a slot is consumed.
Spells can be casted at a higher level as well.

TODO: Spell slot calc (consume get/set and reset), attack bonus
different die and mods for each spell perhaps? 
"""
SPELLS = {
    # Level 0 (Cantrips)
    "light": {
        "level": 0,
        },
    "spare the dying": {
        "level": 0,
        },
    "toll the dead": {
        "level": 0,
        },
    "resistance": {
        "level": 0,
        },
    "word of radiance": {
        "level": 0,
        },
    
    # Level 1
    "bane": {
        "level": 1,
        "prepared": False,
        },
    "false life": {
        "level": 1,
        "prepared": True,
        },
    "detect evil and good": {
        "level": 1,
        "prepared": False,
        },
    "bless": {
        "level": 1,
        "prepared": True,
        },
    "healing word": {
        "level": 1,
        "prepared": True,
        },
    "protection from evil and good": {
        "level": 1,
        "prepared": False,
        },
    
    # Level 2
    "prayer of healing": {
        "level": 2,
        "prepared": True,
        },
    "calm emotions": {
        "level": 2,
        "prepared": True,
        },
}

SPELL_SLOTS = {
    1: 4,
    2: 2,
}

SPELL_SLOTS_REMAIN = SPELL_SLOTS.copy()