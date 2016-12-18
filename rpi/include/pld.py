#PLD Pins from RPI (nRST and CLK)

import RPi.GPIO as GPIO

class pld:
    def __init__(self):
        self.clk    = GPIO.output(22)
        self.nrst   = GPIO.output(9)
