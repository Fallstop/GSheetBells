import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

while True:
    GPIO.output(18,GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(18,GPIO.LOW)
