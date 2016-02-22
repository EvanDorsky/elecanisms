import encodertest
import time
import struct
import Tkinter as tk
import tkMessageBox

enc = encodertest.encodertest()
top = tk.Tk()     #Creates the main GUI window
var = tk.IntVar()

# List of global variables
angle = 0
CS = 0		#Canvas objects for each mode
CD = 0
CW = 0
CT = 0
spring = 0	#Window names for each mode
damper = 0
wall = 0
texture = 0
circle = 0

y1 = 145	#Defines the top and bottom of the position circle	
y2 = 155

joy_mode_spring = 1		#Defines the values for the switch case in PIC code
joy_mode_wall = 0
joy_mode_damper = 2
joy_mode_texture = 3
joy_mode_free = 4

ELEFT = 0
ERIGHT = 0
leftwall = 30
rightwall = 30

EK = 0
springk = 0.8

# -----------------------------------------------------------------------
# Main window functions
def toggleLED1():
	enc.toggle_led1()

def toggleLED2():
	enc.toggle_led2()

def toggleLED3():
	enc.toggle_led3()

def getangle():
	angleBytes = enc.joy_read_angle()
	# print angleBytes
	angleStr = ''.join(map(chr, angleBytes))

	angle, = struct.unpack('f', angleStr)
	bits, = struct.unpack('I', angleStr)
	print "Bin: {0:032b} Dec:{1:0f}".format(bits, angle)

# -----------------------------------------------------------------------
# Spring Mode Functions
def springmode():
	global angle
	global CS
	global spring
	global y1
	global y2
	global joy_mode_spring
	global EK

	spmode = enc.joy_set_mode(joy_mode_spring)
	
	modeStr = ''.join(map(chr,spmode))
	mode, = struct.unpack('h', modeStr)
	print "Mode: {0:0f}".format(mode)

	# read the angle from the encoder
	angleBytes = enc.joy_read_angle()
	angleStr = ''.join(map(chr, angleBytes))
	angle, = struct.unpack('f', angleStr)

	xcenter = 150 + angle*2   #set the center of the circle based on the angle reading

	spring = tk.Tk()	# open the new window for spring mode interactions

	# create the parameter entry widgets for the spring constant
	KLABEL = tk. Label(spring, text="Spring Constant")
	KLABEL.pack()

	EK = tk.Entry(spring, bd=5, width=10, textvariable=tk.StringVar())
	EK.insert(0, 0.8)
	EK.pack()

	KGET = tk.Button(spring, text="Set Parameter", command=getspring)
	KGET.pack()

	# create the canvas that the interface is drawn on
	CS = tk.Canvas(spring, height=300, width=300)
	circle = CS.create_oval(xcenter-5, y1, xcenter+5, y2, fill="red")

	CS.pack()

	OKSPRING = tk.Button(spring, text="Ok", command = quitspring)

	OKSPRING.pack()

	updateCS()

def updateCS():
	# assign the global variables that updateCS will use
	global angle
	global CS
	global spring
	global y1
	global y2
	global springk

	# read the angle from the encoder
	angleBytes = enc.joy_read_angle()
	angleStr = ''.join(map(chr, angleBytes))
	angle, = struct.unpack('f', angleStr)

	xcenter = 150 + angle*2    # set the center of the circle based on the angle reading

	CS.delete("all")  #clear the canvas

	# redraw the canvas objects with the new circle position
	CS.create_line(150, 150, xcenter, 150, width=2)
	CS.create_oval(xcenter-5, y1, xcenter+5, y2, fill="red")
	
	spring.after(16, updateCS)	# call updateCanvas again after 100ms


def getspring():
	global EK
	global springk

	springk = float(EK.get())
	kvalue = int(springk*1000)

	enc.joy_set_k(kvalue)

	print springk

def quitspring():
	global spring
	global joy_mode_free

	enc.joy_set_mode(joy_mode_free)

	spring.destroy()

# -----------------------------------------------------------------------
# Damped Mode Functions
def dampermode():
	global angle
	global CD
	global damper
	global y1
	global y2
	global joy_mode_damper

	dmpmode = enc.joy_set_mode(joy_mode_damper)

	value = ''.join(map(chr,dmpmode))
	mode, = struct.unpack('h',value)
	print "Mode:{0:0f}".format(mode)

	# read the angle from the encoder
	angleBytes = enc.joy_read_angle()
	angleStr = ''.join(map(chr, angleBytes))
	angle, = struct.unpack('f', angleStr)

	xcenter = 150 + angle*2   #set the center of the circle based on the angle reading

	damper = tk.Tk()	# open the new window for damped mode interactions

	# create the canvas that the interface is drawn on
	CD = tk.Canvas(damper, height=300, width=300)
	circle = CD.create_oval(xcenter-5, y1, xcenter+5, y2, fill="red")

	CD.pack()

	OKDAMP = tk.Button(damper, text="Ok", command = quitdamper)

	OKDAMP.pack()


def quitdamper():
	global damper
	global joy_mode_free

	enc.joy_set_mode(joy_mode_free)

	damper.destroy()

# -----------------------------------------------------------------------
# Wall Mode Functions
def wallmode():
	# assign the global variables that wall mode will use
	global CW
	global wall
	global circle
	global angle
	global y1
	global y2
	global joy_mode_wall
	global ELEFT
	global ERIGHT

	enc.joy_set_mode(joy_mode_wall)	# set the joystick mode to wall

	# read the angle from the encoder
	angleBytes = enc.joy_read_angle()
	angleStr = ''.join(map(chr, angleBytes))
	angle, = struct.unpack('f', angleStr)

	xcenter = 150 + angle*2   #set the center of the circle based on the angle reading

	wall = tk.Tk()	# open the new window for wall mode interactions

	# create the parameter entry widgets for the left and right wall positions
	LLABEL = tk. Label(wall, text="Left Wall")
	LLABEL.pack()

	ELEFT = tk.Entry(wall, bd=5, width=10, textvariable=tk.StringVar())
	ELEFT.insert(0, 30)
	ELEFT.pack()

	RLABEL = tk.Label(wall, text="Right Wall")
	RLABEL.pack()

	ERIGHT = tk.Entry(wall, bd=5, width=10, textvariable=tk.StringVar())
	ERIGHT.insert(0, 30)
	ERIGHT.pack()

	WALLGET = tk.Button(wall, text="Set Parameters", command=getwall)
	WALLGET.pack()

	# create the canvas that the interface is drawn on
	CW = tk.Canvas(wall, height=300, width=300, bd=5)
	CW.create_line(90, 50, 90, 250, width=3)
	CW.create_line(210, 50, 210, 250, width=3)
	circle = CW.create_oval(xcenter-5, y1, xcenter+5, y2, fill="red")

	CW.pack()

	OKWALL = tk.Button(wall, text="Ok", command = quitwall)
	OKWALL.pack()

	updateCW()  # call the update function to redraw the circle position

def updateCW():
	# assign the global variables that updateCW will use
	global angle
	global CW
	global wall
	global y1
	global y2
	global leftwall
	global rightwall

	# read the angle from the encoder
	angleBytes = enc.joy_read_angle()
	angleStr = ''.join(map(chr, angleBytes))
	angle, = struct.unpack('f', angleStr)

	xcenter = 150 + angle*2    # set the center of the circle based on the angle reading

	# set the wall coordinates based on the parameters
	leftx = 150 - leftwall*2
	rightx = 150 + rightwall*2

	CW.delete("all")  #clear the canvas

	# redraw the canvas objects with the new circle position
	CW.create_line(leftx, 50, leftx, 250, width=3)
	CW.create_line(rightx, 50, rightx, 250, width=3)
	CW.create_oval(xcenter-5, y1, xcenter+5, y2, fill="red")
	
	wall.after(16, updateCW)	# call updateCanvas again after 100ms

def getwall():
	global ELEFT
	global ERIGHT
	global leftwall
	global rightwall

	leftwall = int(ELEFT.get())
	enc.joy_set_wall_left(leftwall)

	rightwall = int(ERIGHT.get())
	enc.joy_set_wall_right(rightwall)

	print leftwall
	print rightwall

def quitwall():
	global wall
	global joy_mode_free

	enc.joy_set_mode(joy_mode_free)

	wall.destroy()

# -----------------------------------------------------------------------
# Texture Mode Functions
def texturemode():
	global angle
	global CT
	global texture
	global y1
	global y2
	global joy_mode_texture

	txmode = enc.joy_set_mode(joy_mode_texture)

	value = ''.join(map(chr,txmode))
	mode, = struct.unpack('h',value)
	print "Mode:{0:0f}".format(mode)

	# read the angle from the encoder
	angleBytes = enc.joy_read_angle()
	angleStr = ''.join(map(chr, angleBytes))
	angle, = struct.unpack('f', angleStr)

	xcenter = 150 + angle*2   #set the center of the circle based on the angle reading

	texture = tk.Tk()	# open the new window for texture mode interactions

	# create the canvas that the interface is drawn on
	CT = tk.Canvas(texture, height=300, width=300)
	circle = CT.create_oval(xcenter-5, y1, xcenter+5, y2, fill="red")

	CT.pack()

	OKTEXTURE = tk.Button(texture, text="Ok", command = quittexture)

	OKTEXTURE.pack()


def quittexture():
	global texture
	global joy_mode_free

	enc.joy_set_mode(joy_mode_free)

	texture.destroy()
# -----------------------------------------------------------------------
# Setting up the main window
	
LED1 = tk.Button(top, text="LED1", activebackground ="red", command=toggleLED1)
LED2 = tk.Button(top, text="LED2", activebackground = "green", command=toggleLED2)
LED3 = tk.Button(top, text="LED3", activebackground ="blue", command=toggleLED3)
ANGLE = tk.Button(top, text="Angle", command=getangle)

LED1.grid(column=0,row=0)
LED2.grid(column=0,row=1)
LED3.grid(column=0,row=2)
ANGLE.grid(column=0,row=3)

M1 = tk.Radiobutton(top, text="Spring Mode", variable=var, value=1, command=springmode)
M2 = tk.Radiobutton(top, text="Damper Mode", variable=var, value=2, command=dampermode)
M3 = tk.Radiobutton(top, text="Wall Mode", variable=var, value=3, command=wallmode)
M4 = tk.Radiobutton(top, text="Texture Mode", variable=var, value=4, command=texturemode)

M1.grid(column=2,row=0)
M2.grid(column=2,row=1)
M3.grid(column=2,row=2)
M4.grid(column=2,row=3)

top.mainloop()

