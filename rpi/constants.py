from aenum import AutoNumberEnum
from PIL import Image
import time
FRAME_SIZE = (320, 304)
HALF_W = FRAME_SIZE[0] / 2
H_WIND = 0.3
H_FOV = 120
F_LEN = 93.7
SEN_THR = 100


class Timer:
    def __init__(self, timeout=None):
        self.start = time.time()
        self.timeout = timeout
        self.timeLeft = None

    def set(self, timeout):
        self.start = time.time()
        self.timeout = timeout
        self.timeLeft = None

    def pause(self):
        self.timeLeft = self.timeout - (time.time() - self.start)

    def unpause(self):
        if self.timeLeft is None:
            print("Warning: unpausing an unpaused game")
        else:
            self.set(self.timeLeft)

    def isDone(self):
        if self.timeLeft is not None:
            return False
        if self.timeout is None:
            return False
        else:
            return time.time() - self.start > self.timeout


class Mode(AutoNumberEnum):
    _init_ = "time gif audio"
    HUNTING = None, (Image.open("resources/hunting/left.gif"), Image.open("resources/hunting/right.gif")), (["C4", "E4", "CS5"], False, 13)
    SURPRISED = 3, (Image.open("resources/surprised/left.gif"), Image.open("resources/surprised/left.gif")), None
    LOCKED = None, (Image.open("resources/locked/left.gif"), Image.open("resources/locked/right.gif")), (["E5", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P"], True, 9)
    SLEEPING = None, (Image.open("resources/sleeping/left.gif"), Image.open("resources/sleeping/right.gif")), None
    SAD = 6, (Image.open("resources/sad_lose/left.gif"), Image.open("resources/sad_lose/right.gif")), (["P", "P", "F5", "GS4"], False, 8)
    HAPPY = 6, (Image.open("resources/happy_win/left.gif"), Image.open("resources/happy_win/right.gif")), (["E4", "A4", "CS5", "F5", "P", "CS5", "F5", "F5", "F5"], False, 10)
    WIN = 5, (Image.open("resources/happy_win/left.gif"), Image.open("resources/happy_win/right.gif")), (["E4", "A4", "CS5", "F5", "CS5", "A4", "E4", "A4", "CS5", "F5", "CS5", "A4", "E4", "A4", "CS5", "F5", "CS5", "E4", "A4"], False, 10)
    LOSE = 5, (Image.open("resources/sad_lose/left.gif"), Image.open("resources/sad_lose/right.gif")), (["C4", "G3", "A3", "G3", "P", "B3", "C4"], False, 4)


ARGS = {
    "debug": False,
    "file": None
}
