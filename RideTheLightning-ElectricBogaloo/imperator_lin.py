import sys, serial, time, random
import get_last_pos
import pygame
from pygame.locals import *
from random import *
import math
from math import atan2, degrees, pi, sin, cos, radians, sqrt
import numpy as np
import optimize_w_ga

def read_all_serial_input(incoming):
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
    return full_buffer

def substr_in_str_list(substr, str_list):
    for string in str_list:
        if substr in string:
            return True
    return False

class Model:
    """encodes simulator world state"""
    def __init__(self):
        self.text_in = None
        self.last_command = "None"
        self.command_to_send = None
        self.pushed_params = "n,n,n,n,n,n"
        self.to_push = "0,0,0,0,0,0" # replace with draw from optimizer
        self.control_state = "Initializing"
        self.start_run_time = time.time()
        self.start_pos = (0,0)


    def update_model(self):
        # move through control states here?
        dt = self.clock.tick()/1000.0
        state_progression()
        send_command()


    def state_progression(self):
        if self.control_state == "Initializing":
            if substr_in_str_list("EGO RANUNCULUS", self.text_in):
                self.control_state = "send_new"
                return None
        if self.control_state = "send_new":
            new_params = optimize_w_ga.get_new_params()
            self.to_push = ', '.join(map(str, new_params))
            self.command_to_send = "AUDI!" + self.to_push
                
        if self.control_state == "Pushing":





    def send_command(self):
        """sends queued command"""
        if self.command_to_send is not None:
            if self.command_to_send == "AUDI!":
                params = file('params.txt','r').read() # AUDI! a,b,c,d,e,f
                self.command_to_send += params
            ser.write(self.command_to_send)

class PyGameWindowView:
    """encodes view of simulation"""
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
    
    def draw(self):
        self.screen.fill(pygame.Color(255,255,255))
        self.disp_HUD_info()
        pygame.display.update()

    def disp_HUD_info(self):
        """textual interface"""

        myfont = pygame.font.SysFont("monospace", 12, bold = True)
        # key bindings
        binding_text = ["DIC: R", "NICTERE: T", "DORMI: Q", "EXPERGISCERE: E"
                        "SINISTER: A", "DEXTER: D", "DESISTE: S", "ITE: F",
                        "AGGREDERE: W", "AUDI: G"]
        yloc = 20
        for btext in binding_text:
            self.screen.blit(myfont.render(btext), (100, yloc))
            yloc += 20

        text_c = myfont.render("Imperator Control State: "+self.model.control_state)
        text_pushed = myfont.render("pushed_params: "+self.model.pushed_params)
        text_cmd = myfont.render("Last command: "+self.model.last_command)
        text_cmd2 = myfont.render("Next command: "+self.model.command_to_send)
        self.screen.blit(text_c, (100, yloc+20))
        self.screen.blit(text_pushed, (100, yloc+40))
        self.screen.blit(text_cmd, (100, yloc+60))
        self.screen.blit(text_cmd2, (100, yloc+80))

class PyGameController:
    """handles user inputs and communicates with model"""
    def __init__(self,model,view): 
        """initialize the class"""
        self.model = model
        self.view = view
        
    def handle_keystroke_event(self,event): 
        """builds and upgrades towers"""
        if event.type == KEYDOWN:            
            # control of movement
            if event.key == pygame.K_w:
                self.model.command_to_send = "AGGREDERE!"
            if event.key == pygame.K_a:
                self.model.command_to_send = "SINISTER!"
            if event.key == pygame.K_s:
                self.model.command_to_send = "DESISTE!"
            if event.key == pygame.K_d:
                self.model.command_to_send = "DEXTER!"
            if event.key == pygame.K_f:
                self.model.command_to_send = "ITE!"

            # other state modifiers and readers 
            if event.key == pygame.K_r:
                self.model.command_to_send = "DIC!"
            if event.key == pygame.K_t:
                self.model.command_to_send = "NICTERE!"
            if event.key == pygame.K_q:
                self.model.command_to_send = "DORMI!"
            if event.key == pygame.K_e:
                self.model.command_to_send = "EXPERGISCERE!"
            if event.key == pygame.K_g:
                self.model.command_to_send = "AUDI!" # must be written with the params to send


### X-BEE
port = '/dev/ttyUSB0' # This pretty much has to be manually set (see getComPorts.py for help)
ser = serial.Serial(port,38400,bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)
ser.close() # cleanup from old serial communications
ser.timeout = 0.01

# x, y, z = get_last_pos.get_pos(filename)

try: 
    ser.open()
except Exception, e:
    print "error open serial port: " + str(e)
    exit()

# availability check on Tadpole waits for a write
print "INCIPIT"
ser.write("EXPERGISCERE RANUNCULE")


pygame.init()
size = (500,600)
screen = pygame.display.set_mode(size)
model = Model(0,0) #initial windspeed, windheading
view = PyGameWindowView(model,screen)
controller = PyGameController(model,view)
running = True
while running:
    incoming = ser.readline()
    if incoming != '':
        full_buffer = read_all_serial_input(incoming)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            running = False
        controller.handle_keystroke_event(event)
    model.text_in = full_buffer
    model.update_model()
    view.draw()

    if (random.randint(1,1000)==10):
        ser.write("DIC!")
    time.sleep(.001)
pygame.quit()