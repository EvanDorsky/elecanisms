import encodertest
import time
import struct

enc = encodertest.encodertest()

enc.toggle_led3()

while (True):
    angleBytes = enc.enc_readReg(enc.ENC_ANGLE_AFTER_ZERO_POS_ADDER)

    angleStr = ''.join(map(chr, angleBytes))

    angle, = struct.unpack('f', angleStr)
    bits, = struct.unpack('I', angleStr)
    print "Bin: {0:032b} Dec:{1:0f}".format(bits, angle)

    time.sleep(.02)