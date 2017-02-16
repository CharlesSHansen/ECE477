import socket
sd = socket.socket(socket.AF_UNIX)
sd.connect('/home/pi/tmp')
sd.send('10 10')
     
