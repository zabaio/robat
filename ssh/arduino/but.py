
from time import sleep
import RPi.GPIO as GPIO

PIN = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT, initial=0)
buzz = GPIO.PWM(PIN, 1)
LED_COUNT = 8 * 6


def pwm(freq, duty_cycle=30):
    buzz.ChangeDutyCycle(duty_cycle)
    buzz.ChangeFrequency(freq)
    buzz.start(duty_cycle)


def frequency(freq):
    buzz.ChangeFrequency(freq)


def duty_cycle(duty_cycle):
    buzz.ChangeDutyCycle(duty_cycle)


def play_note(note, duration=0.5):
    freq = 0
    if note == 'C':
        freq = 262
    if note == 'D':
        freq = 294
    if note == 'E':
        freq = 330
    if note == 'F':
        freq = 349
    if note == 'G':
        freq = 392
    if note == 'A':
        freq = 440
    if note == 'B':
        freq = 494
    if note == 'C5':
        freq = 523
    if note == 'D5':
        freq = 587
    if note == 'E5':
        freq = 659
    if note == 'F5':
        freq = 698
    play_freq(freq, duration)


def play_freq(freq, duration=0.5):
    if freq > 0:
        pwm(freq)
    sleep(duration)
    buzz.stop()


play_note('G', 0.3)
play_note('G', 0.3)
play_note('A')
play_note('G')
play_note('C5')
play_note('B')
play_note('')


play_note('G', 0.3)
play_note('G', 0.3)
play_note('A')
play_note('G')
play_note('D5')
play_note('C5')
play_note('')


play_note('G', 0.3)
play_note('G', 0.3)
play_note('G')
play_note('E5')

play_note('C5')
play_note('B')
play_note('A')
play_note('')


play_note('F5', 0.3)
play_note('F5', 0.3)
play_note('E5')
play_note('C5')

play_note('D5')
play_note('C5')
play_note('')

sleep(2)
