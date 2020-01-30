# File: EnigmaMachine.py

"""
This module is the starter file for the EnigmaMachine class.
"""

from pgl import *
from EnigmaConstants import *
from invertkey import *

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Class: EnigmaMachine

class EnigmaMachine():
    """
    This class is responsible for storing the data needed to simulate
    the Enigma machine.  If you need to maintain any state information
    that must be shared among different parts of this implementation,
    you should define that information as part of this class and
    provide the necessary getters, setters, and other methods needed
    to manage that information.
    """

    def __init__(self, gw):
        """
        The constructor for the EnigmaMachine class is responsible for
        initializing the graphics window along with the state variables
        that keep track of the machine's operation.
        """
        enigmaImage = GImage("images/EnigmaTopView.png")
        gw.add(enigmaImage)
        self.keys = {}
        self.lamps = {}
        self.rotors = []
        self.currentLamp = None

        for i in range(3):
            temp = EnigmaRotor(ROTOR_PERMUTATIONS[i])
            gw.add(temp, ROTOR_LOCATIONS[i][0], ROTOR_LOCATIONS[i][1])
            self.rotors += [temp]

        for i in range(26):
            temp = EnigmaKey(alphabet[i])
            gw.add(temp, KEY_LOCATIONS[i][0], KEY_LOCATIONS[i][1])
            self.keys[alphabet[i]] = temp

            temp2 = EnigmaLamp(alphabet[i])
            gw.add(temp2, LAMP_LOCATIONS[i][0], LAMP_LOCATIONS[i][1])
            self.lamps[alphabet[i]] = temp2
            

    def keyPressed(self, letter):
        a = self.rotors[2].increment()
        if a:
            b = self.rotors[1].increment()
            if b:
                self.rotors[0].increment()
        self.currentLamp = self.lamps[self.applyPermutation(letter)]
        self.currentLamp.setState(True)
        
    def applyPermutation(self,letter):
        i = alphabet.index(letter)
        for x in range(2,-1,-1):
            i = self.rotors[x].encrypt(i)
        i = REFLECTOR_PERMUTATION.index(alphabet[i])
        for x in range(3):
            i = self.rotors[x].decrypt(i)
        return alphabet[(i)%26]

    def keyReleased(self, letter):
        self.currentLamp.setState(False)

class EnigmaKey(GCompound):
    def __init__(self, letter):
        GCompound.__init__(self)
        
        buttonOval = GOval(-KEY_RADIUS, -KEY_RADIUS, 2*KEY_RADIUS, 2*KEY_RADIUS)
        buttonOval.setColor(KEY_BORDER_COLOR)
        buttonOval.setFilled(True)
        buttonOval.setFillColor(KEY_BGCOLOR)
        buttonOval.setLineWidth(KEY_BORDER)
        self.add(buttonOval)

        self.label = GLabel(letter, 0, KEY_LABEL_DY)
        self.label.setFont(KEY_FONT)
        self.label.move(-self.label.getWidth()/2,0)
        self.label.setColor(KEY_UP_COLOR)
        self.add(self.label)

        self.identity = letter

    def mousedownAction(self,enigma):
        self.label.setColor(KEY_DOWN_COLOR)
        enigma.keyPressed(self.identity)

    def mouseupAction(self,enigma):
        self.label.setColor(KEY_UP_COLOR)
        enigma.keyReleased(self.identity)

class EnigmaLamp(GCompound):
    def __init__(self, letter):
        GCompound.__init__(self)

        lampOval = GOval(-LAMP_RADIUS, -LAMP_RADIUS, 2*LAMP_RADIUS, 2*LAMP_RADIUS)
        lampOval.setColor(LAMP_BORDER_COLOR)
        lampOval.setFilled(True)
        lampOval.setFillColor(LAMP_BGCOLOR)
        self.add(lampOval)

        self.label = GLabel(letter, 0, LAMP_LABEL_DY)
        self.label.setFont(LAMP_FONT)
        self.label.move(-self.label.getWidth()/2,0)
        self.label.setColor(LAMP_OFF_COLOR)
        self.add(self.label)

        self.state = False

    def setState(self, boolean):
        if boolean:
            self.label.setColor(LAMP_ON_COLOR)
        else:
            self.label.setColor(LAMP_OFF_COLOR)
        self.state = boolean

    def getState(self):
        return self.state
    
class EnigmaRotor(GCompound):
    def __init__(self, permutation):
        GCompound.__init__(self)

        self.offset = 0

        rotorBG = GRect(-ROTOR_WIDTH/2, -ROTOR_HEIGHT/2, ROTOR_WIDTH, ROTOR_HEIGHT)
        rotorBG.setFilled(True)
        rotorBG.setColor(ROTOR_BGCOLOR)
        self.add(rotorBG)

        self.label = GLabel(alphabet[self.offset], 0, ROTOR_LABEL_DY)
        self.label.setFont(ROTOR_FONT)
        self.label.move(-self.label.getWidth()/2,0)
        self.label.setColor(ROTOR_COLOR)
        self.add(self.label)

        self.permutation = permutation

    def increment(self):
        self.offset = (self.offset+1)%26
        self.label.setLabel(alphabet[self.offset])
        return self.offset==0

            
    def encrypt(self, index):
        letter = self.permutation[(index+self.offset)%26]
        return (alphabet.index(letter)-self.offset)%26

    def decrypt(self, index):
        key = invertkey(self.permutation) 
        letter = key[(index + self.offset)%26]
        return (alphabet.index(letter)-self.offset)%26


