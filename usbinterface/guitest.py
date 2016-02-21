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
C = 0
wall = 0
circle = 0
y1 = 145
y2 = 155
joy_mode_spring = 0
joy_mode_wall = 1
joy_mode_damper = 2
joy_mode_texture = 3
joy_mode_free = 4

# angleBytes = enc.enc_readReg(enc.ENC_ANGLE_AFTER_ZERO_POS_ADDER)

# angleStr = ''.join(map(chr, angleBytes))

# angle, = struct.unpack('f', angleStr)
# bits, = struct.unpack('I', angleStr)
# print "Bin: {0:032b} Dec:{1:0f}".format(bits, angle)

def toggleLED1():
	enc.toggle_led1()

def toggleLED2():
	enc.toggle_led2()

def toggleLED3():
	enc.toggle_led3()

def getangle():
	angleBytes = enc.enc_readReg(enc.ENC_ANGLE_AFTER_ZERO_POS_ADDER)
	# print angleBytes
	angleStr = ''.join(map(chr, angleBytes))

	angle, = struct.unpack('h', angleStr)
	bits, = struct.unpack('I', angleStr)
	print "Bin: {0:032b} Dec:{1:0f}".format(bits, angle)

def springmode():
	global joy_mode_spring

	spmode = enc.joy_set_mode(joy_mode_spring)

	value = ''.join(map(chr,spmode))
	mode, = struct.unpack('h',value)
	print "Mode:{0:0f}".format(mode)

def dampedmode():
	tkMessageBox.showinfo("Damped Mode", "This is a test")

def wallmode():
	# assign the global variables that wall mode will use
	global C
	global wall
	global circle
	global angle
	global y1
	global y2
	global joy_mode_wall

	wmode = enc.joy_set_mode(joy_mode_wall)	# set the joystick mode to wall

	# check the result of the mode assignment to see that the correct value was sent and received
	value = ''.join(map(chr, wmode))
	mode, = struct.unpack('h', value)
	print "Mode:{0:0f}".format(mode)

	# read the angle from the encoder
	angleBytes = enc.joy_read_angle()
	print angleBytes
	angleStr = ''.join(map(chr, angleBytes))
	angle, = struct.unpack('f', angleStr)

	xcenter = 150 + angle*2   #set the center of the circle based on the angle reading

	wall = tk.Tk()	# open the new window for wall mode interactions

	# create the canvas that the interface is drawn on
	C = tk.Canvas(wall, height=300, width=300)
	leftwall = C.create_line(50, 50, 50, 250, width=3)
	rightwall = C.create_line(250, 50, 250, 250, width=3)
	circle = C.create_oval(xcenter-5, y1, xcenter+5, y2, fill="red")

	C.pack()

	updateCanvas()  # call the update function to redraw the circle position
	
def texturemode():
	tkMessageBox.showinfo("Texture Mode", "This is a test")

def updateCanvas():
	# assign the global variables that updateCanvas will use
	global angle
	global C
	global wall
	global circle
	global y1
	global y2

	# read the angle from the encoder
	angleBytes = enc.joy_read_angle()

	angleStr = ''.join(map(chr, angleBytes))
	angle, = struct.unpack('f', angleStr)

	xcenter = 150 + angle*2     # set the center of the circle based on the angle reading

	C.delete("all")  #clear the canvas

	# redraw the canvas objects with the new circle position
	leftwall = C.create_line(50, 50, 50, 250, width=3)
	rightwall = C.create_line(250,50,250,250, width=3)
	circle = C.create_oval(xcenter-5, y1, xcenter+5, y2, fill="red")

	wall.after(100, updateCanvas)	# call updateCanvas again after 100ms
	
LED1 = tk.Button(top, text="LED1", activebackground ="red", command=toggleLED1)
LED2 = tk.Button(top, text="LED2", activebackground = "green", command=toggleLED2)
LED3 = tk.Button(top, text="LED3", activebackground ="blue", command=toggleLED3)
ANGLE = tk.Button(top, text="Angle", command=getangle)

LED1.grid(column=0,row=0)
LED2.grid(column=0,row=1)
LED3.grid(column=0,row=2)
ANGLE.grid(column=0,row=3)

M1 = tk.Radiobutton(top, text="Spring Mode", variable=var, value=1, command=springmode)
M2 = tk.Radiobutton(top, text="Damped Mode", variable=var, value=2, command=dampedmode)
M3 = tk.Radiobutton(top, text="Wall Mode", variable=var, value=3, command=wallmode)
M4 = tk.Radiobutton(top, text="Texture Mode", variable=var, value=4, command=texturemode)

M1.grid(column=2,row=0)
M2.grid(column=2,row=1)
M3.grid(column=2,row=2)
M4.grid(column=2,row=3)

top.mainloop()

