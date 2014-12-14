# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 14:26:13 2014

@author: atproofer
"""



import socket, select
UDP_PORT = 61557
sock = socket.socket(socket.AF_INET, # Internet
socket.SOCK_DGRAM) # UDP
sock.bind(('', UDP_PORT))
sock.setblocking(0)
bufferSize = 1024
print "Attempting to read UDP"
while True:
                result = select.select([sock],[],[])
                # msg = "$,G,-1,-1,-1,T,-1,-1,-1,P,-1,-1,-1,L,-1,-1,-1,A,228,352,B,708,727,C,-1,-1,D,-1,-1,S,11,11,383\r"
                msg = result[0][0].recv(bufferSize)
                message = msg.split(',')
                i = message.index('G')
                n = message.index('S')
                # position = [x,y,h]
                pos = {'x' : message[i+1], 'y' : message[i+2], 'h' : message[i+3],'t' : (message[n+1],message[n+2],message[n+3].split()[0])}
                for k in pos.keys():
                                print k + ": " + str(pos[k])
                # image is 1031x1031