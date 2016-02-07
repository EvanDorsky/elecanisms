import encodertest
import time
from matplotlib import pyplot as plt
from numpy import *

mask = 0x3FFF
enc = encodertest.encodertest()

enc.toggle_led3()

samples = 1000
encpos = zeros(samples)
times = zeros(samples)
raw = 0

last = time.clock()
step = 1e-3
i = 0

while(i < samples):
    current = time.clock()

    if (current - last > step):
        times[i] = current
        last = current

        angleBytes = enc.enc_readReg(enc.ENC_ANGLE_AFTER_ZERO_POS_ADDER)
        raw = int(angleBytes[0])+int(angleBytes[1])*256
        encpos[i] = float(raw&mask)/mask*360

        i+=1

plt.plot(times, encpos)
plt.show()