#Microcontroller Interfaces

import RPi.gpio as GPIO
import teams.py as teams


class redmicro:
    def __init__(self):
        self.nrst    = GPIO.output(9)
        self.rrsel   = GPIO.output(23)
