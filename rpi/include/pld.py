#PLD Pins from RPI (nRST and CLK)


import time
import RPi.GPIO as GPIO
from pins import Pins

class PLD:
    def __init__(self):
        self.pins   = Pins()
        self.clk    = self.pins.pin5
        self.nrst   = self.pins.pin3


