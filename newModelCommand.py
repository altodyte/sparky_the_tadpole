import serial
import string
import os
import pickle
import random
import numpy as np

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=6) #number of seconds to timeout
point_list = []
 
x = ser.readlines() #ends on timeout
print x
f = open("OpticalEncoderCapture16S.txt",'a')
for line in x:
    f.write(line)
f.close()
