#Classes for Blue and Red Teams

import pins

class blue:
    def __init__(self):
        self.score    = pins.pin0
        self.foul     = pins.pin3
        self.rrcycle  = pins.pin13
        self.rrsel    = pins.pin14
        self.rrout    = pins.pin22

class red:
    def __init__(self):
        self.score    = pins.pin2
        self.foul     = pins.pin12
        self.rrcycle  = pins.pin23
        self.rrsel    = pins.pin24
        self.rrout    = pins.pin25
    
