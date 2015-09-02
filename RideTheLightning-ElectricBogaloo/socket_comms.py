# Imports for communication with God-Eye
import socket, select

UDP_IP = "127.0.0.1"
UDP_PORT = 61557

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(0)
running = True
stale = 0
while running:
    timeout = 0.1
    ready = select.select([sock], [], [], timeout)
    if ready[0]:
        data = sock.recv(4096)
        print data
    else:
        stale += 1
sock.close()