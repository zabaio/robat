import numpy as np
from gpiozero import Device, AngularServo
#from gpiozero.pins.pigpio import PiGPIOFactory
import time

#Device.pin_factory = PiGPIOFactory()

AMIN = -60
AMAX = 60
PMIN = 0.5/1000
PMAX = 2.5/1000

class Servo:

    def __init__(self):
        self.s = AngularServo(4, min_angle=AMIN, max_angle=AMAX, min_pulse_width=PMIN, max_pulse_width=PMAX)

    def addAngle(self, delta):
        print(delta)
        nuovo = np.clip(self.s.angle + delta, AMIN, AMAX)
        print(nuovo)
        self.s.angle = nuovo


if __name__ == "__main__":
    s = Servo()
    delta = 10
    while True:
        if abs(s.s.angle) == AMAX:
            delta = -delta
        s.addAngle(delta)
        time.sleep(1)
