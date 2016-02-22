import encodertest
import time
import struct
from numpy import *
import pickle

mask = 0x3FFF
joy = encodertest.encodertest()

joy.toggle_led3()

samples = 5000
encpos = zeros(samples)
encvel = zeros(samples)
encD = zeros(samples)
times = zeros(samples)
raw = 0

last = time.clock()
step = 1e-3
i = 0

JOY_SPRING = 1

def readAngle():
    bts = joy.joy_read_angle()
    chrs = ''.join(map(chr, bts))

    res, = struct.unpack('f', chrs)

    return res

def readVel():
    bts = joy.joy_read_vel()
    chrs = ''.join(map(chr, bts))

    res, = struct.unpack('f', chrs)

    return res

def readD():
    bts = joy.joy_read_d()
    chrs = ''.join(map(chr, bts))

    res, = struct.unpack('f', chrs)

    return res

joy.joy_set_mode(JOY_SPRING)
while(i < samples):
    current = time.clock()

    if (current - last > step):
        times[i] = current
        last = current

        encpos[i] = readAngle()
        encvel[i] = readVel()
        encD[i] = readD()

        i+=1

pickle.dump({
    'position' : encpos,
    'velocity' : encvel,
    'duty' : encD,
    'time'     : times
    }, open('spring.p', 'wb'))