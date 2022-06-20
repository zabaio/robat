import RPi.GPIO as GPIO
from threading import Thread
import time


class Sensor:
    def __init__(self, trigger, echo):
        self.trigger = trigger
        self.echo = echo
        self.avgDst = 9999


class SensorHandler:

    def __init__(self):
        self.isRunning = False
        self.ssx = Sensor(19, 16)
        self.sdx = Sensor(21, 20)
        self.thread = Thread(target=self.run)
        GPIO.setwarnings(False)
        # set GPIO direction (IN / OUT)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ssx.trigger, GPIO.OUT)
        GPIO.setup(self.ssx.echo, GPIO.IN)
        GPIO.setup(self.sdx.trigger, GPIO.OUT)
        GPIO.setup(self.sdx.echo, GPIO.IN)

    def start(self):
        self.isRunning = True
        if not self.thread.is_alive():
            self.thread.start()

    def stop(self):
        self.isRunning = False

    def run(self):
        while True:
            while not self.isRunning:
                time.sleep(0.2)
            self.ssx.avgDst = SensorHandler.avgDist(self.ssx, 3, 0.05)
            # print(self.ssx.avgDst)
            time.sleep(0.2)
            self.sdx.avgDst = SensorHandler.avgDist(self.sdx, 3, 0.05)
            # print(self.sdx.avgDst)
            time.sleep(0.2)

    @staticmethod
    def avgDist(sen, tries, bouncetime):
        distSum = 0
        for i in range(tries):
            distSum += SensorHandler.distance(sen)
            time.sleep(bouncetime)
        return distSum / tries

    @staticmethod
    def distance(sen: Sensor):
        # send impulse with trigger
        GPIO.output(sen.trigger, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(sen.trigger, GPIO.LOW)

        StartTime = time.time()
        StopTime = time.time()
        # save StartTime                                (Sensor)
        # while GPIO.input(sen.echo) == GPIO.LOW:
        #     StartTime = time.time()
        # save time of arrival                          (Sensor)
        while GPIO.input(sen.echo) == GPIO.LOW:
            StopTime = time.time()
            if StopTime - StartTime > 0.1:
                break

        # time difference between start and arrival     (Sensor)
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)    (Sensor)
        # and divide by 2, because there and back       (Sensor)
        distance = (TimeElapsed * 34300) / 2

        return distance

    def getResult(self):
        if self.ssx.avgDst < self.sdx.avgDst:
            return -80, self.ssx.avgDst
        else:
            return 80, self.sdx.avgDst


def main():
    senH = SensorHandler()
    senH.start()
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
