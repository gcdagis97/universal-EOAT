import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

Motor1StepPin = 27
Motor1DirPin = 22
Encoder1ChA = 23
Encoder1ChB = 24

GPIO.setwarnings(False)
GPIO.setup(Motor1DirPin, GPIO.OUT)
GPIO.setup(Motor1StepPin, GPIO.OUT)
GPIO.setup(Encoder1ChA, GPIO.IN)
GPIO.setup(Encoder1ChB, GPIO.IN)

# Establish a running frequency
runningfreq = 5000

# set the step pins for steppermotors1&2 (pins 20 & 5) to startingfreq
stepper1 = GPIO.PWM(27, runningfreq)

# clockwise = 1
GPIO.output(Motor1DirPin, 1)

# distance in inches
distance = .05

# Step motor appr. amount based on distance
# pitch = 20, steps/rev = 200
steps1 = distance*4000

# Function to step specific motor
def stepmotor(stepsm, motornum, chA, chB):
    
    # Define initial value
    currentA = 0
    currentB = 0
    currentX = 0
    lastA = 0 
    lastB = 0
    lastX = 0
    count = 0
    EncoderChA = chA
    EncoderChB = chB
    stepper = motornum
    
    # Account for encoder (300 cycles/rotation rather than 200)
    # Start motor
    steps = stepsm*1.5
    stepper.start(50)
    
    # Encoder steps
    while count < steps:
    
        # Get current pin values
        currentA = GPIO.input(EncoderChA)
        currentB = GPIO.input(EncoderChB)
        
        # A XOR B
        currentX = bool(currentA) ^ bool(currentB)

        # Rise edge B + falling edge X = add
        if (currentB*1 > lastB*1) and (currentX*1 < lastX*1):
            count += 1

        # Reset X
        lastX = currentX

    stepper.stop()

# Step motor 1 with encoder
stepmotor(steps1, stepper1, Encoder1ChA, Encoder1ChB)