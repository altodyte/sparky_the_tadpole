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
