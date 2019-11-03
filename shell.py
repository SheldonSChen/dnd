import cmd
from roll import *

class DndShell(cmd.Cmd):
    intro = 'Welcome to the dnd shell.   Type help or ? to list commands.\n'
    prompt = '(dnd) '
    file = None

    # call do_xxx() by typing "xxx"
    def do_check(self, arg):
        """
        Rolls an ability/skill check or save.
        Command of the form: check <stat>
        """
        check(arg)

    def do_attack(self, arg):
        """
        Rolls for an attack to hit.
        Command of the form: attack <weapon>
        """
        attack(arg)

    def do_damage(self, arg):
        """
        Rolls for damage.
        Command of the form: damage <weapon>
        """
        damage(arg)
    
    def do_cast(self, arg):
        """
        Rolls for spell casting.
        Command of the form: cast <spell>
        """
        cast(arg)
    
    def do_get_slots(self, arg=None):
        """
        Gets the currently available spell slots.
        Command of the form: get_slots <level (optional)>
        """
        get_slots(arg)

    def do_set_slots(self, arg):
        """
        Sets the currently available spell slots.
        Command of the form: set_slots <level, slot, ...>
        """
        set_slots(arg)
    
    def do_reset_slots(self, arg):
        """
        Resets the currently available spell slots to max.
        Command of the form: reset_slots
        """
        reset_slots()

    def do_exit(self, arg):
        """
        Exits the shell
        """
        print('Thank you for using Dnd')
        return True

if __name__ == '__main__':
    DndShell().cmdloop()