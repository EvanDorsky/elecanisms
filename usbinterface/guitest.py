import encodertest
import time
import struct
import Tkinter as tk
import tkMessageBox

enc = encodertest.encodertest()
top = tk.Tk()     #Creates the main GUI window
var = tk.IntVar()

def toggleLED1():
	enc.toggle_led1()

def toggleLED2():
	enc.toggle_led2()

def toggleLED3():
	enc.toggle_led3()

def springmode():
	tkMessageBox.showinfo("Spring Mode", "This is a test")

def dampedmode():
	tkMessageBox.showinfo("Damped Mode", "This is a test")

def wallmode():
	wall = tk.Tk()

	C = tk.Canvas(wall, height=300, width=300)
	leftwall = C.create_line(50, 50, 50, 250)
	rightwall = C.create_line(250, 50, 250, 250)

	C.pack()
	
def texturemode():
	tkMessageBox.showinfo("Texture Mode", "This is a test")


	
LED1 = tk.Button(top, text="LED1", activebackground ="red", command=toggleLED1)
LED2 = tk.Button(top, text="LED2", activebackground = "green", command=toggleLED2)
LED3 = tk.Button(top, text="LED3", activebackground ="blue", command=toggleLED3)

LED1.grid(column=0,row=0)
LED2.grid(column=0,row=1)
LED3.grid(column=0,row=2)

M1 = tk.Radiobutton(top, text="Spring Mode", variable=var, value=1, command=springmode)
M2 = tk.Radiobutton(top, text="Damped Mode", variable=var, value=2, command=dampedmode)
M3 = tk.Radiobutton(top, text="Wall Mode", variable=var, value=3, command=wallmode)
M4 = tk.Radiobutton(top, text="Texture Mode", variable=var, value=4, command=texturemode)

M1.grid(column=2,row=0)
M2.grid(column=2,row=1)
M3.grid(column=2,row=2)
M4.grid(column=2,row=3)

top.mainloop()