import encodertest
import time
import struct
from numpy import *
import pickle

joy = encodertest.encodertest()

samples = 5000
encpos = zeros(samples)
encvel = zeros(samples)
encD = zeros(samples)
encdir = zeros(samples)
times = zeros(samples)
raw = 0

last = time.clock()
step = 1e-3
i = 0

JOY_MODE_WALL = 0
JOY_MODE_SPRING = 1
JOY_MODE_DAMPER = 2
JOY_MODE_TEXTURE = 3

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

def readDir():
    bts = joy.joy_read_dir()
    chrs = ''.join(map(chr, bts))

    res, = struct.unpack('h', chrs)

    return res

joy.joy_set_mode(JOY_MODE_DAMPER)
joy.joy_set_b(5000)
while(i < samples):
    current = time.clock()

    if (current - last > step):
        times[i] = current
        last = current

        encpos[i] = readAngle()
        encvel[i] = readVel()
        encD[i] = readD()
        encdir[i] = readDir()

        i+=1

pickle.dump({
    'position' : encpos,
    'velocity' : encvel,
    'duty' : encD,
    'direction' : encdir,
    'time'     : times
    }, open('spring2.p', 'wb'))