# As part of the Pitcher's Duel Project, I am conducting a comparative
# analysis of pygame GUI modules, and publishing the results on my blog.
# The comparison consists of implementing the same sample interface on
# each of the various GUIs.  
#
# This code implements the interface using the PGU GUI library, part of
# Phil's pyGame Utilities.  For details on this library, see:
# http://www.imitationpickles.org/pgu/
#
# The module author is: Phil Hassey 
#
# This source code is the work of David Keeney, dkeeney at travelbyroad dot net

#Import Modules
import pygame
from pygame.locals import *
import time
import math

# import gui stuff
from pgu import text, gui as pgui

screenSize = (642, 429)
lines = []
lineLimit = 20

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

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    global lines

    #Initialize Everything
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("default",12)
    fontBig = pygame.font.SysFont("default",16)
    fontSub = pygame.font.SysFont("default",8)

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption('GUI Test - PGU')

    # create GUI object
    gui = pgui.App()
    textArea = pygame.Rect(370, 20, 250, 320)

    # layout using document
    lo = pgui.Container(width=350)

    # create page label
    #lo.block(align=-1) #lo.br(8) #lo.tr()
    title = pgui.Label("PygameTest Page - PGU", font=fontBig) 
    lo.add(title,29,13)

    # create progress bar label
    # progress bar
    pbl = pgui.Label("ProgressNot Supported") 
    lo.add(pbl,354,371)

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
    rb1l = pgui.Label("Radioon 1")
    rbt.add(rb1)
    rbt.add(rb1l)
    rbt.tr()
    rb2 = pgui.Radio(radio, 2)
    rb2l = pgui.Label("Radioon 2")
    rbt.add(rb2)
    rbt.add(rb2l)
    rbt.tr()
    rb3 = pgui.Radio(radio, 3)
    rb3l = pgui.Label("Radioon 3")
    rbt.add(rb3)
    rbt.add(rb3l)
    rbt.tr()
    lo.add(rbt,210,52)
    radio.connect(pgui.CHANGE, logRadioAction, (radio, "Radio Button 3"))

    # create txt box label
    txtl = pgui.Label("Text", font=fontSub)
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

    # create toggle button not avail label
    tbl = pgui.Label("Toggleons Not Supported")
    lo.add(tbl,36,290)
    iml = pgui.Label("ImageNot Supported")
    lo.add(iml,36,340)

    # create slider label
    sll = pgui.Label("Slidernt=fontSub")
    lo.add(sll,36,195)
    # create slider
    sl = pgui.HSlider(value=1,min=0,max=100,size=32,width=200,height=16)
    sl.connect(pgui.CHANGE, logSliderAction, sl)
    lo.add(sl,53,210) #, colspan=3)

    # make some insensitive
    btn2.style.disabled = True
    cb3.style.disabled = True

    # clear setup noise, and put initial content in
    lines = []
    lines.append('top line of input')
    lines.append('second line of input')

    gui.init(lo)

    #Main Loop
    while 1:

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

            # pass event to gui
            gui.event(event)

        # clear background, and draw clock-spinner
        screen.fill((250, 250, 250))
        radius = 30
        spinPos = 240, 362
        sp2 = spinPos[0]+1, spinPos[1]
        progressAngle = int(time.time() % 15 * 24 - 90) #60
        pygame.draw.circle(screen, (180, 180, 180), spinPos, radius, 0)
        for angle in range(-90, progressAngle):
            a = angle*math.pi/180
            tgt = radius*math.cos(a)+spinPos[0], \
                  radius*math.sin(a)+spinPos[1]
            pygame.draw.line(screen, (254,254,254), spinPos, tgt, 2)
        pygame.draw.circle(screen, (0,0,0), spinPos, radius, 2)
        pygame.draw.circle(screen, (0,0,0), spinPos, radius+1, 3)
        pygame.draw.circle(screen, (0,0,0), sp2, radius, 2)
        pygame.draw.circle(screen, (0,0,0), sp2, radius+1, 3)
        pygame.draw.line(screen, (0,0,0), spinPos, tgt, 2)
        tgt = spinPos[0], spinPos[1]-radius
        pygame.draw.line(screen, (0,0,0), spinPos, tgt, 2)

        # Draw GUI
        gui.paint(screen)
        edText = "\n".join(lines)
        text.writepre(screen, font, textArea, (0,0,0), edText)

        pygame.display.flip()

main()