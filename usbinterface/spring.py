import encodertest
import time
import struct
from matplotlib import pyplot as plt
from numpy import *
import pickle

mask = 0x3FFF
joy = encodertest.encodertest()

joy.toggle_led3()

samples = 10000
encpos = zeros(samples)
encvel = zeros(samples)
times = zeros(samples)
raw = 0

last = time.clock()
step = 1e-3
i = 0

def readFloat(fun):
    bts = fun()
    chrs = ''.join(map(chr, bts))

    res, = struct.unpack('f', chrs)

    return res

while(i < samples):
    current = time.clock()

    if (current - last > step):
        times[i] = current
        last = current

        encpos[i] = readFloat(joy.joy_read_angle)
        encvel[i] = readFloat(joy.joy_read_vel)

        i+=1

pickle.dump({
    'position' : encpos,
    'velocity' : encvel,
    'time'     : times
    }, open('spring.p', 'wb'))

plt.plot(times, encpos)
plt.hold(True)
plt.plot(times[0:-1], encvel)
plt.show()