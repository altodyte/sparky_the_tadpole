#!/usr/bin/env python2.7

# NOTE - Not my own code - Abrie Willemse
# NOTE - I am not a programmer - Abrie Willemse

# I am using XBee XB24-Z7 WIT-004 for all devices
# Coordinator is running API
# SENSOR_1 and SENSOR_2 are Sensor Routers running AT (firmware XB24ZB 22A7) (I have tried API firmware XB24ZB 23A7) too)

import serial
from xbee import ZigBee
import time, sys, datetime

serial_port = serial.Serial('/dev/ttyAMA0', 9600)

zb = ZigBee(serial_port)


while True:
    try:
        data = zb.wait_read_frame() #Get data for later use
        print data # To check what comes in before processing / parsing (already buggered up)
        addr = repr(data ['source_addr_long']) # Working sort of, but with @y... issue in results
        file = open('/media/log/senslog.txt','a')
        value = float(((data['samples'])[0])['adc-0'])
        num = (value * 3.0) / 1023.0
        file.write(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') + ' ' + str(addr) + ' ' + str(value) + ' ' + str(num) + '\n')
        print str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') + ' ' + str(addr) + ' ' + str(value) + ' ' + str(num) + '\n')
        file.close()

    except KeyboardInterrupt:
        break

serial_port.close()

#!/usr/bin/python

import serial, time

ser = serial.Serial()

#ser.port = "/dev/ttyUSB0"
ser.port = "/dev/ttyUSB7"
#ser.port = "/dev/ttyS2"

ser.baudrate = 38400
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits

#ser.timeout = None          #block read
ser.timeout = 1            #non-block read
#ser.timeout = 2              #timeout block read

ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control

ser.writeTimeout = 2     #timeout for write

try: 
    ser.open()
except Exception, e:
    print "error open serial port: " + str(e)
    exit()

if ser.isOpen():
    try:
        ser.flushInput() #flush input buffer, discarding all its contents
        ser.flushOutput()#flush output buffer, aborting current output #and discard all that is in buffer

        #write data
        ser.write("AT+CSQ")
        print("write data: AT+CSQ")
        time.sleep(0.5)  #give the serial port sometime to receive the data
        numOfLines = 0
        while True:
            response = ser.readline()
            print("read data: " + response)
            numOfLines = numOfLines + 1
            if (numOfLines >= 5):
                break
        ser.close()
    except Exception, e1:
        print "error communicating...: " + str(e1)
else:
    print "cannot open serial port "