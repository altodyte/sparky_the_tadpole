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
# import gui stuff
from pgu import text, gui as pgui

##############################GOD-EYE_COMMUNICATON_UNIT######################################

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

##############################TADPOLE_COMMUNICATON_UNIT######################################

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

####################################SIMULATOR_UNIT###########################################

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

####################################WINDOW_NONSENSE##########################################

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

###################################GUI_WINDOW_NONSENSE#######################################

def logRadioAction(arg):
    """ add the radio button status to the 'edit' window (callback function)"""
    grp, text = arg
    text = "Radio Button " + str(grp.value) + " selected"
    lines.append(text)
    while len(lines) > lineLimit: lines[0:1] = []

def logCheckAction(arg):
    """ add the button status to the 'edit' window (callback function)"""
    btn, text = arg
    if btn.value:
        text += ' selected';
    else:
        text += ' deselected';
    lines.append(text)
    while len(lines) > lineLimit: lines[0:1] = []

def logButtonAction(text):
    """ add the button status to the 'edit' window (callback function)"""
    lines.append(text)
    while len(lines) > lineLimit: lines[0:1] = []

def logInputAction(txt):
    """ add the input status to the 'edit' window (callback function)"""
    text = txt.value
    lines.append(text)
    while len(lines) > lineLimit: lines[0:1] = []

def logSliderAction(txt):
    """ add the slider status to the 'edit' window (callback function)"""
    text = 'Slider is at ' + str(txt.value)
    lines.append(text)
    while len(lines) > lineLimit: lines[0:1] = []

###################################STUFF_THAT_RUNS#######################################

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

	global lines
	lines = []
	lineLimit = 20

	#Initialize Everything
	# pygame.init()
	pygame.font.init()
	font = pygame.font.SysFont("default",12)
	fontBig = pygame.font.SysFont("default",16)
	fontSub = pygame.font.SysFont("default",8)

	# screen = pygame.display.set_mode(size)
	pygame.display.set_caption('GUI Test - PGU')

	# create GUI object
	gui = pgui.App()
	textArea = pygame.Rect(500, 20, 250, 320)

	# layout using document
	lo = pgui.Container(width=350)

	# create page label
	#lo.block(align=-1) #lo.br(8) #lo.tr()
	title = pgui.Label("PygameTest Page - PGU", font=fontBig) 
	lo.add(title,29,13)

	# create checkbuttons and add to gui
	cbt = pgui.Table()
	cb1 = pgui.Switch()
	cb1.connect(pgui.CHANGE, logCheckAction, (cb1, "Check Box 1"))
	cb1l = pgui.Label("Check1")
	cbt.add(cb1)
	cbt.add(cb1l)
	cbt.tr()
	cb2 = pgui.Switch()
	cb2.connect(pgui.CHANGE, logCheckAction, (cb2, "Check Box 2"))
	cb2l = pgui.Label("Check2")
	cbt.add(cb2)
	cbt.add(cb2l)
	cbt.tr()
	cb3 = pgui.Switch()
	cb3.connect(pgui.CHANGE, logCheckAction, (cb3, "Check Box 3"))
	cb3l = pgui.Label("Check3")
	cbt.add(cb3)
	cbt.add(cb3l)
	lo.add(cbt,52,52)

	# create radio buttons, put in table, and add to gui
	rbt = pgui.Table()
	radio = pgui.Group()
	rb1 = pgui.Radio(radio, 1)
	rb1l = pgui.Label("Mode 1")
	rbt.add(rb1)
	rbt.add(rb1l)
	rbt.tr()
	rb2 = pgui.Radio(radio, 2)
	rb2l = pgui.Label("Mode 2")
	rbt.add(rb2)
	rbt.add(rb2l)
	rbt.tr()
	rb3 = pgui.Radio(radio, 3)
	rb3l = pgui.Label("Mode 3")
	rbt.add(rb3)
	rbt.add(rb3l)
	rbt.tr()
	lo.add(rbt,210,52)
	radio.connect(pgui.CHANGE, logRadioAction, (radio, "Radio Button 3"))

	# create txt box label
	txtl = pgui.Label("Text", font=fontBig)
	lo.add(txtl,30,127) 
	# create text box
	txt = pgui.Input("next of input", size=45)
	txt.connect(pgui.BLUR, logInputAction, txt)
	lo.add(txt,28,149)

	# add buttons, both regular and toggle
	btn1 = pgui.Button("Button 1")
	btn1.connect(pgui.CLICK, logButtonAction, ("Button 1 clicked"))
	lo.add(btn1,36,250)
	btn2 = pgui.Button("Button 2")
	btn2.connect(pgui.CLICK, logButtonAction, ("Button 2 clicked"))
	lo.add(btn2,133,250)
	btn3 = pgui.Button("Button 3")
	btn3.connect(pgui.CLICK, logButtonAction, ("Button 3 clicked"))
	lo.add(btn3,230,250)

	# create slider label
	sll = pgui.Label("Slider",font=fontBig)
	lo.add(sll,36,195)
	# create slider
	sl = pgui.HSlider(value=1,min=0,max=100,size=32,width=200,height=16)
	sl.connect(pgui.CHANGE, logSliderAction, sl)
	lo.add(sl,53,210) #, colspan=3)

	# clear setup noise, and put initial content in
	lines = []
	lines.append('top line of input')
	lines.append('second line of input')

	gui.init(lo)

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

		# Draw GUI
        gui.paint(screen)
        edText = "\n".join(lines)
        text.writepre(screen, font, textArea, (0,0,0), edText)
	pygame.quit()