# File: gtools.py

"""
This module exports a library of three graphics functions
(createFilledRect, createFilledCircle, and createCenteredLabel)
that are used in several different applications.  Each of these
functions is described in its docstring comment.
"""

from pgl import GRect, GOval, GLabel

def createFilledRect(x, y, width, height, fill="Black", border=None):
    """
    Creates a GRect filled with the specified fill color.  If border is
    specified, the border appears in that color.
    """
    rect = GRect(x, y, width, height)
    rect.setFilled(True)
    if border is None:
        rect.setColor(fill)
    else:
        rect.setColor(border)
        rect.setFillColor(fill)
    return rect

def createFilledCircle(x, y, r, fill="Black", border=None):
    """
    Creates a circle of radius r centered at the point (x, y) with the
    specified fill color.  If border is specified, the border appears
    in that color.
    """
    circle = GOval(x - r, y - r, 2 * r, 2 * r)
    circle.setFilled(True)
    if border is None:
        circle.setColor(fill)
    else:
        circle.setColor(border)
        circle.setFillColor(fill)
    return circle

def createCenteredLabel(text, x, y, font=None):
    """
    Creates a new GLabel centered at the point (x, y) in both the
    horizontal and vertical directions.  If font is specified, it
    is used to set the font of the label.
    """
    label = GLabel(text)
    if font is not None:
        label.setFont(font)
    label.setLocation(x - label.getWidth() / 2, y + label.getAscent() / 2)
    return label
