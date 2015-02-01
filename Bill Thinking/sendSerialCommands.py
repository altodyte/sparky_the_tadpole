import serial, serial.tools.list_ports

# Comment out the below block if you know the name of the serial port
# and don't want to blindly choose the first open one
ports = list(serial.tools.list_ports.comports())
port = ports[0][0]
# port = 'COM5'

ser = serial.Serial(port,38400,bytesize=serial.EIGHTBITS,
	parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)
ser.close()
ser.open()

communicate = True
while communicate:
	# Get current fish state
	# "[STP TL STR TR CTL CSTR CTR] State: #" #: 0-6
	if ser.available():
		state = ser.readline()

	# Send fish command
	# [COMMAND(s) FREQ(f) AMP(i,i) PHASE(f,f)]
	# Commands: Stop (all movement), Go (start autonomy), CTL, CSTR, CTR
	ser.write()

ser.close()