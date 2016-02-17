import encodertest
import time
from matplotlib import pyplot as plt
from numpy import *
import pickle
from subprocess import call

mask = 0x3FFF
enc = encodertest.encodertest()
enc.toggle_led3()

step = 4

def getAngle():
    angleBytes = enc.enc_readReg(enc.ENC_ANGLE_AFTER_ZERO_POS_ADDER)
    raw = int(angleBytes[0])+int(angleBytes[1])*256

    return float(raw&mask)/mask*360

def printSample(i):
    if i:
        print ""
        print "Another one."
        print ""
    print "Sample "+str(i)
    print "YOU HAVE "+str(step)+" SECONDS"
    call(["say", "'Another one.'"])

ticks = 20
window = 50
encpos = zeros(ticks)
times = zeros(ticks)
raw = 0

last = time.clock()
i = 0

encsum = 0

angles = linspace(-5, 90, ticks)

print "Get ready!"
print "YOU HAVE "+str(step)+" SECONDS"

while(i < ticks):
    current = time.clock()

    if (current - last > step):
        printSample(i)
        for samp in range(0, window):
            encsum += getAngle()

        encpos[i] = encsum/window

        print "Reading: "+str(encsum/window)+" deg"

        encsum = 0
        last = current
        i+=1

pickle.dump({
    'position' : encpos
    }, open('calibration.p', 'wb'))