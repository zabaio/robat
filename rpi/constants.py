from aenum import AutoNumberEnum
from PIL import Image
FRAME_SIZE = (320, 304)
HALF_W = FRAME_SIZE[0] / 2
H_WIND = 0.3
H_FOV = 120
F_LEN = 93.7
SEN_THR = 100

class Mode(AutoNumberEnum):
    _init_ = "time gif audio"
    HUNTING = None, (Image.open("resources/hunting/left.gif"), Image.open("resources/hunting/right.gif")), (["C4", "E4", "G4", "C5"], False)
    SURPRISED = 3, (Image.open("resources/surprised/left.gif"), Image.open("resources/surprised/left.gif")), None
    LOCKED = None, (Image.open("resources/locked/left.gif"), Image.open("resources/locked/right.gif")), (["C5", "P", "P"], True)
    SLEEPING = None, (Image.open("resources/sleeping/left.gif"), Image.open("resources/sleeping/right.gif")), None
    SAD = 6, (Image.open("resources/sad_lose/left.gif"), Image.open("resources/sad_lose/right.gif")), (["C5", "GS4"], False)
    HAPPY = 6, (Image.open("resources/happy_win/left.gif"), Image.open("resources/happy_win/right.gif")), (["E4", "G4", "A4", "A4"])
    WIN = 5, (Image.open("resources/happy_win/left.gif"), Image.open("resources/happy_win/right.gif")), (["B4", "B4", "B4", "DS5",  "B4",  "GS5"], False)
    LOSE = 5, (Image.open("resources/sad_lose/left.gif"), Image.open("resources/sad_lose/right.gif")), (["C4", "G3", "A3", "G3", "P", "B3", "C4"], False)

ARGS = {
    "debug": False,
    "file": None
}
