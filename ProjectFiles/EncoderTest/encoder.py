# George Dagis
# Encoder test
# 5/1/2019

import RPi.GPIO as GPIO

# Set up GPIO pins
pinA = 23
pinB = 24
GPIO.setmode(GPIO.bcm)
GPIO.setup(pinA, GPIO.IN)
GPIO.setup(pinB, GPIO.IN)

# Define initial values
currentA = 0
currentB = 0
currentX = 0
lastA = 0 
lastB = 0
lastX = 0
count = 0


while True:
    # Get current pin values
    currentA = GPIO.input(pinA)
    currentB = GPIO.input(pinB)
    # A XOR B
    currentX = bool(currentA) ^ bool(currentB)

    # Falling edge B + rising edge X = subtract
    if (currentB*1 < lastB*1) and (currentX*1 > lastX*1):
        count -= 1
    # Rise edge B + falling edge X = add
    if (currentB*1 > lastB*1) and (currentX*1 < lastX*1):
        count += 1
    # Check count
    print(str(count))
    # Reset X
    lastX = currentX