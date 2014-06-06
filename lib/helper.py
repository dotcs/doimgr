import os
import sys
from colorama import Fore

class Helper(object):
    @staticmethod
    def get_fg_colorcode_by_identifier(identifier):
        if identifier == 'black':
            return Fore.BLACK
        elif identifier == 'cyan':
            return Fore.CYAN
        elif identifier == 'magenta':
            return Fore.MAGENTA
        elif identifier == 'yellow':
            return Fore.YELLOW
        elif identifier == 'blue':
            return Fore.BLUE
        elif identifier == 'green':
            return Fore.GREEN
        elif identifier == 'red':
            return Fore.RED
        elif identifier == 'white':
            return Fore.WHITE
        elif identifier == 'reset':
            return Fore.RESET
        raise ValueError("Color identifier {} is unknown.".format(identifier))
