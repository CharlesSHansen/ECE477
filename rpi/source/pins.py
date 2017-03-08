
#Raspberry PI Pin Input/Output

import RPi.GPIO as GPIO
import time

class Pins:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        #GPIO.setup(0, GPIO.IN), pull_up_down = GPIO.PUD_UP)
        #self.pin0  = GPIO.input(0)
        #self.pin1  = GPIO
        GPIO.setup(2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.pin2  = GPIO.input(2)
        GPIO.setup(3, GPIO.OUT)
        self.pin3  = GPIO.output(3, 0)
        GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.pin4  = GPIO.input(4)
        GPIO.setup(5, GPIO.OUT)
        self.pin5  = GPIO.output(5, 1)
        GPIO.setup(6, GPIO.OUT)
        self.pin6  = GPIO.output(6, 0)
        GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.pin7  = GPIO.input(7)
        GPIO.setup(8, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.pin8  = GPIO.input(8)
        #GPIO.setup(9, GPIO.OUT)
        GPIO.setup(9, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.pin9  = GPIO.input(9)
        GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.pin10 = GPIO.input(10)
        GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.pin11 = GPIO.input(11)
        GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        #GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        #self.pin12 = GPIO.input(12)
        GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.pin13 = GPIO.input(13)
        #GPIO.setup(14, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        #self.pin14 = GPIO.input(14)
        #self.pin15 =
        #self.pin16 =
        GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(17, GPIO.IN)#, pull_up_down = GPIO.PUD_DOWN)
        self.pin17 = GPIO.input(17)
        #self.pin18 =
        GPIO.setup(18, GPIO.OUT)#, pull_up_down = GPIO.PUD_DOWN)
        self.pin18 = GPIO.output(18,0)
        GPIO.setup(19, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.pin19 = GPIO.input(19)
        GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        #self.pin20 =
        GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        #self.pin21 = GPIO.output(21, 0)
        GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.pin22 = GPIO.input(2)
        #GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        #self.pin23 = GPIO.input(23)
        GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.pin24 = GPIO.input(24)
        GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.pin25 = GPIO.input(25)
        GPIO.setup(26, GPIO.OUT)
        self.pin26 = GPIO.output(26, 0)
        GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.pin27 = GPIO.input(27)
