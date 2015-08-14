# To Tadpole: Mode S0command S1command S2command freq amp0 amp1 amp2 phase1 phase2
# To Tadpole: 5 90 90 90 1 10 10 10 1.57 1.57
# From Tadpole: Mode S0command S0actual S1c S1a S2c S2a freq amp0 amp1 amp2 phase1 phase2
# From Tadpole: 0 90 90 90 90 90 90 2.00 40.00 60.00 60.00 1.57 1.57

# Imports for communication to Tadpole
import serial, serial.tools.list_ports
# Imports for communication with God-Eye
import socket, select, time
# Other Imports for Simulation/UI

UDP_IP = "127.0.0.1"
UDP_PORT = 61557

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

sock.setblocking(0)

data = "$,G,-1,-1,-1,T,-1,-1,-1,P,400,400,123,L,-1,-1,-1,A,228,352,B,708,727,C,-1,-1,D,-1,-1,S,11,11,383\r"

xpos = 400
ypos = 400
heading = 0

coords_start = (xpos, ypos)
time_start = time.time()

running = True
while running:
    # getPosition() # Updates xpos, ypos, heading when available (Via God-Eye UDP)
    timeout = 0.1
    ready = select.select([sock], [], [], timeout)
    if ready[0]:
        data = sock.recv(4096)
        print data
        """
        posStale = 0
        message = data.split(',')
        i = message.index('P') # UPDATE THIS TO THE CORRECT LETTER FOR THE FIDUCIAL
        n = message.index('S')
        # position = [x,y,h]
        pos = {'x' : message[i+1], 'y' : message[i+2], 'h' : message[i+3],'t' : (message[n+1],message[n+2],message[n+3].split()[0])}
        xpos = int(pos['x'])
        ypos = int(pos['y'])
        heading = int(pos['h'])
        """
    else:
        stale += 1
sock.close()