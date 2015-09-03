import sys, serial, time, random
import get_last_pos
import pygame
from pygame.locals import *
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
        self.text_in = []
        self.last_command = "None"
        self.command_to_send = "None"
        self.pushed_params_list = [0,0,0,0,0,0]
        self.pushed_params = "n,n,n,n,n,n"
        self.to_push = "0,0,0,0,0,0" # replace with draw from optimizer
        self.control_state = "Initializing"
        self.start_run_time = time.time()
        self.start_pos = (0,0,0)

    def update_model(self):
        # move through control states here
        self.state_progression()
        self.send_command()

    def state_progression(self):
        if self.control_state == "Initializing":
            if substr_in_str_list("EGO RANUNCULUS", self.text_in):
                print "hit"
                time.sleep(1)
                new_params = optimize_w_ga.get_new_params()
                self.to_push = ','.join(map(str, new_params))
                self.command_to_send = "AUDI!" + self.to_push
                self.pushed_params = self.to_push
                self.pushed_params_list = new_params
                
                self.control_state = "Pushing"
                return None                
        if self.control_state == "Pushing":
            if substr_in_str_list("AUDIVI", self.text_in):
                self.command_to_send = "ITE!"
                self.control_state = "Starting_run"
                return None
        if self.control_state == "Starting_run":
            if substr_in_str_list("EO", self.text_in):
                x, y, z = get_last_pos.get_pos('test3.txt')
                self.start_pos = (x,y,z)
                self.start_run_time = time.time()
                self.control_state = "Running"
                return None
        if self.control_state == "Running":
            if substr_in_str_list("From STRAIGHT", self.text_in):
                print "logging run"
                x_e, y_e, z_e = get_last_pos.get_pos('test3.txt')
                end_time = time.time()
                parameter_list = self.pushed_params_list
                time_diff = end_time - self.start_run_time
                euclid_dist = sqrt((x_e-self.start_pos[0])**2+(y_e-self.start_pos[1])**2)
                speed = euclid_dist/time_diff
                d_h1 = z_e - self.start_pos[2]
                d_h2 = self.start_pos[2] - z_e
                if abs(d_h1)<abs(d_h2):
                    heading_change = d_h1
                else:
                    heading_change = d_h2
                print speed
                optimize_w_ga.write_back(parameter_list, speed, heading_change, euclid_dist, time_diff)
                
                new_params = optimize_w_ga.get_new_params()
                self.to_push = ','.join(map(str, new_params))
                self.command_to_send = "AUDI!" + self.to_push
                self.pushed_params = self.to_push
                self.pushed_params_list = new_params

                self.control_state = "Starting_run"
                return None
            if (time.time()-self.start_run_time)>30:
                print "logging run"
                x_e, y_e, z_e = get_last_pos.get_pos('test3.txt')
                end_time = time.time()
                parameter_list = self.pushed_params_list
                time_diff = end_time - self.start_run_time
                euclid_dist = sqrt((x_e-self.start_pos[0])**2+(y_e-self.start_pos[1])**2)
                speed = euclid_dist/time_diff
                d_h1 = z_e - self.start_pos[2]
                d_h2 = self.start_pos[2] -z_e
                if abs(d_h1)<abs(d_h2):
                    heading_change = d_h1
                else:
                    heading_change = d_h2
                print speed
                optimize_w_ga.write_back(parameter_list, speed, heading_change, euclid_dist, time_diff)
                new_params = optimize_w_ga.get_new_params()
                self.to_push = ','.join(map(str, new_params))
                self.command_to_send = "AUDI!" + self.to_push
                self.pushed_params = self.to_push
                self.pushed_params_list = new_params

                self.command_to_send = "DESISTE!"
                self.control_state = "Starting_run"
                return None
        
    def log_run(self):
        print "logging run"
        x_e, y_e, z_e = get_last_pos.get_pos('test3.txt')
        end_time = time.time()
        parameter_list = self.pushed_params_list
        time_diff = end_time - self.start_run_time
        euclid_dist = sqrt((x_e-self.start_pos[0])**2+(y_e-self.start_pos[1])**2)
        speed = euclid_dist/time_diff
        d_h1 = z_e - self.start_pos[2]
        d_h2 = self.start_pos[2]
        if abs(d_h1)<abs(d_h2):
            heading_change = d_h1
        else:
            heading_change = d_h2
        optimize_w_ga.write_back(parameter_list, speed, heading_change, euclid_dist, time_diff)
        
    def send_command(self):
        """sends queued command"""
        if self.command_to_send is not "None":
            if self.command_to_send == "AUDI!":
                params = file('params.txt','r').read() # AUDI! a,b,c,d,e,f
                self.command_to_send += params
            ser.write(self.command_to_send)
            self.last_command = self.command_to_send
            self.command_to_send = "None"


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
        binding_text = ["DIC: R", "NICTERE: T", "DORMI: Q", "EXPERGISCERE: E",
                        "SINISTER: A", "DEXTER: D", "DESISTE: S", "ITE: F",
                        "AGGREDERE: W", "AUDI: G"]
        yloc = 20
        for btext in binding_text:
            self.screen.blit(myfont.render(btext, 1, (0,0,0)), (100, yloc))
            yloc += 20

        text_c = myfont.render("Imperator Control State: "+self.model.control_state,1, (0,0,0))
        text_pushed = myfont.render("pushed_params: "+self.model.pushed_params, 1, (0,0,0))
        text_cmd = myfont.render("Last command: "+self.model.last_command, 1, (0,0,0))
        text_cmd2 = myfont.render("Next command: "+self.model.command_to_send, 1, (0,0,0))
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
            if event.key == pygame.K_x:
                self.model.command_to_send = "None"


### X-BEE
port = '/dev/ttyUSB0' # This pretty much has to be manually set (see getComPorts.py for help)
ser = serial.Serial(port,38400,bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)
ser.close() # cleanup from old serial communications
ser.timeout = 0.01



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
model = Model() #initial windspeed, windheading
view = PyGameWindowView(model,screen)
controller = PyGameController(model,view)
running = True
while running:
    incoming = ser.readline()
    if incoming != '':
        full_buffer = read_all_serial_input(incoming)
        model.text_in = full_buffer
    else:
        model.text_in = []

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            running = False
        controller.handle_keystroke_event(event)
    model.update_model()
    view.draw()

    if (random.randint(1,1000)==10):
        ser.write("DIC!")
    time.sleep(.001)
pygame.quit()