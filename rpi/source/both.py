#!/usr/bin/python
import time
import random
import numpy
from neopixel import *
from PIL import Image
from math import *
import sys
import os
import serial
import RPi.GPIO as GPIO
import pins

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
    return()

def twochase(strip, col1, col2):
    for i in range(0, LED_COUNT):
        strip.setPixelColor(i, col1)
        strip.setPixelColor(LED_COUNT - 1 - i)
        if(i == LED_COUNT - 1 - i):
            break;
        strip.show()
    return()


        

def sendMicro(message,port):
    #w = message.encode(encoding='ASCII')
    #w = bytes("dicks", "ASCII")
    #Turn off CPLD button lights
    if(message.isupper()):
        GPIO.output(9, 1)
        time.sleep(0.3)
        GPIO.output(9, 0)
    else:
        GPIO.output(24, 1)
        time.sleep(0.3)
        GPIO.output(24, 0)
    #Send Message
    port.write(message)
    print(message)
    time.sleep(0.1)
    #port.close()
    #while(1):
        #port.write(w)
        #print(port.readline())

def updateScore(RedTeamScore, BlueTeamScore, scoreMode, recentScore):

    if (__debug__):
        print "(debug) Flashing Lights for Score: ", time.strftime('%H:%M:%S')
    if(recentScore == 'r'):
        theaterChase(strip, Color(0,   127,   0), 50, 5)  # Red theater chase
    elif(recentScore == 'b'):
        theaterChase(strip, Color(  0,   0, 127), 50, 5)  # Blue theater chase

    clearStrip(strip)
    setBorder(strip)
    strip.show()
    if (__debug__):
        print "(debug) Updating Score: ", time.strftime('%H:%M:%S')
        outputScore(strip, redScore, blueScore, False)
        time.sleep(2)
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
        
def main():
    if (__debug__):
        print "(debug) both.py Started: ", time.strftime('%H:%M:%S')
    #Vars
    matrix = numpy.zeros((30,15))
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

    GPIO.setwarnings(False)
        #GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)
    pins.Pins()
    #UART Port declaration
    GPIO.setup(9, GPIO.OUT, initial=GPIO.LOW)
    #GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)
    #GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)#, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(19, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)

    
    port = serial.Serial("/dev/serial0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1.0)
   
    #sendMicro("g",port)
    #return

    global Start
    global globalLock
    global globalLockTime

    if (__debug__):
        print "(debug) Initializing Variables: ", time.strftime('%H:%M:%S')

    Start = 1

    #Send out an nRST
    GPIO.output(19,1)
    time.sleep(1)
    GPIO.output(19,0)
    
    RedTeamScore = 10
    RedFlag = 0
    RedRack = 2
    RedRackFlag = 0
    
    BlueTeamScore = 10
    BlueFlag = 0
    BlueRack = 2
    BlueRackFlag = 0

    lastPattern = 1
    #Score Mode vs Pattern Mode Startup Select
    if(GPIO.input(11) == 0):
        if (__debug__):
            print "(debug) Starting in Score Mode: ", time.strftime('%H:%M:%S')
        scoreMode = 0
    else:
        if (__debug__):
            print "(debug) Starting in Pattern Mode: ", time.strftime('%H:%M:%S')
        scoreMode = 1
        
    if (__debug__):
        print "(debug) Starting Display: ", time.strftime('%H:%M:%S')
    scoreprog = updateScore(None, RedTeamScore, BlueTeamScore, scoreMode, None)
    
    if (__debug__):
        print "(debug) Entering Main Loop: ", time.strftime('%H:%M:%S')
    while(True):
        #Global Lock
        if(globalLock):
            if(time.time() - globalLockTime >= 0.5):
                globalLock = 0
                globalLockTime = 0
                if (__debug__):
                    print "(debug) Global Lock Released", time.strftime('%H:%M:%S')
        else:  #Process Flag
            if(RedFlag):
                if (__debug__):
                    print "(debug) Red Team Update Score: ", time.strftime('%H:%M:%S')
                RedFlag = 0
                scoreprog = updateScore(RedTeamScore, BlueTeamScore, scoreMode, 'r')
                time.sleep(1)

            if(BlueFlag):
                if (__debug__):
                    print "(debug) Blue Team Update Score: ", time.strftime('%H:%M:%S')
                BlueFlag = 0
                scoreprog = updateScore(RedTeamScore, BlueTeamScore, scoreMode, 'b')
                time.sleep(1)
            
        #Score Mode Switch
        if(GPIO.input(11) == 0 and scoreMode != 0):
            if (__debug__):
                print "(debug) Switching to Score Mode: ", time.strftime('%H:%M:%S')
            lastPattern = scoreMode
            scoreMode = 0
            scoreprog = updateScore(None, RedTeamScore, BlueTeamScore, scoreMode, None)
        elif(GPIO.input(11) == 1 and scoreMode == 0):
            if (__debug__):
                print "(debug) Switching to Pattern Mode: ", time.strftime('%H:%M:%S')
            scoreMode = lastPattern
            scoreprog = updateScore(None, RedTeamScore, BlueTeamScore, scoreMode, None)

        #Switch Pattern
        if(GPIO.input(13) == 1 and scoreMode != 0):
            if (__debug__):
                print "(debug) Next Pattern: ", time.strftime('%H:%M:%S')
            scoreMode += 1
            scoreprog = updateScore(None, RedTeamScore, BlueTeamScore, scoreMode, None)


            
        #Reset Game
        if(GPIO.input(6) == 1):
            if (__debug__):
                print "(debug) Game Reset: ", time.strftime('%H:%M:%S')
            Start = 1
            port = serial.Serial("/dev/ttyS0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1.0)

            RedTeamScore = 10
            RedFlag = 0
            RedRack = 2
            RedRackFlag = 0
            
            BlueTeamScore = 10
            BlueFlag = 0
            BlueRack = 2
            BlueRackFlag = 0

            GPIO.output(19,1)
            time.sleep(0.3)
            GPIO.output(19,0)


        #Start the Game    
        if(Start):
            
            #Red Score Signal
            if(GPIO.input(25) == 1 and RedFlag == 0):
                RedFlag = 1
                RedTeamScore -= 1
                if (__debug__):
                    print "(debug) Red Team Scored: ", time.strftime('%H:%M:%S')
                    print "(debug) Game Score - Blue: ", BlueTeamScore, " Red: ", RedTeamScore, ": ", time.strftime('%H:%M:%S')
                setGlobalLock()
                
            #Blue Score Signal
            if(GPIO.input(10) == 1 and BlueFlag == 0):
                BlueFlag = 1
                BlueTeamScore -= 1
                GPIO.output(23, 1)
                time.sleep(1)
                GPIO.output(23, 0)
                if (__debug__):
                    print "(debug) Blue Team Scored: ", time.strftime('%H:%M:%S')
                    print "(debug) Game Score - Blue: ", BlueTeamScore, " Red: ", RedTeamScore, ": ", time.strftime('%H:%M:%S')
                setGlobalLock()

            #Send Red Re-rack Signal #Talk with Mikey to see which ones are which
            if(RedRack > 0 and RedFlag == 0):
                if(RedRack == 2):
                    RedRack -= 1
                    if(GPIO.input(21) and RedTeamScore == 6 ):
                        if (__debug__):
                            print "(debug) Red Reracking to 3-2-1: ", time.strftime('%H:%M:%S')
                        sendMicro("a",port)
                        RedRackFlag = 1
                    elif(GPIO.input(20) and RedTeamScore == 4):
                        if (__debug__):
                            print "(debug) Red Reracking to Diamond: ", time.strftime('%H:%M:%S')
                        sendMicro("b",port)
                        RedRackFlag = 1
                    elif(GPIO.input(16) and RedTeamScore == 5):
                        if (__debug__):
                            print "(debug) Red Reracking to Box: ", time.strftime('%H:%M:%S')
                        sendMicro("c",port)
                        RedRackFlag = 1
                    elif(GPIO.input(12) and RedTeamScore == 2):
                        if (__debug__):
                            print "(debug) Red Reracking to Gentlemen's: ", time.strftime('%H:%M:%S')
                        sendMicro("d",port)
                        RedRackFlag = 1
                    elif(GPIO.input(7) and RedTeamScore == 3):
                        if (__debug__):
                            print "(debug) Red Reracking to Line: ", time.strftime('%H:%M:%S')
                        sendMicro("e",port)
                        RedRackFlag = 1
                    elif(GPIO.input(8) and RedTeamScore == 3):
                        if (__debug__):
                            print "(debug) Red Reracking to Triangle: ", time.strftime('%H:%M:%S')
                        sendMicro("f",port)
                        RedRackFlag = 1
                    else:
                        RedRack += 1
                        RedRackFlag = 0
                else:
                    if(GPIO.input(8) and RedTeamScore == 2):
                        if (__debug__):
                            print "(debug) Red Reracking to Gentlemen's: ", time.strftime('%H:%M:%S')
                        sendMicro("c", port)
                        RedRack = 0
        
            #Send Blue Re-rack Signal
            if(BlueRack > 0 and BlueFlag == 0):
                if(BlueRack == 2):
                    BlueRack -= 1
                    if(GPIO.input(2) == False and BlueTeamScore == 6):
                        if (__debug__):
                            print "(debug) Blue Reracking to 3-2-1: ", time.strftime('%H:%M:%S')
                        sendMicro("A",port)
                        BlueRackFlag = 1
                    elif(GPIO.input(3)== False and BlueTeamScore == 4):
                        if (__debug__):
                            print "(debug) Blue Reracking to Diamond: ", time.strftime('%H:%M:%S')
                        sendMicro("B",port)
                        BlueRackFlag = 1
                    elif(GPIO.input(4) == False and BlueTeamScore == 5):
                        if (__debug__):
                            print "(debug) Blue Reracking to Box: ", time.strftime('%H:%M:%S')
                        sendMicro("C",port)
                        BlueRackFlag = 1
                    elif(GPIO.input(17) == False and BlueTeamScore == 2):
                        if (__debug__):
                            print "(debug) Blue Reracking to Gentlemen's: ", time.strftime('%H:%M:%S')
                        sendMicro("D",port)
                        BlueRackFlag = 1
                    elif(GPIO.input(27) == False and BlueTeamScore == 3):
                        if (__debug__):
                            print "(debug) Blue Reracking to Line: ", time.strftime('%H:%M:%S')
                        sendMicro("E",port)
                        BlueRackFlag = 1
                    elif(GPIO.input(22)== False and BlueTeamScore == 3):
                        if (__debug__):
                            print "(debug) Blue Reracking to Triangle: ", time.strftime('%H:%M:%S')
                        sendMicro("F",port)
                        BlueRackFlag = 1
                    else:
                        BlueRack += 1
                        BlueRackFlag = 0
                else:
                    if(GPIO.input(17)== False and BlueTeamScore == 2):
                        if (__debug__):
                            print "(debug) Blue Reracking to Gentlemen's: ", time.strftime('%H:%M:%S')
                        sendMicro("C", port)
                        BlueRack = 0
            #Game End State
            if(RedTeamScore == 0 or BlueTeamScore == 0):
                Start = 0
                port.close()

def setGlobalLock():
    global globalLock
    global globalLockTime
    globalLock = 1
    globalLockTime = time.time()
    if (__debug__):
        print "(debug) Setting Global Lock: ", time.strftime('%H:%M:%S')
    return

if __name__ == '__main__':
    main()
