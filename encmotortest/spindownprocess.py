import pickle
from matplotlib import pyplot as plt
from numpy import *

def wrapfix(epos):
    ediff = append(array(0), diff(epos))

    possteps = cumsum(-360*(ediff>180))
    negsteps = cumsum(360*(ediff<-180))

    epos += possteps+negsteps
    return epos

spindown = pickle.load(open('spindown0.p', 'rb'))

encpos = -spindown['position']
encvel = -append(array(0), spindown['velocity'])
times = spindown['time']
tstart = 3.5
tend = 6.25 

posstart = encpos[searchsorted(times, tstart)]
posend = encpos[searchsorted(times, tend)]

plt.figure(1)
plt.subplot(211)
plt.title('"Spin-down" of loaded shaft from full speed')
plt.plot(times-tstart, encpos-posstart)
plt.xlim([0, tend-tstart])
plt.ylim([0, (posend-posstart)*1.1])
plt.legend(['Position'], loc='upper left')

plt.ylabel('Position (deg)')

plt.subplot(212)
plt.plot(times-tstart, encvel)
plt.xlim([0, tend-tstart])

plt.xlabel('Time (seconds)')
plt.ylabel('Speed (deg/sec)')
plt.ylim([-10000, 100000])
plt.legend(['Velocity'])

plt.show()