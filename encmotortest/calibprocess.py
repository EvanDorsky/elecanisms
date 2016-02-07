import pickle
from matplotlib import pyplot as plt
from numpy import *

def wrapfix(epos):
    ediff = append(array(0), diff(epos))

    possteps = cumsum(-360*(ediff>180))
    negsteps = cumsum(360*(ediff<-180))

    epos += possteps+negsteps
    return epos

encpos = pickle.load(open('calibration0.p', 'rb'))['position']
angles = linspace(0, 90, len(encpos)-1)
angles = append(angles[0]-7.5, angles)

encpos = -wrapfix(encpos)
encpos -= encpos[int(len(encpos)/2)]
angles -= angles[int(len(encpos)/2)]

[m1, b1] = polyfit(angles, encpos, 1)

estangles = encpos/(15+1/3)

[m2, b2] = polyfit(angles, estangles, 1)

plt.grid(True)
plt.scatter(angles, encpos)
plt.hold(True)
plt.plot(angles, m1*angles+b1)
plt.title('Calibration Curve 1')
plt.xlabel('Joystick Angle (deg)')
plt.ylabel('Encoder Angle (deg)')
plt.ylim([-800, 800])
plt.legend(['Fit', 'Data'], loc='upper left')

plt.figure()
plt.grid(True)
plt.scatter(angles, estangles)
plt.hold(True)
plt.plot(angles, m2*angles+b2)
plt.plot(angles, angles)
plt.title('Calibration Curve 2')
plt.xlabel('Joystick Angle (deg)')
plt.ylabel('Corrected Encoder Angle (Based on CAD)')
plt.legend(['Fit', 'Unity', 'Data'], loc='upper left')

plt.show()