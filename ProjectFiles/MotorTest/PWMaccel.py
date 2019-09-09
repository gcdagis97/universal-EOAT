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

LinearActuatorStepPin = 24
LinearActuatorDir = 25

GPIO.setwarnings(False)
GPIO.setup(LinearActuatorDir, GPIO.OUT)
GPIO.setup(LinearActuatorStepPin, GPIO.OUT)

# Establish a running frequency and an optimal frequency
runningfreq = 5000
optimalfreq = 8500

# set the pin for steppermotor1 (pin 23) to startingfreq
stepper1 = GPIO.PWM(23, runningfreq)

# duty cycle is 50%
stepper1.start(50)

# What's clockwise / cclockwise?
# 0 = backwards, 1 = forwards
GPIO.output(LinearActuatorDir, 0)

# Delay for .1 seconds
delay = .1


# While motor is too slow increase freq by 100 every .25 seconds
# 9000 - 5000 = 4000 increase
# 4000/100 = 40 times through the loop
# 40*.1seconds = 4 seconds to get to optimal frequency
while (runningfreq < optimalfreq):
        
    # Pause
    time.sleep(delay)
    
    # Increase frequency by 10
    runningfreq += 100