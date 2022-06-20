import RPi.GPIO as GPIO
import time

channel = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def buttonCallback(hello):
    print(hello)
    print("ciao")
    time.sleep(0.1)
    if GPIO.input(channel) is GPIO.LOW:
        print("Low")
    if GPIO.input(channel) is GPIO.HIGH:
        print("High")


GPIO.add_event_detect(channel, GPIO.BOTH, callback=buttonCallback, bouncetime=100)

while True:
    time.sleep(1)