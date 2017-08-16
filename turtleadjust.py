import RPi.GPIO as GPIO
from time import sleep, localtime, time

def feedTurtle():
    motor_pins = [6, 13, 19, 26]
    step1 = [6, 13]
    step2 = [13, 19]
    step3 = [19, 26]
    step4 = [26, 6]
    steps = [step1, step2, step3, step4]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_pins, GPIO.OUT)

    for i in range(10):
        for step in steps:
            GPIO.output(step, True)
            sleep(.01)
            GPIO.output(step, False)

    GPIO.cleanup()


feedTurtle()
