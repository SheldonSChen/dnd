import dill
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
    if "save" in stat:
        action(stat, CHAR_STATS, 20, [], "save")
    else:
        action(stat, CHAR_STATS, 20, [])

def percent():
    print("{}%".format(roll_d(100)))

def attack(weapon):
    action(weapon, WEAPONS, 20, ["mod", "prof"], "attack")

def damage(weapon):
    action(weapon, WEAPONS, "dice", ["mod"], "damage")

def cast(spell, level=None):
    '''
    Casts a spell or long rest spell.

    Args:
        spell (str): The spell to be cast.
        level (int): The level at which to cast the spell. (default=None)
    '''
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
            total_bonus = CHAR_STATS["spell attack"] + roll_bonuses("attack")
            print("Spell attack: {}".format(roll_d(20) + total_bonus))
        
        if "damage" in SPELLS[spell]:
            total_bonus = roll_bonuses("damage")
            for possible_damage in SPELLS[spell]["damage"](cast_level):
                print("Spell damage: {}".format(possible_damage + total_bonus))
        
        if "self heal" in SPELLS[spell]:
            hp_change(SPELLS[spell]["self heal"](cast_level), temp=True)

        if "heal" in SPELLS[spell]:
            print("Target(s) regained {} HP".format(SPELLS[spell]["heal"](cast_level)))

        print("{} was cast at level {}.".format(spell, cast_level))
    else:
        if level != None:
            print("ERROR: Unnecessary level specified: {}".format(level))
            return
            
        if spell in CHANNEL_DIVINITIES:
            cast_special_spell(spell, CHANNEL_DIVINITIES)
        elif spell in LONG_REST_SPELLS:
            cast_special_spell(spell, LONG_REST_SPELLS)
        else:
            print("ERROR: {} not found".format(spell))

def bonus(die, target, num_turns):
    if num_turns > 0:
        global BONUSES
        BONUSES[target].append({
            "die": die, 
            "num_turns": num_turns,
            })

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

def hp_change(change, temp=False, critical=False):
    '''
    Player's CUR_HP changes by change points.
    If temp, then it can exceed MAX_HP
    Damage can be a critical hit.

    Healed: change > 0
    Damaged: change < 0
    '''

    global DEATH_SAVE_SUCCESS, DEATH_SAVE_FAILURE
    if CUR_HP <= 0 and change < 0:
        if abs(change) >= MAX_HP:
            #immediate death
            while DEATH_SAVE_FAILURE < 3:
                death_save(2, False) # rolling a 2 counts as one failure
        elif critical:
            death_save(1) # rolling a 1 counts as two failures
        else:
            death_save(2) # rolling a 2 counts as one failure
        
        return

    if CUR_HP == 0 and change > 0:
        DEATH_SAVE_SUCCESS = 0
        DEATH_SAVE_FAILURE = 0
    
    remaining_hp = CUR_HP + change
    if not temp and remaining_hp > MAX_HP:
        remaining_hp = MAX_HP
    elif change < 0 and abs(remaining_hp) >= MAX_HP:
        #immediate death
        while DEATH_SAVE_FAILURE < 3:
            death_save(2, False) # rolling a 2 counts as one failure
        remaining_hp = 0
    elif remaining_hp < 0:
        remaining_hp = 0
    set_hp(remaining_hp)

def reset_hp():
    set_hp(MAX_HP)

def death_save(roll_val=None, print_=True):
    if CUR_HP != 0:
        print("ERROR: No need to roll death save. {} HP".format(CUR_HP))
        return

    if not roll_val:
        roll_val = roll_d(20)

    global DEATH_SAVE_SUCCESS, DEATH_SAVE_FAILURE
    num = 0
    success_or_failure = ""
    if roll_val == 20:
        print("You rolled a 20! You're now stable with 1 HP.")
        hp_change(1)
        return
    elif roll_val == 1:
        num = 2
        success_or_failure = "failures"
        DEATH_SAVE_FAILURE += num
    elif roll_val < 10:
        num = 1
        success_or_failure = "failure"
        DEATH_SAVE_FAILURE += num
    else:
        num = 1
        success_or_failure = "success"
        DEATH_SAVE_SUCCESS += num
    
    if print_:
        print("You rolled a {}. That's {} {}.".format(roll_val, num, success_or_failure))

    if DEATH_SAVE_SUCCESS >= 3:
        print("You're now stable with 1 HP.")
        hp_change(1)
    elif DEATH_SAVE_FAILURE >= 3:
        print("Oh no you died!")

def get_hit_dice():
    print("Your current number of hit dice: {}".format(CUR_HIT_DICE))

def short_rest(hit_dice=0):
    reset_spell_uses(CHANNEL_DIVINITIES, "Channel Divinity")

    global CUR_HIT_DICE
    if hit_dice < 0 or hit_dice > CUR_HIT_DICE:
        print("ERROR: Invalid number of hit dice: {}. {} currently available".format(hit_dice, CUR_HIT_DICE))
        return
    if hit_dice > 0:
        CUR_HIT_DICE -= hit_dice
        hp_change(roll_d(HIT_DICE_TYPE, hit_dice) + CHAR_STATS["con"])

def long_rest():
    if CUR_HP == 0:
        print("Long rest cannot restore. 0 HP")
        return
    reset_hp()
    reset_slots()
    reset_spell_uses(CHANNEL_DIVINITIES, "Channel Divinity")
    reset_spell_uses(LONG_REST_SPELLS, "Long rest")
    
    # restores at least half of total hit dice
    restored_hit_dice = MAX_HIT_DICE / 2
    if restored_hit_dice == 0:
        restored_hit_dice = 1
    global CUR_HIT_DICE
    CUR_HIT_DICE += restored_hit_dice
    if CUR_HIT_DICE > MAX_HIT_DICE:
        CUR_HIT_DICE = MAX_HIT_DICE
    get_hit_dice()

############### Helper Fn ###############
def print_dict(arg):
    print(globals()[arg])

def action(arg, dictionary, dice, mod_prof, action_type=None):
    '''
    Rolls a dice and adds corresponding bonuses.
    dice        - either num or "dice" if dependent on arg
    mod_prof    - list of sub categories for dictionary[arg]
    action_type - type of action
    '''

    if arg not in dictionary:
        print("ERROR: {} not found".format(arg))
        return 
    
    total_bonus = 0
    if len(mod_prof) == 0:
        total_bonus = dictionary[arg]
    else:
        for category in mod_prof:
            total_bonus += dictionary[arg][category]
    
    if action_type:
        total_bonus += roll_bonuses(action_type)    
    
    n = dictionary[arg][dice] if dice == "dice" else dice
    print(roll_d(n) + total_bonus)

def roll_bonuses(action_type):
    total_bonus = 0
    global BONUSES
    for i in range(len(BONUSES[action_type])):
        total_bonus += roll_d(BONUSES[action_type][i]["die"])
        BONUSES[action_type][i]["num_turns"] -= 1
    BONUSES[action_type] = [b for b in BONUSES[action_type] if b["num_turns"] > 0]
    return total_bonus

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

def cast_special_spell(spell, dict_type):
    '''
    Helper function that casts a channel divinity or long rest spell.

    Args:
        spell (str): The special spell to be cast.
        dict_type (dict): Either CHANNEL_DIVINITIES or LONG_REST_SPELLS
    '''
    if dict_type[spell]["uses"] == 0:
        print("ERROR: Rest needed to cast {}.".format(spell))
        return
    
    dict_type[spell]["uses"] -= 1
    
    if "action" in dict_type[spell]:
        dict_type[spell]["action"]()
    
    print("{} was cast.".format(spell))

def reset_spell_uses(dict_type, spell_type):
    for spell in dict_type:
        if "uses" in dict_type[spell]:
            dict_type[spell]["uses"] = dict_type[spell]["max uses"]
    print(spell_type + " spell usages restored.")

def save_char_data():
    '''Saves character data into a JSON file.
        Only saves values that may change during play.
        Hit dice, spell slots, money, hp, long spell usage.
    '''
    data = {}
    data["CUR_HIT_DICE"] = CUR_HIT_DICE
    data["CUR_HP"] = CUR_HP
    data["DEATH_SAVE_SUCCESS"] = DEATH_SAVE_SUCCESS
    data["DEATH_SAVE_FAILURE"] = DEATH_SAVE_FAILURE
    data["BONUSES"] = BONUSES
    data["MONEY"] = MONEY
    data["CHANNEL_DIVINITIES"] = CHANNEL_DIVINITIES
    data["LONG_REST_SPELLS"] = LONG_REST_SPELLS
    data["SPELL_SLOTS_REMAIN"] = SPELL_SLOTS_REMAIN

    with open('data.txt', 'w') as outfile:
        dill.dump(data, outfile)
        outfile.close()

def load_char_data():
    '''Saves character data into a JSON file.
        Only saves values that may change during play.
        Hit dice, spell slots, money, hp, long spell usage.
    '''

    with open('data.txt', 'r') as infile:
        data = dill.load(infile)
        infile.close()
    
    global CUR_HIT_DICE, CUR_HP, MONEY, CHANNEL_DIVINITIES, LONG_REST_SPELLS, SPELL_SLOTS_REMAIN, DEATH_SAVE_SUCCESS, DEATH_SAVE_FAILURE, BONUSES
    CUR_HIT_DICE = data["CUR_HIT_DICE"]
    CUR_HP = data["CUR_HP"]
    DEATH_SAVE_SUCCESS = data["DEATH_SAVE_SUCCESS"]
    DEATH_SAVE_FAILURE = data["DEATH_SAVE_FAILURE"]
    BONUSES = data["BONUSES"]
    MONEY = data["MONEY"]
    CHANNEL_DIVINITIES = data["CHANNEL_DIVINITIES"]
    LONG_REST_SPELLS = data["LONG_REST_SPELLS"]
    SPELL_SLOTS_REMAIN = data["SPELL_SLOTS_REMAIN"]
