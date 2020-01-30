# File: AdvRoom.py

"""
This module is responsible for modeling a single room in Adventure.
"""

###########################################################################
# Your job in this milestone is to fill in the definitions of the         #
# methods listed in this file, along with any helper methods you need.    #
# The public methods shown in this file are the ones you need for         #
# Milestone #1.  You will need to add other public methods for later      #
# milestones, as described in the handout.  For Milestone #7, you will    #
# need to move the getNextRoom method into the AdvGame class and replace  #
# it with a getPassages method that returns the dictionary of passages.   #
###########################################################################

# Constants

MARKER = "-----"

class AdvRoom:

    def __init__(self, name, shortdesc, longdesc, passages):
        """Creates a new room with the specified attributes."""
        self._name = name
        self._shortdesc = shortdesc
        self._longdesc = longdesc
        self._passages = passages
        self._visited = False
        self._objects = []

    def getName(self):
        """Returns the name of this room.."""
        return self._name

    def getShortDescription(self):
        """Returns a one-line short description of this room.."""
        return self._shortdesc

    def getLongDescription(self):
        """Returns the list of lines describing this room."""
        return self._longdesc

    def getPassages(self, verb):
        """Returns the name of the destination room after applying verb."""
        passages = self._passages.get(verb, None)
        return passages

    def setVisited(self,value):
        self._visited = value

    def hasBeenVisited(self):
        return self._visited

    def addObject(self, obj):
        self._objects += [obj]

    def removeObject(self, obj):
        self._objects.remove(obj)

    def containsObject(self, obj):
        return obj in self._objects

    def getContents(self):
        return self._objects.copy()

    @staticmethod
    def readRoom(f):
        """Reads a room from the data file."""
        name = f.readline().rstrip()
        if name=="":
            return None
        shortdesc = f.readline().rstrip()
        text = []
        while True:
            line = f.readline().rstrip()
            if line == MARKER: break
            text.append(line)
        answers = {}
        while True:
            line = f.readline().rstrip()
            if line == "": break
            colon = line.find(":")
            if colon == -1:
                raise ValueError("Missing colon in "+line)
            response = line[:colon].strip().upper()
            next = line[colon + 1:].strip()
            try:
                answers[response] += [next]
            except KeyError:
                answers[response] = [next]
        return AdvRoom(name, shortdesc, text, answers)
