# Imports for communication to Tadpole
import serial, serial.tools.list_ports
# Imports for communication with God-Eye
import socket, select
# Imports for Simulation/UI
import pygame
from pygame.locals import *
import time

##############################TADPOLE_COMMUNICATON_UNIT######################################

# Use the below code to see available serial ports, set port to correct one (EX: 'COM9')
	# ports = list(serial.tools.list_ports.comports())
	# for p in ports:
	# 	print p

class Ribbit:
	def __init__(self,port):
		self.port = port
		self.ser = serial.Serial(self.port,38400,bytesize=serial.EIGHTBITS,
			parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)
		ser.close() # cleanup from old serial communications
		try: 
		    ser.open()
		except Exception, e:
		    print "error open serial port: " + str(e)
		    exit()
		self.stale = 0 # Number of calls since freshness
		self.line = "" # storage for raw line

	def readStatus(self):
		if self.ser.available():
			self.stale = 0
			self.line = self.ser.readline()
		else:
			self.stale += 1

	def sendCommand(self):
		"""need to write something to package commands into commandString"""
		commandString = "I'm a command string!"
		ser.write(commandString)

##############################GOD-EYE_COMMUNICATON_UNIT######################################

class GodEye():
	def __init__(self):
		UDP_IP = "127.0.0.1"
		self.UDP_PORT = 61557

		self.sock = socket.socket(socket.AF_INET, # Internet
								  socket.SOCK_DGRAM) # UDP
		self.sock.bind((self.UDP_IP, self.UDP_PORT))

		self.sock.setblocking(0)
		self.bufferSize = 1024

		self.data = "$,G,-1,-1,-1,T,-1,-1,-1,P,400,400,123,L,-1,-1,-1,A,228,352,B,708,727,C,-1,-1,D,-1,-1,S,11,11,383\r"
		self.stale = 0

	def prayToTheGodEye(self,timeout=0.1): #timeout in seconds
		ready = select.select([sock], [], [], timeout)
		self.data = "(OLD +"str(self.stale)+") "+self.data
		if ready[0]:
			self.data = self.sock.recv(4096)
			self.stale = 0
		if ready[3]:
			self.stale += 1
		print "received vision:", data
		if "END" in data:
			self.sock.close()
			print "END OF VISION"
			# yes I know this will break things for now

	def prayToGodEyeOLD(self):
		""" """
		result = select.select([self.sock],[],[])
		# msg = "$,G,-1,-1,-1,T,-1,-1,-1,P,-1,-1,-1,L,-1,-1,-1,A,228,352,B,708,727,C,-1,-1,D,-1,-1,S,11,11,383\r"
		msg = result[0][0].recv(self.bufferSize) 
		message = msg.split(',')
		i = message.index('G')
		n = message.index('S')
		# position = [x,y,h]
		pos = {'x' : message[i+1], 'y' : message[i+2], 'h' : message[i+3],'t' : (message[n+1],message[n+2],message[n+3].split()[0])}
		return pos
		# for k in pos.keys():
		# 	print k + ": " + str(pos[k])
		# image is 1031x1031


####################################SIMULATOR_UNIT###########################################

class WorldModel:
    """encodes simulator world state"""
    def __init__(self): #,windspeed,windheading):
        self.tadpole1 = Tadpole() #later include boat list for support of multiple boats
        self.clock = pygame.time.Clock()
        self.godEye = GodEye()
            
    def update_model(self):
        dt = self.clock.tick()/1000.0
        self.tadpole1.updatePos(self.godEye)
        self.tadpole1.updateVels()
        self.tadpole1.drive()

        # self.wind.update(dt) # maybe use as a model for getting boat position from god-eye?

class Tadpole:
	"""encodes information about Sparky"""
	def __init__(self):
		self.length = 40 # HEAD length will need to adjust
		self.segmentLength = 30 # will need to adjust
		self.color = (100,100,100) # color #should be a three-tuple

		self.xpos = 400 # updated by God-Eye
		self.ypos = 400 # updated by God-Eye

		self.heading = 0 # (HEAD Heading) Updated by God-Eye
		self.servo1 = 0 # needs to be mapped so that 0 is neutral position of servo
		self.servo2 = 0 # needs to be mapped so that 0 is neutral position of servo
		self.servo3 = 0 # needs to be mapped so that 0 is neutral position of servo

		self.vx = 0 # calculated by WorldSim
		self.vy = 0 # calculated by WorldSim

		def drive(self,model):
			"""Command the servos"""

		def updatePos(self,godEye):
			"""Get the position from the God-Eye"""
			pos = godEye.prayToTheGodEye()
			self.xpos = pos['x']
			self.ypos = pos['y']

		def updateVels(self):
			"""Calculate the velocity"""
			# This is obviously not yet a calculation
			self.vx = 0
			self.vy = 0



#### EXTRACTED NONSENSE
# import pygame
# from pygame.locals import *
# from random import *
# import math
# from math import atan2, degrees, pi, sin, cos, radians
# import time
# import numpy as np

# class WorldModel:
#     """encodes simulator world state"""
#     def __init__(self): #,windspeed,windheading):
#         self.boat1 = Boat(40,400,400,(100,100,100)) #later include boat list for support of multiple boats
#         self.clock = pygame.time.Clock()
            
#     def update_model(self):
#         dt = self.clock.tick()/1000.0
#         self.boat1.update(dt,model)
#         # self.wind.update(dt) # maybe use as a model for getting boat position from god-eye?
    
# class Boat:
#     """encodes information about the boat"""
#     def __init__(self,length,xpos,ypos,color):
#         self.length = length
#         self.xpos = xpos
#         self.ypos = ypos
#         self.MainPos = 0
#         self.JibPos = 0
#         self.MainSuggestion = 0
#         self.JibSuggestion = 0
#         self.RudderPos = 0
#         self.RudderSuggestion = 0
#         self.vx = 0
#         self.vy = 0
#         self.heading = 0 #note: not redundant with vx, vy; in simple model could be
#         self.angularVelocity = 0
#         self.forward_speed = 0
#         self.color = color #should be a three-tuple
#         # self.wind_over_port = True 
#         self.log_coefficient = 0.1
#         self.lambda_1 = 0.1 #can't be named lambda, reserved
#         self.lambda_2 = 0.4 #decay rate for angular velocity, to zero, way of encoding drag
#         self.strength_Main = 0.65
#         self.strength_Jib = 1-self.strength_Main
#         self.debug_list = (0,0)
#         self.main_angle = 0
#         self.jib_angle = 0
        
#         self.k = 2 #velocity scaling for the wind
#         self.kw = 0.3 #angular velocity scaling for the torque from the rudder
#         self.q = 1 #ang vel scaling for torque from the scales
        
#         self.disp_k =1 #scaling for the output
        
#     def update(self,dt,model):
#         self.heading = self.heading % (2.0*pi) #sanitization
#         self.trim(model)
#         self.kinematics(dt,model)
#         if self.xpos > 820:
#             self.xpos = 0
#         if self.xpos < 0:
#             self.xpos = 820
#         if self.ypos > 800:
#             self.ypos = 0
#         if self.ypos < 0:
#             self.ypos = 800
    
#     def trim(self,model):
#         """readjust sails and rudder to suggestions if possible"""
    
#     def kinematics(self,dt,model):
#         """updates kinematics"""
    
# class PyGameWindowView:
#     """encodes view of simulation"""
#     def __init__(self,model,screen):
#         self.model = model
#         self.screen = screen
    
#     def draw(self):
#         self.screen.fill(pygame.Color(255,255,255))
#         #later include for loop of boats
#         self.draw_boat(self.model.boat1)
#         # self.draw_wind_vane(self.model.wind)
#         self.disp_HUD_info()

#         pygame.display.update()
    
#     def draw_boat(self,boat):
# #        try:
#         bow = (boat.xpos+boat.length/2.0*cos(boat.heading),boat.ypos+boat.length/2.0*sin(boat.heading))
#         starboard_stern = (boat.xpos+boat.length/2.0*cos(boat.heading+pi*5.0/6),boat.ypos+boat.length/2.0*sin(boat.heading+pi*5.0/6))
#         port_stern = (boat.xpos+boat.length/2.0*cos(boat.heading+pi*7.0/6),boat.ypos+boat.length/2.0*sin(boat.heading+pi*7.0/6))
#         pygame.draw.line(self.screen, boat.color, bow, starboard_stern, 3)
#         pygame.draw.line(self.screen, boat.color, bow, port_stern, 2)
#         pygame.draw.line(self.screen, boat.color, starboard_stern, port_stern, 1)
# #        except:
# #            print boat.heading
# #            print boat.angularVelocity
#         # if boat.wind_over_port:  #non-intuitive reversal needs to be explained
#         #     switch = -1
#         # else:
#         #     switch = 1
#         switch = 1
#         main_end = (boat.xpos-boat.length/2.0*cos(boat.heading+boat.MainPos*pi/2.0*switch), boat.ypos-boat.length/2.0*sin(boat.heading+boat.MainPos*pi/2.0*switch))
#         pygame.draw.line(self.screen, (0,255,0), (boat.xpos,boat.ypos), main_end, 2)
#         jib_end = (bow[0]-boat.length/3.0*cos(boat.heading+boat.JibPos*pi/2.0*switch),bow[1]-boat.length/3.0*sin(boat.heading+boat.JibPos*pi/2.0*switch))
#         pygame.draw.line(self.screen, (0,255,0), bow, jib_end, 2)
#         rudder_origin = (np.mean((starboard_stern[0],port_stern[0])),np.mean((starboard_stern[1],port_stern[1])))
#         rudder_end = (rudder_origin[0]-boat.length/3.0*cos(boat.heading+boat.RudderPos*pi/4.0),rudder_origin[1]-boat.length/3.0*sin(boat.heading+boat.RudderPos*pi/4.0))
#         pygame.draw.line(self.screen, (0,0,0), rudder_origin, rudder_end, 3)
#         boat.main_angle = atan2(main_end[1]-boat.ypos,main_end[0]-boat.xpos)
#         boat.jib_angle = atan2(jib_end[1]-bow[1],jib_end[0]-bow[0])

#     # def draw_wind_vane(self,wind):
#     #     origin = (30,30)
#     #     dest = (30+(4+wind.windspeed)*cos(wind.windheading),30+(4+wind.windspeed)*sin(wind.windheading))
#     #     pygame.draw.line(self.screen, (255,0,0), origin, dest, 2)
#     #     pygame.draw.circle(self.screen, (100,100,100),origin, 3)
        
#     def disp_HUD_info(self):
#         """displays the relwind next to the wind vane"""
#         myfont = pygame.font.SysFont("monospace", 12, bold = True)
#         # text = myfont.render("Relative Wind: "+str(self.model.relwind), 1, (0,0,0))
#         text_2 = myfont.render("Boat angularVelocity: "+str(self.model.boat1.angularVelocity), 1, (0,0,0))
#         text_3 = myfont.render("Boat debug: "+str(self.model.boat1.debug_list), 1, (0,0,0))
#         # self.screen.blit(text, (100,20))
#         self.screen.blit(text_2, (100, 40))
#         self.screen.blit(text_3, (100, 60))
        
# class PyGameController:
#     """handles user inputs and communicates with model"""
#     def __init__(self,model,view): 
#         """initialize the class"""
#         self.model = model
#         self.view = view
        
#     def handle_keystroke_event(self,event): 
#         """builds and upgrades towers"""
#         if event.type == KEYDOWN:
#             #remember that the directions are reversed in view
#             #direct control, deprecated
#             if event.key == pygame.K_LEFT:
#                 self.model.boat1.vx += -10      
#             if event.key == pygame.K_RIGHT:
#                 self.model.boat1.vx += 10                          
#             if event.key == pygame.K_UP:
#                 self.model.boat1.vy += -10              
#             if event.key == pygame.K_DOWN:
#                 self.model.boat1.vy += 10  
                
#             #ijkl to modify forward and angular velocity
#             if event.key == pygame.K_i:
#                 self.model.boat1.forward_speed += 10
#             if event.key == pygame.K_k:
#                 self.model.boat1.forward_speed += -10  
#             if event.key == pygame.K_l:
#                 self.model.boat1.angularVelocity += 1  
#             if event.key == pygame.K_j:
#                 self.model.boat1.angularVelocity += -1
                
#             if event.key == pygame.K_b:
#                 self.model.boat1.xpos = 200
#                 self.model.boat1.ypos = 200
#                 self.model.boat1.vx = 0
#                 self.model.boat1.vy = 0
#                 self.model.boat1.heading = 0
#                 self.model.boat1.angularVelocity = 0
#                 self.model.boat1.forward_speed = 0
                
#             # #tg, rf modify wind
#             # if event.key == pygame.K_t:
#             #     self.model.wind.windspeed += 1
#             # if event.key == pygame.K_g:
#             #     self.model.wind.windspeed += -1
#             # if event.key == pygame.K_r:
#             #     self.model.wind.windheading += pi/16.0                
#             # if event.key == pygame.K_f:
#             #     self.model.wind.windheading += -pi/16.0
                
#             #ws, ed, modify main and jib
#             if event.key == pygame.K_w:
#                 self.model.boat1.MainSuggestion += 0.1
#             if event.key == pygame.K_s:
#                 self.model.boat1.MainSuggestion += -0.1
#             if event.key == pygame.K_e:
#                 self.model.boat1.JibSuggestion += 0.1
#             if event.key == pygame.K_d:
#                 self.model.boat1.JibSuggestion += -0.1
                
#             #qa control rudder, zxc throw it
#             if event.key == pygame.K_q:
#                 self.model.boat1.RudderSuggestion += 0.1
#             if event.key == pygame.K_a:
#                 self.model.boat1.RudderSuggestion += -0.1
#             if event.key == pygame.K_z:
#                 self.model.boat1.RudderSuggestion = -1
#             if event.key == pygame.K_x:
#                 self.model.boat1.RudderSuggestion = 0
#             if event.key == pygame.K_c:
#                 self.model.boat1.RudderSuggestion = 1
                
# if __name__ == '__main__':
#     pygame.init()
#     size = (820,800)
#     screen = pygame.display.set_mode(size)
#     model = WorldModel() #initial windspeed, windheading
#     view = PyGameWindowView(model,screen)
#     controller = PyGameController(model,view)
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.mouse.set_cursor(*pygame.cursors.arrow)
#                 running = False
#             controller.handle_keystroke_event(event)
#         model.update_model()
#         view.draw()
#         time.sleep(.01)
#     pygame.quit()