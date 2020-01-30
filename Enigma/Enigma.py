# File: Enigma.py

"""
This module is the main program for the Enigma machine.  You should
not need to change this file unless you are implementing extensions.
"""

from pgl import GWindow
from EnigmaMachine import EnigmaMachine
from EnigmaConstants import *

# Main program

def Enigma():

    def mousedownAction(e):
        gobj = gw.getElementAt(e.getX(), e.getY())
        if gobj is not None:
            if getattr(gobj, "mousedownAction", None) is not None:
                gobj.mousedownAction(enigma)

    def mouseupAction(e):
        gobj = gw.getElementAt(e.getX(), e.getY())
        if gobj is not None:
            if getattr(gobj, "mouseupAction", None) is not None:
                gobj.mouseupAction(enigma)

    def clickAction(e):
        gobj = gw.getElementAt(e.getX(), e.getY())
        if gobj is not None:
            if getattr(gobj, "clickAction", None) is not None:
                gobj.clickAction(enigma)

    gw = GWindow(ENIGMA_WIDTH, ENIGMA_HEIGHT)
    enigma = EnigmaMachine(gw)
    gw.addEventListener("mousedown", mousedownAction)
    gw.addEventListener("mouseup", mouseupAction)
    gw.addEventListener("click", clickAction)

# Startup code

if __name__ == "__main__":
    Enigma()
