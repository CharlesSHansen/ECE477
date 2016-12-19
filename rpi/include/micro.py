#Microcontroller Interfaces

import pins
import teams.py as teams


class redmicro:
    def __init__(self):
        self.nrst    = pins.pin9
        self.rrout   = teams.red.rrout

class redmicro:
    def __init__(self):
        self.nrst    = pins.pin9
        self.rrout   = teams.blue.rrout
