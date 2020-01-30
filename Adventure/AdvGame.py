# File: AdvGame.py
from tokenscanner import *
"""
This module defines the AdvGame class, which records the information
necessary to play a game.
"""

###########################################################################
# Your job in this assignment is to fill in the definitions of the        #
# methods listed in this file, along with any helper methods you need.    #
# Unless you are implementing extensions, you won't need to add new       #
# public methods (i.e., methods called from other modules), but the       #
# amount of code you need to add is large enough that decomposing it      #
# into helper methods will be essential.                                  #
###########################################################################

from AdvRoom import AdvRoom
from AdvObject import AdvObject

class AdvGame:

    def __init__(self, prefix):
        self._inventory = []
        """Reads the game data from files with the specified prefix."""
        with open(prefix + "Rooms.txt") as f:
            rooms = {}
            while True:
                tempRoom = AdvRoom.readRoom(f)
                if tempRoom is None:
                    break
                if len(rooms)==0:
                    rooms["START"] = tempRoom
                rooms[tempRoom.getName()] = tempRoom
        self._rooms = rooms
        try:
            with open(prefix + "Objects.txt") as f:
                objects = {}
                while True:
                    tempObject = AdvObject.readObject(f)
                    if tempObject is None:
                        break
                    objects[tempObject.getName()] = tempObject
                    location = tempObject.getInitialLocation()
                    if location == 'PLAYER':
                        self._inventory += [tempObject.getName()]
                    elif self._rooms[location] is not None:
                        self._rooms[location].addObject(tempObject.getName())

            self._objects = objects
        except FileNotFoundError:
            self._objects = {}

        try:
            with open(prefix + "Synonyms.txt") as f:
                synonyms = {}
                while True:
                    line = f.readline().rstrip()
                    if line=='':
                        break
                    eq = line.find('=')
                    if eq == -1:
                        raise ValueError('Missing equals sign in '+line)
                    key = line[:eq].strip().upper()
                    value = line[eq+1:].strip()
                    synonyms[key] = value
            self._synonyms = synonyms
        except FileNotFoundError:
            self._synonyms = {}

    def synonym(self, word):
        try:
            return self._synonyms[word]
        except KeyError:
            return word
            
    def getRoom(self, name):
        """Returns the AdvRoom object with the specified name."""
        return self._rooms[name]

    def getNextRoom(self, room, verb):
        passages = room.getPassages(verb)
        if passages is None:
            return None
        if len(passages)==1:
            return passages[0]
        for p in passages:
            slash = p.find('/')
            if slash == -1:
                return p
            requiredItem = p[slash+1:]
            if requiredItem in self._inventory:
                if verb == 'UNLOCK':
                    self._rooms[room.getName()] = self._rooms[room.getName()+'2']
                return p[:slash]

    def run(self):
        """Plays the adventure game stored in this object."""
        current = "START"
        scanner = TokenScanner()
        scanner.ignoreWhitespace()
        room = self._rooms[current]
        while current != "EXIT":
            room = self._rooms[current]
            if not room.hasBeenVisited():
                for line in room.getLongDescription():
                    print(line)
                for item in room.getContents():
                    print('There is',str(self._objects[item]),'here.')
                room.setVisited(True)
            if self.getNextRoom(room,'FORCED') is not None:
                room.setVisited(False)
                current = self.getNextRoom(room,'FORCED')
                continue
            response = input("> ").strip().upper()
            scanner.setInput(response)
            answer = self.synonym(scanner.nextToken())
            if self.getNextRoom(room,answer) is not None:
                current = self.getNextRoom(room,answer)
                room = self._rooms[current]
                if room.hasBeenVisited():
                    print(room.getShortDescription())
            elif answer=='HELP':
                for line in HELP_TEXT:
                    print(line)
            elif answer=='QUIT':
                break
            elif answer=='LOOK':
                room.setVisited(False)
            elif answer=='INVENTORY':
                if len(self._inventory)==0:
                    print('You are empty-handed.')
                else:
                    print('You are carrying:')
                    for item in self._inventory:
                        print('\t'+str(self._objects[item]))
            elif answer=='TAKE':
                obj = self.synonym(scanner.nextToken())
                if obj=='ALL':
                    if len(room.getContents())==None:
                        print('Nothing here to take.')
                    else:
                        for item in room.getContents():
                            self._inventory += [item]
                            room.removeObject(obj)
                        print('Taken.')
                elif room.containsObject(obj):
                    self._inventory += [obj]
                    room.removeObject(obj)
                    print('Taken.')
                else:
                    print("I don't see that here.")
            elif answer=='DROP':
                obj = self.synonym(scanner.nextToken())
                if obj in self._inventory:
                    room.addObject(obj)
                    self._inventory.remove(obj)
                    print('Dropped.')
                else:
                    print("You aren't carrying "+obj.lower()+'.')
            elif self.getNextRoom(room, '*') is not None:
                current = self.getNextRoom(room,'*')
                room = self._rooms[current]
                if room.hasBeenVisited():
                    print(room.getShortDescription())
            else:
                print("I don't understand that response.")
                    
            
# Constants

HELP_TEXT = [
    "Welcome to Adventure!",
    "Somewhere nearby is Colossal Cave, where others have found fortunes in",
    "treasure and gold, though it is rumored that some who enter are never",
    "seen again.  Magic is said to work in the cave.  I will be your eyes",
    "and hands.  Direct me with natural English commands; I don't understand",
    "all of the English language, but I do a pretty good job.",
    "",
    "It's important to remember that cave passages turn a lot, and that",
    "leaving a room to the north does not guarantee entering the next from",
    "the south, although it often works out that way.  You'd best make",
    "yourself a map as you go along.",
    "",
    "Much of my vocabulary describes places and is used to move you there.",
    "To move, try words like IN, OUT, EAST, WEST, NORTH, SOUTH, UP, or DOWN.",
    "I also know about a number of objects hidden within the cave which you",
    "can TAKE or DROP.  To see what objects you're carrying, say INVENTORY.",
    "To reprint the detailed description of where you are, say LOOK.  If you",
    "want to end your adventure, say QUIT."
]
