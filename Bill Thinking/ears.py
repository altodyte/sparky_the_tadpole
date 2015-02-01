import socket, select
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 61557

sock = socket.socket(socket.AF_INET, # Internet
					 socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

sock.setblocking(0)

data = "$,G,-1,-1,-1,T,-1,-1,-1,P,400,400,123,L,-1,-1,-1,A,228,352,B,708,727,C,-1,-1,D,-1,-1,S,11,11,383\r"
stale = 0

while True:
	# data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	ready = select.select([sock], [], [], 0.1)
	data = "(OLD "+str(stale)+") "+data
	if ready[0]:
		data = sock.recv(4096)
		stale = 0
	else:
		stale += 1
	print "received vision:", data
	if "END" in data:
		break
sock.close()

# import socket
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.bind(('',61557))
# test = True
# while test:
#     data,address = s.recvfrom(10000)
#     print data
#     if data.equals('B'):
#     	test = False