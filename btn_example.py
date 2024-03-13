import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

i = 0
while True:
	if GPIO.input(6) == GPIO.HIGH:
		print("clicked" + str(i))
		i += 1
		sleep(0.5)
