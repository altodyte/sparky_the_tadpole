import socket, select

UDP_IP = "127.0.0.1"
UDP_PORT = 61557

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
timeout = 0.1
while True:
    ready = select.select([sock], [], [], timeout)
    if ready[0]:
        data = sock.recv(4096)
        print data
    
    #data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #print "received message:", data