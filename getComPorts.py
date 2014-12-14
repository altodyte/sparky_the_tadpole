import serial.tools.list_ports

'''Use this script to get a list of all of the open ports,
then manually choose the correct port from the first tuple 
dimensionfor the serial command script (EX: 'COM9')'''

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print p