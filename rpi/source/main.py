# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
from __future__ import print_function
import time
import random
import numpy
#from enum import Enum
from neopixel import *
from PIL import Image
from math import *


# LED strip configuration:
WIDTH 		   = 30
HEIGHT		   = 15
LED_COUNT      = WIDTH * HEIGHT    # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


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
        strip.setPixelColor(disp[i],Color(mask[i]*g,mask[i]*b,mask[i]*r))
        strip.show()


def outputScore(strip, redScore, blueScore, clear):
    if (clear):
        clearStrip(strip)
        #setBorder(strip)

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
        setScoreDisplay(strip,blue1,one,255,0,0)
        setScoreDisplay(strip,blue2,zero,255,0,0)
    else:
        setScoreDisplay(strip,blue1,eight,0,0,0)
        if (blueScore == 9):
            setScoreDisplay(strip,blue2,nine,255,0,255)
        elif (blueScore == 8):
            setScoreDisplay(strip,blue2,eight,255,0,0)
        elif (blueScore == 7):
            setScoreDisplay(strip,blue2,seven,255,0,0)
        elif (blueScore == 6):
            setScoreDisplay(strip,blue2,six,255,0,0)
        elif (blueScore == 5):
            setScoreDisplay(strip,blue2,five,255,0,0)
        elif (blueScore == 4):
            setScoreDisplay(strip,blue2,four,255,0,0)
        elif (blueScore == 3):
            setScoreDisplay(strip,blue2,three,255,0,0)
        elif (blueScore == 2):
            setScoreDisplay(strip,blue2,two,255,0,0)
        elif (blueScore == 1):
            setScoreDisplay(strip,blue2,one,255,0,0)
        else:
            setScoreDisplay(strip,blue2,zero,255,0,0)


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
        strip.setPixelColor(i,Color(255,255,255))
        strip.setPixelColor(i+30,Color(255,255,255))
    for i in range(WIDTH * HEIGHT - 30, WIDTH * HEIGHT - 1):
        strip.setPixelColor(i,Color(255,255,255))
        strip.setPixelColor(i-30,Color(255,255,255))
    for i in range(HEIGHT):
        strip.setPixelColor(i*30 + 29,Color(255,255,255))
        strip.setPixelColor(i*30, Color(255,255,255))
        strip.setPixelColor(i*30 + 14, Color(255,255,255))
        strip.setPixelColor(i*30 + 15, Color(255,255,255))

def clearStrip(strip):
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))


#def sendReRack(option):


def main():
    #Vars
    matrix = numpy.zeros((30,15))
    scoreMode = True
    redScore = 10
    blueScore = 10
    initStarts()


    print(red1)
    print("")
    print(red2)
    print("")
    print(blue1)
    print("")
    print(blue2)
    print("")


    #***** LED MATRIX ************
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    #Blank all LED's
    #clearStrip(strip)


    #***** UART ***************



    #******* BUTTONS ***********

    h = 1
    while (h == 1):
        h = 0
        #How to get this to run smooth while still listening for input from micro?

        if (scoreMode):
            outputScore(strip,redScore,blueScore, True)
        else:
            #print designs
            theaterChaseRainbow(strip)
    '''
    # Color wipe animations.
    colorWipe(strip, Color(255, 0, 0))  # Green wipe
    colorWipe(strip, Color(0, 255, 0))  # Red wipe
    colorWipe(strip, Color(0, 0, 255))  # Blue wipe
    # Theater chase animations.
    theaterChase(strip, Color(127, 127, 127))  # White theater chase
    theaterChase(strip, Color(127,   0,   0))  # Red theater chase
    theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
    # Rainbow animations.
    rainbow(strip)
    rainbowCycle(strip)
    theaterChaseRainbow(strip)
    '''

if __name__ == '__main__':
    main()

