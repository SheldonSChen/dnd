import cmd
from roll import *

class DndShell(cmd.Cmd):
    intro = 'Welcome to the dnd shell.   Type help or ? to list commands.\n'
    prompt = '(dnd) '
    file = None

    # call do_xxx() by typing "xxx"
    def do_check(self, arg):
        check(arg)

    def do_attack(self, arg):
        attack(arg)

    def do_damage(self, arg):
        damage(arg)

    def do_exit(self, arg):
        print('Thank you for using Dnd')
        return True

if __name__ == '__main__':
    DndShell().cmdloop()