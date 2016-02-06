import encodertest
import time

mask = 0x3FFF
enc = encodertest.encodertest()

enc.toggle_led3()

while (True):
    angleBytes = enc.enc_readReg(enc.ENC_ANGLE_AFTER_ZERO_POS_ADDER)
    angle = int(angleBytes[0])+int(angleBytes[1])*256

    print "Dec: {2:0f}".format(angle, angle, float(angle&mask)/mask*360)

    time.sleep(.02)