def get_comms():
    line = (sys.stdin.readline())[24:]
    tokens = line.split(",")
    state = int(tokens[0]);
    p0 = int(tokens[1])
    p1 = int(tokens[2])
    p2 = int(tokens[3])

