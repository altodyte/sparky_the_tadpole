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

def print_comms(state,freq,amp0,amp1,amp2,phase1,phase2,mode):
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
