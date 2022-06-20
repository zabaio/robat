import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
from time import sleep
count = 0
def button_callback(channel):
    global start
    global end
    a=GPIO.input(10)
    print(a)
    sleep(0.01)
    if GPIO.input(10) == 1:
        start = time.time()
        global count
        count = count + 1
        print("Button was pushed nr = ", count)

    if GPIO.input(10) == 0:
        print("Button was released ")
        end = time.time()
        elapsed = end - start
        print(elapsed)



GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10, GPIO.BOTH, callback=button_callback, bouncetime=20) # Setup event on pin 10 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up
