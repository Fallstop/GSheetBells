import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
while True:
    GPIO.output(18,GPIO.HIGH)
    GPIO.output(18,GPIO.LOW)
