from matplotlib import pyplot as plt
from numpy import *
import pickle

d = pickle.load(open('spring.p', 'rb'))
encpos = d['position']
encvel = d['velocity']
encD =d['duty']
times = d['time']

plt.plot(times, encpos)
plt.hold(True)
plt.plot(times, encvel)
plt.plot(times, encD*30)
plt.legend(['Position', 'Velocity'])
plt.show()