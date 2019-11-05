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

    # SPELL
    "spell save dc": 8 + CHAR_MODS["wis"] + PROF,
    "spell attack": CHAR_MODS["wis"] + PROF,
}

############### Money ###############
# Only the wealthy have platinum
COINAGE = ["copper", "silver", "gold", "platinum"]
EXCHANGE = [1, 10, 100, 1000]
MONEY = [0, 13, 42, 0]

MAX_HP = 18
CUR_HP = 18

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
'''
Making a spell attack = 1d20 + Spell Attack Bonus
Spell Attack Bonus = Proficiency + Wisdom mod

TODO: attack bonus
different die and mods for each spell perhaps
cast spells at specific levels
other spells on first page - once every long_rest 
'''
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
        },
    
    # Level 1
    "bane": {
        # 30ft, up to (2 + cast level) targets
        # CHA save or 1d4 penalty to attacks/saves
        "level": 1,
        "prepared": True,
        },
    "false life": {
        # self
        # Gain 1d4 + 5(cast level) - 1 temp HP
        "level": 1,
        "prepared": False,
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
        },
    "aid": {
        # 30ft, choose up to 3 allies
        # Each gain 5 HP and 5 max HP
        "level": 2,
        "prepared": True,
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