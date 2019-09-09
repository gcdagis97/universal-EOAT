import RPi.GPIO as GPIO
import PWM
import time

GPIO.setmode(GPIO.BCM)

LinearActuatorDir = 18
LinearActuatorStepPin = 23

GPIO.setwarnings(False)
GPIO.setup(LinearActuatorDir, GPIO.OUT)
GPIO.setup(LinearActuatorStepPin, GPIO.OUT)

delay = .000007 #Test for this value
GPIO.output(LinearActuatorDir, 1)

def stepforward():
    GPIO.output(LinearActuatorStepPin, 1)
    time.sleep(delay)
    GPIO.output(LinearActuatorStepPin, 0)
    time.sleep(delay)

while (1):
    # Move stepper forward
    stepforward()