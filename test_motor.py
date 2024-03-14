from motor import GroveServo
import RPi.GPIO as IO

IO.setwarnings(False)
IO.setmode(IO.BCM)

motor = GroveServo(12)
motor.left()
motor.right()
