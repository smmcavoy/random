# File: ImageShop.py

"""
This program is the starter file for the ImageShop application, which
implements the "Load" and "Flip Vertical" buttons.
"""

from filechooser import chooseInputFile
from pgl import GWindow, GImage, GRect, GButton
from blackandwhite import blackandwhite

# Constants

GWINDOW_WIDTH = 1024
GWINDOW_HEIGHT = 700
BUTTON_WIDTH = 125
BUTTON_HEIGHT = 20
BUTTON_MARGIN = 10
BUTTON_BACKGROUND = "#CCCCCC"

# Derived constants

BUTTON_AREA_WIDTH = 2 * BUTTON_MARGIN + BUTTON_WIDTH
IMAGE_AREA_WIDTH = GWINDOW_WIDTH - BUTTON_AREA_WIDTH

# The ImageShop application

def ImageShop():
    def addButton(label, action):
        """
        Adds a button to the region on the left side of the window
        """
        nonlocal nextButtonY
        x = BUTTON_MARGIN
        y = nextButtonY
        button = GButton(label, action)
        button.setSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        gw.add(button, x, y)
        nextButtonY += BUTTON_HEIGHT + BUTTON_MARGIN

    def setImage(image):
        """
        Sets image as the current image after removing the old one.
        """
        nonlocal currentImage
        if currentImage is not None:
            gw.remove(currentImage)
        currentImage = image
        x = BUTTON_AREA_WIDTH + (IMAGE_AREA_WIDTH - image.getWidth()) / 2
        y = (gw.getHeight() - image.getHeight()) / 2
        gw.add(image, x, y)

    def loadButtonAction():
        """Callback function for the Load button"""
        filename = chooseInputFile()
        if filename != "":
            setImage(GImage(filename))

    def flipVerticalAction():
        """Callback function for the FlipVertical button"""
        if currentImage is not None:
            setImage(flipVertical(currentImage))

    def flipHorizontalAction():
        if currentImage is not None:
            setImage(flipHorizontal(currentImage))
    
    def rotateRightAction():
        if currentImage is not None:
            setImage(rotateRight(currentImage))

    def rotateLeftAction():
        if currentImage is not None:
            setImage(rotateLeft(currentImage))
            
    def BWAction():
        if currentImage is not None:
            setImage(blackandwhite(currentImage))

    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    buttonArea = GRect(0, 0, BUTTON_AREA_WIDTH, GWINDOW_HEIGHT)    
    buttonArea.setFilled(True)
    buttonArea.setColor(BUTTON_BACKGROUND)
    gw.add(buttonArea)
    nextButtonY = BUTTON_MARGIN
    currentImage = None
    addButton("Load", loadButtonAction)
    addButton("Flip Vertical", flipVerticalAction)
    addButton("Flip Horizontal", flipHorizontalAction)
    addButton("Rotate Right", rotateRightAction)
    addButton("Rotate Left", rotateLeftAction)
    addButton("Black and White", BWAction)

def flipVertical(image):
    array = image.getPixelArray()
    return GImage(array[::-1])

def flipHorizontal(image):
    array = image.getPixelArray()
    for i in range(len(array)):
        array[i] = array[i][::-1]
    return GImage(array)

def rotateRight(image):
    array = image.getPixelArray()
    new = []
    for x in range(len(array[0])):
        row = []
        for y in range(len(array)-1,-1,-1):
            row += [array[y][x]]
        new += [row]
    return GImage(new)

def rotateLeft(image):
    #hehe
    #return rotateRight(rotateRight(rotateRight(image)))

    array = image.getPixelArray()
    new = []
    for x in range(len(array[0])-1,-1,-1):
        row = []
        for y in range(len(array)):
            row += [array[y][x]]
        new += [row]
    return GImage(new)


if __name__ == "__main__":
    ImageShop()
