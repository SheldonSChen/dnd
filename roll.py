from char import *
from sharedHelpers import *
# TODO: rolling w/ ADVANTAGE, and boosts!

############### Shell Fn ################
def get(stat):
    if stat not in CHAR_STATS:
        print("ERROR: {} not valid stat.".format(stat))
        return
    
    print(CHAR_STATS[stat])

def check(stat):
    action(stat, CHAR_STATS, 20, [])

def attack(weapon):
    action(weapon, WEAPONS, 20, ["mod", "prof"])

def damage(weapon):
    action(weapon, WEAPONS, "dice", ["mod"])

def cast(spell, level=None):
    '''
    Casts a spell or long rest spell.

    Args:
        spell (str): The spell to be cast.
        level (int): The level at which to cast the spell. (default=None)
    '''
    # TODO: incorporate LONG_REST_SPELLS
    if spell in SPELLS:
        # spell prepared? (level 0 always prepared)
        if SPELLS[spell]["level"] > 0 and not SPELLS[spell]["prepared"]:
            print("ERROR: {} is not prepared. Cannot be cast".format(spell))
            return
        
        # cast level greater than base level?
        base_level = SPELLS[spell]["level"]
        search_slot = False
        # cast level not specified, default to base, can cast at any higher level
        if level == None:
            level = base_level
            search_slot = True
        
        if level < base_level:
            print("Spell must be cast at level {} or higher.".format(base_level))
            return
        
        # spell slot available? if so, consume
        cast_level = consume_spell_slot(level, search_slot)
        if cast_level == None:
            print("ERROR: Spell slot not available for level {}".format(level))
            return
        
        if "attack roll" in SPELLS[spell]:
            print("Spell attack: {}".format(roll_d(20) + CHAR_STATS["spell attack"]))
        
        if "self heal" in SPELLS[spell]:
            hp_change(SPELLS[spell]["self heal"](cast_level))

        if "action" in SPELLS[spell]:
            SPELLS[spell]["action"](cast_level)

        print("{} was cast at level {}.".format(spell, cast_level))
    elif spell in LONG_REST_SPELLS:
        if level != None:
            print("ERROR: Unnecessary level specified: {}".format(level))
            return
        cast_long_spell(spell)
    else:
        print("ERROR: {} not found".format(spell))

# Can probably combine get_long_spell_usage() and get_slots()
def get_long_spell_usage(spell=None):
    print_long_rest_spells(LONG_REST_SPELLS, spell)

def get_slots(level=None):    
    print_cur_spell_slots(SPELL_SLOTS_REMAIN, level)

def set_slots(level_slots):
    levels, slots = zip(*level_slots)
    if not all(level in SPELL_SLOTS_MAX for level in levels):
        print("ERROR: Invalid levels: {}".format(levels))
        return
    if not all(slot >= 0 for slot in slots):
        print("ERROR: Invalid slots: {}".format(slots))
        return

    for level, slots in level_slots:
        SPELL_SLOTS_REMAIN[level] = slots
    
    print("SUCCESS: Your slots are now: {}".format(SPELL_SLOTS_REMAIN))

def reset_slots():
    global SPELL_SLOTS_REMAIN # need global tag for global var assignment in func
    SPELL_SLOTS_REMAIN = SPELL_SLOTS_MAX.copy()

def get_money():
    print_cur_money(MONEY, COINAGES)

def transaction(amounts_coinage, earn_or_spend):
    amounts, coinages = zip(*amounts_coinage)
    if not all(coinage in COINAGES for coinage in coinages):
        print("ERROR: Invalid coinages: {}".format(coinages))
        return
    if not all(amount >= 0 for amount in amounts):
        print("ERROR: Invalid amounts: {}".format(amounts))
        return
    if not (earn_or_spend == "earn" or earn_or_spend == "spend"):
        print("ERROR: Invalid transaction type: {}".format(earn_or_spend))
        return

    if earn_or_spend == "spend":
        # check if I have enough money
        total_spend = 0
        for amount, coinage in amounts_coinage:
            total_spend += amount * (10 ** coin_to_index(coinage, COINAGES))

        total_money = 0
        for amount in reversed(MONEY):
            total_money = total_money * 10 + amount

        if total_spend > total_money:
            print("ERROR: Insufficient funds")
            return 
        
        remaining_money = total_money - total_spend
        # Ignore platinum. Exchange for least coins possible
        for i in range(coin_to_index("gold", COINAGES)):
            MONEY[i] = remaining_money % 10
            remaining_money /= 10
        MONEY[coin_to_index("gold", COINAGES)] = remaining_money

    elif earn_or_spend == "earn":
        # Assumed cannot exchange when receiving specific coins.
        for amount, coinage in amounts_coinage:
            MONEY[coin_to_index(coinage, COINAGES)] += amount

    print_cur_money(MONEY, COINAGES)

def get_hp():
    print("Your current HP: {}".format(CUR_HP))
    print("Your current MAX HP: {}".format(MAX_HP))

def set_hp(hp, hp_type=None):
    '''
    Sets either the current hp or max hp.
    hp - (int) new hp value
    hp_type - (string) "max" if max hp is to be set.
    '''
    if hp < 0:
        hp = 0
    if hp_type == None:
        global CUR_HP
        CUR_HP = hp
    elif hp_type == "max":
        global MAX_HP
        MAX_HP = hp

    get_hp()

def hp_change(change):
    '''
    Player's CUR_HP changes by change points.
    Healed: change > 0
    Damaged: change < 0
    '''
    remaining_hp = CUR_HP + change
    set_hp(remaining_hp)

def reset_hp():
    set_hp(MAX_HP)

def long_rest():
    if CUR_HP == 0:
        print("Long rest cannot restore. 0 HP")
        return
    reset_hp()
    reset_long_spell_uses()

def test(arg):
    print(arg)

############### Helper Fn ###############
def action(arg, dictionary, dice, bonus_sub_cats):
    '''
    Rolls a dice and adds corresponding bonuses.
    dice           - either num or "dice" if dependent on arg
    bonus_sub_cats - list of sub categories for dictionary[arg]
    '''

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

def consume_spell_slot(level, search=True):
    '''
    Every time a spell is casted, a level's spell slot is consumed.
    Level 0 spells (i.e. Cantrips) do not consume any slots.
    Spells can be casted at a higher level as well, if not specified and available.
    '''
    if level == 0:
        return 0

    curr_level = level
    consumed = None
    while not consumed and curr_level in SPELL_SLOTS_REMAIN:
        if SPELL_SLOTS_REMAIN[curr_level] > 0:
            SPELL_SLOTS_REMAIN[curr_level] -= 1
            consumed = curr_level
        else:
            curr_level += 1
        
        if not search:
            break
    
    return consumed

def cast_long_spell(spell):
    '''
    Helper function that casts a long rest spell.

    Args:
        spell (str): The long rest spell to be cast.
    '''
    if "uses" in LONG_REST_SPELLS[spell]:
        if LONG_REST_SPELLS[spell]["uses"] == 0:
            print("ERROR: Long rest needed to cast {}.".format(spell))
            return
        
        LONG_REST_SPELLS[spell]["uses"] -= 1
    
    if "action" in LONG_REST_SPELLS[spell]:
        LONG_REST_SPELLS[spell]["action"]()
    
    print("{} was cast.".format(spell))
    
def reset_long_spell_uses():
    for spell in LONG_REST_SPELLS:
        if "uses" in LONG_REST_SPELLS[spell]:
            LONG_REST_SPELLS[spell]["uses"] = LONG_REST_SPELLS[spell]["max uses"]
    print("Long rest spell usages restored.")