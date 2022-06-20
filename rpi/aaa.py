import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO_TRIG = 4
GPIO_ECHO = 17
GPIO.setup(GPIO_TRIG, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.output(GPIO_TRIG, GPIO.LOW)
time.sleep(2)
while True:
    GPIO.output(GPIO_TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIG, GPIO.LOW)
    start_time = time.time()
    bounce_back_time = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        bounce_back_time = time.time()
    pulse_duration = bounce_back_time - start_time
    distance = round(pulse_duration * 17150, 2)
    print (f"Distance: {distance} cm")
GPIO.cleanup()

