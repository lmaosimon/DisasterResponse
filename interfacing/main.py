from interfacing.classes.GUI import GUI
from interfacing.classes.utils import get_assistant
from interfacing.classes.Search import Search
import os

if __name__ == '__main__':
    os.chdir('..')
    assistant = get_assistant(type='ibm')
    GUI(assistant)

