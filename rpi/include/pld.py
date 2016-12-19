#PLD Pins from RPI (nRST and CLK)

import pins

class pld:
    def __init__(self):
        self.clk    = pins.pin21
        self.nrst   = pins.pin9
