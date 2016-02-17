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

blue = [0, .51, 1]
orange = [1, .6, .1]
green = [.1, .5, .3]

plt.grid(True)
plt.scatter(angles, encpos, color=blue)
plt.hold(True)
plt.plot(angles, m1*angles+b1, color=orange)
plt.title('Encoder Calibration Curve')
plt.xlabel('Joystick Angle (deg)')
plt.ylabel('Encoder Angle (deg)')
plt.ylim([-800, 800])
plt.legend(['Fit', 'Data'], loc='upper left')

plt.figure()
plt.grid(True)
plt.scatter(angles, estangles, color=blue)
plt.hold(True)
plt.plot(angles, m2*angles+b2, color=orange)
plt.plot(angles, angles, color=green)
plt.title('Estimated Joystick Reduction Ratio Calibration Curve')
plt.xlabel('Joystick Angle (deg)')
plt.ylabel('Joystick Raio-Corrected Encoder Angle (deg)')
plt.legend(['Fit', 'Unity', 'Data'], loc='upper left')

plt.show()