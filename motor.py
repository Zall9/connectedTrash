import RPi.GPIO as IO
import sys
from time import sleep
from numpy import interp

class GroveServo:
    MIN_DEGREE = 0
    MAX_DEGREE = 180
    INIT_DUTY = 1.5
    MIDDLE = 92

    def __init__(self, channel):
        IO.setup(channel,IO.OUT)
        self.pwm = IO.PWM(channel,50)
        self.pwm.start(GroveServo.INIT_DUTY)

    def __del__(self):
        self.pwm.stop()

    def setAngle(self, angle=0):
        # Map angle from range 0 ~ 180 to range 25 ~ 125
        angle = max(min(angle, GroveServo.MAX_DEGREE), GroveServo.MIN_DEGREE)
        tmp = interp(angle, [0, 180], [25, 125])
        self.pwm.ChangeDutyCycle(round(tmp/10.0, 1))
        sleep(2)

    def right(self, step=45):
        self.setAngle(GroveServo.MIDDLE + step)
        self.reset()

    def left(self, step=45):
        self.setAngle(GroveServo.MIDDLE - step)
        self.reset()

    def reset(self):
        self.setAngle(GroveServo.MIDDLE)
