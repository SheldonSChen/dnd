############### Char Stats ##############
CHAR_ABILITY = {
    "str": 0,
    "dex": 0,
    "con": 1,
    "int": 1,
    "wis": 2,
    "cha": 3,
}

PROF = 2

CHAR_STAT = {
    # STRENGTH
    "str":       CHAR_ABILITY["str"],
    "str save":  CHAR_ABILITY["str"],
    "athletics": CHAR_ABILITY["str"],

    # DEXTERITY
    "dex":        CHAR_ABILITY["dex"],
    "dex save":   CHAR_ABILITY["dex"],
    "acrobatics": CHAR_ABILITY["dex"],
    "sleight":    CHAR_ABILITY["dex"],
    "stealth":    CHAR_ABILITY["dex"],

    # CONSTITUTION
    "con":      CHAR_ABILITY["con"],
    "con save": CHAR_ABILITY["con"],

    # INTELLIGENCE
    "int":           CHAR_ABILITY["int"],
    "int save":      CHAR_ABILITY["int"],
    "arcana":        CHAR_ABILITY["int"],
    "history":       CHAR_ABILITY["int"] + PROF,
    "investigation": CHAR_ABILITY["int"],
    "nature":        CHAR_ABILITY["int"],
    "religion":      CHAR_ABILITY["int"],

    # WISDOM
    "wis":        CHAR_ABILITY["wis"],
    "wis save":   CHAR_ABILITY["wis"] + PROF,
    "animal":     CHAR_ABILITY["wis"],
    "insight":    CHAR_ABILITY["wis"] + PROF,
    "medicine":   CHAR_ABILITY["wis"] + PROF,
    "perception": CHAR_ABILITY["wis"],
    "survival":   CHAR_ABILITY["wis"],

    # CHARISMA
    "cha":          CHAR_ABILITY["cha"],
    "cha save":     CHAR_ABILITY["cha"] + PROF,
    "deception":    CHAR_ABILITY["cha"],
    "intimidation": CHAR_ABILITY["cha"],
    "performance":  CHAR_ABILITY["cha"],
    "persuasion":   CHAR_ABILITY["cha"] + PROF,
}

############### Weapons ##############
WEAPON = {
    "mace": {
        "mod": CHAR_ABILITY["str"],
        "prof": PROF,
        "dice": 6,
        },
    "dart": {
        "mod": CHAR_ABILITY["dex"],
        "prof": PROF,
        "dice": 4,
        },
}

############### Spells ##############