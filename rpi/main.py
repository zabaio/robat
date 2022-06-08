from multiprocessing import Process, Queue
from camera import CVProcess
from servo import Servo
import numpy as np
from constants import FRAME_SIZE, H_WIND, F_LEN


def main():
    s = Servo()
    new = False
    res = None
    q = Queue()
    p = Process(target=CVProcess, args=(q,))
    p.start()
    hw = FRAME_SIZE[0]/2
    while True:
        if not q.empty():
            res = q.get_nowait()
            print(res)
            new = True
        else:
            new = False
        if new and res is not None:
            offset = res[0] + res[2]/2 - hw
            print(offset / hw)
            if abs(offset)/hw > H_WIND:
               s.addAngle(-np.degrees(np.arctan(offset/F_LEN)/2))

if __name__ == "__main__":
    main()
