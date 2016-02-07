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

plt.scatter(angles, encpos)
plt.grid(True)
plt.title('Calibration Curve')
plt.xlabel('Joystick Angle (deg)')
plt.ylabel('Encoder Angle (deg)')
plt.show()