#Raspberry PI Pin Input/Output

import RPi.gpio as GPIO

class pins:
    def __init__(self):
        self.pin0  = GPIO.input(0)
        #self.pin1  = 
        self.pin2  = GPIO.input(2)
        self.pin3  = GPIO.input(3)
        #self.pin4  = 
        #self.pin5  =
        #self.pin6  =
        self.pin7  = GPIO.input(7)
        self.pin8  = GPIO.input(8)
        self.pin9  = GPIO.output(9)
        #self.pin10 =
        #self.pin11 =
        self.pin12 = GPIO.input(12)
        self.pin13 = GPIO.input(13)
        self.pin14 = GPIO.input(14)
        #self.pin15 =
        #self.pin16 =
        #self.pin17 =
        #self.pin18 =
        #self.pin19 =
        #self.pin20 =
        #self.pin21 = CLK
        self.pin22 = GPIO.output(22)
        self.pin23 = GPIO.input(23)
        self.pin24 = GPIO.input(24)
        self.pin25 = GPIO.output(25)
        #self.pin26 =
        #self.pin27 =
        #self.pin28 =
        #self.pin29 =
        #self.pin30 =
        #self.pin31 =
        #self.pin32 =
        #self.pin33 =
        #self.pin34 =
        #self.pin35 =
        #self.pin36 =
        #self.pin37 =
        #self.pin38 =
        #self.pin39 =
        #self.pin40 =
