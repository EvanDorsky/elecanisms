from matplotlib import pyplot as plt
from numpy import *
import pickle

d = pickle.load(open('spring1.p', 'rb'))
encpos = d['position']
encvel = d['velocity']
encD =d['duty']
encdir =d['direction']
encdir = encdir*2-1
print encdir[encdir>0]
times = d['time']

blue = [0, .51, 1]
orange = [1, .6, .1]
green = [.1, .5, .3]

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.plot(times, encpos, color=green)
ax1.hold(True)
ax1.plot(times, encD*100, color=orange)

ax2.plot(times, encvel, color=blue)

ax1.set_xlabel('Time (Seconds)')

ax1.set_ylabel('Anglular Position (Deg)', color=green)
ax2.set_ylabel('Angular Velocity (Deg/sec)', color=blue)

plt.title('Texture: Time Domain Response')
plt.xlim([3, pi])
ax1.set_ylim([-60, 120])
ax1.legend(['Angular Position', 'Duty Cycle (%)'], loc='upper left')
ax2.legend(['Velocity'])
plt.grid(True)

plt.figure()
plt.title('Texture: Motor Response')
plt.plot(encpos, encD*100, color=blue)
plt.ylabel('Duty Cycle (%)')
plt.xlabel('Angular Position (Deg)')
plt.grid(True)

plt.figure()
plt.title('Texture: Motor Velocity Response')
plt.plot(encvel, encdir*encD*100, color=blue)
plt.ylabel('Duty Cycle (%)')
plt.xlabel('Velocity (Deg/sec)')
plt.grid(True)
plt.show()