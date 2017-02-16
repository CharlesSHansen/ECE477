#Microcontroller Interfaces

from pins import Pins
from teams import Red
from teams import Blue

class Redmicro:
    def __init__(self):
        self.red     = Red()
        self.pins    = Pins()
        self.nrst    = self.pins.pin3
        self.rrout   = self.red.rrout

class Bluemicro:
    def __init__(self):
        self.blue    = Blue()
        self.pins    = Pins()
        self.nrst    = self.pins.pin3
        self.rrout   = self.blue.rrout
