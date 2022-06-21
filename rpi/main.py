import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from camera import CameraHandler
from servo import ServoHandler
from sensor import SensorHandler
from display import DisplayHandler
from buzzer import BuzzerHandler
import argparse
from constants import SEN_THR, Mode, Timer
import time
import RPi.GPIO as GPIO


class Robat:
    def __init__(self):
        self.serH = ServoHandler()
        self.camH = CameraHandler()
        self.senH = SensorHandler()
        self.disH = DisplayHandler()
        self.buzH = BuzzerHandler()
        self.isPlaying = False
        self.mode = None
        self.rivalsLeft = 1
        self.tm = Timer()
        self.gameTm = Timer()

    def game(self):
        self.gameTm.set(30*self.rivalsLeft)
        self.setMode(Mode.HUNTING)
        self.disH.start()
        self.camH.start()
        #self.senH.start()
        self.buzH.start()

        while self.isPlaying:

            print(self.mode, self.senH.ssx.avgDst, self.senH.sdx.avgDst)
            if self.gameTm.isDone() and self.mode != Mode.LOSE:
                self.setMode(Mode.LOSE)

            elif self.mode == Mode.LOCKED:
                camRec, camRes = self.camH.try_get()
                if camRec is True:
                    if camRes is None:
                        self.setMode(Mode.SAD)
                    else:
                        self.serH.update(camRes)

            elif self.mode == Mode.HUNTING:
                self.checkArea()

            elif self.mode in (Mode.SURPRISED, Mode.SAD):
                if self.tm.isDone():
                    self.setMode(Mode.HUNTING)
                else:
                    self.checkArea()

            elif self.mode == Mode.HAPPY:
                if self.tm.isDone():
                    self.setMode(Mode.SLEEPING)

            elif self.mode in (Mode.WIN, Mode.LOSE):
                if self.tm.isDone():
                    break

            time.sleep(0.2)

        self.disH.stop()
        self.senH.stop()
        self.camH.stop()
        self.buzH.stop()
        self.isPlaying = False
        time.sleep(0.5)

    def checkArea(self):
        camRec, camRes = self.camH.try_get()
        print(camRec, camRes)
        if camRec is True and camRes is not None:
            self.setMode(Mode.LOCKED)
            self.serH.update(camRes)
        '''
        else:
            senAngle, dst = self.senH.getResult()
            if dst < SEN_THR:
                self.serH.addAngle(senAngle)
                self.setMode(Mode.SURPRISED)
        '''

    def setMode(self, mode):
        self.mode = mode
        self.tm.set(mode.time)
        self.disH.setMode(mode)
        self.buzH.setMode(mode)

    def longPress(self):
        if self.isPlaying:
            self.isPlaying = False
        else:
            self.isPlaying = True
            print("now it's playing")

    def shortPress(self):
        if self.isPlaying:
            if self.mode in (Mode.SLEEPING, Mode.HAPPY):
                self.gameTm.unpause()
                self.setMode(Mode.HUNTING)
            elif self.rivalsLeft > 1:
                self.rivalsLeft -= 1
                self.gameTm.pause()
                self.setMode(Mode.HAPPY)
            elif self.rivalsLeft == 1:
                self.gameTm.pause()
                self.setMode(Mode.WIN)
        else:
            self.rivalsLeft = (self.rivalsLeft % 9) + 1
            self.disH.draw_text(str(self.rivalsLeft), 160, (35, -25))


robat = Robat()

channel = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
buttonTimer = Timer()
lastTouch = GPIO.HIGH


def buttonCallback(channel):
    time.sleep(0.05)
    global lastTouch
    if GPIO.input(channel) is GPIO.LOW:
        if lastTouch != GPIO.LOW:
            lastTouch = GPIO.LOW
            print("low")
            buttonTimer.set(2)
    elif GPIO.input(channel) is GPIO.HIGH:
        if lastTouch != GPIO.HIGH:
            lastTouch = GPIO.HIGH
            print("high")
            if buttonTimer.isDone():
                print("long")
                robat.longPress()
            else:
                print("short")
                robat.shortPress()


GPIO.add_event_detect(channel, GPIO.BOTH, callback=buttonCallback, bouncetime=50)


def main():
    while True:
        robat.disH.draw_text(str(robat.rivalsLeft), 160, (35, -25))
        while not robat.isPlaying:
            time.sleep(0.3)
        robat.game()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", type=str, help="test video path")
    ap.add_argument("-d", "--debug", action=argparse.BooleanOptionalAction)
    args = vars(ap.parse_args())
    main()
