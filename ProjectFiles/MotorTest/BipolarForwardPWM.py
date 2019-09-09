# PWM FUNCTIONS

# Create a PWM instance:
# p = GPIO.PWM(channel, frequency)

#To start PWM:
#p.start(dc)   # where dc is the duty cycle (0.0 <= dc <= 100.0)

#To change the frequency:
#p.ChangeFrequency(freq)   # where freq is the new frequency in Hz

#To change the duty cycle:
#p.ChangeDutyCycle(dc)  # where 0.0 <= dc <= 100.0

#To stop PWM:
#p.stop()

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

LinearActuatorDir = 18
LinearActuatorStepPin = 23

GPIO.setwarnings(False)
GPIO.setup(LinearActuatorDir, GPIO.OUT)
GPIO.setup(LinearActuatorStepPin, GPIO.OUT)

# Establish a starting frequency and an optimal frequency
startingfreq = 5000

# set the pin for steppermotor1 (pin 23) to startingfreq
stepper1 = GPIO.PWM(23, startingfreq)

# duty cycle is 50%
stepper1.start(50)

# 1 = forwards (clockwise?), 0 = backwards (counterclockwise)
GPIO.output(LinearActuatorDir, 1)