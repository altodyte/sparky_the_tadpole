# Imports for communication to Tadpole
import serial, serial.tools.list_ports
# Imports for communication with God-Eye
import socket, select
# Imports for Simulation/UI
import pygame
from pygame.locals import *
from random import *
import math
from math import atan2, degrees, pi, sin, cos, radians
import time
import numpy as np
from optimize_w_ga import *

class WorldModel:
	"""encodes simulator world state"""
	def __init__(self): #,windspeed,windheading):
		self.tadpole1 = Tadpole() #later include tadpole list for support of multiple tadpoles
		self.clock = pygame.time.Clock()
		self.godEye = GodEye()
			
	def update_model(self):
		dt = self.clock.tick()/1000.0
		self.tadpole1.updatePos(self.godEye)
		self.tadpole1.updateVels()
		self.tadpole1.drive(self)

class GodEye():
	def __init__(self):
		self.UDP_IP = "127.0.0.1"
		self.UDP_PORT = 61557

		self.sock = socket.socket(socket.AF_INET, # Internet
								  socket.SOCK_DGRAM) # UDP
		self.sock.bind((self.UDP_IP, self.UDP_PORT))

		self.sock.setblocking(0)
		self.bufferSize = 1024

		self.data = "$,G,-1,-1,-1,T,-1,-1,-1,P,400,400,123,L,-1,-1,-1,A,228,352,B,708,727,C,-1,-1,D,-1,-1,S,11,11,383\r"
		self.stale = 0

	def prayToTheGodEye(self,timeout=0.1): #timeout in seconds
		ready = select.select([self.sock], [], [], timeout)
		if len(self.data.split(' '))>1:
			self.data = "(OLD "+str(self.stale)+") "+self.data.split(' ')[2]
		else:
			self.data = "(OLD "+str(self.stale)+") "+self.data
		if ready[0]:
			self.data = self.sock.recv(4096)
			self.stale = 0
		else:
		 	self.stale += 1
		if "END" in self.data:
			print "END OF VISION"
			# self.sock.close()
			# yes I know this will break things for now
		return self.data

class Ribbit:
	def __init__(self,tadpole,port=61557):
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

		self.tadpole = tadpole

		self.control_state = "Manual" #either manual or auto or run_opt
		self.tadpole_prev_state = "STOP"
		self.tadpole_new_state = None #needs to be read in
		self.commandString = "STOP 0 0 0 0 0 0" #determined by transmission protocol
		self.coords_start = (self.tadpole.xpos, self.tadpole.ypos)
		self.time_start = time.time()
		self.heading_start = self.tadpole.heading
		self.command_params = [0 0 0 0 0 0]

	def readStatus(self):
		if self.ser.available():
			self.stale = 0
			self.line = self.ser.readline()

			#parse status line
			self.tadpole_prev_state = self.tadpole_new_state
			self.tadpole_new_state = parsed_state
			self.tadpole.xpos = parsed_state
			self.tadpole.ypos = parsed_state
			self.tadpole.heading = parsed_state
		else:
			self.stale += 1

	def updateCommand(self):
		if self.control_state == "run_opt":
			if ((self.tadpole_prev_state != "Straight") && (self.tadpole_new_state == "Straight")):
				self.command_params = optimize_w_ga.get_new_params()
				self.commandString = "Straight"+self.command_params #or whatever the transmission protocol is
				self.coords_start = (self.tadpole.xpos, self.tadpole.ypos)
				self.time_start = time.time()
			if ((self.tadpole_prev_state == "Straight") && (self.tadpole_new_state != "Straight")):
				dist = math.sqrt((self.tadpole.xpos - self.coords_start[0])**2+(self.tadpole.ypos - self.coords_start[1])**2)
				tdiff = time.time()-self.time_start
				speed = dist/tdiff
				heading_change = math.abs(self.heading_start-self.tadpole.heading)
				optimize_w_ga.write_back(self.command_params, speed, heading_change, dist, tdiff)

	def sendCommand(self):
		"""need to write something to package commands into commandString"""
		#commandString = "I'm a command string!"
		ser.write(self.commandString)

class Tadpole:
	"""encodes information about Sparky"""
	def __init__(self):
		self.length = 40 # HEAD length will need to adjust
		self.segmentLength = 30 # will need to adjust
		self.color = (100,100,100) # color #should be a three-tuple

		self.xpos = 400 # updated by God-Eye
		self.ypos = 400 # updated by God-Eye

		self.heading = 0 # (HEAD Heading) Updated by God-Eye
		self.servo1 = 19 # needs to be mapped so that 0 is neutral position of servo
		self.servo2 = 15 # needs to be mapped so that 0 is neutral position of servo
		self.servo3 = -30 # needs to be mapped so that 0 is neutral position of servo

		self.vx = 0 # calculated by WorldSim
		self.vy = 0 # calculated by WorldSim

		self.state = "STOP"

	def drive(self,model):
		"""Command the servos"""

	def updatePos(self,godEye):
		"""Get the position from the God-Eye"""
		msg = godEye.prayToTheGodEye(0.1)
		message = msg.split(',')
		i = message.index('P')
		n = message.index('S')
		# position = [x,y,h]
		pos = {'x' : message[i+1], 'y' : message[i+2], 'h' : message[i+3],'t' : (message[n+1],message[n+2],message[n+3].split()[0])}
		self.xpos = int(pos['x'])
		self.ypos = int(pos['y'])
		self.heading = int(pos['h'])

	def updateVels(self):
		"""Calculate the velocity"""
		# This is obviously not yet a calculation
		self.vx = 0
		self.vy = 0

class PyGameWindowView:
	"""encodes view of simulation"""
	def __init__(self,model,screen):
		self.model = model
		self.screen = screen
	
	def draw(self):
		self.screen.fill(pygame.Color(255,255,255))

		self.draw_tadpole(self.model.tadpole1)
		self.disp_HUD_info()

		pygame.display.update()
	
	def draw_tadpole(self,tadpole):
		heading = math.radians(tadpole.heading)
		servo1 = math.radians(tadpole.servo1)
		servo2 = math.radians(tadpole.servo2)
		servo3 = math.radians(tadpole.servo3)
		bow = (tadpole.xpos+tadpole.length/2.0*cos(heading),tadpole.ypos+tadpole.length/2.0*sin(heading))
		starboard_stern = (tadpole.xpos+tadpole.length/2.0*cos(heading+pi*5.0/6),tadpole.ypos+tadpole.length/2.0*sin(heading+pi*5.0/6))
		port_stern = (tadpole.xpos+tadpole.length/2.0*cos(heading+pi*7.0/6),tadpole.ypos+tadpole.length/2.0*sin(heading+pi*7.0/6))
		pygame.draw.line(self.screen, tadpole.color, bow, starboard_stern, 3)
		pygame.draw.line(self.screen, tadpole.color, bow, port_stern, 2)
		pygame.draw.line(self.screen, tadpole.color, starboard_stern, port_stern, 1)
		segment1_head = ((starboard_stern[0]+port_stern[0])/2,(starboard_stern[1]+port_stern[1])/2)
		segment2_head = (segment1_head[0]-tadpole.segmentLength*cos(-heading+servo1),segment1_head[1]+tadpole.segmentLength*sin(-heading+servo1))
		segment3_head = (segment2_head[0]-tadpole.segmentLength*cos(-heading+servo1+servo2),segment2_head[1]+tadpole.segmentLength*sin(-heading+servo1+servo2))
		segment3_tail = (segment3_head[0]-tadpole.segmentLength*cos(-heading+servo1+servo2+servo3),segment3_head[1]+tadpole.segmentLength*sin(-heading+servo1+servo2+servo3))
		pygame.draw.line(self.screen, (200,0,0), segment1_head, segment2_head, 3)
		pygame.draw.line(self.screen, (0,200,0), segment2_head, segment3_head, 3)
		pygame.draw.line(self.screen, (0,0,200), segment3_head, segment3_tail, 3)
		
	def disp_HUD_info(self):
		"""displays the relwind next to the wind vane"""
		myfont = pygame.font.SysFont("monospace", 12, bold = True)
		text = myfont.render("tadpole h: "+str(self.model.tadpole1.heading), 1, (0,0,0))
		text_2 = myfont.render("tadpole x: "+str(self.model.tadpole1.xpos), 1, (0,0,0))
		text_3 = myfont.render("tadpole y: "+str(self.model.tadpole1.ypos), 1, (0,0,0))
		text_4 = myfont.render("servo 1: "+str(self.model.tadpole1.servo1), 1, (0,0,0))
		text_5 = myfont.render("servo 2: "+str(self.model.tadpole1.servo2), 1, (0,0,0))
		text_6 = myfont.render("servo 3: "+str(self.model.tadpole1.servo3), 1, (0,0,0))

		self.screen.blit(text, (10, 20))
		self.screen.blit(text_2, (10, 40))
		self.screen.blit(text_3, (10, 60))
		self.screen.blit(text_4, (120, 20))
		self.screen.blit(text_5, (120, 40))
		self.screen.blit(text_6, (120, 60))

class PyGameController:
	"""handles user inputs and communicates with model"""
	def __init__(self,model,view): 
		"""initialize the class"""
		self.model = model
		self.view = view
		
	def handle_keystroke_event(self,event): 
		"""builds and upgrades tadpole"""
		if event.type == KEYDOWN:
			#remember that the directions are reversed in view
			#direct control, deprecated
			pass
				
if __name__ == '__main__':
	pygame.init()
	size = (1020,800)
	screen = pygame.display.set_mode(size)
	model = WorldModel() #initial windspeed, windheading
	view = PyGameWindowView(model,screen)
	controller = PyGameController(model,view)
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.mouse.set_cursor(*pygame.cursors.arrow)
				running = False
			controller.handle_keystroke_event(event)
		model.update_model()
		view.draw()
		time.sleep(.01)
	pygame.quit()