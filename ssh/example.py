import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import time
buzzerPin = 7  # define the buzzerPin
p = None
tones = {
            "B0": 31,
            "C1": 33,
            "CS1": 35,
            "D1": 37,
            "DS1": 39,
            "E1": 41,
            "F1": 44,
            "FS1": 46,
            "G1": 49,
            "GS1": 52,
            "A1": 55,
            "AS1": 58,
            "B1": 62,
            "C2": 65,
            "CS2": 69,
            "D2": 73,
            "DS2": 78,
            "E2": 82,
            "F2": 87,
            "FS2": 93,
            "G2": 98,
            "GS2": 104,
            "A2": 110,
            "AS2": 117,
            "B2": 123,
            "C3": 131,
            "CS3": 139,
            "D3": 147,
            "DS3": 156,
            "E3": 165,
            "F3": 175,
            "FS3": 185,
            "G3": 196,
            "GS3": 208,
            "A3": 220,
            "AS3": 233,
            "B3": 247,
            "C4": 262,
            "CS4": 277,
            "D4": 294,
            "DS4": 311,
            "E4": 330,
            "F4": 349,
            "FS4": 370,
            "G4": 392,
            "GS4": 415,
            "A4": 440,
            "AS4": 466,
            "B4": 494,
            "C5": 523,
            "CS5": 554,
            "D5": 587,
            "DS5": 622,
            "E5": 659,
            "F5": 698,
            "FS5": 740,
            "G5": 784,
            "GS5": 831,
            "A5": 880,
            "AS5": 932,
            "B5": 988,
            "C6": 1047,
            "CS6": 1109,
            "D6": 1175,
            "DS6": 1245,
            "E6": 1319,
            "F6": 1397,
            "FS6": 1480,
            "G6": 1568,
            "GS6": 1661,
            "A6": 1760,
            "AS6": 1865,
            "B6": 1976,
            "C7": 2093,
            "CS7": 2217,
            "D7": 2349,
            "DS7": 2489,
            "E7": 2637,
            "F7": 2794,
            "FS7": 2960,
            "G7": 3136,
            "GS7": 3322,
            "A7": 3520,
            "AS7": 3729,
            "B7": 3951,
            "C8": 4186,
            "CS8": 4435,
            "D8": 4699,
            "DS8": 4978
}


class BuzzerHandler:
    def setMode(self, mode):
        p0=8


def setup():
    global p
    GPIO.setmode(GPIO.BOARD)  # Use PHYSICAL GPIO Numbering
    GPIO.setup(buzzerPin, GPIO.OUT)  # set buzzer pin to OUTPUT mode
    p = GPIO.PWM(buzzerPin, 1)

    p.start(0)

'''
def loop():
    while True:
        if GPIO.input(buttonPin) == GPIO.LOW:
            alertor()
            print ('alertor turned on >>> ')
        else :
            stopAlertor()
            print ('alertor turned off <<<')

def alertor():
    p.start(50)
    for x in range(0,361): # Make frequency of the alertor consistent with the sine wave
        sinVal = math.sin(x * (math.pi / 180.0)) # calculate the sine value
        toneVal = 2000 + sinVal * 500 # Add to the resonant frequency with a Weighted
        p.ChangeFrequency(toneVal) # Change Frequency of PWM to toneVal
        time.sleep(0.001)

def stopAlertor():
    p.stop()
'''
def play_tone(frequency):
    global p
    """"this should be the volume"""
    p.ChangeFrequency(frequency)

def be_quiet():
    p.stop(0)

"""the song galery, how to set duration?"""

song1 = ["E5", "G5", "A5", "P", "E5", "G5", "B5", "A5", 0, "E5", "G5", "A5", "P", "G5", "E5"]
game_over = ["C4", "G3", "A3", "G3", 0, "B3", "C4"]
happy = ["E4", "G4", "A4", "A4", 0]
hunting = [262, 330, 392, 523]
sad = [523, 415]
win = [500, 500, 500, 800, 500, 600]

def play_song(song):
    for i in range(len(song)):
        play_tone([song[i]])
        time.sleep(0.5)
    be_quiet()

def destroy():
    GPIO.output(buzzerPin, GPIO.LOW)  # Turn off buzzer
    GPIO.cleanup()  # Release GPIO resource


if __name__ == '__main__':  # Program entrance
    print('Program is starting...')
    setup()
    try:
        p.start(50)
        play_song(hello)

        time.sleep(1)
        toneVal = 50
        while True:


            """p.ChangeFrequency(toneVal)
            toneVal *= 2
            time.sleep(0.5)
            print(toneVal)
            if toneVal > 5000:
                p.stop()
                toneVal = 1
                time.sleep(10)"""

    except KeyboardInterrupt:
        destroy()

