#!/usr/bin/python

import time
import random
from pld import PLD
import pins
import RPi.GPIO as GPIO
import serial
import os
import subprocess

Start = 0
globalLock = 0
globalLockTime = 0
def sendMicro(message,port):
    #w = message.encode(encoding='ASCII')
    #w = bytes("dicks", "ASCII")
    port.write("a")
    port.close()
    #while(1):
        #port.write(w)
        #print(port.readline())

def updateScore(scoreprog, RedTeamScore, BlueTeamScore, scoreMode, recentScore):
    if(scoreprog != None):
        scoreprog.terminate()
        scoreprog.kill()
    scoreargs = "exec /usr/bin/python main.py " + str(RedTeamScore) + " " + str(BlueTeamScore) + " " + str(scoreMode) + " " + str(recentScore)
    #print scoreargs
    scoreprog = subprocess.Popen(scoreargs, shell=True)
    return scoreprog
        
def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    pins.Pins()
    #Socket Communication
    #sd = socket.socket(socket.AF_UNIX)
    #sd.connect('/home/pi/game')
    #sd.send('connect')
    #UART Port declaration
    #port = serial.Serial("/dev/ttyS0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1.0)
   
    #sendMicro("g",port)
    #return

    global Start
    global globalLock
    global globalLockTime
    
    RedTeamScore = 10
    RedFlag = 0
    RedRack = 2
    RedRackFlag = 0
    
    BlueTeamScore = 10
    BlueFlag = 0
    BlueRack = 2
    BlueRackFlag = 0

    if(GPIO.input(22) == 1):
        scoreMode = 0
    else:
        scoreMode = 1

    scoreprog = updateScore(None, RedTeamScore, BlueTeamScore, scoreMode, None)

    
    while(True):
        #Global Lock
        if(globalLock):
            if(time.time() - globalLockTime >= 0.5):
                globalLock = 0
                globalLockTime = 0
                print("Lock removed")
        else:  #Process Flag
            if(RedFlag):
                RedFlag = 0
                scoreprog = updateScore(None, RedTeamScore, BlueTeamScore, scoreMode, r)
                time.sleep(2)

            if(BlueFlag):
                BlueFlag = 0
                scoreprog = updateScore(None, RedTeamScore, BlueTeamScore, scoreMode, r)
                time.sleep(2)

        #Set Start
        if(GPIO.input(4) == 1 and Start == 0):
            Start = 1
            print("Game Start")
            
        #Score Mode Switch
        if(GPIO.input(22) == 1 and scoreMode != 0):
            scoreMode = 0
            scoreprog = updateScore(None, RedTeamScore, BlueTeamScore, scoreMode, None)

        #Switch Pattern
        if(GPIO.input(10) == 1 and scoreMode != 0):
            scoreMode += 1
            scoreprog = updateScore(None, RedTeamScore, BlueTeamScore, scoreMode, None)


            
        #Reset Game
        if(GPIO.input(2) == 1):
            print("Game Reset")
            Start = 0

            RedTeamScore = 10
            RedFlag = 0
            RedRack = 2
            RedRackFlag = 0
            
            BlueTeamScore = 10
            BlueFlag = 0
            BlueRack = 2
            BlueRackFlag = 0

            GPIO.output(3,1)
            time.sleep(0.2)
            GPIO.output(3,0)

        #Start the Game    
        if(Start):
            
            #Red Score Signal
            if(GPIO.input(27) == 1 and RedFlag == 0):
                print('Red Score')
                RedFlag = 1
                RedTeamScore -= 1
                setGlobalLock()
            #elif(GPIO.input(27) == 0 and RedFlag == 1):
            #RedFlag = 0
            #RedRackFlag = 0
                
            #Blue Score Signal
            if(GPIO.input(17) == 1 and BlueFlag == 0):
                print('Blue Score')
                BlueFlag = 1
                BlueTeamScore -= 1
                setGlobalLock()
            #elif(GPIO.input(17) == 0 and BlueFlag == 1):
            #BlueFlag = 0
            #BlueRackFlag = 0

                #Send Red Re-rack Signal
            if(RedRack > 0 and RedFlag == 0):
                RedRack -= 1
                if(GPIO.input(13)):
                    sendMicro("1",port)
                    RedRackFlag = 1
                elif(GPIO.input(19)):
                    sendMicro("2",port)
                    RedRackFlag = 1
                elif(GPIO.input(16)):
                    sendMicro("3",port)
                    RedRackFlag = 1
                elif(GPIO.input(12)):
                    sendMicro("4",port)
                    RedRackFlag = 1
                elif(GPIO.input(25)):
                    sendMicro("5",port)
                    RedRackFlag = 1
                elif(GPIO.input(24)):
                    sendMicro("6",port)
                    RedRackFlag = 1
                else:
                    RedRack += 1
                    RedRackFlag = 0

            #Send Blue Re-rack Signal
            if(BlueRack > 0 and BlueFlag == 0):
                BlueRack -= 1
                if(GPIO.input(9)):
                    sendMicro("11",port)
                    BlueRackFlag = 1
                elif(GPIO.input(11)):
                    sendMicro("12",port)
                    BlueRackFlag = 1
                elif(GPIO.input(21)):
                    sendMicro("13",port)
                    BlueRackFlag = 1
                elif(GPIO.input(20)):
                    sendMicro("14",port)
                    BlueRackFlag = 1
                elif(GPIO.input(7)):
                    sendMicro("15",port)
                    BlueRackFlag = 1
                elif(GPIO.input(8)):
                    sendMicro("16",port)
                    BlueRackFlag = 1
                else:
                    BlueRack += 1
                    BlueRackFlag = 0

            

def setGlobalLock():
    global globalLock
    global globalLockTime
    globalLock = 1
    globalLockTime = time.time()
    print("Lock set at: ", globalLockTime)
    return

if __name__ == '__main__':
    main()
