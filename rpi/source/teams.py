#Classes for Blue and Red Teams

from pins import Pins
import RPi.GPIO as GPIO
import time


class Blue():
    def __init__(self):
        self.pins     = Pins()
        self.score    = self.pins.pin17
        self.foul     = self.pins.pin22
        self.rrcycle  = self.pins.pin9
        self.rrsel    = self.pins.pin11
        self.rrout    = self.pins.pin6

    def rerack(self, type):
        if(type == 1):
            print("Type 1 Blue RR")
            GPIO.output(6, 1)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 1)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 1)
            time.sleep(0.001)
            GPIO.output(6, 0)
        elif(type == 2):
            print("Type 2 Blue RR")
            GPIO.output(6, 1)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 1)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 0)
        elif(type == 3):
            print("Type 3 Blue RR")
            GPIO.output(6, 1)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 1)
            time.sleep(0.001)
            GPIO.output(6, 0)
        elif(type == 4):
            print("Type 4 Blue RR")
            GPIO.output(6, 1)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 0)
        elif(type == 5):
            print("Type 5 Blue RR")
            GPIO.output(6, 1)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 1)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 0)
        elif(type == 6):
            print("Type 6 Blue RR")
            GPIO.output(6, 1)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 1)
            time.sleep(0.001)
            GPIO.output(6, 0)
            time.sleep(0.001)
            GPIO.output(6, 0)
            

class Red():
    def __init__(self):
        self.pins     = Pins()
        self.score    = self.pins.pin27
        self.foul     = self.pins.pin10
        self.rrcycle  = self.pins.pin13
        self.rrsel    = self.pins.pin19
        self.rrout    = self.pins.pin26
    def rerack(self, type):
        if(type == 1):
            print("Type 1 Red RR")
            GPIO.output(26, 1)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 1)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 1)
            time.sleep(0.001)
            GPIO.output(26, 0)
        elif(type == 2):
            print("Type 2 Red RR")
            GPIO.output(26, 1)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 1)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 0)
        elif(type == 3):
            print("Type 3 Red RR")
            GPIO.output(26, 1)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 1)
            time.sleep(0.001)
            GPIO.output(26, 0)
        elif(type == 4):
            print("Type 4 Red RR")
            GPIO.output(26, 1)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 0)
        elif(type == 5):
            print("Type 5 Red RR")
            GPIO.output(26, 1)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 1)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 0)
        elif(type == 6):
            print("Type 6 Red RR")
            GPIO.output(26, 1)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 1)
            time.sleep(0.001)
            GPIO.output(26, 0)
            time.sleep(0.001)
            GPIO.output(26, 0)
            
            
