import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
time.sleep(5)
GPIO.output(18,GPIO.HIGH)
time.sleep(3)
print "LED off"
GPIO.output(18,GPIO.LOW)
