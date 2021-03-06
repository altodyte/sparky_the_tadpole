import serial, time
import random
import msvcrt, sys
### X-BEE
port = 'COM11' # This pretty much has to be manually set (see getComPorts.py for help)
ser = serial.Serial(port,38400,bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)
ser.close() # cleanup from old serial communications
ser.timeout = 0.01

def get_pos(filename):
    """reads tcpdump file and returns latest position"""
    # command prior to start in separate process to read from ethport:
    # sudo tcpdump -i eth0 udp port 61557 -A >>test3.txt

    x = file(filename,'r').read()
    x = x.splitlines()
    last = -1
    proper_read = False
    while not(proper_read):
        y = x[last] # assumes there will be a successful read
        try:
            if y[0] == '.':
                msg = y.split(',')
                xpos =int(msg[6])
                ypos =int(msg[7])
                zpos =int(msg[8])
                proper_read = True
            else:
                last += -1
        except:
            last += -1

    return xpos, ypos, zpos

def readInput( caption, default, timeout = 0.1):
    start_time = time.time()
    sys.stdout.write('%s: '%(caption)); #('%s(%s):'%(caption, default));
    input = ''
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getche()
            if ord(char) == 13: # enter_key
                break
            elif ord(char) >= 32: #space_char
                input += char
        if len(input) == 0 and (time.time() - start_time) > timeout:
            break
    print ''  # needed to move to next line
    if len(input) > 0:
        return input
    else:
        return default

def read_all_input(incoming):
    full_buffer = [incoming]
    empty = False
    while(not(empty)):
        next_read = ser.readline()
        if next_read == '':
            empty = True
        else:
            full_buffer += [next_read]
    for line in full_buffer:
        print line


try: 
    ser.open()
except Exception, e:
    print "error open serial port: " + str(e)
    exit()

# availability check on Tadpole waits for a write
print "INCIPIT"
ser.write("EXPERGISCERE RANUNCULE")


while(True):
    incoming = ser.readline()
    if incoming != '':
        read_all_input(incoming)
    cmd = readInput("IMPERA> ", '')
    if cmd in ["DIC!", "NICTERE!", "DORMI!", "EXPERGISCERE!", 
    "SINISTER!", "DEXTER!","DESISTE!","ITE!","AGGREDERE!", "X!", "AUDI!"]:
        ser.write(cmd)
    if cmd[0:5] == "AUDI!": # AUDI! a,b,c,d,e,f
        print "Params Sent: "
        print cmd[5:]
        ser.write(cmd)
    if (random.randint(1,1000)==10):
        ser.write("DIC!")
    time.sleep(0.001)
