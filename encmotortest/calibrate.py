import encodertest
import time
from matplotlib import pyplot as plt
from numpy import *
import pickle

mask = 0x3FFF
enc = encodertest.encodertest()
enc.toggle_led3()

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
    print "YOU HAVE "+str(5)+" SECONDS"

ticks = 19
window = 50
encpos = zeros(ticks)
times = zeros(ticks)
raw = 0

last = time.clock()
step = 5
i = 0

encsum = 0

angles = linspace(0, 90, ticks)

print "Get ready!"
print "YOU HAVE "+str(5)+" SECONDS"

while(i < ticks):
    current = time.clock()

    if (current - last > step):
        printSample(i)
        for samp in range(0, window):
            encsum += getAngle()

        encpos[i] = encsum/window

        encsum = 0
        last = current
        i+=1

pickle.dump({
    'position' : encpos
    }, open('calibration.p', 'wb'))

plt.plot(encpos)
plt.hold(True)
plt.plot(times[0:-1], encvel)
plt.show()