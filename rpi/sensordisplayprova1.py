import busio
import digitalio
from board import SCK, MOSI, MISO, CE0, D24, D25

from adafruit_rgb_display import color565
from adafruit_rgb_display.st7735 import ST7735

#Libraries                                          (Sensor)
import RPi.GPIO as GPIO

#BUTTON
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN,pull_up_down=GPIO.PUD_UP)

# THE SOFTWARE                                                      (Display)
from PIL import Image
import ST7735
import time

#GPIO Mode (BOARD / BCM)                            (Sensor)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO.setwarnings(False)
GPIO_TRIGGER = 18
GPIO_ECHO = 23
GPIO_TRIGGER_1 = 21
GPIO_ECHO_1 = 20
#set GPIO direction (IN / OUT)                      (Sensor)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_1, GPIO.OUT)
GPIO.setup(GPIO_ECHO_1, GPIO.IN)


# Create TFT LCD display class.                                     (Display)
disp = ST7735.ST7735(port=0, cs=0, dc=24, backlight=None, rst=25, width=125, rotation=180, spi_speed_hz=20000000)
disp1 = ST7735.ST7735(port=0, cs=1, dc=17, backlight=None, rst=27, width=125, rotation=180, spi_speed_hz=20000000)

# Initialize display.                                               (Display)
disp.begin()
width = disp.width
height = disp.height

disp1.begin()
width1 = disp1.width
height1 = disp1.height


def distance():
    # set Trigger to HIGH                           (Sensor)
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW               (Sensor)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime                                (Sensor)
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival                          (Sensor)
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival     (Sensor)
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)    (Sensor)
    # and divide by 2, because there and back       (Sensor)
    distance = (TimeElapsed * 34300) / 2

    return distance

def distance1():
    # set Trigger to HIGH                           (Sensor)
    GPIO.output(GPIO_TRIGGER_1, True)

    # set Trigger after 0.01ms to LOW               (Sensor)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_1, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime                                (Sensor)
    while GPIO.input(GPIO_ECHO_1) == 0:
        StartTime = time.time()

    # save time of arrival                          (Sensor)
    while GPIO.input(GPIO_ECHO_1) == 1:
        StopTime = time.time()

    # time difference between start and arrival     (Sensor)
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)    (Sensor)
    # and divide by 2, because there and back       (Sensor)
    distance1 = (TimeElapsed * 34300) / 2

    return distance1

if __name__ == '__main__':
    try:
        while True:


           # if (inputValue == False):
               # print("Button press ")
               # break

            inputValue = GPIO.input(26)
            if (inputValue == False):
                print("Button press ")
                break
            dist1=distance()
            dist2=distance1()
            dist =min(dist1, dist2)
           
           
            print ("Measured Distance = %.1f cm" % dist)
            print ("Sensor 1 = %.1f cm" % dist1)
            print ("Sensor 2 = %.1f cm" % dist2)
            if dist>200:
                # Load an image.                                    (Display)
                image = Image.open('sad.gif')
                
                frame = 0
                j=0
                for j in range(8):
                    try:
                        image.seek(frame)
                        disp1.display(image.resize((width1, height1)))
                        disp.display(image.resize((width, height)))
                        frame += 1
                        time.sleep(0.05)
                        if frame > 8:
                            continue
                        

                    except EOFError:
                        frame = 0
            
            if dist<=200 and dist>70:
                # Load an image.                                    (Display)
                image = Image.open('trying.gif')
                
                frame = 0
                r=0
                for r in range(34):
                    try:
                        image.seek(frame)
                        disp1.display(image.resize((width1, height1)))
                        disp.display(image.resize((width, height)))
                        frame += 1
                        time.sleep(0.05)
                        if frame > 34:
                            continue

                    except EOFError:
                        frame = 0


            if dist<=70:
                # Load an image.                                    (Display)
                image = Image.open('happy.gif')
                frame = 0
                i=0
                for i in range(38):
                    try:
                        image.seek(frame)
                        disp1.display(image.resize((width1, height1)))
                        disp.display(image.resize((width, height)))
                        
                        frame += 1
                        time.sleep(0.05)
                        if frame > 38:
                            continue

                    except EOFError:
                        frame = 0
                #break
            


            time.sleep(0.05)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()







