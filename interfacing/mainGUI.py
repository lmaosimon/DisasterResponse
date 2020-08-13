from interfacing.classes.GUI import GUI
from interfacing.classes.utils import get_assistant
from interfacing.classes.Search import Search

if __name__ == '__main__':
    assistant = get_assistant(type='ibm')
    GUI(assistant)
