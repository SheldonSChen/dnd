import cmd
import re
from roll import *
from sharedHelpers import *

class DndShell(cmd.Cmd):
    intro = 'Welcome to the dnd shell.   Type help or ? to list commands.\n'
    prompt = '(dnd) '
    file = None

    def precmd(self, line):
        '''Prepare given user input for interpretation by other do_xxx() funcs.
            Simply strips trailing whitespaces.
        '''
        return line.rstrip()

    def do_get(self, arg):
        '''Gets the requested stat.
            (dnd) get <stat>
        '''
        if len(arg) == 0:
            print("ERROR: Missing arguments.")
            return
        get(arg)
    
    def do_check(self, arg):
        '''Rolls an ability/skill check or save.
            (dnd) check <stat>
        '''
        if len(arg) == 0:
            print("ERROR: Missing arguments.")
            return
        check(arg)

    def do_attack(self, arg):
        '''Rolls for an attack to hit.
            (dnd) attack <weapon>
        '''
        if len(arg) == 0:
            print("ERROR: Missing arguments.")
            return
        attack(arg)

    def do_damage(self, arg):
        '''Rolls for damage with a weapon.
            (dnd) damage <weapon>
        '''
        if len(arg) == 0:
            print("ERROR: Missing arguments.")
            return
        damage(arg)

    def do_cast(self, arg):
        '''Rolls for spell casting.
            (dnd) cast <spell> <level (optional)>
        '''
        if len(arg) == 0:
            print("ERROR: Missing arguments.")
            return
        m = re.search(r'(?P<spell>^.+) (?P<level>\d+$)', arg)
        if m is not None:
            cast(m.group("spell"), int(m.group("level")))
        else:
            cast(arg)
    
    def do_get_slots(self, arg):
        '''Gets the currently available spell slots.
            (dnd) get_slots <level (optional)>
        '''
        if arg and not num_in_col(arg):
            print("ERROR: Invalid arg: {}".format(arg))
            return
        
        if len(arg) == 0:
            get_slots()
        else:
            get_slots(int(arg))

    # Unnecessary?
    def do_set_slots(self, arg):
        '''Sets the currently available spell slots.
            (dnd) set_slots <level> <slot> ...
        '''
        if len(arg) == 0:
            print("ERROR: Missing arguments.")
            return

        pairs_list = convert_str_to_pairs(arg, int, int, num_in_col, num_in_col)
        if pairs_list:
            set_slots(pairs_list)
    
    # Unnecessary?
    def do_reset_slots(self, arg):
        '''Resets the currently available spell slots to max.
            (dnd) reset_slots
        '''
        if len(arg) > 0:
            print("ERROR: Unnecesary arguments: {}".format(arg))
            return
        reset_slots()
    
    def do_get_money(self, arg):
        '''Returns the current amount of money.
            (dnd) get_money
        '''
        if len(arg) > 0:
            print("ERROR: Unnecesary arguments: {}".format(arg))
            return
        get_money()

    def do_earn_money(self, arg):
        '''Earns money of each coinage.
            (dnd) earn_money <amount> <coinage>...
        '''
        do_transaction(arg, "earn")

    def do_spend_money(self, arg):
        '''Spends money of each coinage.
            (dnd) spend_money <amount> <coinage>...
        '''
        do_transaction(arg, "spend")
    
    def do_get_hp(self, arg):
        '''Returns current HP.
            (dnd) get_hp
        '''
        if len(arg) > 0:
            print("ERROR: Unnecesary arguments: {}".format(arg))
            return
        get_hp()
    
    def do_set_hp(self, arg):
        '''Sets current HP to arg
            (dnd) set_hp <cur_hp> <"max" (optional)>
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
    
    def do_lose_hp(self, arg):
        '''Decreases current HP by damage taken.
            (dnd) lose_hp <damage>
        '''
        do_hp_change(arg, -1)
    
    def do_gain_hp(self, arg):
        '''Increases current HP by amount healed.
            (dnd) gain_hp <heal>
        '''
        do_hp_change(arg, +1)
    
    def do_reset_hp(self, arg):
        '''Resets the current HP to max.
            (dnd) reset_hp
        '''
        reset_hp()

    def do_short_rest(self, arg):
        '''Take a short rest. Consumes hit dice for healing.
            (dnd) short_rest <num hit dice>
        '''
        if len(arg) == 0:
            print("ERROR: Missing arguments.")
            return
        if not num_in_col(arg):
            print("ERROR: not a number: {}".format(arg))
            return
        short_rest(int(arg))

    def do_long_rest(self, arg):
        '''Take a long rest.
            (dnd) long_rest
        '''
        long_rest()

    def do_exit(self, arg):
        '''Exits the shell.
            (dnd) exit
        '''
        #TODO: printing long_rest usage
        print('Thank you for using Dnd.')
        print('Please change the following in the code:')
        print('')
        get_hit_dice()
        print('')
        get_slots()
        print('')
        get_money()
        print('')
        get_hp()
        print('')
        get_long_spell_usage()
        print('')
        return True

############### Helper Fn ###############
def do_transaction(arg, earn_or_spend):
    if len(arg) == 0:
        print("ERROR: Missing arguments.")
        return
    pairs_list = convert_str_to_pairs(arg, int, str, num_in_col)
    if pairs_list:
        transaction(pairs_list, earn_or_spend)

def do_hp_change(arg, sign):
    if len(arg) == 0:
        print("ERROR: Missing arguments.")
        return
    if not num_in_col(arg):
        print("ERROR: Invalid damage value: {}".format(arg))
        return
    hp_change(int(arg) * sign)

############### Main Fn ###############
if __name__ == '__main__':
    DndShell().cmdloop()