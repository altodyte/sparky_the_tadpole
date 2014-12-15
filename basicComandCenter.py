# Imports for communication to Tadpole
import serial, serial.tools.list_ports
# Imports for communication with God-Eye
import socket, select, time
# Other Imports for Simulation/UI
from optimize_w_ga import *
import math, sys, msvcrt

def print_bytes(write_data, num_bytes, space=True):
	ans = ""
	for i in range(num_bytes-len(write_data)):
		ans+=" "

	ans+=write_data
	
	if space:
		ans+=" "
	return ans

def get_float(write_data,dot):
	temp=str(write_data)
	if temp.find(".")==-1:
		temp+=".000"
	else:
		temp+="000"
	index = temp.find(".")
	return temp[:index+dot+1]

def get_int(write_data):
	temp = str(write_data)+"."
	return temp[:temp.find(".")]

def print_comms(state,freq,amp0,amp1,amp2,phase1,phase2,mode=0):
	ans = ""
	ans+=print_bytes(state,4)
	ans+=print_bytes(get_float(freq,2),4,True)
	ans+=print_bytes(get_int(amp0),2,True)
	ans+=print_bytes(get_int(amp1),2,True)
	ans+=print_bytes(get_int(amp2),2,True)
	ans+=print_bytes(get_float(phase1,2),5,True)
	ans+=print_bytes(get_float(phase2,2),5,True)
	ans+=print_bytes(get_int(mode),2,False)
	return ans

def readInput( caption, default, timeout = 0.1):
	start_time = time.time()
	sys.stdout.write('%s: '%(caption)); #('%s(%s):'%(caption, default));
	input = ''
	while True:
		if msvcrt.kbhit():
			chr = msvcrt.getche()
			if ord(chr) == 13: # enter_key
				break
			elif ord(chr) >= 32: #space_char
				input += chr
		if len(input) == 0 and (time.time() - start_time) > timeout:
			break

	print ''  # needed to move to next line
	if len(input) > 0:
		return input
	else:
		return default

##############################################################

### GOD-EYE
UDP_IP = "127.0.0.1"
UDP_PORT = 61557

sock = socket.socket(socket.AF_INET, # Internet
					 socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

sock.setblocking(0)

data = "$,G,-1,-1,-1,T,-1,-1,-1,P,400,400,123,L,-1,-1,-1,A,228,352,B,708,727,C,-1,-1,D,-1,-1,S,11,11,383\r"
posStale = 0 # maybe reincorporate staleness later

### X-BEE
port = 'COM9' # This pretty much has to be manually set (see getComPorts.py for help)
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

### SYSTEM VARIABLES
xpos = 400
ypos = 400
heading = 0
servo0 = 0
servo1 = 0
servo2 = 0

### CONTROL VARIABLES
tadpole_mode = 0
coords_start = (xpos, ypos)
time_start = time.time()
heading_start = heading

control_states = ["MANUAL", "AUTO", "OPT"]
control_state = "MANUAL" #either manual or auto or run_opt
tadpole_states = ["STOP", "AUTO LEFT", "AUTO STRAIGHT", "AUTO RIGHT", "CONTROL LEFT", "CONTROL STRAIGHT", "CONTROL RIGHT"]
tadpole_prev_state = "STOP"
tadpole_new_state = None #needs to be read in
commandString = "STOP 0 0 0 0 0 0" #determined by transmission protocol

man_command = "s"
command_params = [0, 0, 0, 0, 0, 0]

running = True
while running:
	# getPosition() # Updates xpos, ypos, heading when available (Via God-Eye UDP)
	timeout = 0.1
	ready = select.select([sock], [], [], timeout)
	if ready[0]:
		data = sock.recv(4096)
		posStale = 0
		message = data.split(',')
		i = message.index('P') # UPDATE THIS TO THE CORRECT LETTER FOR THE FIDUCIAL
		n = message.index('S')
		# position = [x,y,h]
		pos = {'x' : message[i+1], 'y' : message[i+2], 'h' : message[i+3],'t' : (message[n+1],message[n+2],message[n+3].split()[0])}
		xpos = int(pos['x'])
		ypos = int(pos['y'])
		heading = int(pos['h'])
	# readStatus() # Updates tadpole_..._state, servo[0-2] when available (Via Tadpole XBee)
	if ser.inWaiting():
		stale = 0
		line = ser.readline()

		tokens = line.split(",")
		state = tadpole_states[int(tokens[0])];
		servo0 = int(tokens[1])
		servo1 = int(tokens[2])
		servo2 = int(tokens[3])

		tadpole_prev_state = tadpole_new_state
		tadpole_new_state = state
	else:
		stale += 1
	# updateCommand(readInput("Tadpole Command",'same'))
	command = readInput("Tadpole Command",'same',0.3)
	if command in control_states:
		control_state = command
	elif command=="same":
		pass
	elif command in ["r","str","l","right","straight","left","s","stop","STOP"]:
		control_state = "MANUAL"
		man_command = command
	else:
		print "Your command was invalid. No changes have been made. (Mode: "+str(control_state)+")"
	if control_state == "OPT":
		if ((tadpole_prev_state != "AUTO STRAIGHT") and (tadpole_new_state == "AUTO STRAIGHT")):
			command_params = optimize_w_ga.get_new_params()
			commandString = print_comms("GO", command_params[0], command_params[1], command_params[2], command_params[3], command_params[4], command_params[5],tadpole_mode)
			#send command here as well
			coords_start = (xpos, ypos) # bookkeeping for optimization
			time_start = time.time()
		if ((tadpole_prev_state == "AUTO STRAIGHT") and (tadpole_new_state != "AUTO STRAIGHT")):
			dist = math.sqrt((xpos - coords_start[0])**2+(ypos - coords_start[1])**2)
			tdiff = time.time()-time_start
			speed = dist/tdiff
			heading_change = math.abs(heading_start-heading)
			optimize_w_ga.write_back(command_params, speed, heading_change, dist, tdiff)
	elif control_state == "AUTO":
		commandString = print_comms("GO", command_params[0], command_params[1], command_params[2], command_params[3], command_params[4], command_params[5],tadpole_mode)
	elif control_state == "MANUAL":
		# remap command inputs
		if command in ["s","stop","STOP","MANUAL"]: 
			command="STOP"
			commandString = print_comms(command, command_params[0], command_params[1], command_params[2], command_params[3], command_params[4], command_params[5],tadpole_mode)
		elif command in ["r","right"]:
			command="CONTROL RIGHT"
			commandString = print_comms(command, command_params[0], command_params[1], command_params[2], command_params[3], command_params[4], command_params[5],tadpole_mode)
		elif command in ["str","straight"]: 
			command="CONTROL STRAIGHT"
			commandString = print_comms(command, command_params[0], command_params[1], command_params[2], command_params[3], command_params[4], command_params[5],tadpole_mode)
		elif command in ["l","left"]:
			command="CONTROL LEFT"
			commandString = print_comms(command, command_params[0], command_params[1], command_params[2], command_params[3], command_params[4], command_params[5],tadpole_mode)
	if command != "same":
		print commandString
	ser.write(commandString) # Pass the command string to the tadpole


		# runs optimization mumbo jumbo if in mode OPT
		# generally parses command input
sock.close()