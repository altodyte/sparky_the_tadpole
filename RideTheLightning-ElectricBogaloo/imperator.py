import serial, time
import random
import msvcrt, sys
### X-BEE
port = 'COM11' # This pretty much has to be manually set (see getComPorts.py for help)
ser = serial.Serial(port,38400,bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)
ser.close() # cleanup from old serial communications
ser.timeout = 0.01

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
stale = 0 # Number of calls since freshness
line = "" # storage for raw line

# availability check on Tadpole waits for a write
print "INCIPIT"
ser.write("EXPERGISCERE RANUNCULE")


while(True):
    incoming = ser.readline()
    if incoming != '':
        read_all_input(incoming)
    cmd = readInput("IMPERA> ", '')
    if cmd in ["DIC!", "NICTERE!", "DORMI!", "EXPERGISCERE!", "SINISTER!", "DEXTER!"]:
        ser.write(cmd)
    if (random.randint(1,1000)==10):
        ser.write("DIC!")
    time.sleep(0.001)
