from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
import RPi.GPIO as GPIO
import time

# Instantiate gpio pins
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 12
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# instantiate lcd and specify pins
lcd = Adafruit_CharLCD(rs=25, en=24,
                       d4=23, d5=17, d6=21, d7=22,
                       cols=16, lines=2)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

lcd.clear()
# display text on LCD display \n = new line
lcd.message('Initializing...\n')

try:
        while True:
                dist = distance()
                lcd.clear()
                lcd.message('%.1f cm' % dist)
                time.sleep(0.05)
except KeyboardInterrupt:
        print('Stopped')
        GPIO.cleanup()
