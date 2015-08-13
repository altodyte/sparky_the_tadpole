import serial, time

### X-BEE
port = 'COM11' # This pretty much has to be manually set (see getComPorts.py for help)
ser = serial.Serial(port,38400,bytesize=serial.EIGHTBITS,
			parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)
ser.close() # cleanup from old serial communications
try: 
	ser.open()
except Exception, e:
	print "error open serial port: " + str(e)
	exit()
stale = 0 # Number of calls since freshness
line = "" # storage for raw line

i = 1000
while i>0:
	i=i-50
	print "$"+str(i)+" "+str(1000-i)
	ser.write("$"+str(i)+" "+str(1000-i))
	time.sleep(3*max(i,1000-i)/1000.0)