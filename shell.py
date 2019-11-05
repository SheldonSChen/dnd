import cmd
from roll import *

class DndShell(cmd.Cmd):
    intro = 'Welcome to the dnd shell.   Type help or ? to list commands.\n'
    prompt = '(dnd) '
    file = None

    def do_check(self, arg):
        '''
        Rolls an ability/skill check or save.
        Command: 
            check <stat>
        '''
        if len(arg) == 0:
            print("ERROR: Missing arguments.")
            return
        check(arg)

    def do_attack(self, arg):
        '''
        Rolls for an attack to hit.
        Command: 
            attack <weapon>
        '''
        if len(arg) == 0:
            print("ERROR: Missing arguments.")
            return
        attack(arg)

    def do_damage(self, arg):
        '''
        Rolls for damage with a weapon.
        Command:
            damage <weapon>
        '''
        if len(arg) == 0:
            print("ERROR: Missing arguments.")
            return
        damage(arg)
    
    def do_cast(self, arg):
        '''
        Rolls for spell casting.
        Command: 
            cast <spell> <level (optional)>
        '''
        if len(arg) == 0:
            print("ERROR: Missing arguments.")
            return
        args = arg.rsplit(" ", 1)
        if len(args) == 2 and not num_in_col(args[1]):
            print("ERROR: Invalid cast level: {}".format(args[1]))
            return
        if len(args) > 2:
            print("ERROR: Invalid arg length: {}".format(args))
            return

        if len(args) == 1:
            cast(args[0])
        else:
            cast(args[0], int(args[1]))
    
    def do_get_slots(self, arg):
        '''
        Gets the currently available spell slots.
        Command: 
            get_slots <level (optional)>
        '''
        if arg and not num_in_col(arg):
            print("ERROR: Invalid arg: {}".format(arg))
            return
        
        if len(arg) == 0:
            get_slots()
        else:
            get_slots(int(arg))

    def do_set_slots(self, arg):
        '''
        Sets the currently available spell slots.
        Command: 
            set_slots <level> <slot> ...
        '''
        if len(arg) == 0:
            print("ERROR: Missing arguments.")
            return

        pairs_list = convert_str_to_pairs(arg, int, int, num_in_col, num_in_col)
        if pairs_list:
            set_slots(pairs_list)
    
    def do_reset_slots(self, arg):
        '''
        Resets the currently available spell slots to max.
        Command: 
            reset_slots
        '''
        if len(arg) > 0:
            print("ERROR: Unnecesary arguments: {}".format(arg))
            return
        reset_slots()
    
    def do_get_money(self, arg):
        '''
        Returns the current amount of money.
        Command: 
            get_money
        '''
        if len(arg) > 0:
            print("ERROR: Unnecesary arguments: {}".format(arg))
            return
        get_money()

    def do_earn_money(self, arg):
        '''
        Earns money of each coinage.
        Command:
            earn_money <amount> <coinage>...
        '''
        do_transaction(arg, "earn")

    def do_spend_money(self, arg):
        '''
        Spends money of each coinage.
        Command: 
            spend_money <amount> <coinage>...
        '''
        do_transaction(arg, "spend")
    
    def do_get_hp(self, arg):
        '''
        Returns current HP.
        Command: 
            get_hp
        '''
        if len(arg) > 0:
            print("ERROR: Unnecesary arguments: {}".format(arg))
            return
        get_hp()
    
    def do_set_hp(self, arg):
        '''
        Sets current HP to arg
        Command: 
            set_hp <cur_hp> <"max" (optional)>
        '''
        if len(arg) == 0:
            print("ERROR: Missing arguments.")
            return
        args = arg.split()
        if not num_in_col(args[0]):
            print("ERROR: Invalid HP: {}".format(args[0]))
            return
        if len(args) == 2 and args[1] != "max":
            print("ERROR: Invalid HP type: {}".format(args[1]))
            return
        if len(args) > 2:
            print("ERROR: Invalid arg length: {}".format(args))
            return 

        if len(args) == 1:
            set_hp(int(args[0]))
        else:
            set_hp(int(args[0]), args[1])
    
    def do_take_damage(self, arg):
        '''
        Decreases current HP by damage taken.
        Command: 
            take_damage <damage>
        '''
        if len(arg) == 0:
            print("ERROR: Missing arguments.")
            return
        if not num_in_col(arg):
            print("ERROR: Invalid damage value: {}".format(arg))
            return
        take_damage(int(arg))

    def do_exit(self, arg):
        '''
        Exits the shell
        '''
        print('Thank you for using Dnd')
        return True

############### Helper Fn ###############
def num_in_col(input_col):
    return all(char.isdigit() for char in input_col)

def do_transaction(arg, earn_or_spend):
    if len(arg) == 0:
        print("ERROR: Missing arguments.")
        return
    pairs_list = convert_str_to_pairs(arg, int, str, num_in_col)
    if pairs_list:
        transaction(pairs_list, earn_or_spend)

def convert_str_to_pairs(flat_list, key_map_fn, val_map_fn, key_check=None, val_check=None):
    ''' Converts a string into a list of (key, value) pairs.

    Args:
        flat_list (str): The string representation of the pairs ("<key> <value> ...")
        key_map_fn (func): The function to be mapped to keys
        val_map_fn (func): The function to be mapped to values
        key_check (func): Returns if key is valid type. (default=None)
        val_check (func): Returns if value is valid type. (default=None)
    
    Returns:
        The new list of pairs, or None if error
    '''

    flat_list = flat_list.split()
    if len(flat_list) == 0 or len(flat_list) % 2 != 0:
        print("ERROR: invalid list length: {}".format(flat_list))
        return None
    
    keys = flat_list[0::2]
    if key_check and not key_check(keys):
        print("Error: Invalid keys: {}".format(keys))
        return None
    keys = map(key_map_fn, keys)
    
    values = flat_list[1::2]
    if val_check and not val_check(values):
        print("Error: Invalid values: {}".format(values))
        return None
    values = map(val_map_fn, values)

    return zip(keys, values)

if __name__ == '__main__':
    DndShell().cmdloop()