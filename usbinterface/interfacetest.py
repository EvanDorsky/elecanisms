import encodertest
import time
import struct

enc = encodertest.encodertest()

enc.toggle_led3()

while (True):
	spring_k = 8
	ks = enc.write_ks(spring_k)

	kStr = ''.join(map(chr, ks))

	angle, = struct.unpack('h', kStr)
	print "Value:{0:0f}".format(angle)

	time.sleep(.02)