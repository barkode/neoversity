import os
import pathlib
import sys
from colorama import Fore, Back, Style, init

# init(autoreset=True)
def colorize_directory(path):
    """Function colorize directory"""
    pass


def clear_screen():
    """Function that clear console"""
    os.system("clear" if os.name == "posix" else "cls")



print(Fore.RED + 'some red text')
# print(Back.GREEN + 'and with a green background')
# print(Style.DIM + 'and in dim text')
# print(Style.RESET_ALL)
print('back to normal now')