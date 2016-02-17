import pickle
from matplotlib import pyplot as plt
from numpy import *
from scipy import signal as sig

def wrapfix(epos):
    ediff = append(array(0), diff(epos))

    possteps = cumsum(-360*(ediff>180))
    negsteps = cumsum(360*(ediff<-180))

    epos += possteps+negsteps
    return epos

spindown = pickle.load(open('spindown0.p', 'rb'))

encpos = -spindown['position']
encvel = -append(array(0), spindown['velocity'])

Fs = 1e3
buttfil = sig.butter(3, 200/Fs)
velfil = sig.lfilter(buttfil[0], buttfil[1], encvel)

times = spindown['time']
tstart = 3.5
tend = 6.25 

posstart = encpos[searchsorted(times, tstart)]
posend = encpos[searchsorted(times, tend)]

blue = [0, .51, 1]
orange = [1, .6, .1]
green = [.1, .5, .3]

ctime = .81

ylim1 = [0, (posend-posstart)*1.1]
ylim2 = [-10000, 100000]

plt.figure(1)
plt.subplot(211)
plt.title('"Spin-down" of loaded shaft from full speed')
plt.plot(times-tstart, encpos-posstart, color=blue)
plt.hold(True)
plt.plot([ctime, ctime], ylim1, color=green, ls='dashed')
plt.xlim([0, tend-tstart])
plt.ylim(ylim1)
plt.legend(['Position'], loc='upper left')

plt.ylabel('Position (deg)')

plt.subplot(212)
plt.plot(times-tstart, encvel, color=blue)
plt.hold(True)
plt.plot(times-tstart, velfil, color=orange)
plt.plot([ctime, ctime], ylim2, color=green, ls='dashed')
plt.xlim([0, tend-tstart])

plt.xlabel('Time (seconds)')
plt.ylabel('Velocity (deg/sec)')
plt.ylim(ylim2)
plt.legend(['Velocity', 'Velocity (filtered)'])

plt.show()