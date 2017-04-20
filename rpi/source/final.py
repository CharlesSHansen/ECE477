#!/usr/bin/python

import os
import time
import subprocess
import serial
import RPi.GPIO as GPIO
import pins

Start = 0
globalLock = 0
globalLockTime = 0

def sendMicro(message,port):
    #w = message.encode(encoding='ASCII')
    #w = bytes("dicks", "ASCII")
    #Turn off CPLD button lights
    if(message.isupper()):
        GPIO.output(9, 1)
        time.sleep(0.3)
        GPIO.output(9, 0)
    else:
        GPIO.output(24, 1)
        time.sleep(0.3)
        GPIO.output(24, 0)
    #Send Message
    port.write(message)
    print(message)
    time.sleep(0.1)
    #port.close()
    #while(1):
        #port.write(w)
        #print(port.readline())

def updateScore(scoreprog, RedTeamScore, BlueTeamScore, scoreMode, recentScore):
    if (__debug__):
        print "(debug) Updating Score: ", time.strftime('%H:%M:%S')
    if(scoreprog != None):
        os.killpg(os.getpgid(scoreprog.pid), signal.SIGTERM)
        #scoreprog.terminate()
        #scoreprog.kill()
    scoreargs = "exec /usr/bin/python main.py " + str(RedTeamScore) + " " + str(BlueTeamScore) + " " + str(scoreMode) + " " + str(recentScore)
    #print scoreargs
    scoreprog = subprocess.Popen(scoreargs, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    return scoreprog
        
def main():
    GPIO.setwarnings(False)
    if (__debug__):
        print "(debug) Game.py Started: ", time.strftime('%H:%M:%S')
        #GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)
    pins.Pins()
    #UART Port declaration
    GPIO.setup(9, GPIO.OUT, initial=GPIO.LOW)
    #GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)
    #GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)#, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(19, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)

    
    port = serial.Serial("/dev/serial0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1.0)
   
    #sendMicro("g",port)
    #return

    global Start
    global globalLock
    global globalLockTime

    if (__debug__):
        print "(debug) Initializing Variables: ", time.strftime('%H:%M:%S')

    Start = 1

    #Send out an nRST
    GPIO.output(19,1)
    time.sleep(1)
    GPIO.output(19,0)
    
    RedTeamScore = 10
    RedFlag = 0
    RedRack = 2
    RedRackFlag = 0
    
    BlueTeamScore = 10
    BlueFlag = 0
    BlueRack = 2
    BlueRackFlag = 0

    lastPattern = 1
    #Score Mode vs Pattern Mode Startup Select
    if(GPIO.input(11) == 0):
        if (__debug__):
            print "(debug) Starting in Score Mode: ", time.strftime('%H:%M:%S')
        scoreMode = 0
    else:
        if (__debug__):
            print "(debug) Starting in Pattern Mode: ", time.strftime('%H:%M:%S')
        scoreMode = 1

    if (__debug__):
        print "(debug) Spawning main.py process: ", time.strftime('%H:%M:%S')
    scoreprog = updateScore(None, RedTeamScore, BlueTeamScore, scoreMode, None)

    if (__debug__):
        print "(debug) Entering Main Loop: ", time.strftime('%H:%M:%S')
    while(True):
        #Global Lock
        if(globalLock):
            if(time.time() - globalLockTime >= 0.5):
                globalLock = 0
                globalLockTime = 0
                if (__debug__):
                    print "(debug) Global Lock Released", time.strftime('%H:%M:%S')
        else:  #Process Flag
            if(RedFlag):
                if (__debug__):
                    print "(debug) Red Team Update Score: ", time.strftime('%H:%M:%S')
                RedFlag = 0
                scoreprog = updateScore(None, RedTeamScore, BlueTeamScore, scoreMode, 'r')
                time.sleep(1)

            if(BlueFlag):
                if (__debug__):
                    print "(debug) Blue Team Update Score: ", time.strftime('%H:%M:%S')
                BlueFlag = 0
                scoreprog = updateScore(None, RedTeamScore, BlueTeamScore, scoreMode, 'b')
                time.sleep(1)

        #Set Start
        #if(GPIO.input(5) == 1 and Start == 0):
        #if (__debug__):
        #print "(debug) Game Start: ", time.strftime('%H:%M:%S')
        
            
        #Score Mode Switch
        if(GPIO.input(11) == 0 and scoreMode != 0):
            if (__debug__):
                print "(debug) Switching to Score Mode: ", time.strftime('%H:%M:%S')
            lastPattern = scoreMode
            scoreMode = 0
            scoreprog = updateScore(None, RedTeamScore, BlueTeamScore, scoreMode, None)
        elif(GPIO.input(11) == 1 and scoreMode == 0):
            if (__debug__):
                print "(debug) Switching to Pattern Mode: ", time.strftime('%H:%M:%S')
            scoreMode = lastPattern
            scoreprog = updateScore(None, RedTeamScore, BlueTeamScore, scoreMode, None)

        #Switch Pattern
        if(GPIO.input(13) == 1 and scoreMode != 0):
            if (__debug__):
                print "(debug) Next Pattern: ", time.strftime('%H:%M:%S')
            scoreMode += 1
            scoreprog = updateScore(None, RedTeamScore, BlueTeamScore, scoreMode, None)


            
        #Reset Game
        if(GPIO.input(6) == 1):
            if (__debug__):
                print "(debug) Game Reset: ", time.strftime('%H:%M:%S')
            Start = 1
            port = serial.Serial("/dev/ttyS0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1.0)

            RedTeamScore = 10
            RedFlag = 0
            RedRack = 2
            RedRackFlag = 0
            
            BlueTeamScore = 10
            BlueFlag = 0
            BlueRack = 2
            BlueRackFlag = 0

            GPIO.output(19,1)
            time.sleep(0.3)
            GPIO.output(19,0)


        #Start the Game    
        if(Start):
            
            #Red Score Signal
            if(GPIO.input(25) == 1 and RedFlag == 0):
                RedFlag = 1
                RedTeamScore -= 1
                if (__debug__):
                    print "(debug) Red Team Scored: ", time.strftime('%H:%M:%S')
                    print "(debug) Game Score - Blue: ", BlueTeamScore, " Red: ", RedTeamScore, ": ", time.strftime('%H:%M:%S')
                setGlobalLock()
                
            #Blue Score Signal
            if(GPIO.input(10) == 1 and BlueFlag == 0):
                BlueFlag = 1
                BlueTeamScore -= 1
                GPIO.output(23, 1)
                time.sleep(1)
                GPIO.output(23, 0)
                if (__debug__):
                    print "(debug) Blue Team Scored: ", time.strftime('%H:%M:%S')
                    print "(debug) Game Score - Blue: ", BlueTeamScore, " Red: ", RedTeamScore, ": ", time.strftime('%H:%M:%S')
                setGlobalLock()

            #Send Red Re-rack Signal #Talk with Mikey to see which ones are which
            if(RedRack > 0 and RedFlag == 0):
                if(RedRack == 2):
                    RedRack -= 1
                    if(GPIO.input(21) and RedTeamScore == 6 ):
                        if (__debug__):
                            print "(debug) Red Reracking to 3-2-1: ", time.strftime('%H:%M:%S')
                        sendMicro("a",port)
                        RedRackFlag = 1
                    elif(GPIO.input(20) and RedTeamScore == 4):
                        if (__debug__):
                            print "(debug) Red Reracking to Diamond: ", time.strftime('%H:%M:%S')
                        sendMicro("b",port)
                        RedRackFlag = 1
                    elif(GPIO.input(16) and RedTeamScore == 5):
                        if (__debug__):
                            print "(debug) Red Reracking to Box: ", time.strftime('%H:%M:%S')
                        sendMicro("c",port)
                        RedRackFlag = 1
                    elif(GPIO.input(12) and RedTeamScore == 2):
                        if (__debug__):
                            print "(debug) Red Reracking to Gentlemen's: ", time.strftime('%H:%M:%S')
                        sendMicro("d",port)
                        RedRackFlag = 1
                    elif(GPIO.input(7) and RedTeamScore == 3):
                        if (__debug__):
                            print "(debug) Red Reracking to Line: ", time.strftime('%H:%M:%S')
                        sendMicro("e",port)
                        RedRackFlag = 1
                    elif(GPIO.input(8) and RedTeamScore == 3):
                        if (__debug__):
                            print "(debug) Red Reracking to Triangle: ", time.strftime('%H:%M:%S')
                        sendMicro("f",port)
                        RedRackFlag = 1
                    else:
                        RedRack += 1
                        RedRackFlag = 0
                else:
                    if(GPIO.input(8) and RedTeamScore == 2):
                        if (__debug__):
                            print "(debug) Red Reracking to Gentlemen's: ", time.strftime('%H:%M:%S')
                        sendMicro("c", port)
                        RedRack = 0
        
            #Send Blue Re-rack Signal
            if(BlueRack > 0 and BlueFlag == 0):
                if(BlueRack == 2):
                    BlueRack -= 1
                    if(GPIO.input(2) == False and BlueTeamScore == 6):
                        if (__debug__):
                            print "(debug) Blue Reracking to 3-2-1: ", time.strftime('%H:%M:%S')
                        sendMicro("A",port)
                        BlueRackFlag = 1
                    elif(GPIO.input(3)== False and BlueTeamScore == 4):
                        if (__debug__):
                            print "(debug) Blue Reracking to Diamond: ", time.strftime('%H:%M:%S')
                        sendMicro("B",port)
                        BlueRackFlag = 1
                    elif(GPIO.input(4) == False and BlueTeamScore == 5):
                        if (__debug__):
                            print "(debug) Blue Reracking to Box: ", time.strftime('%H:%M:%S')
                        sendMicro("C",port)
                        BlueRackFlag = 1
                    elif(GPIO.input(17) == False and BlueTeamScore == 2):
                        if (__debug__):
                            print "(debug) Blue Reracking to Gentlemen's: ", time.strftime('%H:%M:%S')
                        sendMicro("D",port)
                        BlueRackFlag = 1
                    elif(GPIO.input(27) == False and BlueTeamScore == 3):
                        if (__debug__):
                            print "(debug) Blue Reracking to Line: ", time.strftime('%H:%M:%S')
                        sendMicro("E",port)
                        BlueRackFlag = 1
                    elif(GPIO.input(22)== False and BlueTeamScore == 3):
                        if (__debug__):
                            print "(debug) Blue Reracking to Triangle: ", time.strftime('%H:%M:%S')
                        sendMicro("F",port)
                        BlueRackFlag = 1
                    else:
                        BlueRack += 1
                        BlueRackFlag = 0
                else:
                    if(GPIO.input(17)== False and BlueTeamScore == 2):
                        if (__debug__):
                            print "(debug) Blue Reracking to Gentlemen's: ", time.strftime('%H:%M:%S')
                        sendMicro("C", port)
                        BlueRack = 0
            #Game End State
            if(RedTeamScore == 0 or BlueTeamScore == 0):
                Start = 0
                port.close()

def setGlobalLock():
    global globalLock
    global globalLockTime
    globalLock = 1
    globalLockTime = time.time()
    if (__debug__):
        print "(debug) Setting Global Lock: ", time.strftime('%H:%M:%S')
    return

if __name__ == '__main__':
    main()
