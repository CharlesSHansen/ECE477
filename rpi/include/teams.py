#Classes for Blue and Red Teams

import RPi.GPIO as GPIO

class blue:
    def __init__(self):
        self.score    = GPIO.input(0)
        self.foul     = GPIO.input(3)
        self.rrcycle  = GPIO.input(13)
        self.rrsel    = GPIO.output(14)


class red:
    def __init__(self):
        self.score    = GPIO.input(2)
        self.foul     = GPIO.input(12)
        self.rrcycle  = GPIO.input(22)
        self.rrsel    = GPIO.output(23)
    
