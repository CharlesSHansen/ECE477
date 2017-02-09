#!/usr/bin/python3


import time
from pld import PLD
import RPi.GPIO as GPIO

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    pld = PLD()
    while(True):
        GPIO.output(5, 1)
        time.sleep(.001)
        GPIO.output(5, 0)
        time.sleep(.001)
        
if __name__ == "__main__":
    main()
