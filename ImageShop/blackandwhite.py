from pgl import GImage

def luminance(pixel):
    """
    Returns the luminance of a pixel, which indicates its subjective
    brightness.  This implementation uses the NTSC formula.
    """
    r = GImage.getRed(pixel)
    g = GImage.getGreen(pixel)
    b = GImage.getBlue(pixel)
    return round(0.299 * r + 0.587 * g + 0.114 * b)

def cumulativeHistogram(image):
    hist = []
    for i in range(256):
        hist += [0]
    array = image.getPixelArray()
    for row in array:
        for px in row:
            hist[luminance(px)] += 1
    for i in range(1,len(hist)):
        hist[i] += hist[i-1] 
    return hist

def equalizeImage(image):
    hist = cumulativeHistogram(image)
    array = image.getPixelArray()
    for y in range(len(array)):
        for x in range(len(array[0])):
            i = luminance(array[y][x])
            gray = 255*hist[i]//hist[-1]
            array[y][x] = GImage.createRGBPixel(gray, gray, gray)
    return GImage(array)

def blackandwhite(image):
    divisions = 4 
    black = GImage.createRGBPixel(0,0,0)
    white = GImage.createRGBPixel(255,255,255)
    s = 256//divisions
    array = equalizeImage(image).getPixelArray()
    for y in range(len(array)):
        for x in range(len(array[0])):
            p = array[y][x]
            intensity = GImage.getRed(p)//s + 1
            if intensity==divisions:
                array[y][x]=white
            else:
                if y%(intensity) == 0 or x%(intensity) == 0:
                    array[y][x] = black
                else:
                    array[y][x] = white
    return GImage(array)

def linedrawing(image):
    array = GImage.getPixelArray(image)
    return
