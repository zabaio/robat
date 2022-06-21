import numpy as np
from gpiozero import AngularServo
from constants import H_WIND, F_LEN, HALF_W, Timer
import time

MIN_A = -90
MAX_A = 90
MIN_P = 0.5/1000
MAX_P = 2.5/1000

SER_TM = 0.5

class ServoHandler:

    def __init__(self):
        self.s = AngularServo(4, min_angle=MIN_A, max_angle=MAX_A, min_pulse_width=MIN_P, max_pulse_width=MAX_P)
        self.s.angle = 0
        self.angle = self.s.angle
        time.sleep(SER_TM)
        self.s.detach()
        self.tm = Timer(2)

    def update(self, res):
        if res is not None and self.tm.isDone():
            print("AAAA")
            offset = res[0] + res[2] / 2 - HALF_W
            print(offset / HALF_W)
            if abs(offset) / HALF_W > H_WIND:
                self.addAngle(-np.degrees(np.arctan(offset / F_LEN) / 2))
                self.tm.set(2)

    def addAngle(self, delta):
        self.s.angle = np.clip(self.angle + delta, MIN_A, MAX_A)
        self.angle = self.s.angle
        time.sleep(SER_TM)
        self.s.detach()
        print(self.s.angle)


def main():
    sh = ServoHandler()
    delta = 10
    while True:
        if abs(sh.s.angle) == MAX_A:
            delta = -delta
        sh.addAngle(delta)
        time.sleep(1)


if __name__ == "__main__":
    main()
