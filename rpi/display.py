import busio
import digitalio
import board
import time
from constants import Mode
from PIL import Image, ImageDraw, ImageFont
from threading import Thread

from adafruit_rgb_display import color565
import adafruit_rgb_display.st7735 as st7735
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)


class DisplayHandler:
    def __init__(self):
        self.isRunning = False
        self.rate = 8
        self.nextFrame = 0
        self.mode = Mode.HUNTING
        self.thread = Thread(target=self.draw_continuous)
        self.dsx = st7735.ST7735R(spi, cs=digitalio.DigitalInOut(board.D5),
                             dc=digitalio.DigitalInOut(board.D24), rst=digitalio.DigitalInOut(board.D25), rotation=90)
        self.ddx = st7735.ST7735R(spi, cs=digitalio.DigitalInOut(board.CE1),
                                  dc=digitalio.DigitalInOut(board.D24), rst=digitalio.DigitalInOut(board.D25),
                                  rotation=270)
        self.ddx.init()
        self.dsx.init()
        self.ddx.fill(color565(0))
        self.dsx.fill(color565(0))

    def setMode(self, mode):
        self.mode = mode
        self.nextFrame = 0

    def start(self):
        self.isRunning = True
        if not self.thread.is_alive():
            self.thread.start()

    def stop(self):
        self.isRunning = False

    def draw_text(self, text, size, coords):
        img = Image.new('RGB', (self.ddx.height, self.ddx.width))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("resources/arial.ttf", size)
        draw.text(coords, text, font=font, fill=(255, 255, 255))
        self.dsx.image(img)
        self.ddx.image(img)

    def draw_continuous(self):
        while True:
            while not self.isRunning:
                time.sleep(0.2)
            min_frames = min(self.mode.gif[0].n_frames, self.mode.gif[0].n_frames) - 1
            self.mode.gif[0].seek(self.nextFrame % min_frames)
            self.mode.gif[1].seek(self.nextFrame % min_frames)
            self.dsx.image(self.mode.gif[0].convert("RGB"))
            self.ddx.image(self.mode.gif[1].convert("RGB"))
            self.nextFrame += 1
            time.sleep(1/(self.rate*1.5))


'''
disH = DisplayHandler()
disH.start()

while True:
    print("Happy")
    disH.setMode(Mode.HAPPY)
    time.sleep(10)
    print("Hunting")
    disH.setMode(Mode.HUNTING)
    time.sleep(10)
    print("Locked")
    disH.setMode(Mode.LOCKED)
    time.sleep(10)
    print("Lose")
    disH.setMode(Mode.LOSE)
    time.sleep(10)
    print("Surprised")
    disH.setMode(Mode.SURPRISED)
    time.sleep(10)
    print("Sleeping")
    disH.setMode(Mode.SLEEPING)
    time.sleep(10)
'''