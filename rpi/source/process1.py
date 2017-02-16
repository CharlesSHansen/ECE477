#!/usr/bin/python
import socket

sd = socket.socket(socket.AF_UNIX)
sd.bind('/home/pi/tmp')
sd.listen(5)
(client,addr) = sd.accept()
print(client.recv(1024))


