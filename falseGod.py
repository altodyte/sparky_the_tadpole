import socket
import sys, time, msvcrt

UDP_IP = "127.0.0.1"
UDP_PORT = 61557
MESSAGE = "$,G,-1,-1,-1,T,-1,-1,-1,P,400,400,123,L,-1,-1,-1,A,228,352,B,708,727,C,-1,-1,D,-1,-1,S,11,11,383\r"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
					 socket.SOCK_DGRAM) # UDP

# 	'''http://stackoverflow.com/questions/3471461/raw-input-and-timeout'''
def readInput( caption, default, timeout = 0.3):
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

while True:
	s = str(readInput("The word of the Idol",'p'))
	if 'p'==s:
		sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	elif "e"==s:
		sock.sendto("END VISION FROM GOD", (UDP_IP, UDP_PORT))
		break
	else:
		sock.sendto(s, (UDP_IP, UDP_PORT))

# # and some examples of usage
# ans = readInput('Please type a name', 'john') 
# print 'The name is %s' % ans
# ans = readInput('Please enter a number', 10 ) 
# print 'The number is %s' % ans 

# import socket, sys
# s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# host = '127.0.0.1' #sys.argv[1]
# s.sendto('A'*10,   (host,61557))
# s.sendto('B', (host,61557))

# import socket

# UDP_IP = "127.0.0.1"
# UDP_PORT = 61557
# MESSAGE = "Hello, World!"

# print "UDP target IP:", UDP_IP
# print "UDP target port:", UDP_PORT
# print "message:", MESSAGE

# sock = socket.socket(socket.AF_INET, # Internet
#              socket.SOCK_DGRAM) # UDP
# sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

# import socket, select

# UDP_PORT = 61557

# sock = socket.socket(socket.AF_INET, # Internet
# 					 socket.SOCK_DGRAM) # UDP
# sock.bind(('', UDP_PORT))

# sock.setblocking(0)
# bufferSize = 1024

# print "Attempting to read UDP"
# while True:
# 	result = select.select([sock],[],[])
# 	# msg = "$,G,-1,-1,-1,T,-1,-1,-1,P,-1,-1,-1,L,-1,-1,-1,A,228,352,B,708,727,C,-1,-1,D,-1,-1,S,11,11,383\r"
# 	msg = result[0][0].recv(bufferSize) 
# 	message = msg.split(',')
# 	i = message.index('G')
# 	n = message.index('S')
# 	# position = [x,y,h]
# 	pos = {'x' : message[i+1], 'y' : message[i+2], 'h' : message[i+3],'t' : (message[n+1],message[n+2],message[n+3].split()[0])}
# 	for k in pos.keys():
# 		print k + ": " + str(pos[k])
# 	# image is 1031x1031