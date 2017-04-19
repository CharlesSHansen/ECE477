import time
import random
import numpy
from neopixel import *
from PIL import Image
from math import *
import sys

# LED strip configuration:
WIDTH 		   = 30
HEIGHT		   = 16
LED_COUNT      = WIDTH * HEIGHT   # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 700000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
PATTERN_COUNT = 10

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
                strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
            strip.show()
            time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
            strip.show()
            time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):

        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
                strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i+q, 0)

def transform(arr):
    invert = True
    ret = []
    offset = WIDTH

    for i in range(0, len(arr)):
        if(i % WIDTH == 0):
            invert = not invert;
        if((not invert)):
            ret.append(arr[i])
        else:
            #print(i + offset)
            ret.append(arr[int(i + offset -1)])
            offset = offset - 2
        if(offset == -30):
            offset = WIDTH
            '''
    for i in range(0, len(ret)):
        if(i % 30 == 0):
            print("")
            print ret[i],
            '''
    return(ret)

red1 = []
red2 = []
blue1 = []
blue2 = []

blank =  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
zero =   [1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1]
one =    [0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,1]
two =    [1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,1,1]
three =  [1,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1]
four =   [1,0,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,0,0,1]
five =   [1,1,1,1,1,0,1,0,1,1,1,1,0,1,0,1,1,1,1,1]
six =    [1,0,0,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1]
seven =  [1,1,1,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,1]
eight =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
nine =   [1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,0,0,1]

def initStarts():
    global red1
    global red2
    global blue1
    global blue2
    
    r1 = 3
    r2 = 8
    b1 = 18
    b2 = 23
    
    col1 = []
    for i in range(HEIGHT):
        val = i * 30
        if (i % 2 == 0):
            col1.append(val)
        else:
            col1.append(val + 30 - 1)

    for i in range(7):
        row = (HEIGHT - 1) / 2 - 3 + i
        if (i % 3 == 0): #long row
            for j in range(4):
                if (row % 2 == 0):
                    red1.append(col1[row] + 3 + j)

                    red2.append(col1[row] + 8 + j)
                    blue1.append(col1[row] + 18 + j)
                    blue2.append(col1[row] + 23 + j)
                else:
                    red1.append(col1[row] - 3 - j)
                    red2.append(col1[row] - 8 - j)
                    blue1.append(col1[row] - 18 - j)
                    blue2.append(col1[row] - 23 - j)
        else: #short row
            if (row % 2 == 0):
                red1.append(col1[row] + 3)
                red1.append(col1[row] + 6)
                red2.append(col1[row] + 8)
                red2.append(col1[row] + 11)
                blue1.append(col1[row] + 18)
                blue1.append(col1[row] + 21)
                blue2.append(col1[row] + 23)
                blue2.append(col1[row] + 26)
            else:
                red1.append(col1[row] - 3)
                red1.append(col1[row] - 6)
                red2.append(col1[row] - 8)
                red2.append(col1[row] - 11)
                blue1.append(col1[row] - 18)
                blue1.append(col1[row] - 21)
                blue2.append(col1[row] - 23)
                blue2.append(col1[row] - 26)
                
def setScoreDisplay(strip,disp,mask,r,g,b):
    for i in range(20):
        strip.setPixelColor(disp[i],Color(mask[i]*g,mask[i]*r,mask[i]*b))
        strip.show()


def outputScore(strip, redScore, blueScore, clear):
    if (clear):
        clearStrip(strip)
        setBorder(strip)

    #set red score
    if (redScore == 10):
        setScoreDisplay(strip,red1,one,255,0,0)
        setScoreDisplay(strip,red2,zero,255,0,0)
    else:
        setScoreDisplay(strip,red1,eight,0,0,0)
        if (redScore == 9):
            setScoreDisplay(strip,red2,nine,255,0,0)
        elif (redScore == 8):
            setScoreDisplay(strip,red2,eight,255,0,0)
        elif (redScore == 7):
            setScoreDisplay(strip,red2,seven,255,0,0)
        elif (redScore == 6):
            setScoreDisplay(strip,red2,six,255,0,0)
        elif (redScore == 5):
            setScoreDisplay(strip,red2,five,255,0,0)
        elif (redScore == 4):
            setScoreDisplay(strip,red2,four,255,0,0)
        elif (redScore == 3):
            setScoreDisplay(strip,red2,three,255,0,0)
        elif (redScore == 2):
            setScoreDisplay(strip,red2,two,255,0,0)
        elif (redScore == 1):
            setScoreDisplay(strip,red2,one,255,0,0)
        else:
            setScoreDisplay(strip,red2,zero,255,0,0)


    #set blue score
    if (blueScore == 10):
        setScoreDisplay(strip,blue1,one,0,0,255)
        setScoreDisplay(strip,blue2,zero,0,0,355)
    else:
        setScoreDisplay(strip,blue2,eight,0,0,0)
        if (blueScore == 9):
            setScoreDisplay(strip,blue1,nine,0,0,255)
        elif (blueScore == 8):
            setScoreDisplay(strip,blue1,eight,0,0,255)
        elif (blueScore == 7):
            setScoreDisplay(strip,blue1,seven,0,0,255)
        elif (blueScore == 6):
            setScoreDisplay(strip,blue1,six,0,0,255)
        elif (blueScore == 5):
            setScoreDisplay(strip,blue1,five,0,0,255)
        elif (blueScore == 4):
            setScoreDisplay(strip,blue1,four,0,0,255)
        elif (blueScore == 3):
            setScoreDisplay(strip,blue1,three,0,0,255)
        elif (blueScore == 2):
            setScoreDisplay(strip,blue1,two,0,0,255)
        elif (blueScore == 1):
            setScoreDisplay(strip,blue1,one,0,0,255)
        else:
            setScoreDisplay(strip,blue1,zero,0,0,255)


    strip.show()
    '''
    index = 0
    direction = 1
    for j in range(0,15):
    for i in range(0,30):
    if(((i > 5 and i < 11) or (i > 20 and i < 26)) and (j > 2 and j < 12)):
    strip.setPixelColor(index, Color(255,0,0))
    strip.show()
    else:
    strip.setPixelColor(index, Color(0,255,0))
    strip.show() 
    if(direction):
    index += 1
    else:
    index -= 1

    strip.setPixelColor(index, Color(0,255,0))
    strip.show()                 
    index += 30
    if(direction):
    direction = 0
    else:
    direction = 1
    '''



    '''
    #Random LED Output

    for i in range(0, strip.numPixels()):
    strip.setPixelColor(i , Color(int(random.random() * 255), int(random.random() * 255), int(random.random() * 255)))
    strip.show()
    time.sleep(wait_ms/1000)
    '''

def setBorder(strip):
    for i in range(WIDTH):
        strip.setPixelColor(i,Color(255,0,0))
        strip.setPixelColor(i+30,Color(255,0,0))
    for i in range(WIDTH * HEIGHT - 30, WIDTH * HEIGHT - 1):
        strip.setPixelColor(i,Color(255,0,0))
        strip.setPixelColor(i-30,Color(255,0,0))
    for i in range(HEIGHT):
        strip.setPixelColor(i*30 + 29,Color(255,0,0))
        strip.setPixelColor(i*30, Color(255,0,0))
        strip.setPixelColor(i*30 + 14, Color(255,0,0))
        strip.setPixelColor(i*30 + 15, Color(255,0,0))

def clearStrip(strip):
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))

def purdueP(strip):
    """p = [
        0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,
        0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,
        0,0,0,0,0,0,1,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,1,
        0,0,0,0,0,1,2,3,3,3,3,3,3,3,3,2,2,2,2,2,2,3,3,3,3,3,3,3,2,1,
        0,0,0,0,0,1,2,2,2,3,3,3,3,3,2,1,1,1,1,1,1,2,3,3,3,3,3,3,2,1,
        0,0,0,0,0,1,1,1,2,3,3,3,3,3,3,2,2,2,2,2,2,3,3,3,3,3,3,2,1,1,
        0,0,0,0,0,0,0,1,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,1,0,
        0,0,0,0,0,0,0,1,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,0,
        0,0,0,0,0,0,1,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,1,0,0,
        0,0,0,0,0,0,1,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,0,0,0,
        0,0,1,1,1,1,1,2,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,0,0,0,0,0,
        0,0,1,2,2,2,2,2,3,3,3,3,3,3,3,3,2,2,1,0,0,0,0,0,0,0,0,0,0,0,
        0,0,1,2,3,3,3,3,3,3,3,3,3,3,3,3,2,1,0,0,0,0,0,0,0,0,0,0,0,0,
        0,1,2,3,3,3,3,3,3,3,3,3,3,3,3,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,
        0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,
    ]
    """
    """p = [
        0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,
        0,0,0,0,0,0,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,0,
        0,0,0,0,0,0,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,
        0,0,0,0,0,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,
        0,0,0,0,0,1,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,3,3,3,3,3,3,3,3,1,
        0,0,0,0,0,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,
        0,0,0,0,0,0,0,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,0,
        0,0,0,0,0,0,0,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,0,
        0,0,0,0,0,0,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,0,0,
        0,0,0,0,0,0,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,0,0,0,
        0,0,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,0,0,0,0,0,
        0,0,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,0,0,0,0,0,0,0,0,0,0,0,
        0,0,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,0,0,0,0,0,0,0,0,0,0,0,0,
        0,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,0,0,0,0,0,0,0,0,0,0,0,0,
        0,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,
    ]
    """
    p = [
        0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,
        0,0,0,0,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,0,
        0,0,0,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
        0,0,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,1,1,1,1,3,3,3,3,3,3,3,3,3,
        0,0,0,0,1,1,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,3,3,3,3,3,3,3,
        0,0,0,0,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,3,3,3,3,3,3,3,1,
        0,0,0,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,0,
        0,0,0,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,0,
        0,0,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,0,0,
        0,0,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,0,0,0,
        0,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,0,0,0,0,0,
        0,1,1,1,1,1,3,3,3,3,3,3,3,3,3,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,
        1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,
        1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,
        1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0
    ]

    p = transform(p)
    for i in range(0, len(p)):
        if(p[i] == 0):
            #strip.setPixelColor(i, Color(200, 200, 200))
            strip.setPixelColor(i, Color(0, 0, 0))
        if(p[i] == 1):
            strip.setPixelColor(i, Color(0, 0, 0))
            #strip.setPixelColor(i, Color(10, 10, 5))
        if(p[i] == 2):
            strip.setPixelColor(i, Color(64, 88, 5))
            #strip.setPixelColor(i, Color(105, 105, 105))
        if(p[i] == 3):    
            strip.setPixelColor(i, Color(129, 177 , 11))
            strip.show()
            time.sleep(5)
    return()

def usaFlag(strip):
    p = [
        3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
        1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
        1,0,1,0,1,0,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        1,1,0,1,0,1,0,1,0,1,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
        1,0,1,0,1,0,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        1,1,0,1,0,1,0,1,0,1,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
        1,0,1,0,1,0,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
        3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
        3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
    ]

    p = transform(p)
    for i in range(0, len(p)):
        if(p[i] == 0):
            #strip.setPixelColor(i, Color(200, 200, 200))
            strip.setPixelColor(i, Color(100, 100, 100))
        if(p[i] == 1):
            strip.setPixelColor(i, Color(0, 0, 255))
        if(p[i] == 2):
            strip.setPixelColor(i, Color(0, 255, 0))
        if(p[i] == 3):    
            strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    time.sleep(5)
    return()

def twochase(strip, col1, col2):
    for i in range(0, LED_COUNT):
        strip.setPixelColor(i, col1)
        strip.setPixelColor(LED_COUNT - 1 - i)
        if(i == LED_COUNT - 1 - i):
            break;
        strip.show()
    return()


        
def main():
    #Socket
    #sd = socket.socket(socket.AF_UNIX)
    #sd.bind('/home/pi/game')

    #Vars
    matrix = numpy.zeros((30,15))
    #scoreMode = True
    #redScore = 10
    #blueScore = 10
    redScore = int(sys.argv[1])
    blueScore = int(sys.argv[2])
    scoreMode = int(sys.argv[3])
    recentScore = sys.argv[4]
    
    
    initStarts()

    #***** LED MATRIX ************
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    #Blank all LED's
    #clearStrip(strip)


    #***** UART ***************

    clearStrip(strip)
    setBorder(strip)
    strip.show()


    #******* BUTTONS ***********

    if(recentScore == 'r'):
        theaterChase(strip, Color(0,   127,   0), 50, 5)  # Red theater chase
    elif(recentScore == 'b'):
        theaterChase(strip, Color(  0,   0, 127), 50, 5)  # Blue theater chase

    #Temporary
    #purdueP(strip)

    #clearStrip(strip)
    #setBorder(strip)
    #strip.show()

    '''
    pattern = {
            0  : outputScore(strip, redScore, blueScore, False),
            1  : purdueP(strip),
            2  : usaFlag(strip),
            3  : twochase(strip, Color(255, 0, 0), Color(0, 0, 255)),
            4  : colorWipe(strip, Color(255, 0, 0)),  # Green wipe,
            5  : colorWipe(strip, Color(0, 255, 0)),
            6  : colorWipe(strip, Color(0, 0, 255)),
            7  : rainbow(strip),
            8  : rainbowCycle(strip),
            9  : theaterChase(strip, Color(127, 127, 127))
    }
    '''
    while(True):
        if(scoreMode == 0):
            outputScore(strip, redScore, blueScore, False)
        elif(scoreMode == 1):
            purdueP(strip)
        elif(scoreMode == 2):
            usaFlag(strip)
        elif(scoreMode == 3):
            twochase(strip, Color(255, 0, 0), Color(0, 0, 255))
        elif(scoreMode == 4):
            colorWipe(strip, Color(255, 0, 0))
        elif(scoreMode == 5):
            colorWipe(strip, Color(0, 255, 0))
        elif(scoreMode == 6):
            colorWipe(strip, Color(0, 0, 255))
        elif(scoreMode == 7):
            rainbow(strip)
        elif(scoreMode == 8):
            rainbowCycle(strip)
        else:
            theaterChase(strip, Color(127, 127, 127))
if __name__ == '__main__':
    main()

